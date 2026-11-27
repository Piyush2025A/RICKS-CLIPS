#!/usr/bin/env python3
"""ratios.py landmarks.csv -> per-person ratios (head width HW = unit) and per-archetype median/IQR. stdlib only."""
import csv, sys, statistics as S
rows = list(csv.DictReader(open(sys.argv[1])))
f = lambda r, k: float(r[k]) if r[k] else None
out = []
for r in rows:
    hw = f(r, 'head_r') - f(r, 'head_l'); d = dict(id=r['frame_id'], who=r['person'], arch=r['archetype'], view=r['view'], pose=r['pose'], hat=r['headgear'], hw=hw)
    ht, ch, tb, tl, tr, so = (f(r, k) for k in ('head_top', 'chin', 'torso_bot', 'torso_l', 'torso_r', 'sole'))
    d['head_hw'] = (ch - ht) / hw if ht else None
    d['torsoW_HW'] = (tr - tl) / hw if tl else None
    d['torsoL_HW'] = (tb - ch) / hw if tb else None
    d['leg_HW'] = (so - tb) / hw if so and tb else None
    d['leg_frac'] = (so - tb) / ((so - ht) if ht else (so - ch + 0.0)) if so and tb and ht else None
    d['height_HW'] = (so - ht) / hw if so and ht else None
    out.append(d)
keys = ['hw', 'head_hw', 'torsoW_HW', 'torsoL_HW', 'leg_HW', 'leg_frac', 'height_HW']
print('id,who,arch,view,pose,hat,' + ','.join(keys))
for d in out: print(','.join(str(d[k]) if k in ('id','who','arch','view','pose','hat') else ('' if d[k] is None else '%.3f' % d[k]) for k in ['id','who','arch','view','pose','hat'] + keys))
def q(v):
    v = sorted(v); n = len(v)
    if n < 2: return n, v[0] if v else None, None
    qs = S.quantiles(v, n=4, method='inclusive'); return n, S.median(v), (qs[0], qs[2])
print('\n# per group (front view, standing/dynamic only): n, median, IQR')
for g in ['all', 'slim', 'stout', 'tall', 'robe']:
    for k in keys[1:]:
        v = [d[k] for d in out if d[k] is not None and d['view'] == 'front' and d['pose'] != 'seated' and (g == 'all' or d['arch'] == g)]
        if v: print(g, k, q(v))
