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
whole game.** The oracle column shows the information exists in
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

# v0.2.0: the refusing committee

## Question

Does a per-member refusal gate fix the committee? Each member calibrates a threshold tau on its maximum overlap (Youden's J), freezes it, and votes only when the overlap reaches tau. The received package compared one calibration and evaluation seed set; `sweep_refusing.py` repeats the comparison on 20 disjoint seed sets and reports mean and standard error, with the paired difference on the same probes.

## Findings (results_refusing.md)

- With the received gate (in-library vs random states), the refusing committee is below the plain committee at sigma = 0.25 by 0.025 ± 0.004, and by 0.140 ± 0.009 at sigma = 0.50, where 21% of probes are refused. The received text mentioned "three seed sets" and a refusal rate of "17-30%"; neither is in the received code, so both are replaced by these sweep numbers.
- The received explanation was that the committee's errors are high-confidence. Measured per member, wrong votes have slightly lower overlap than right ones for four of five members, but the distributions overlap heavily. For the 2-amplitude member, wrong votes have higher overlap. The plain committee's winning votes differ by only about 0.01 between right and wrong outcomes. So the errors are not reliably low-confidence, and an overlap threshold cannot remove them.
- A gate calibrated on right vs wrong votes (gate B) does worse: -0.114 ± 0.010 at sigma = 0.25. Because the 2-amplitude member's errors cannot be separated by overlap (J about 0.02), its threshold ends near zero and it keeps voting, while the full-resolution member is silenced more often.

## Limits

- Toy scale: 3 qubits, 4 patterns, 5 members, majority vote.
- Gates use overlap magnitude only, are calibrated per member (not jointly for the committee), and are frozen at sigma = 0.25.
- Refusal counts as a miss. Where deferring has value, the trade-off would look different.
