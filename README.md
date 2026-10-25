# Membrane Committee

Software DOI for v0.2.0: [10.5281/zenodo.23583048](https://doi.org/10.5281/zenodo.23583048) (all versions: [10.5281/zenodo.23583047](https://doi.org/10.5281/zenodo.23583047)).

**Heterogeneity by design, inside the memory — and the honest
finding that it isn't enough.**

Five holographic membranes see the same patterns at different
resolutions (full, three 4-amp coarse views, one 2-amp view) and
vote. Majority, confidence-weighted, and reliability-weighted
rules fail to beat the best single member at low-to-moderate noise
(σ 0.10–0.50) and only edge past it by 0.015–0.025 at σ=0.75, near
chance — while the oracle
gap shows the information is there. Diversity without a good
aggregator is just disagreement. Stdlib-only Python. AGPL-3.0.

> Synthetic toy simulation; classical software; not physical holography
> hardware. "Qubit" and "amplitude" refer to classically simulated
> 8-amplitude state vectors; nothing here runs on quantum hardware.

## Measured in this repo (v0.1.0 committee)

- Members genuinely disagree (0.44–0.94 across noise levels)
- No voting rule beats best-single at σ 0.10–0.50; at σ=0.75 majority
  (0.530) and weighted (0.540) narrowly beat best-single (0.515),
  a small margin near chance
- Oracle headroom 0.81–1.00: the information exists, no tested
  rule extracts it
- A regression test pins the normalization bug the measurements
  caught

## Run it

```bash
python tests.py              # 8 script-style tests (v0.1.0 committee)
python tests_refusing.py     # 10 script-style tests (refusing committee)
python demo.py               # member accuracies, committee, oracle, disagreement
python demo_refusing.py      # one seed set: calibration table and comparison
python sweep_refusing.py     # 20 seed sets, about 5 s (results_refusing.md)
pip install -r requirements-dev.txt && python -m pytest -q   # 25 tests, warnings are errors
```

## v0.2.0: the refusing committee (unreleased)

Each member gets its own refusal gate on its maximum overlap: it votes only when the overlap reaches a threshold tau, frozen after calibration at sigma = 0.25 on seeds kept apart from the evaluation seeds. The majority is taken among voters, and if every member refuses, the committee refuses. A refusal counts as a miss. Code: `rcommittee.py`, `demo_refusing.py`, `sweep_refusing.py`; full output in [results_refusing.md](results_refusing.md).

**SYNTHETIC.** 20 independent seed sets, 200 fresh probes per noise level each. Values are mean ± standard error over seed sets; "refusing - plain" is the paired difference on the same probes. Noise levels other than 0.25 are a shift from the calibration setting.

**Gate A, as received: in-library probes vs random states.**

| sigma | plain | refusing | refusing - plain | refusal rate | acc on answered | best single |
|---|---|---|---|---|---|---|
| 0.1 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |
| 0.25 | 0.862 ± 0.005 | 0.837 ± 0.007 | -0.025 ± 0.004 | 0.022 ± 0.003 | 0.856 ± 0.006 | 0.917 ± 0.005 |
| 0.5 | 0.542 ± 0.011 | 0.402 ± 0.012 | -0.140 ± 0.009 | 0.207 ± 0.009 | 0.506 ± 0.012 | 0.591 ± 0.010 |
| 0.75 | 0.406 ± 0.009 | 0.263 ± 0.009 | -0.143 ± 0.009 | 0.285 ± 0.010 | 0.368 ± 0.012 | 0.441 ± 0.009 |

**Gate B, calibrated on each member's right vs wrong votes** (held-out calibration seeds):

| sigma | plain | refusing | refusing - plain | refusal rate | acc on answered | best single |
|---|---|---|---|---|---|---|
| 0.1 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |
| 0.25 | 0.862 ± 0.005 | 0.748 ± 0.010 | -0.114 ± 0.010 | 0.035 ± 0.011 | 0.777 ± 0.013 | 0.917 ± 0.005 |
| 0.5 | 0.542 ± 0.011 | 0.343 ± 0.012 | -0.199 ± 0.014 | 0.139 ± 0.043 | 0.411 ± 0.016 | 0.591 ± 0.010 |
| 0.75 | 0.406 ± 0.009 | 0.255 ± 0.014 | -0.150 ± 0.016 | 0.177 ± 0.053 | 0.321 ± 0.011 | 0.441 ± 0.009 |

**Confidence of right vs wrong votes** (max overlap; mean when right / mean when wrong, with the share of votes that are wrong):

| sigma | full | mrg0 | mrg1 | mrg2 | mrg01 | plain committee winners |
|---|---|---|---|---|---|---|
| 0.1 | 0.937 / - (0.00) | 0.952 / 0.928 (0.01) | 0.952 / 0.925 (0.01) | 0.952 / 0.915 (0.01) | 0.972 / 0.985 (0.40) | 0.951 / - (0.00) |
| 0.25 | 0.746 / 0.681 (0.08) | 0.824 / 0.793 (0.27) | 0.828 / 0.789 (0.28) | 0.825 / 0.793 (0.27) | 0.896 / 0.933 (0.61) | 0.811 / 0.800 (0.14) |
| 0.5 | 0.592 / 0.535 (0.41) | 0.719 / 0.694 (0.56) | 0.723 / 0.697 (0.56) | 0.723 / 0.695 (0.56) | 0.847 / 0.863 (0.71) | 0.702 / 0.692 (0.46) |
| 0.75 | 0.534 / 0.502 (0.56) | 0.685 / 0.664 (0.66) | 0.684 / 0.667 (0.65) | 0.684 / 0.668 (0.65) | 0.829 / 0.838 (0.74) | 0.667 / 0.662 (0.59) |

In plain terms:

- **Refusal does not fix the committee.** With gate A it scores below the plain committee at every noise level above 0.1, and below the best single member everywhere.
- **At sigma = 0.25 the drop is small but resolved.** The paired drop is 0.025 ± 0.004 over 20 seed sets. A single seed set of 200 probes (as in the received demo) has a standard error of roughly 0.02, so one run alone could not distinguish this gap from noise.
- **Under shift the drop is large.** At sigma = 0.5 it is 0.140 ± 0.009, with 21% of probes refused; at 0.75 it is 0.143 ± 0.009, with 29% refused.
- **"High-confidence errors" holds only in part.** For four members, wrong votes have slightly lower overlap than right ones: for the full-resolution member, 0.681 vs 0.746 at sigma = 0.25. The two distributions overlap heavily, so a threshold on overlap separates them poorly (Youden J from 0.20 to 0.37). For the coarsest member (2 amplitudes), wrong votes have *higher* overlap than right ones. The plain committee's winning votes have almost the same overlap whether the committee is right or wrong (0.811 vs 0.800).
- **A gate tuned on right vs wrong is worse, not better.** It drops the paired difference to -0.114 ± 0.010 at sigma = 0.25. Its threshold for the coarsest member is near zero (J = 0.02, so it almost never silences that member), while it silences the full-resolution member, the most accurate one, more often than gate A does.

## Honest limits

Toy scale; three voting rules tested (a smarter aggregator might
win — untested, claimed nowhere); resolution is one heterogeneity
axis; the oracle peeks at the label. For the refusing committee: per-member gates on overlap magnitude with majority vote only, gates frozen at one noise level, refusal counted as a miss. Full account in `DESIGN.md`.

## Provenance

A package received under Mun Seok Lee's name, which lists him as sole author under AGPL-3.0-only, is kept unchanged in [spec/refusing-committee/](spec/refusing-committee/). We could not independently verify who wrote it. The refusing-committee code in this repository is derived from it: `rcommittee.py` is about 92% line-similar to the received `rcommittee.py`, and `demo_refusing.py` and `tests_refusing.py` are about 99% similar to the received `demo.py` and `tests.py`. The original committee (`hcommittee.py`, `demo.py`, `tests.py`) was committed before the received package was added and is not derived from it. `sweep_refusing.py`, `tests_sweep.py` and `results_refusing.md` were added by this project. Line similarity here comes from a plain diff, not from a review of intent. [CHANGELOG.md](CHANGELOG.md) lists the changes. Mun Seok Lee is not an author of this release, and he has not reviewed or endorsed this software.

## Acknowledgements

Thanks to Mun Seok Lee for the package received under his name (see Provenance above). This is an acknowledgement only: it implies no endorsement of this code or its conclusions.

## License

Copyright (c) 2026 Jean-François Brisson, Spark AI NLP.

This software is available under the GNU Affero General Public License v3.0 only (AGPL-3.0-only); see [LICENSE](LICENSE).
