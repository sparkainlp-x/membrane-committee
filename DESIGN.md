# DESIGN — Deep think: heterogeneous committees

## The hypothesis

Heterogeneity by design, inside the memory itself: five membranes
seeing the same patterns at different resolutions (full 8 amps;
merge qubit {0} / {1} / {2} → 4 amps; merge {0,1} → 2 amps),
voting. Members genuinely disagree (disagreement rate 0.44–0.94
across noise levels). Surely the ensemble beats any single member?

## The finding: no.

Neither majority vote, confidence-weighted vote, nor
reliability-weighted vote (members weighted by calibration
accuracy) beats the best single member at σ 0.10–0.50. At σ=0.75
the committee edges past it by 0.015–0.025, a small margin
near chance on 200 trials:

| σ    | best single | majority | weighted | oracle |
|------|-------------|----------|----------|--------|
| 0.10 | 1.000       | 0.995    | 0.995    | 1.000  |
| 0.25 | 0.925       | 0.860    | 0.870    | 0.970  |
| 0.50 | 0.690       | 0.675    | 0.685    | 0.890  |
| 0.75 | 0.515       | 0.530    | 0.540    | 0.805  |

**Heterogeneity alone does not help. The aggregation rule is the
whole game.** The oracle column proves the information exists in
the ensemble — on 97% of trials at σ=0.25 *some* member is right —
but no tested voting rule extracts it. Diversity without a good
aggregator is just disagreement.

## The bug the measurement caught

First run showed coarse members *crushing* full resolution
(0.98 vs 0.60). It was a normalization bug: the full-resolution
member (empty merge set) skipped the normalization that
merge_qubit applies, so one unnormalized pattern's overlaps were
inflated and it won every vote. The "surprising" result was an
artifact. After the fix, full resolution is the best single
member everywhere — which is itself the honest baseline the
committee fails to beat. There is a regression test pinning this.

## Why this matters beyond the toy

This is a counterpoint with teeth for the heterogeneity debate:
heterogeneity by design in the *agents* is not sufficient — the
*shared aggregation* (the common scale, the decision rule) does
the real work. A committee of diverse members with a naive vote
is strictly worse than the best member alone. Anyone selling
"ensemble = better" owes you the aggregation analysis, not just
the diversity.

## Honest limits

- **Toy scale** (3 qubits, 4 patterns, 5 members, 3 voting rules).
  A smarter aggregator (learned weights, stacking, per-noise
  routing) might win — untested here, claimed nowhere.
- **Majority vote is one rule.** The negative result covers the
  three rules tested, not all possible rules.
- **Resolution is one heterogeneity axis.** Different pattern
  subsets, different noise models per member, or mixed
  architectures could behave differently.
- The oracle is a headroom bound, not a method — it peeks at the
  label.
