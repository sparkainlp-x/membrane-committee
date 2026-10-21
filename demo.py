"""Demo: does a heterogeneous committee beat its best member?

Patterns (3 qubits, 8 amplitudes): GHZ, W, |000>, |+++>.
Members: full resolution + four coarse members (merge {0}, {1},
{2}, {0,1}). 200 seeded trials per noise level; each trial picks a
random true pattern and a noisy probe.

Reports per sigma: each member's accuracy, committee accuracy,
oracle headroom (any member right), and disagreement rate (the
heterogeneity measure).

Run: python demo.py
"""

import random

from hcommittee import Committee, Member, noisy

S2 = 2 ** -0.5
S3 = 3 ** -0.5
S8 = 1.0 / (2 * S2)  # 1/sqrt(8)

PATTERNS = [
    [S2, 0j, 0j, 0j, 0j, 0j, 0j, S2],          # GHZ
    [0j, S3, S3, 0j, S3, 0j, 0j, 0j],          # W
    [1, 0j, 0j, 0j, 0j, 0j, 0j, 0j],           # |000>
    [S8] * 8,                                   # |+++>
]
NAMES = ["GHZ", "W", "|000>", "|+++>"]

MEMBERS = [
    ("full", set()),
    ("mrg0", {0}),
    ("mrg1", {1}),
    ("mrg2", {2}),
    ("mrg01", {0, 1}),
]


def trial(com, sigma, seed):
    rng = random.Random(seed)
    label = rng.randrange(len(PATTERNS))
    probe = noisy(PATTERNS[label], sigma, rng)
    winner, votes, agree = com.decide(probe)
    # confidence-weighted vote as second aggregation rule
    score = {}
    for w_, wt in votes:
        score[w_] = score.get(w_, 0.0) + wt
    wtd = max(score, key=lambda w_: score[w_])
    return winner == label, wtd == label, com.oracle(probe, label), agree, \
        [m.vote(probe)[0] == label for m in com.members]


def main():
    members = [Member(name, ms, PATTERNS) for name, ms in MEMBERS]
    com = Committee(members)
    print(f"{'sigma':>6} " + " ".join(f"{n:>7}" for n, _ in MEMBERS) +
          f" {'commit':>7} {'weight':>7} {'oracle':>7} {'disagr':>7}")
    for sigma in (0.10, 0.25, 0.50, 0.75):
        n = 200
        acc = [0] * len(members)
        c_ok = w_ok = o_ok = dis = 0
        for s in range(n):
            ok, wok, orc, agree, moks = trial(com, sigma, 5000 + s)
            for i, mk in enumerate(moks):
                acc[i] += mk
            c_ok += ok
            w_ok += wok
            o_ok += orc
            dis += (not agree)
        row = " ".join(f"{a / n:>7.3f}" for a in acc)
        print(f"{sigma:>6.2f} {row} {c_ok / n:>7.3f} {w_ok / n:>7.3f} "
              f"{o_ok / n:>7.3f} {dis / n:>7.3f}")
    print("\nRESULT: heterogeneity alone does not beat the best member --")
    print("the aggregation rule is the whole game (see DESIGN.md).")


if __name__ == "__main__":
    main()
