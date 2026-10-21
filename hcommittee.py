"""Heterogeneous committees: membranes at different resolutions voting.

One membrane sees 8 amplitudes; others see the same patterns through
different coarse-grainings (merge qubit 0 / 1 / 2 -> 4 amps; merge
0+1 -> 2 amps). Each member projects the probe at its own resolution
and votes. Majority wins; ties break by highest vote weight.

The question: does heterogeneity by design -- members that differ
in *resolution*, not just random seeds -- beat the best single
member? And where (which noise level) does the gain come from?

Whatever the numbers say is the finding, including "it doesn't help".
"""

import math
import random


def normalize(v):
    n = math.sqrt(sum(abs(c) ** 2 for c in v))
    return [c / n for c in v]


def overlap(field, pattern):
    return sum(p.conjugate() * f for p, f in zip(pattern, field))


def noisy(state, sigma, rng):
    return normalize([c + complex(rng.gauss(0, sigma), rng.gauss(0, sigma))
                      for c in state])


def merge_qubit(state, q):
    """Haar low-pass merging qubit q: 2^n -> 2^(n-1) amplitudes."""
    s2 = math.sqrt(2.0)
    out = []
    for i in range(len(state)):
        j = i ^ (1 << q)
        if j > i:
            out.append((state[i] + state[j]) / s2)
    return normalize(out)


def merge_qubits(state, qs):
    """Merge a set of *original* qubit indices (order-independent).
    After merging qubit q, higher original qubits shift down by one,
    which the index adjustment handles."""
    for shift, q in enumerate(sorted(set(qs))):
        state = merge_qubit(state, q - shift)
    return state


class Member:
    """One committee member: a fixed resolution (set of original
    qubits merged away) and the patterns stored at that resolution."""

    def __init__(self, name, merge_set, patterns):
        self.name = name
        self.merge_set = set(merge_set)
        # normalize AFTER merging: merge_qubit normalizes, but the
        # empty merge set (full resolution) must normalize too --
        # otherwise an unnormalized pattern's overlaps are inflated
        # and it wins every vote.
        self.patterns = [normalize(merge_qubits(p, self.merge_set))
                         for p in patterns]

    def _view(self, probe):
        return merge_qubits(probe, self.merge_set)

    def vote(self, probe):
        """(winner, weight): winner by max overlap, weight = top prob."""
        pv = self._view(probe)
        ms = [overlap(pv, p) for p in self.patterns]
        tot = sum(abs(m) ** 2 for m in ms)
        w = max(range(len(ms)), key=lambda i: abs(ms[i]))
        return w, (abs(ms[w]) ** 2 / tot if tot else 0.0)


class Committee:
    def __init__(self, members):
        self.members = members

    def decide(self, probe):
        """Majority vote; ties broken by highest vote weight.
        Returns (winner, votes_per_member, all_agree)."""
        votes = [m.vote(probe) for m in self.members]
        tally = {}
        for w, wt in votes:
            tally[w] = tally.get(w, [0, 0.0])
            tally[w][0] += 1
            tally[w][1] = max(tally[w][1], wt)
        winner = max(tally, key=lambda w: (tally[w][0], tally[w][1]))
        return winner, votes, len(tally) == 1

    def oracle(self, probe, label):
        """1 if ANY member is right: the headroom upper bound."""
        return any(m.vote(probe)[0] == label for m in self.members)
