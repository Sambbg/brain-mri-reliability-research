# Email draft

**To:** Assoc. Prof. Ir. Dr. Tan Tian Swee
**Subject:** Seed sweep completed ? correction to earlier results

---

Dear Dr. Tan,

I have completed the five-seed sweep across all three architectures, giving 15 training
runs in place of the earlier three. I need to report something I found in the process.

The earlier draft's Chapter 4 draws its internal, calibration and D3B numbers from one
set of trained checkpoints and its D3C numbers from another. They were trained at
different times on different machines. The study's headline claim ? that the
architecture ordering reverses between the canine and human probes ? was an artefact of
that mixing. Under the sweep the ordering is the same on both probes, and ResNet18 ranks
first on the human probe in all five seeds. There is no reversal.

Three smaller claims were also single-seed artefacts: the D3B prediction distributions,
the apparent per-architecture differences in learned temperature, and the finding that
ViT-B/16 was the best-improved model under calibration. Across seeds ViT is consistently
the worst calibrated.

The corrected result is better evidenced than the one it replaces. Internal macro-F1
cannot reliably rank these three architectures: the spread between architecture means is
0.0116 against a mean seed standard deviation of 0.0046, the top two differ by 0.0011,
and the ordering changes between seeds. The human shifted-domain probe does separate
them, consistently. And the association between internal performance and shift behaviour
reverses sign when centred within architecture ? a Simpson's paradox specific to the
human probe.

This supports a clearer claim than the original: on this benchmark, the standard
single-run internal metric does not carry the architecture-comparison signal the
literature routinely draws from it.

I have regenerated every table and figure from a single verified run set, and added a
check that refuses to produce a summary unless all runs share one run identifier, data
split, seed set and evaluation cohort. The earlier run sets are preserved as the
historical record.

Chapters 4 and 5 need rewriting against the corrected results, which I am starting now.
I have attached a full memo with the numbers and the evidence trail.

I would rather raise this now than have it surface later.

Kind regards,
Samuel Bertrand Bernard Gonzalves
MKE251020
