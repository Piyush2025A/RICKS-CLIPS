"""Agreement for the Phase 3B blind two-axis hook coding (director). Run: python3 research/data/phase3b_hook_agreement.py"""
import csv, collections, os
D = os.path.dirname(os.path.abspath(__file__))
A = {r["key"]: r for r in csv.DictReader(open(f"{D}/phase3b_hook_codes_coderA.csv"))}
B = {r["key"]: r for r in csv.DictReader(open(f"{D}/phase3b_hook_codes_coderB.csv"))}
K = sorted(A)
def kappa(x, y):
    n = len(x); po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = collections.Counter(x), collections.Counter(y)
    pe = sum(cx[c] * cy[c] for c in set(x) | set(y)) / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")
def any_match(a1, a2, b1, b2):
    return bool({a1, a2} - {""} & {b1, b2} - {""})
print("n videos", len(K))
for lab, xa, xb in (("D primary (A 0-1.6 s vs B 0-1.6 s)", [A[k]["D_primary"] for k in K], [B[k]["D16_primary"] for k in K]),
                    ("D primary (A 0-1.6 s vs B 0-3 s)", [A[k]["D_primary"] for k in K], [B[k]["D13_primary"] for k in K]),
                    ("V primary", [A[k]["V_primary"] for k in K], [B[k]["V_primary"] for k in K]),
                    ("V complete_by", [A[k]["V_complete_by"] for k in K], [B[k]["V_complete_by"] for k in K])):
    po, kp = kappa(xa, xb); print(f"{lab}: Po={po:.2f} kappa={kp:.2f}")
print("D any-label overlap", sum(any_match(A[k]["D_primary"], A[k]["D_secondary"], B[k]["D13_primary"], B[k]["D13_secondary"]) for k in K))
print("V any-label overlap", sum(any_match(A[k]["V_primary"], A[k]["V_secondary"], B[k]["V_primary"], B[k]["V_secondary"]) for k in K))
for ax in ("D_primary", "V_primary"):
    print("A", ax, dict(collections.Counter(A[k][ax] for k in K)))
print("B D13", dict(collections.Counter(B[k]["D13_primary"] for k in K)), "B V", dict(collections.Counter(B[k]["V_primary"] for k in K)))
# A19 F-a19-003 single-axis labels mapped per codebook
A19 = {}
for lab, keys in (("V1", "01 08 16 22 23 27 29"), ("D12", "05 06 11 13 15 20 21"), ("V2", "04 09 19 24 26"),
                  ("V3", "03 10 12 17 28"), ("D3", "02 07 18"), ("V5", "14 30"), ("V4", "25")):
    for k in keys.split(): A19[f"RC30-{k}"] = lab
def hit(lab, r, dcol, d2col):
    if lab.startswith("V"): return lab in (r["V_primary"], r.get("V_secondary", "")), lab == r["V_primary"]
    want = {"D1", "D2"} if lab == "D12" else {lab}
    return bool(want & {r[dcol], r[d2col]}), r[dcol] in want
for name, R, dcol, d2 in (("coder A", A, "D_primary", "D_secondary"), ("coder B", B, "D13_primary", "D13_secondary")):
    prim = sum(hit(A19[k], R[k], dcol, d2)[1] for k in K); anyh = sum(hit(A19[k], R[k], dcol, d2)[0] for k in K)
    print(f"A19 vs {name}: primary-axis match {prim}/30, primary-or-secondary {anyh}/30")
# consensus where coders agree
cons = [k for k in K if A[k]["V_primary"] == B[k]["V_primary"]]
print("V consensus", len(cons), dict(collections.Counter(A[k]["V_primary"] for k in cons)))
consd = [k for k in K if A[k]["D_primary"] == B[k]["D16_primary"]]
print("D consensus (0-1.6 s)", len(consd), dict(collections.Counter(A[k]["D_primary"] for k in consd)))
# A18 5-video recode (F-a18-001): primary labels: 04 odd act, 09 odd act, 16 claim, 23 odd act, 30 odd act
A18 = {"RC30-04": "D1", "RC30-09": "D1", "RC30-16": "V1", "RC30-23": "D1", "RC30-30": "D1"}
for k, l in A18.items():
    print("A18", k, l, "| A:", A[k]["D_primary"], A[k]["V_primary"], "| B:", B[k]["D13_primary"], B[k]["V_primary"], "| A19:", A19[k])
