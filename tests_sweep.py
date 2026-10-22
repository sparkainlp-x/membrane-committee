"""Tests for the correctness gate and the seed sweep. Run: python -m pytest"""

import math
import random

from demo_refusing import MEMBERS, PATTERNS
from rcommittee import RefusingMember, noisy
import sweep_refusing as sw


def test_correctness_gate_deterministic_and_bounded():
    a = RefusingMember("full", set(), PATTERNS).calibrate_correctness(seed=3)
    b = RefusingMember("full", set(), PATTERNS).calibrate_correctness(seed=3)
    assert a == b
    assert 0.0 <= a["tau"] <= 1.0 and a["J"] >= 0.0
    assert a["n_right"] + a["n_wrong"] == 200


def test_correctness_gate_without_errors_disables_gate():
    m = RefusingMember("full", set(), PATTERNS)
    r = m.calibrate_correctness(sigma=0.0, n=20, seed=1)
    assert r["n_wrong"] == 0 and m.tau == 0.0


def test_mean_se():
    m, se = sw.mean_se([1.0, 2.0, 3.0])
    assert m == 2.0 and abs(se - 1 / math.sqrt(3)) < 1e-12
    assert sw.mean_se([5.0]) == (5.0, 0.0)


def test_calibration_and_evaluation_seeds_disjoint():
    cal = {10_000_000 + 1000 * k + i for k in range(sw.N_SETS) for i in range(len(MEMBERS))}
    ev = {20_000_000 + 10_000 * k + s for k in range(sw.N_SETS) for s in range(sw.N_TRIALS)}
    assert not cal & ev


def test_sweep_small_run_shape_and_paired_difference():
    r = sw.run(n_sets=3)
    for gate in ("ood", "correctness"):
        rows = r[gate]["rows"]
        assert set(rows) == set(sw.SIGMAS)
        for row in rows.values():
            assert abs(row["diff"][0] - (row["refusing"][0] - row["plain"][0])) < 1e-12
            assert 0 <= row["refusal_rate"][0] <= 1
    assert r["ood"]["rows"][0.1]["plain"][0] == 1.0


def test_report_text_is_labelled_and_deterministic():
    a, _ = sw.report(n_sets=2)
    b, _ = sw.report(n_sets=2)
    assert a == b and a.startswith("SYNTHETIC")


def test_member_votes_reported_per_member():
    r = sw.run(n_sets=2)
    conf = r["ood"]["rows"][0.25]["conf"]
    total = sum(conf[f"m{i}_right"][1] + conf[f"m{i}_wrong"][1] for i in range(len(MEMBERS)))
    assert total == 2 * sw.N_TRIALS * len(MEMBERS)
    rng = random.Random(0)
    assert noisy(PATTERNS[0], 0.1, rng)
