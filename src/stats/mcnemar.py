"""McNemar's test for paired binary outcomes, with Holm correction.

The three models are evaluated on identical slices, so comparisons between them are
paired and an unpaired test would be wrong. McNemar's test uses only the discordant
pairs: b, where model A predicts 1 and model B predicts 0, and c, the reverse.

The chi-square approximation is unreliable when discordant pairs are few, so below a
threshold (25 by convention) an exact two-sided binomial test is used instead. The
exact test is computed with integer binomial coefficients rather than a normal
approximation, so it is exact in the arithmetic as well as in name.

Not wired into the pipeline. Import with:

    import sys; sys.path.insert(0, "src/stats")
    from mcnemar import mcnemar_test, holm_correction, mcnemar_family
"""

from dataclasses import dataclass
from typing import Optional, Sequence
import math

import numpy as np
from scipy.stats import chi2

# Below this many discordant pairs the chi-square approximation is not trustworthy.
EXACT_THRESHOLD = 25


@dataclass(frozen=True)
class McNemarResult:
    label: str
    n_pairs: int
    b: int
    c: int
    n_discordant: int
    statistic: Optional[float]
    p_value: float
    method: str
    p_value_adjusted: Optional[float] = None

    def format(self, digits: int = 4) -> str:
        adjusted = (
            "" if self.p_value_adjusted is None
            else f", Holm p={self.p_value_adjusted:.{digits}f}"
        )
        return (
            f"{self.label}: b={self.b}, c={self.c}, "
            f"p={self.p_value:.{digits}f} ({self.method}){adjusted}"
        )


def _as_binary(values, name: str) -> np.ndarray:
    array = np.asarray(values)

    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional, got shape {array.shape}")

    numeric = array.astype(float)

    if not np.all(np.isin(numeric, (0.0, 1.0))):
        raise ValueError(f"{name} must contain only 0/1 or boolean values")

    return numeric.astype(int)


def exact_binomial_two_sided(b: int, c: int) -> float:
    """Two-sided p-value for b successes out of b + c trials under p = 0.5.

    Computed from exact integer binomial coefficients: the one-sided tail is
    sum_{i<=min(b,c)} C(n, i) / 2^n, doubled and capped at 1.
    """
    n = b + c

    if n == 0:
        return 1.0

    k = min(b, c)
    tail_numerator = sum(math.comb(n, i) for i in range(k + 1))
    tail = tail_numerator / (2**n)

    return min(1.0, 2.0 * tail)


def mcnemar_test(
    outcome_a,
    outcome_b,
    label: str = "A vs B",
    exact_threshold: int = EXACT_THRESHOLD,
) -> McNemarResult:
    """McNemar's test on paired binary outcomes.

    outcome_a and outcome_b are aligned per-observation binary outcomes for the two
    models being compared, for example whether each slice was predicted glioma.
    """
    a = _as_binary(outcome_a, "outcome_a")
    b_arr = _as_binary(outcome_b, "outcome_b")

    if a.size != b_arr.size:
        raise ValueError(
            f"paired outcomes must be the same length, got {a.size} and {b_arr.size}"
        )

    if a.size == 0:
        raise ValueError("paired outcomes are empty")

    b = int(np.sum((a == 1) & (b_arr == 0)))
    c = int(np.sum((a == 0) & (b_arr == 1)))
    n_discordant = b + c

    if n_discordant == 0:
        # Every pair agrees; there is no evidence of a difference and no statistic.
        return McNemarResult(
            label=label,
            n_pairs=int(a.size),
            b=b,
            c=c,
            n_discordant=0,
            statistic=None,
            p_value=1.0,
            method="no_discordant_pairs",
        )

    if n_discordant < exact_threshold:
        return McNemarResult(
            label=label,
            n_pairs=int(a.size),
            b=b,
            c=c,
            n_discordant=n_discordant,
            statistic=None,
            p_value=exact_binomial_two_sided(b, c),
            method="exact_binomial",
        )

    # Edwards continuity correction. Clamped at zero so |b - c| < 1 cannot produce a
    # spurious positive statistic.
    corrected = max(0.0, abs(b - c) - 1.0)
    statistic = corrected * corrected / n_discordant

    return McNemarResult(
        label=label,
        n_pairs=int(a.size),
        b=b,
        c=c,
        n_discordant=n_discordant,
        statistic=float(statistic),
        p_value=float(chi2.sf(statistic, 1)),
        method="chi2_continuity_corrected",
    )


def holm_correction(p_values: Sequence[float]) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values, returned in the input order.

    Step-down: the k-th smallest raw p-value is multiplied by (m - k), and a running
    maximum enforces monotonicity so an adjusted p-value can never fall below one for a
    more significant test. Holm controls the family-wise error rate without assuming
    independence, and is uniformly more powerful than Bonferroni.
    """
    p = np.asarray(p_values, dtype=float)

    if p.ndim != 1:
        raise ValueError(f"p_values must be one-dimensional, got shape {p.shape}")

    if p.size == 0:
        raise ValueError("p_values is empty")

    if np.any(p < 0.0) or np.any(p > 1.0):
        raise ValueError("p_values must lie in [0, 1]")

    m = p.size
    order = np.argsort(p, kind="mergesort")
    adjusted = np.empty(m, dtype=float)

    running_max = 0.0
    for rank, index in enumerate(order):
        candidate = (m - rank) * p[index]
        running_max = max(running_max, candidate)
        adjusted[index] = min(1.0, running_max)

    return adjusted


def mcnemar_family(comparisons, exact_threshold: int = EXACT_THRESHOLD):
    """Run a family of McNemar tests and Holm-correct across them.

    comparisons is a sequence of (label, outcome_a, outcome_b). With three models there
    are three pairwise comparisons, so correcting across the family is required before
    any of them is described as significant.
    """
    comparisons = list(comparisons)

    if not comparisons:
        raise ValueError("comparisons is empty")

    results = [
        mcnemar_test(a, b, label=label, exact_threshold=exact_threshold)
        for label, a, b in comparisons
    ]

    adjusted = holm_correction([r.p_value for r in results])

    return [
        McNemarResult(
            label=r.label,
            n_pairs=r.n_pairs,
            b=r.b,
            c=r.c,
            n_discordant=r.n_discordant,
            statistic=r.statistic,
            p_value=r.p_value,
            method=r.method,
            p_value_adjusted=float(adj),
        )
        for r, adj in zip(results, adjusted)
    ]
