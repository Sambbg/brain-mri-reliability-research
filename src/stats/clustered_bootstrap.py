"""Patient-clustered bootstrap.

D3C contributes five central slices per patient, so slices are not independent
observations. Resampling slices would treat five correlated slices as five independent
draws and produce intervals that are too narrow by roughly sqrt(1 + (K - 1) * ICC) --
the design effect. This module resamples *patients* with replacement and carries every
slice belonging to each sampled patient, which propagates the within-patient
correlation into the interval instead of discarding it.

Not wired into the pipeline. Import with:

    import sys; sys.path.insert(0, "src/stats")
    from clustered_bootstrap import clustered_bootstrap_ci
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np


@dataclass(frozen=True)
class BootstrapInterval:
    estimate: float
    lower: float
    upper: float
    confidence: float
    n_patients: int
    n_observations: int
    n_resamples: int
    resample_estimates: np.ndarray = field(repr=False)

    @property
    def width(self) -> float:
        return self.upper - self.lower

    def format(self, digits: int = 4) -> str:
        return (
            f"{self.estimate:.{digits}f} "
            f"({self.lower:.{digits}f}, {self.upper:.{digits}f})"
        )


def _patient_index_groups(patient_ids: np.ndarray):
    """Row indices belonging to each distinct patient, in stable patient order."""
    unique_patients, inverse = np.unique(patient_ids, return_inverse=True)

    order = np.argsort(inverse, kind="mergesort")
    sorted_inverse = inverse[order]
    boundaries = np.searchsorted(sorted_inverse, np.arange(unique_patients.size + 1))

    groups = [
        order[boundaries[i]:boundaries[i + 1]] for i in range(unique_patients.size)
    ]

    return unique_patients, groups


def clustered_bootstrap_ci(
    values,
    patient_ids,
    statistic: Optional[Callable[[np.ndarray], float]] = None,
    confidence: float = 0.95,
    n_resamples: int = 2000,
    seed: int = 42,
) -> BootstrapInterval:
    """Percentile bootstrap confidence interval, resampling patients not observations.

    values may be 1-D (one column of outcomes) or 2-D (n_observations x k), so paired
    statistics such as a difference in glioma prediction rate between two models can be
    computed on the same resampled patients.

    statistic receives the resampled value array and returns a float. It defaults to the
    mean, which for 0/1 outcomes is the proportion.
    """
    values = np.asarray(values)
    patient_ids = np.asarray(patient_ids)

    if values.shape[0] != patient_ids.shape[0]:
        raise ValueError(
            f"values has {values.shape[0]} rows but patient_ids has "
            f"{patient_ids.shape[0]}"
        )

    if values.shape[0] == 0:
        raise ValueError("values is empty")

    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0, 1), got {confidence!r}")

    if n_resamples < 1:
        raise ValueError(f"n_resamples must be positive, got {n_resamples!r}")

    if statistic is None:
        def statistic(array):
            return float(np.mean(array))

    unique_patients, groups = _patient_index_groups(patient_ids)
    n_patients = unique_patients.size

    rng = np.random.default_rng(seed)
    estimates = np.empty(n_resamples, dtype=float)

    for draw in range(n_resamples):
        picked = rng.integers(0, n_patients, size=n_patients)
        rows = np.concatenate([groups[i] for i in picked])
        estimates[draw] = statistic(values[rows])

    alpha = 1.0 - confidence
    lower = float(np.percentile(estimates, 100.0 * alpha / 2.0))
    upper = float(np.percentile(estimates, 100.0 * (1.0 - alpha / 2.0)))

    return BootstrapInterval(
        estimate=float(statistic(values)),
        lower=lower,
        upper=upper,
        confidence=confidence,
        n_patients=int(n_patients),
        n_observations=int(values.shape[0]),
        n_resamples=int(n_resamples),
        resample_estimates=estimates,
    )


def intraclass_correlation(values, patient_ids) -> float:
    """One-way random-effects ICC(1) for clustered observations.

    Reported alongside a clustered interval so the degree of within-patient correlation
    driving the widening is visible rather than implicit.
    """
    values = np.asarray(values, dtype=float)
    patient_ids = np.asarray(patient_ids)

    unique_patients, groups = _patient_index_groups(patient_ids)
    n_patients = unique_patients.size

    if n_patients < 2:
        raise ValueError("ICC needs at least two patients")

    sizes = np.array([g.size for g in groups], dtype=float)
    group_means = np.array([values[g].mean() for g in groups])
    grand_mean = values.mean()
    n_total = values.size

    between = float(np.sum(sizes * (group_means - grand_mean) ** 2) / (n_patients - 1))
    within_sum = float(
        sum(np.sum((values[g] - group_means[i]) ** 2) for i, g in enumerate(groups))
    )

    if n_total == n_patients:
        raise ValueError("ICC needs at least one patient with more than one observation")

    within = within_sum / (n_total - n_patients)

    # Mean cluster size correction for unbalanced designs.
    k = (n_total - float(np.sum(sizes**2)) / n_total) / (n_patients - 1)

    if between + (k - 1) * within == 0:
        return 0.0

    return float((between - within) / (between + (k - 1) * within))
