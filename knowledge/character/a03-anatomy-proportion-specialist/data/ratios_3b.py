#!/usr/bin/env python3
"""ratios_3b.py v1.0 (A03, Phase 3B). Combines landmarks.csv (3A, 22 rows) + landmarks_3b.csv (3B) -> per-row ratios, per-character medians,
per-type stats (n = CHARACTERS), annotation error, limb width. stdlib only.
Usage: ratios_3b.py landmarks.csv landmarks_3b.csv limbw_3b.csv reannot_3b.csv OUTPREFIX"""
import csv, sys, statistics as S, collections
old = list(csv.DictReader(open(sys.argv[1]))); new = list(csv.DictReader(open(sys.argv[2])))
limb = {(r['frame_id'], r['character_id']): r for r in csv.DictReader(open(sys.argv[3]))}
re_ = list(csv.DictReader(open(sys.argv[4]))); pre = sys.argv[5]
TYPE = {'slim': 'adult', 'stout': 'large', 'tall': 'tall', 'robe': 'robe'}
CHAR_MERGE = {'RC30-07:yellow2': 'RC30-07:yellow', 'RC30-14:redcowboy': 'RC30-14:redcowboy'}
rows = []
for r in old:
    v = r['frame_id'][:7]; cid = CHAR_MERGE.get(v + ':' + r['person'], v + ':' + r['person'])
    if r['person'] == 'cowboy': cid = 'RC30-14:cowboy_unmatched'
    rows.append(dict(phase='3A', video=v, frame_id=r['frame_id'], cid=cid, type=TYPE[r['archetype']], view=r['view'], pose=r['pose'], hat=int(r['headgear']),
                     **{k: r[k] for k in ('head_l','head_r','head_top','chin','torso_bot','torso_l','torso_r','sole')}))
for r in new:
    rows.append(dict(phase='3B', video=r['video'], frame_id=r['frame_id'], cid=r['character_id'], type=r['type'], view=r['view'], pose=r['pose'], hat=int(r['headgear']),
                     **{k: r[k] for k in ('head_l','head_r','head_top','chin','torso_bot','torso_l','torso_r','sole')}))
f = lambda r, k: float(r[k]) if r[k] not in ('', None) else None
KEYS = ['head_hw', 'torsoW_HW', 'torsoL_HW', 'leg_HW', 'leg_frac', 'height_HW', 'height_HH']
for r in rows:
    hw = f(r, 'head_r') - f(r, 'head_l'); ht, ch, tb, tl, tr, so = (f(r, k) for k in ('head_top', 'chin', 'torso_bot', 'torso_l', 'torso_r', 'sole'))
    r['hw'] = hw
    r['head_hw'] = (ch - ht) / hw if ht and not r['hat'] else None
    r['torsoW_HW'] = (tr - tl) / hw if tl else None
    r['torsoL_HW'] = (tb - ch) / hw if tb else None
    r['leg_HW'] = (so - tb) / hw if so and tb else None
    r['leg_frac'] = (so - tb) / (so - ht) if so and tb and ht and not r['hat'] else None
    r['height_HW'] = (so - ht) / hw if so and ht and not r['hat'] else None
    r['height_HH'] = (so - ht) / (ch - ht) if so and ht and not r['hat'] else None
    lm = limb.get((r['frame_id'], r['cid']))
    r['limb_clean'] = None
    if lm and 4 <= int(lm['n_runs']) <= 8 and int(lm['max_run']) <= 2.5 * float(lm['limb_w_px']): r['limb_clean'] = float(lm['limb_w_over_hw'])
    r['limb_all'] = float(lm['limb_w_over_hw']) if lm else None
KEYS += ['limb_clean']
def usable(r):  # standing/walking/dynamic, front or 3/4, not seated; robe legs not meaningful
    return r['pose'] != 'seated' and r['view'] in ('front', 'threequarter') and r['cid'] != 'RC30-14:cowboy_unmatched'
with open(pre + '_rows.csv', 'w') as fo:
    fo.write('phase,frame_id,character_id,type,view,pose,hat,hw_px,' + ','.join(KEYS) + '\n')
    for r in rows:
        fo.write(','.join([r['phase'], r['frame_id'], r['cid'], r['type'], r['view'], r['pose'], str(r['hat']), '%.0f' % r['hw']] + [('' if r[k] is None else '%.3f' % r[k]) for k in KEYS]) + '\n')
def q(v):
    v = sorted(v); n = len(v)
    if n == 0: return 'n=0'
    if n < 4: return 'n=%d median %.3f range %.3f-%.3f' % (n, S.median(v), v[0], v[-1])
    qs = S.quantiles(v, n=4, method='inclusive')
    return 'n=%d median %.3f IQR %.3f-%.3f range %.3f-%.3f' % (n, S.median(v), qs[0], qs[2], v[0], v[-1])
# per character: median of per-row values (front view only for torso/leg/head; 3/4 excluded from these)
bych = collections.defaultdict(list)
for r in rows:
    if usable(r) and r['view'] == 'front': bych[r['cid']].append(r)
chars = {}
for cid, rs in bych.items():
    d = {'type': collections.Counter(x['type'] for x in rs).most_common(1)[0][0], 'video': rs[0]['video'], 'rows': len(rs)}
    for k in KEYS:
        v = [x[k] for x in rs if x[k] is not None]
        d[k] = S.median(v) if v else None
    d['hat_any'] = int(any(x['hat'] for x in rs)); chars[cid] = d
out = open(pre + '_stats.txt', 'w')
P = lambda *a: (print(*a), print(*a, file=out))
allc = set(r['cid'] for r in rows if r['cid'] != 'RC30-14:cowboy_unmatched')
P('# rows: %d (3A %d, 3B %d); distinct characters with any landmark row (excl. unmatched 14 cowboy): %d; videos with landmark rows: %d'
  % (len(rows), len(old), len(new), len(allc), len(set(r['video'] for r in rows))))
P('# characters in front-view standing stats: %d in %d videos' % (len(chars), len(set(c['video'] for c in chars.values()))))
tcount = collections.Counter(c['type'] for c in chars.values()); P('# characters by type:', dict(tcount))
P('\n## per measurement, n = characters (front-view, non-seated; head_hw/height exclude headgear characters)')
for grp in ['all', 'adult', 'large', 'tall', 'robe', 'child']:
    P('\n[%s]' % grp)
    for k in KEYS:
        if grp == 'robe' and k in ('leg_HW', 'leg_frac', 'height_HW', 'height_HH', 'limb_clean'): pass
        v = [c[k] for c in chars.values() if c[k] is not None and (grp == 'all' or c['type'] == grp)]
        if v: P('  %-10s %s' % (k, q(v)))
P('\n## adult+large+tall+child, excluding robe (robe legs hidden): leg and height')
for k in ['leg_HW', 'leg_frac', 'height_HW', 'height_HH']:
    v = [c[k] for c in chars.values() if c[k] is not None and c['type'] != 'robe']; P('  %-10s %s' % (k, q(v)))
# 3/4 view rows separately (rows, not characters)
P('\n## three-quarter rows (n rows): torsoW_HW, head_hw')
tq = [r for r in rows if r['view'] == 'threequarter']
for r in tq: P('  ', r['frame_id'], r['cid'], 'torsoW_HW', None if r['torsoW_HW'] is None else round(r['torsoW_HW'], 3), 'head_hw', None if r['head_hw'] is None else round(r['head_hw'], 3))
# within-character repeat spread (characters with >=2 rows)
P('\n## within-character spread across shots (max-min)/median, characters with >=2 usable rows')
for cid, rs in sorted(bych.items()):
    if len(rs) < 2: continue
    s = []
    for k in ('head_hw', 'torsoW_HW', 'torsoL_HW', 'leg_HW'):
        v = [x[k] for x in rs if x[k] is not None]
        if len(v) >= 2: s.append('%s %.0f%%' % (k, 100 * (max(v) - min(v)) / S.median(v)))
    P('  %-32s rows=%d %s' % (cid, len(rs), '; '.join(s)))
# per-character table
with open(pre + '_characters.csv', 'w') as fo:
    fo.write('character_id,video,type,front_rows,hat_any,' + ','.join(KEYS) + '\n')
    for cid, d in sorted(chars.items()):
        fo.write(','.join([cid, d['video'], d['type'], str(d['rows']), str(d['hat_any'])] + [('' if d[k] is None else '%.3f' % d[k]) for k in KEYS]) + '\n')
# annotation error
P('\n## re-annotation (6 frames of 60 rows = 10 % of frames? frames: 6 of 46 3B frames = 13 %)')
newidx = {(r['frame_id'], r['person']): r for r in new}
diffs = collections.defaultdict(list); ratio_d = collections.defaultdict(list)
for a in re_:
    b = newidx[(a['frame_id'], a['person'])]
    for k in ('head_l','head_r','head_top','chin','torso_bot','torso_l','torso_r','sole'):
        if a[k] and b[k]: diffs[k].append(abs(float(a[k]) - float(b[k])))
    hw1, hw2 = float(a['head_r']) - float(a['head_l']), float(b['head_r']) - float(b['head_l'])
    ratio_d['torsoW_HW'].append(abs((float(a['torso_r']) - float(a['torso_l'])) / hw1 - (float(b['torso_r']) - float(b['torso_l'])) / hw2))
    ratio_d['leg_HW'].append(abs((float(a['sole']) - float(a['torso_bot'])) / hw1 - (float(b['sole']) - float(b['torso_bot'])) / hw2))
    ratio_d['torsoL_HW'].append(abs((float(a['torso_bot']) - float(a['chin'])) / hw1 - (float(b['torso_bot']) - float(b['chin'])) / hw2))
    if a['head_top'] and b['head_top']:
        ratio_d['head_hw'].append(abs((float(a['chin']) - float(a['head_top'])) / hw1 - (float(b['chin']) - float(b['head_top'])) / hw2))
allp = []
for k, v in diffs.items(): P('  %-10s |diff| px native: median %.1f max %.0f n=%d' % (k, S.median(v), max(v), len(v))); allp += v
P('  all landmarks: median %.1f px, p90 %.1f px, max %.0f px (n=%d); native frame is 1080x1920 (annotation error unit px@native; at 720p multiply by 0.667)' % (S.median(allp), sorted(allp)[int(0.9 * len(allp))], max(allp), len(allp)))
for k, v in ratio_d.items(): P('  derived %-10s |diff| ratio units: median %.3f max %.3f n=%d' % (k, S.median(v), max(v), len(v)))
out.close()
