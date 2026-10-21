"""Tests for membrane-committee. Run: python tests.py"""

import math
import random

from hcommittee import (Committee, Member, merge_qubit, merge_qubits,
                        normalize, noisy)

S2 = 2 ** -0.5


def test_merge_qubit_known():
    # GHZ = (|000> + |111>)/sqrt2; merging qubit 2 (MSB) pairs
    # (0,4): s2/sqrt2, (3,7): s2/sqrt2 -> [s2,0,0,s2] after renorm.
    ghz = [S2, 0j, 0j, 0j, 0j, 0j, 0j, S2]
    m = merge_qubit(ghz, 2)
    assert len(m) == 4
    assert abs(m[0] - S2) < 1e-12 and abs(m[3] - S2) < 1e-12
    assert abs(m[1]) < 1e-12 and abs(m[2]) < 1e-12


def test_merge_qubit_preserves_norm():
    rng = random.Random(4)
    v = normalize([complex(rng.gauss(0, 1), rng.gauss(0, 1))
                   for _ in range(8)])
    for q in (0, 1, 2):
        m = merge_qubit(v, q)
        assert abs(sum(abs(c) ** 2 for c in m) - 1.0) < 1e-12


def test_merge_set_order_independent():
    rng = random.Random(5)
    v = normalize([complex(rng.gauss(0, 1), rng.gauss(0, 1))
                   for _ in range(8)])
    a = merge_qubits(v, {0, 1})
    b = merge_qubits(v, {1, 0})
    assert len(a) == 2
    assert max(abs(x - y) for x, y in zip(a, b)) < 1e-12


def test_member_normalizes_even_without_merge():
    # regression: the full-resolution member once skipped
    # normalization, inflating one pattern's overlaps so it won
    # every vote. Stored patterns must be unit norm, always.
    bad = [0.7071] * 8  # norm 2, not 1
    m = Member("full", set(), [bad, [1] + [0j] * 7])
    for p in m.patterns:
        assert abs(sum(abs(c) ** 2 for c in p) - 1.0) < 1e-12


def test_clean_probe_unanimous():
    pats = [[1] + [0j] * 7, [0j] * 7 + [1]]
    com = Committee([Member("full", set(), pats),
                     Member("mrg0", {0}, pats)])
    w, votes, agree = com.decide(pats[0])
    assert w == 0 and agree


def test_tiebreak_deterministic():
    pats = [[1] + [0j] * 7, [0j] * 7 + [1]]
    com = Committee([Member("a", set(), pats), Member("b", {0}, pats)])
    r1 = com.decide(pats[1])
    r2 = com.decide(pats[1])
    assert r1[0] == r2[0]


def test_decision_deterministic():
    rng = random.Random(6)
    pats = [[1] + [0j] * 7, [0j] * 7 + [1]]
    com = Committee([Member("full", set(), pats)])
    p1 = noisy(pats[0], 0.3, rng)
    rng = random.Random(6)
    p2 = noisy(pats[0], 0.3, rng)
    assert com.decide(p1)[0] == com.decide(p2)[0]


def test_members_genuinely_disagree():
    # heterogeneity is real: at high noise the members don't all
    # vote together.
    S8 = 1 / math.sqrt(8)
    pats = [[S2, 0j, 0j, 0j, 0j, 0j, 0j, S2], [S8] * 8]
    com = Committee([Member("full", set(), pats),
                     Member("mrg01", {0, 1}, pats)])
    dis = 0
    for s in range(50):
        rng = random.Random(1000 + s)
        probe = noisy(pats[rng.randrange(2)], 0.75, rng)
        dis += (not com.decide(probe)[2])
    assert dis > 0


if __name__ == "__main__":
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith("test_")]):
        fn()
        print(f"PASS {name}")
    print("all tests passed")
