# Membrane Committee

**Heterogeneity by design, inside the memory — and the honest
finding that it isn't enough.**

Five holographic membranes see the same patterns at different
resolutions (full, three 4-amp coarse views, one 2-amp view) and
vote. Majority, confidence-weighted, and reliability-weighted
rules fail to beat the best single member at low-to-moderate noise
(σ 0.10–0.50) and only edge past it by 0.015–0.025 at σ=0.75, near
chance — while the oracle
gap proves the information is there. Diversity without a good
aggregator is just disagreement. Stdlib-only Python. AGPL-3.0.

> Synthetic toy simulation; classical software; not physical holography
> hardware. "Qubit" and "amplitude" refer to classically simulated
> 8-amplitude state vectors; nothing here runs on quantum hardware.

## Verified

- Members genuinely disagree (0.44–0.94 across noise levels)
- No voting rule beats best-single at σ 0.10–0.50; at σ=0.75 majority
  (0.530) and weighted (0.540) narrowly beat best-single (0.515),
  a small margin near chance
- Oracle headroom 0.81–1.00: the information exists, no tested
  rule extracts it
- 8/8 tests pass, including a regression test for the
  normalization bug the measurements caught

## Run it

```bash
python tests.py   # 8 tests
python demo.py    # member accuracies, committee, oracle, disagreement
```

## Honest limits

Toy scale; three voting rules tested (a smarter aggregator might
win — untested, claimed nowhere); resolution is one heterogeneity
axis; the oracle peeks at the label. Full account in `DESIGN.md`.
