#!/usr/bin/env python3
"""A15 Phase 3B: dataset-wide transition counts and shot-length statistics from data/transitions_confirmed.csv.
Method (same as A28 audit): non-FP rows are boundaries at the candidate-range centre; boundaries within 15 frames are merged;
shots = gaps between 0, boundaries and video length (frames.csv). Shot length is an UPPER BOUND when continuous-camera scene
changes without an edit exist. Usage: python3 src/transitions/a15_stats.py [out_csv]"""
import csv, os, sys, collections
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = ROOT + '/knowledge/cinematography/a15-transition-specialist/data/transitions_confirmed.csv'
V = os.path.expanduser('~/ricks-clips-private/analysis-data/rc30/v0.2.0')
rows = list(csv.DictReader(open(CSV)))
nfr = {k: sum(1 for _ in open(f'{V}/{k}/frames.csv')) - 1 for k in sorted(os.listdir(V))}
def q(a):
    a = np.asarray(a, float); return f"n={len(a)} median={np.median(a):.2f} IQR={np.percentile(a,25):.2f}-{np.percentile(a,75):.2f} min={a.min():.2f} max={a.max():.2f}"
types = collections.Counter(r['type'] for r in rows)
print('rows', len(rows), dict(types), 'videos', len({r['video'] for r in rows}))
pervid = {}; allshots = []
for v in sorted(nfr):
    rs = [r for r in rows if r['video'] == v]
    cnt = collections.Counter(r['type'] for r in rs)
    b = sorted((int(r['cand_start']) + int(r['cand_end'])) / 2 for r in rs if r['type'] != 'FP')
    m = []
    for x in b:
        if m and x - m[-1] <= 15: continue
        m.append(x)
    edges = [0] + m + [nfr[v]]
    L = [(edges[i + 1] - edges[i]) / 30 for i in range(len(edges) - 1)]
    allshots += L
    pervid[v] = (cnt, len(L), float(np.median(L)), nfr[v] / 30)
out = [['video', 'XF', 'HC', 'ZT', 'FT', 'VB', 'FP', 'shots', 'median_shot_s', 'duration_s']]
for v, (c, n, md, d) in pervid.items():
    out.append([v, c['XF'], c['HC'], c['ZT'], c['FT'], c['VB'], c['FP'], n, round(md, 2), round(d, 2)])
    print(out[-1])
print('SHOTS', q(allshots))
print('shots/video', q([x[7] for x in out[1:]]))
print('per-video median shot', q([x[8] for x in out[1:]]))
real = {k: types[k] for k in ('XF', 'HC', 'ZT', 'FT', 'VB')}
print('REAL', sum(real.values()), real)
if len(sys.argv) > 1: csv.writer(open(sys.argv[1], 'w')).writerows(out)
