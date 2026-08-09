"""Random-intercept logistic regression: y ~ fixed effects + (1|group).

For D3C the model is

    glioma_predicted ~ model + (1|patient)

which compares the three models' glioma prediction rates while allowing each patient to
have their own baseline propensity. Without the random intercept the five slices of a
patient are treated as five independent observations and standard errors are too small.

No GLMM package is available in this environment -- statsmodels is not a project
dependency -- so the marginal likelihood is integrated directly with Gauss-Hermite
quadrature and maximised with L-BFGS-B. For each group,

    L_i = integral over u of  prod_j Bernoulli(y_ij | logistic(x_ij'beta + u))  N(u|0, s^2) du

and substituting u = sqrt(2) * s * t turns that into a Gauss-Hermite sum with weights
w_q / sqrt(pi), which sum to exactly 1. That identity gives a strong correctness check:
at s = 0 the marginal log-likelihood must equal the ordinary logistic log-likelihood
exactly, and the test suite asserts it.

Quadrature is not adaptive, so accuracy depends on having enough nodes. Fits should be
checked for stability against node count; `fit_random_intercept_logistic` exposes
n_quadrature for exactly that purpose.

Not wired into the pipeline. Import with:

    import sys; sys.path.insert(0, "src/stats")
    from mixed_effects import fit_d3c_glioma_model
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence
import math

import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy.stats import norm


@dataclass(frozen=True)
class Term:
    name: str
    estimate: float
    std_error: float
    z_value: float
    p_value: float

    @property
    def odds_ratio(self) -> float:
        return math.exp(self.estimate)

    def format(self, digits: int = 4) -> str:
        return (
            f"{self.name}: beta={self.estimate:.{digits}f} "
            f"(SE {self.std_error:.{digits}f}), OR={self.odds_ratio:.{digits}f}, "
            f"z={self.z_value:.{digits}f}, p={self.p_value:.{digits}f}"
        )


@dataclass(frozen=True)
class MixedModelResult:
    terms: list
    group_sd: float
    group_sd_std_error: float
    icc: float
    log_likelihood: float
    n_observations: int
    n_groups: int
    n_quadrature: int
    converged: bool
    message: str
    params: np.ndarray = field(repr=False)

    def term(self, name: str) -> Term:
        for t in self.terms:
            if t.name == name:
                return t
        raise KeyError(f"no term named {name!r}")

    def summary(self, digits: int = 4) -> str:
        lines = [
            f"Random-intercept logistic regression "
            f"({self.n_observations} observations, {self.n_groups} groups)",
            f"  log-likelihood {self.log_likelihood:.{digits}f}, "
            f"{self.n_quadrature} quadrature nodes, converged={self.converged}",
        ]
        for t in self.terms:
            lines.append("  " + t.format(digits))
        lines.append(
            f"  group SD={self.group_sd:.{digits}f} "
            f"(SE {self.group_sd_std_error:.{digits}f}), ICC={self.icc:.{digits}f}"
        )
        return "\n".join(lines)


def gauss_hermite(n_quadrature: int):
    """Nodes and log weights normalised so the weights sum to exactly 1."""
    if n_quadrature < 3:
        raise ValueError(f"n_quadrature must be at least 3, got {n_quadrature!r}")

    nodes, weights = hermgauss(n_quadrature)
    log_weights = np.log(weights) - 0.5 * math.log(math.pi)

    return nodes, log_weights


def marginal_log_likelihood(beta, sigma, X, y, group_index, n_groups, nodes, log_weights) -> float:
    """Marginal log-likelihood with the random intercept integrated out."""
    beta = np.asarray(beta, dtype=float)
    eta_fixed = X @ beta

    u = math.sqrt(2.0) * sigma * nodes
    eta = eta_fixed[:, None] + u[None, :]

    # log Bernoulli pmf, written to avoid overflow for large |eta|.
    log_prob = y[:, None] * eta - np.logaddexp(0.0, eta)

    group_log_prob = np.empty((n_groups, nodes.size), dtype=float)
    for q in range(nodes.size):
        group_log_prob[:, q] = np.bincount(
            group_index, weights=log_prob[:, q], minlength=n_groups
        )

    return float(np.sum(logsumexp(log_weights[None, :] + group_log_prob, axis=1)))


def _numerical_hessian(function, x, step: float = 1e-5) -> np.ndarray:
    n = x.size
    hessian = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(i, n):
            x_pp = x.copy(); x_pp[i] += step; x_pp[j] += step
            x_pm = x.copy(); x_pm[i] += step; x_pm[j] -= step
            x_mp = x.copy(); x_mp[i] -= step; x_mp[j] += step
            x_mm = x.copy(); x_mm[i] -= step; x_mm[j] -= step

            value = (
                function(x_pp) - function(x_pm) - function(x_mp) + function(x_mm)
            ) / (4.0 * step * step)

            hessian[i, j] = value
            hessian[j, i] = value

    return hessian


def fit_random_intercept_logistic(
    X,
    y,
    group_ids,
    coefficient_names: Optional[Sequence[str]] = None,
    n_quadrature: int = 31,
    maxiter: int = 1000,
) -> MixedModelResult:
    """Maximum likelihood fit of y ~ X*beta + (1|group)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    if X.ndim != 2:
        raise ValueError(f"X must be two-dimensional, got shape {X.shape}")

    if y.ndim != 1 or y.size != X.shape[0]:
        raise ValueError("y must be one-dimensional and aligned with the rows of X")

    if not np.all(np.isin(y, (0.0, 1.0))):
        raise ValueError("y must contain only 0/1 values")

    unique_groups, group_index = np.unique(np.asarray(group_ids), return_inverse=True)
    n_groups = int(unique_groups.size)

    if group_index.size != y.size:
        raise ValueError("group_ids must be aligned with y")

    if coefficient_names is None:
        coefficient_names = [f"x{i}" for i in range(X.shape[1])]

    if len(coefficient_names) != X.shape[1]:
        raise ValueError("coefficient_names must match the number of columns of X")

    nodes, log_weights = gauss_hermite(n_quadrature)

    def negative_log_likelihood(params):
        beta = params[:-1]
        sigma = math.exp(params[-1])
        return -marginal_log_likelihood(
            beta, sigma, X, y, group_index, n_groups, nodes, log_weights
        )

    start = np.zeros(X.shape[1] + 1, dtype=float)
    start[-1] = math.log(0.5)

    fit = minimize(
        negative_log_likelihood,
        start,
        method="L-BFGS-B",
        options={"maxiter": maxiter},
    )

    params = np.asarray(fit.x, dtype=float)
    hessian = _numerical_hessian(negative_log_likelihood, params)

    try:
        covariance = np.linalg.inv(hessian)
    except np.linalg.LinAlgError:
        covariance = np.full_like(hessian, np.nan)

    std_errors = np.sqrt(np.clip(np.diag(covariance), 0.0, np.inf))

    terms = []
    for i, name in enumerate(coefficient_names):
        estimate = float(params[i])
        std_error = float(std_errors[i])
        z_value = estimate / std_error if std_error > 0 else float("nan")
        p_value = float(2.0 * norm.sf(abs(z_value))) if std_error > 0 else float("nan")
        terms.append(
            Term(
                name=name,
                estimate=estimate,
                std_error=std_error,
                z_value=z_value,
                p_value=p_value,
            )
        )

    log_sigma = float(params[-1])
    sigma = math.exp(log_sigma)
    # Delta method: SE(sigma) = sigma * SE(log sigma).
    sigma_std_error = float(sigma * std_errors[-1])

    return MixedModelResult(
        terms=terms,
        group_sd=sigma,
        group_sd_std_error=sigma_std_error,
        icc=float(sigma**2 / (sigma**2 + math.pi**2 / 3.0)),
        log_likelihood=float(-fit.fun),
        n_observations=int(y.size),
        n_groups=n_groups,
        n_quadrature=int(n_quadrature),
        converged=bool(fit.success),
        message=str(fit.message),
        params=params,
    )


def build_categorical_design(labels, reference: Optional[str] = None):
    """Treatment-coded design matrix for one categorical predictor, plus intercept."""
    labels = [str(v) for v in labels]
    levels = sorted(set(labels))

    if len(levels) < 2:
        raise ValueError(f"need at least two levels, got {levels}")

    if reference is None:
        reference = levels[0]

    if reference not in levels:
        raise ValueError(f"reference {reference!r} is not one of {levels}")

    non_reference = [level for level in levels if level != reference]

    n = len(labels)
    X = np.zeros((n, 1 + len(non_reference)), dtype=float)
    X[:, 0] = 1.0

    for column, level in enumerate(non_reference, start=1):
        X[:, column] = [1.0 if label == level else 0.0 for label in labels]

    names = ["intercept"] + [f"model[{level}]" for level in non_reference]

    return X, names, reference


def fit_d3c_glioma_model(
    glioma_predicted,
    model_labels,
    patient_ids,
    reference_model: Optional[str] = None,
    n_quadrature: int = 31,
) -> MixedModelResult:
    """Fit glioma_predicted ~ model + (1|patient).

    Each patient is evaluated by every model, so the shared random intercept both
    absorbs the patient's baseline propensity and respects the paired design. The
    coefficient for each non-reference model is the log odds ratio of predicting glioma
    relative to the reference model, holding the patient fixed.
    """
    X, names, _ = build_categorical_design(model_labels, reference=reference_model)

    return fit_random_intercept_logistic(
        X,
        glioma_predicted,
        patient_ids,
        coefficient_names=names,
        n_quadrature=n_quadrature,
    )
