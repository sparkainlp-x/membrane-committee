# Changelog

## 0.2.0 (2026-10-22)

- Archived on Zenodo: version DOI [10.5281/zenodo.23583048](https://doi.org/10.5281/zenodo.23583048), concept DOI [10.5281/zenodo.23583047](https://doi.org/10.5281/zenodo.23583047).
- Added the refusing committee (`rcommittee.py`, `demo_refusing.py`, `tests_refusing.py`): per-member refusal gates calibrated by Youden's J and frozen, majority among voters, committee refusal when all members refuse. The package as received is kept unchanged in `spec/refusing-committee/`.
- Added `sweep_refusing.py` and `results_refusing.md`: 20 disjoint calibration and evaluation seed sets, mean and standard error per noise level, paired refusing-minus-plain difference.
- Added a measurement of vote confidence for right vs wrong votes per member, testing the "high-confidence errors" explanation. It holds only in part.
- Added a gate calibrated on right vs wrong votes (`calibrate_correctness`) on held-out seeds, compared with the received gate. It performs worse.
- Removed claims the received package did not support ("three independent seed sets", a "17-30%" refusal range, "Verified" headings) and corrected test counts.
- Wording: "proves" changed to "shows" for the oracle headroom.
- Added a pytest configuration (25 tests, warnings are errors), and CI now runs pytest, both demos and a short sweep on Python 3.10 to 3.13.
- Author: Jean-François Brisson. Mun Seok Lee is credited in the acknowledgements only.

## 0.1.0 (2026-10-21)

- Heterogeneous committee of five membranes at different coarse-graining resolutions; majority, confidence-weighted and reliability-weighted voting; oracle headroom; normalization regression test.
