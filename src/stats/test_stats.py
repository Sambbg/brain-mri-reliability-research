"""Unit tests for src/stats, run as a plain script.

    venv/bin/python src/stats/test_stats.py

No test framework is used because none is a project dependency, and the repository's
convention is standalone argument-free scripts. Exit status is the number of failures.

Every test checks against something independently known: published Wilson intervals and
an independent root-finding solution of the score equation, hand-computed binomial
tails, the design-effect prediction sqrt(1 + (K-1) * ICC) for clustered resampling, and
the exact identity that a random-intercept log-likelihood at sigma = 0 equals the
ordinary logistic log-likelihood.
"""

from pathlib import Path
import math
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import binomtest, chi2

sys.path.insert(0, str(Path(__file__).resolve().parent))

from clustered_bootstrap import (  # noqa: E402
    clustered_bootstrap_ci,
    intraclass_correlation,
)
from mcnemar import (  # noqa: E402
    exact_binomial_two_sided,
    holm_correction,
    mcnemar_family,
    mcnemar_test,
)
from mixed_effects import (  # noqa: E402
    build_categorical_design,
    fit_d3c_glioma_model,
    fit_random_intercept_logistic,
    gauss_hermite,
    marginal_log_likelihood,
)
from wilson import wilson_interval, wilson_interval_from_flags, z_for_confidence  # noqa: E402


FAILURES = []
PASSED = 0


def check(name, condition, detail=""):
    global PASSED
    if condition:
        PASSED += 1
        print(f"  PASS  {name}")
    else:
        FAILURES.append((name, detail))
        print(f"  FAIL  {name}  {detail}")


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def raises(exception_type, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except exception_type:
        return True
    except Exception:
        return False
    return False


# ----------------------------------------------------------------------------------
# Wilson score intervals
# ----------------------------------------------------------------------------------

def wilson_bounds_by_root_finding(successes, n, confidence=0.95):
    """Independent solution: the bounds are the roots of the score equation.

    Solving |p_hat - p| / sqrt(p(1-p)/n) = z numerically is algebraically independent of
    the closed form in wilson.py, so agreement is a real check rather than a restatement.
    """
    z = z_for_confidence(confidence)
    p_hat = successes / n
    epsilon = 1e-12

    def score(p):
        return (p_hat - p) / math.sqrt(p * (1.0 - p) / n)

    lower = brentq(lambda p: score(p) - z, epsilon, p_hat, xtol=1e-15, rtol=1e-15)
    upper = brentq(lambda p: score(p) + z, p_hat, 1.0 - epsilon, xtol=1e-15, rtol=1e-15)

    return lower, upper


def test_wilson():
    print("\nWilson score intervals")

    # Published worked example: 2 of 10, 95 per cent -> (0.0567, 0.5098).
    interval = wilson_interval(2, 10)
    check(
        "published example 2/10",
        close(interval.lower, 0.0567, 5e-5) and close(interval.upper, 0.5098, 5e-5),
        f"got ({interval.lower:.6f}, {interval.upper:.6f})",
    )

    # Published worked example (Newcombe 1998): 81 of 263 -> (0.2553, 0.3662).
    interval = wilson_interval(81, 263)
    check(
        "published example 81/263",
        close(interval.lower, 0.2553, 5e-5) and close(interval.upper, 0.3662, 5e-5),
        f"got ({interval.lower:.6f}, {interval.upper:.6f})",
    )

    # Boundary cases where the Wald interval collapses to zero width.
    zero = wilson_interval(0, 10)
    full = wilson_interval(10, 10)
    check(
        "boundary 0/10 -> (0, 0.2775)",
        close(zero.lower, 0.0, 1e-12) and close(zero.upper, 0.2775, 5e-5),
        f"got ({zero.lower:.6f}, {zero.upper:.6f})",
    )
    check(
        "boundary 10/10 -> (0.7225, 1)",
        close(full.lower, 0.7225, 5e-5) and close(full.upper, 1.0, 1e-12),
        f"got ({full.lower:.6f}, {full.upper:.6f})",
    )
    check("boundary intervals have non-zero width", zero.width > 0 and full.width > 0)

    # Agreement with an independent numerical solution of the score equation.
    worst = 0.0
    for successes, n, confidence in [
        (2, 10, 0.95), (81, 263, 0.95), (5, 20, 0.99),
        (137, 200, 0.90), (1, 1000, 0.95), (999, 1000, 0.95),
    ]:
        analytic = wilson_interval(successes, n, confidence)
        numeric_lower, numeric_upper = wilson_bounds_by_root_finding(
            successes, n, confidence
        )
        worst = max(
            worst,
            abs(analytic.lower - numeric_lower),
            abs(analytic.upper - numeric_upper),
        )
    check(
        "closed form matches score-equation roots",
        worst < 1e-9,
        f"max deviation {worst:.3e}",
    )

    # Symmetry: the interval for x is the mirror of the interval for n - x.
    a = wilson_interval(37, 100)
    b = wilson_interval(63, 100)
    check(
        "symmetry under successes -> n - successes",
        close(a.lower, 1.0 - b.upper, 1e-12) and close(a.upper, 1.0 - b.lower, 1e-12),
    )

    # Width shrinks with n at fixed proportion, and grows with confidence.
    widths = [wilson_interval(n // 2, n).width for n in (20, 200, 2000, 20000)]
    check("width decreases with n", all(x > y for x, y in zip(widths, widths[1:])))
    check(
        "width increases with confidence",
        wilson_interval(50, 100, 0.90).width < wilson_interval(50, 100, 0.99).width,
    )

    check("z at 95 per cent is 1.959964", close(z_for_confidence(0.95), 1.959964, 1e-6))

    check("from_flags matches counts",
          close(wilson_interval_from_flags([1, 0, 1, 1, 0]).proportion, 0.6, 1e-12))

    check("rejects n <= 0", raises(ValueError, wilson_interval, 0, 0))
    check("rejects successes > n", raises(ValueError, wilson_interval, 11, 10))
    check("rejects negative successes", raises(ValueError, wilson_interval, -1, 10))
    check("rejects confidence outside (0,1)", raises(ValueError, wilson_interval, 5, 10, 1.5))


# ----------------------------------------------------------------------------------
# Patient-clustered bootstrap
# ----------------------------------------------------------------------------------

def simulate_clustered(n_patients, slices_per_patient, concentration, seed):
    """Beta-Bernoulli clusters with mean 0.5 and ICC = 1 / (1 + 2 * concentration)."""
    rng = np.random.default_rng(seed)
    patient_rates = rng.beta(concentration, concentration, size=n_patients)

    values = np.concatenate([
        (rng.random(slices_per_patient) < rate).astype(float) for rate in patient_rates
    ])
    patient_ids = np.repeat(np.arange(n_patients), slices_per_patient)

    return values, patient_ids


def test_clustered_bootstrap():
    print("\nPatient-clustered bootstrap")

    n_patients = 400
    slices_per_patient = 5
    n_observations = n_patients * slices_per_patient

    # Independent-sampling width for a proportion near 0.5, used as the reference the
    # design effect is measured against.
    independent_width = 2.0 * 1.959964 * math.sqrt(0.25 / n_observations)

    widths = []
    ratios = []
    expected_ratios = []

    for concentration in (50.0, 5.0, 0.5, 0.05):
        values, patient_ids = simulate_clustered(
            n_patients, slices_per_patient, concentration, seed=20260809
        )
        interval = clustered_bootstrap_ci(
            values, patient_ids, n_resamples=800, seed=7
        )
        realized_icc = intraclass_correlation(values, patient_ids)

        widths.append(interval.width)
        ratios.append(interval.width / independent_width)
        expected_ratios.append(
            math.sqrt(1.0 + (slices_per_patient - 1) * max(0.0, realized_icc))
        )

        print(
            f"        concentration={concentration:<5} ICC={realized_icc:.4f} "
            f"width={interval.width:.4f} ratio={ratios[-1]:.3f} "
            f"expected~{expected_ratios[-1]:.3f}"
        )

    check(
        "interval widens monotonically as within-patient correlation increases",
        all(x < y for x, y in zip(widths, widths[1:])),
        f"widths {[round(w, 4) for w in widths]}",
    )

    worst = max(abs(r - e) / e for r, e in zip(ratios, expected_ratios))
    check(
        "widening tracks the design effect sqrt(1 + (K-1) * ICC)",
        worst < 0.20,
        f"worst relative deviation {worst:.3f}",
    )

    check(
        "near-independent clusters give a width close to the independent case",
        abs(ratios[0] - 1.0) < 0.15,
        f"ratio {ratios[0]:.3f}",
    )

    check(
        "highly correlated clusters give a much wider interval",
        ratios[-1] > 2.0,
        f"ratio {ratios[-1]:.3f}",
    )

    # Resampling slices instead of patients understates the interval: this is the error
    # the module exists to prevent.
    values, patient_ids = simulate_clustered(n_patients, slices_per_patient, 0.05, seed=1)
    clustered = clustered_bootstrap_ci(values, patient_ids, n_resamples=800, seed=7)
    naive = clustered_bootstrap_ci(
        values, np.arange(values.size), n_resamples=800, seed=7
    )
    check(
        "patient-level resampling is wider than slice-level resampling",
        clustered.width > 1.8 * naive.width,
        f"clustered {clustered.width:.4f} vs slice-level {naive.width:.4f}",
    )

    # Determinism and basic contracts.
    first = clustered_bootstrap_ci(values, patient_ids, n_resamples=200, seed=99)
    second = clustered_bootstrap_ci(values, patient_ids, n_resamples=200, seed=99)
    check("same seed gives identical interval",
          close(first.lower, second.lower, 0) and close(first.upper, second.upper, 0))

    check("point estimate is the statistic on the full sample",
          close(first.estimate, float(np.mean(values)), 1e-12))
    check("interval brackets the point estimate",
          first.lower <= first.estimate <= first.upper)
    check("reports patient and observation counts",
          first.n_patients == n_patients and first.n_observations == n_observations)

    # A custom statistic on paired columns, the shape a model-vs-model difference takes.
    paired = np.column_stack([values, np.roll(values, 1)])
    difference = clustered_bootstrap_ci(
        paired, patient_ids,
        statistic=lambda a: float(np.mean(a[:, 0]) - np.mean(a[:, 1])),
        n_resamples=200, seed=3,
    )
    check("supports a two-column paired statistic",
          difference.lower <= difference.estimate <= difference.upper)

    check("rejects mismatched lengths",
          raises(ValueError, clustered_bootstrap_ci, np.zeros(5), np.zeros(4)))
    check("rejects empty input",
          raises(ValueError, clustered_bootstrap_ci, np.zeros(0), np.zeros(0)))


# ----------------------------------------------------------------------------------
# McNemar and Holm
# ----------------------------------------------------------------------------------

def paired_from_counts(both_one, b, c, both_zero):
    """Build paired outcome vectors with prescribed discordant counts."""
    a = [1] * both_one + [1] * b + [0] * c + [0] * both_zero
    d = [1] * both_one + [0] * b + [1] * c + [0] * both_zero
    return np.array(a), np.array(d)


def test_mcnemar():
    print("\nMcNemar's test")

    # Hand-computed exact tail: n = 3, k = 0 -> 2 * (1/8) = 0.25.
    a, b = paired_from_counts(both_one=10, b=3, c=0, both_zero=10)
    result = mcnemar_test(a, b)
    check(
        "exact path, b=3 c=0, p = 0.25",
        result.method == "exact_binomial" and close(result.p_value, 0.25, 1e-12),
        f"got {result.method}, p={result.p_value}",
    )

    # Hand-computed: n = 10, k = 2 -> 2 * (1 + 10 + 45) / 1024 = 0.109375.
    a, b = paired_from_counts(both_one=5, b=2, c=8, both_zero=5)
    result = mcnemar_test(a, b)
    check(
        "exact path, b=2 c=8, p = 0.109375",
        result.method == "exact_binomial" and close(result.p_value, 0.109375, 1e-12),
        f"got {result.method}, p={result.p_value}",
    )

    # Cross-check the exact tail against scipy's binomial test.
    worst = 0.0
    for b_count, c_count in [(0, 5), (1, 6), (3, 9), (7, 7), (2, 20), (11, 4)]:
        mine = exact_binomial_two_sided(b_count, c_count)
        theirs = binomtest(b_count, b_count + c_count, 0.5).pvalue
        worst = max(worst, abs(mine - theirs))
    check(
        "exact tail matches scipy binomtest",
        worst < 1e-12,
        f"max deviation {worst:.3e}",
    )

    # Chi-square path with continuity correction: (|20-5|-1)^2 / 25 = 7.84.
    a, b = paired_from_counts(both_one=50, b=20, c=5, both_zero=50)
    result = mcnemar_test(a, b)
    check(
        "chi-square path statistic = 7.84",
        result.method == "chi2_continuity_corrected" and close(result.statistic, 7.84, 1e-12),
        f"got {result.method}, stat={result.statistic}",
    )
    check(
        "chi-square p-value matches chi2 survival function",
        close(result.p_value, float(chi2.sf(7.84, 1)), 1e-12),
    )

    # Threshold behaviour: 24 discordant pairs exact, 25 chi-square.
    a, b = paired_from_counts(both_one=10, b=12, c=12, both_zero=10)
    check("24 discordant pairs uses the exact test",
          mcnemar_test(a, b).method == "exact_binomial")
    a, b = paired_from_counts(both_one=10, b=13, c=12, both_zero=10)
    check("25 discordant pairs uses chi-square",
          mcnemar_test(a, b).method == "chi2_continuity_corrected")

    # No discordant pairs at all.
    a, b = paired_from_counts(both_one=20, b=0, c=0, both_zero=20)
    result = mcnemar_test(a, b)
    check("no discordant pairs gives p = 1 and no statistic",
          result.method == "no_discordant_pairs"
          and close(result.p_value, 1.0, 0)
          and result.statistic is None)

    # Symmetry: swapping the two models cannot change the p-value.
    a, b = paired_from_counts(both_one=30, b=17, c=6, both_zero=30)
    check("p-value is symmetric under swapping the models",
          close(mcnemar_test(a, b).p_value, mcnemar_test(b, a).p_value, 1e-15))

    # Continuity correction clamped: |b - c| = 1 must not give a positive statistic.
    a, b = paired_from_counts(both_one=10, b=13, c=14, both_zero=10)
    result = mcnemar_test(a, b)
    check("continuity correction clamps at zero",
          close(result.statistic, 0.0, 1e-15) and close(result.p_value, 1.0, 1e-12),
          f"stat={result.statistic}")

    check("rejects non-binary input",
          raises(ValueError, mcnemar_test, np.array([0, 1, 2]), np.array([0, 1, 0])))
    check("rejects mismatched lengths",
          raises(ValueError, mcnemar_test, np.array([0, 1]), np.array([0, 1, 0])))

    print("\nHolm correction")

    # Hand-computed: sorted 0.01, 0.03, 0.04 -> 3*0.01=0.03, 2*0.03=0.06, 1*0.04=0.04
    # which is raised to 0.06 by the running maximum.
    adjusted = holm_correction([0.01, 0.04, 0.03])
    check(
        "worked example [0.01, 0.04, 0.03] -> [0.03, 0.06, 0.06]",
        close(adjusted[0], 0.03, 1e-12)
        and close(adjusted[1], 0.06, 1e-12)
        and close(adjusted[2], 0.06, 1e-12),
        f"got {adjusted}",
    )

    check("adjusted p-values are capped at 1",
          np.all(holm_correction([0.5, 0.5, 0.5]) == 1.0))
    check("single test is unchanged",
          close(holm_correction([0.023])[0], 0.023, 1e-12))
    check("adjusted p-values never fall below raw",
          np.all(holm_correction([0.001, 0.02, 0.3, 0.7]) >= np.array([0.001, 0.02, 0.3, 0.7])))

    adjusted = holm_correction([0.001, 0.02, 0.3, 0.7])
    check("monotone in the sorted order",
          np.all(np.diff(np.sort(adjusted)) >= -1e-15))
    check("most significant test gets the full family multiplier",
          close(adjusted[0], 0.004, 1e-12), f"got {adjusted[0]}")

    check("rejects p outside [0,1]", raises(ValueError, holm_correction, [0.5, 1.2]))
    check("rejects empty family", raises(ValueError, holm_correction, []))

    # Family of three pairwise comparisons, at the D3C shape: three models scoring the
    # same slices at roughly the observed glioma prediction rates.
    rng = np.random.default_rng(3)
    n_slices = 500
    e001 = (rng.random(n_slices) < 0.69).astype(int)
    e002 = (rng.random(n_slices) < 0.46).astype(int)
    e003 = (rng.random(n_slices) < 0.22).astype(int)

    family = mcnemar_family([
        ("E001 vs E002", e001, e002),
        ("E001 vs E003", e001, e003),
        ("E002 vs E003", e002, e003),
    ])
    check("family returns one result per comparison", len(family) == 3)
    check("family reports Holm-adjusted p-values",
          all(r.p_value_adjusted is not None for r in family))
    check("adjusted p-values are at least the raw ones",
          all(r.p_value_adjusted >= r.p_value - 1e-15 for r in family))


# ----------------------------------------------------------------------------------
# Random-intercept logistic regression
# ----------------------------------------------------------------------------------

def simulate_d3c_like(n_patients, slices_per_patient, betas, sigma, seed):
    """Three models scoring the same slices, with a shared per-patient intercept."""
    rng = np.random.default_rng(seed)
    model_names = ["E001", "E002", "E003"]

    patient_effects = rng.normal(0.0, sigma, size=n_patients)

    patient_ids, labels, outcomes = [], [], []

    for patient in range(n_patients):
        for model_position, model_name in enumerate(model_names):
            linear = betas[0] + (betas[model_position] if model_position > 0 else 0.0)
            probability = 1.0 / (1.0 + math.exp(-(linear + patient_effects[patient])))
            draws = rng.random(slices_per_patient) < probability

            patient_ids.extend([patient] * slices_per_patient)
            labels.extend([model_name] * slices_per_patient)
            outcomes.extend(draws.astype(float).tolist())

    return np.array(outcomes), labels, np.array(patient_ids)


def test_mixed_effects():
    print("\nRandom-intercept logistic regression")

    nodes, log_weights = gauss_hermite(31)
    check(
        "Gauss-Hermite weights sum to exactly 1",
        close(float(np.sum(np.exp(log_weights))), 1.0, 1e-12),
        f"got {float(np.sum(np.exp(log_weights))):.15f}",
    )

    # Analytic identity: at sigma = 0 the marginal log-likelihood must equal the
    # ordinary logistic log-likelihood, because the weights sum to 1 and every node
    # collapses onto the same linear predictor.
    rng = np.random.default_rng(11)
    n = 500
    X = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n)])
    beta_true = np.array([0.3, -0.8, 1.1])
    probability = 1.0 / (1.0 + np.exp(-(X @ beta_true)))
    y = (rng.random(n) < probability).astype(float)
    groups = rng.integers(0, 60, size=n)
    _, group_index = np.unique(groups, return_inverse=True)

    marginal = marginal_log_likelihood(
        beta_true, 0.0, X, y, group_index, int(group_index.max()) + 1, nodes, log_weights
    )
    eta = X @ beta_true
    plain = float(np.sum(y * eta - np.logaddexp(0.0, eta)))
    check(
        "sigma = 0 reproduces the logistic log-likelihood exactly",
        close(marginal, plain, 1e-9),
        f"marginal {marginal:.10f} vs plain {plain:.10f}",
    )

    # Parameter recovery on data simulated from the model.
    betas_true = [0.5, -1.0, -2.0]
    sigma_true = 1.2
    outcomes, labels, patient_ids = simulate_d3c_like(
        n_patients=400, slices_per_patient=5, betas=betas_true,
        sigma=sigma_true, seed=20260809,
    )

    result = fit_d3c_glioma_model(outcomes, labels, patient_ids, n_quadrature=31)
    print("        " + result.summary().replace("\n", "\n        "))

    check("fit converged", result.converged, result.message)

    estimates = {
        "intercept": (result.term("intercept").estimate, betas_true[0]),
        "model[E002]": (result.term("model[E002]").estimate, betas_true[1]),
        "model[E003]": (result.term("model[E003]").estimate, betas_true[2]),
    }
    for name, (estimate, truth) in estimates.items():
        std_error = result.term(name).std_error
        check(
            f"recovers {name} (true {truth})",
            abs(estimate - truth) < max(0.25, 3.5 * std_error),
            f"estimate {estimate:.4f}, SE {std_error:.4f}",
        )

    check(
        f"recovers group SD (true {sigma_true})",
        abs(result.group_sd - sigma_true) < 0.2,
        f"estimate {result.group_sd:.4f}",
    )
    check(
        "ICC equals sigma^2 / (sigma^2 + pi^2/3)",
        close(
            result.icc,
            result.group_sd**2 / (result.group_sd**2 + math.pi**2 / 3.0),
            1e-12,
        ),
    )
    check("standard errors are finite and positive",
          all(t.std_error > 0 and math.isfinite(t.std_error) for t in result.terms))
    check("the two model contrasts are detected as non-zero",
          result.term("model[E002]").p_value < 0.001
          and result.term("model[E003]").p_value < 0.001)

    # Quadrature adequacy: the answer must not depend on the node count.
    small_outcomes, small_labels, small_patients = simulate_d3c_like(
        n_patients=150, slices_per_patient=5, betas=betas_true,
        sigma=sigma_true, seed=5,
    )
    coarse = fit_d3c_glioma_model(small_outcomes, small_labels, small_patients, n_quadrature=21)
    fine = fit_d3c_glioma_model(small_outcomes, small_labels, small_patients, n_quadrature=41)
    largest_shift = max(
        abs(c.estimate - f.estimate) for c, f in zip(coarse.terms, fine.terms)
    )
    check(
        "estimates are stable between 21 and 41 quadrature nodes",
        largest_shift < 1e-3,
        f"largest shift {largest_shift:.3e}",
    )

    # With a negligible random effect the fit must agree with plain logistic regression.
    flat_outcomes, flat_labels, flat_patients = simulate_d3c_like(
        n_patients=200, slices_per_patient=5, betas=betas_true, sigma=0.01, seed=17
    )
    flat_fit = fit_d3c_glioma_model(flat_outcomes, flat_labels, flat_patients, n_quadrature=31)

    from sklearn.linear_model import LogisticRegression

    design, names, _ = build_categorical_design(flat_labels)
    plain_fit = LogisticRegression(penalty=None, max_iter=5000)
    plain_fit.fit(design[:, 1:], flat_outcomes)

    plain_coefficients = [float(plain_fit.intercept_[0])] + [
        float(v) for v in plain_fit.coef_[0]
    ]
    largest_gap = max(
        abs(t.estimate - p) for t, p in zip(flat_fit.terms, plain_coefficients)
    )
    check(
        "reduces to ordinary logistic regression when the random effect vanishes",
        largest_gap < 0.05,
        f"largest gap {largest_gap:.4f}",
    )

    print("\nDesign matrix construction")

    X_design, term_names, reference = build_categorical_design(
        ["E001", "E002", "E003", "E001"]
    )
    check("design has an intercept and one dummy per non-reference level",
          X_design.shape == (4, 3), f"shape {X_design.shape}")
    check("reference level is the first sorted level", reference == "E001")
    check("term names identify the levels",
          term_names == ["intercept", "model[E002]", "model[E003]"], f"got {term_names}")
    check("intercept column is all ones", np.all(X_design[:, 0] == 1.0))
    check("reference rows have zero in every dummy",
          np.all(X_design[0, 1:] == 0.0) and np.all(X_design[3, 1:] == 0.0))

    X_design, term_names, reference = build_categorical_design(
        ["E001", "E002", "E003"], reference="E003"
    )
    check("explicit reference level is honoured",
          reference == "E003"
          and term_names == ["intercept", "model[E001]", "model[E002]"])

    check("rejects a single level",
          raises(ValueError, build_categorical_design, ["E001", "E001"]))
    check("rejects an unknown reference",
          raises(ValueError, build_categorical_design, ["E001", "E002"], "E999"))
    check("rejects non-binary outcomes",
          raises(ValueError, fit_random_intercept_logistic,
                 np.ones((4, 1)), np.array([0.0, 1.0, 2.0, 1.0]), np.arange(4)))


def main():
    print("src/stats unit tests")

    test_wilson()
    test_clustered_bootstrap()
    test_mcnemar()
    test_mixed_effects()

    print(f"\n{PASSED} passed, {len(FAILURES)} failed")

    for name, detail in FAILURES:
        print(f"  FAILED: {name}  {detail}")

    return len(FAILURES)


if __name__ == "__main__":
    sys.exit(main())
