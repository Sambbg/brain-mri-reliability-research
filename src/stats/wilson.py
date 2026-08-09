"""Wilson score intervals for binomial proportions.

The Wilson interval is used in preference to the Wald interval because the Wald
interval degenerates to zero width at p = 0 and p = 1 and undercovers badly for small
n -- both of which matter here, where per-class glioma prediction rates can sit close
to the boundary.

Not wired into the pipeline. Import with:

    import sys; sys.path.insert(0, "src/stats")
    from wilson import wilson_interval
"""

from dataclasses import dataclass
import math

from scipy.stats import norm


@dataclass(frozen=True)
class ProportionInterval:
    successes: int
    n: int
    proportion: float
    lower: float
    upper: float
    confidence: float

    @property
    def width(self) -> float:
        return self.upper - self.lower

    def format(self, digits: int = 4) -> str:
        return (
            f"{self.proportion:.{digits}f} "
            f"({self.lower:.{digits}f}, {self.upper:.{digits}f})"
        )


def z_for_confidence(confidence: float) -> float:
    """Two-sided normal critical value, e.g. 1.959964 at 95 per cent."""
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0, 1), got {confidence!r}")

    return float(norm.ppf(0.5 + confidence / 2.0))


def wilson_interval(successes: int, n: int, confidence: float = 0.95) -> ProportionInterval:
    """Wilson score interval for a binomial proportion.

    The bounds are the two roots in p of the score equation

        |p_hat - p| / sqrt(p (1 - p) / n) = z

    which is why the interval stays inside [0, 1] and never has zero width at the
    boundaries. Solving that quadratic gives the closed form below.
    """
    if n <= 0:
        raise ValueError(f"n must be positive, got {n!r}")

    if not 0 <= successes <= n:
        raise ValueError(f"successes must be in [0, {n}], got {successes!r}")

    z = z_for_confidence(confidence)
    p_hat = successes / n
    z_squared = z * z

    denominator = 1.0 + z_squared / n
    centre = (p_hat + z_squared / (2 * n)) / denominator
    half_width = (z / denominator) * math.sqrt(
        p_hat * (1.0 - p_hat) / n + z_squared / (4 * n * n)
    )

    return ProportionInterval(
        successes=int(successes),
        n=int(n),
        proportion=p_hat,
        # Clamp only to absorb floating point drift at the boundaries; the algebraic
        # bounds already lie within [0, 1].
        lower=max(0.0, centre - half_width),
        upper=min(1.0, centre + half_width),
        confidence=confidence,
    )


def wilson_interval_from_flags(flags, confidence: float = 0.95) -> ProportionInterval:
    """Wilson interval for an iterable of 0/1 or boolean outcomes."""
    values = [bool(v) for v in flags]

    if not values:
        raise ValueError("flags is empty")

    return wilson_interval(sum(values), len(values), confidence=confidence)
