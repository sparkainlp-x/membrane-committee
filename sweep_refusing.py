"""Seed sweep for the refusing committee. SYNTHETIC data only.

For each of N_SETS independent seed sets (calibration seeds and
evaluation seeds disjoint), every member is calibrated at sigma=0.25
and the committee is evaluated on 200 fresh probes per sigma.
Reported: mean and standard error over seed sets, plus the paired
difference refusing - plain (same probes).

Also measured:
  * confidence of member votes that are right vs wrong, and of the
    winning votes when the plain committee is right vs wrong
    (tests the "high-confidence errors" explanation);
  * a gate calibrated on right-vs-wrong votes (held-out calibration
    seeds) compared with the in-library-vs-random gate.

Run: python sweep_refusing.py [n_sets]
"""

import math
import random
import statistics
import sys

from demo_refusing import MEMBERS, PATTERNS
from rcommittee import RefusingCommittee, RefusingMember, noisy

SIGMAS = (0.10, 0.25, 0.50, 0.75)
N_TRIALS = 200
N_SETS = 20


def mean_se(xs):
    m = statistics.fmean(xs)
    se = statistics.stdev(xs) / math.sqrt(len(xs)) if len(xs) > 1 else 0.0
    return m, se


def build(set_index, gate):
    members = [RefusingMember(n, ms, PATTERNS) for n, ms in MEMBERS]
    for i, m in enumerate(members):
        seed = 10_000_000 + 1000 * set_index + i        # calibration seeds
        if gate == "ood":
            rep = m.calibrate(sigma=0.25, n_in=100, n_ood=100, seed=seed)
        else:
            rep = m.calibrate_correctness(sigma=0.25, n=200, seed=seed)
        m.calib_J = rep["J"]
    return RefusingCommittee(members)


def evaluate(com, sigma, set_index):
    acc = ref = ans_ok = ans = plain = 0
    single = [0] * len(com.members)
    conf = {"plain_right": [], "plain_wrong": []}
    for i in range(len(com.members)):
        conf[f"m{i}_right"], conf[f"m{i}_wrong"] = [], []
    for s in range(N_TRIALS):
        rng = random.Random(20_000_000 + 10_000 * set_index + s)  # evaluation seeds
        label = rng.randrange(len(PATTERNS))
        probe = noisy(PATTERNS[label], sigma, rng)
        status, winner, _ = com.decide(probe)
        if status == "refuse":
            ref += 1
        else:
            ans += 1
            ans_ok += winner == label
            acc += winner == label
        votes = [m.vote(probe) for m in com.members]
        pw = com._majority(votes)
        plain += pw == label
        for i, (w, _) in enumerate(votes):
            single[i] += w == label
            c = com.members[i].max_overlap(probe)
            conf[f"m{i}_right" if w == label else f"m{i}_wrong"].append(c)
        win_conf = statistics.fmean(com.members[i].max_overlap(probe)
                                    for i, (w, _) in enumerate(votes) if w == pw)
        conf["plain_right" if pw == label else "plain_wrong"].append(win_conf)
    return {"refusing": acc / N_TRIALS, "plain": plain / N_TRIALS,
            "refusal_rate": ref / N_TRIALS,
            "acc_on_answered": ans_ok / ans if ans else float("nan"),
            "best_single": max(single) / N_TRIALS,
            "full_member": single[0] / N_TRIALS,
            "diff": (acc - plain) / N_TRIALS, "conf": conf}


def run(n_sets=N_SETS):
    out = {}
    for gate in ("ood", "correctness"):
        coms = [build(k, gate) for k in range(n_sets)]
        taus = [[m.tau for m in c.members] for c in coms]
        rows = {}
        for sigma in SIGMAS:
            res = [evaluate(c, sigma, k) for k, c in enumerate(coms)]
            row = {key: mean_se([r[key] for r in res])
                   for key in ("refusing", "plain", "refusal_rate", "best_single",
                               "full_member", "diff")}
            aoa = [r["acc_on_answered"] for r in res if not math.isnan(r["acc_on_answered"])]
            row["acc_on_answered"] = mean_se(aoa) if aoa else (float("nan"), 0.0)
            pooled = {k: [x for r in res for x in r["conf"][k]] for k in res[0]["conf"]}
            row["conf"] = {k: (statistics.fmean(v) if v else float("nan"), len(v))
                           for k, v in pooled.items()}
            rows[sigma] = row
        js = [c.members[i].calib_J for c in coms for i in range(len(MEMBERS))]
        out[gate] = {"rows": rows,
                     "J_mean": [statistics.fmean(c.members[i].calib_J for c in coms)
                                for i in range(len(MEMBERS))],
                     "tau_mean": [statistics.fmean(t[i] for t in taus)
                                  for i in range(len(MEMBERS))]}
    return out


def fmt(ms, d=3):
    return f"{ms[0]:.{d}f} ± {ms[1]:.{d}f}"


def report(n_sets=N_SETS):
    r = run(n_sets)
    L = [f"SYNTHETIC. {n_sets} seed sets x {N_TRIALS} probes per sigma; mean ± standard error over seed sets.",
         "Gates calibrated at sigma=0.25 on held-out calibration seeds; sigma != 0.25 is a shift.", ""]
    for gate, title in (("ood", "Gate A: in-library vs random states (the received design)"),
                        ("correctness", "Gate B: right vs wrong votes")):
        g = r[gate]
        L.append(title)
        L.append("mean tau per member (" + ", ".join(n for n, _ in MEMBERS) + "): "
                 + ", ".join(f"{t:.3f}" for t in g["tau_mean"]))
        L.append("mean Youden J per member: " + ", ".join(f"{j:.3f}" for j in g["J_mean"]))
        L.append("| sigma | plain | refusing | refusing - plain | refusal rate | acc on answered | best single |")
        L.append("|---|---|---|---|---|---|---|")
        for s, row in g["rows"].items():
            L.append(f"| {s} | {fmt(row['plain'])} | {fmt(row['refusing'])} | {fmt(row['diff'])} | "
                     f"{fmt(row['refusal_rate'])} | {fmt(row['acc_on_answered'])} | {fmt(row['best_single'])} |")
        L.append("")
    L.append("Confidence (max overlap) of right vs wrong votes, pooled over seed sets: mean right / mean wrong (share wrong)")
    names = [n for n, _ in MEMBERS]
    L.append("| sigma | " + " | ".join(names) + " | plain committee winners |")
    L.append("|---|" + "---|" * (len(names) + 1))
    for s, row in r["ood"]["rows"].items():
        c = row["conf"]
        cells = []
        for key in [f"m{i}" for i in range(len(names))] + ["plain"]:
            rt, wr = c[key + "_right"], c[key + "_wrong"]
            share = wr[1] / (rt[1] + wr[1])
            w = f"{wr[0]:.3f}" if wr[1] else "-"
            cells.append(f"{rt[0]:.3f} / {w} ({share:.2f})")
        L.append(f"| {s} | " + " | ".join(cells) + " |")
    return "\n".join(L), r


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else N_SETS
    print(report(n)[0])
