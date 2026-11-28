#!/usr/bin/env python3
"""limbw.py v1.0 (A03, 3B): leg-stroke width from native frames. For each landmark row with torso_bot and sole, scan rows at 25/40/55 % of
the leg span inside x in [torso_l-0.35HW, torso_r+0.35HW]; ink = max(R,G,B) < 70; keep dark runs of width 3..0.25*HW; report median run width,
number of runs, and the spread. Usage: limbw.py landmarks_3b.csv FRAMES_DIR OUT.csv   (run with .venv-analysis python -I)"""
import csv, sys, os, numpy as np, cv2
rows = list(csv.DictReader(open(sys.argv[1]))); fd = sys.argv[2]
out = []
for r in rows:
    if not (r['torso_bot'] and r['sole']) or r['type'] == 'robe': continue
    p = os.path.join(fd, r['frame_id'] + '.png')
    im = cv2.imread(p)
    if im is None: continue
    ink = im.max(axis=2) < 70
    hw = int(r['head_r']) - int(r['head_l']); tb, so = int(r['torso_bot']), int(r['sole'])
    x0 = max(0, int(int(r['torso_l']) - 0.35 * hw)); x1 = min(im.shape[1], int(int(r['torso_r']) + 0.35 * hw))
    ws = []
    for f in (0.25, 0.40, 0.55):
        y = int(tb + f * (so - tb)); line = ink[y, x0:x1].astype(np.int8)
        d = np.diff(np.concatenate([[0], line, [0]])); st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
        ws += [int(e - s) for s, e in zip(st, en) if 3 <= e - s <= 0.25 * hw]
    if len(ws) >= 2:
        out.append((r['frame_id'], r['character_id'], hw, len(ws), float(np.median(ws)), float(np.median(ws)) / hw, int(min(ws)), int(max(ws))))
with open(sys.argv[3], 'w') as f:
    f.write('frame_id,character_id,hw_px,n_runs,limb_w_px,limb_w_over_hw,min_run,max_run\n')
    for o in out: f.write('%s,%s,%d,%d,%.1f,%.4f,%d,%d\n' % o)
print(len(out), 'figures with limb width')
