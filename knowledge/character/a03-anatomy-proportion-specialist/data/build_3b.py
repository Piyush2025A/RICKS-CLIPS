#!/usr/bin/env python3
"""build_3b.py v1.0 (A03, Phase 3B). disp.csv (landmarks read on 844x1500 grid overlays, display px) -> landmarks_3b.csv (native 1080x1920 px).
Usage: build_3b.py DISP.csv OUT.csv     scale = 1.28 (1080/844 = 1920/1500). Adds phase, video, character_id."""
import csv, sys
S = 1.28
rows = list(csv.DictReader(open(sys.argv[1])))
num = ['head_l','head_r','head_top','chin','torso_bot','torso_l','torso_r','sole']
out = []
for r in rows:
    d = {'phase': '3B', 'video': r['frame_id'][:7], 'frame_id': r['frame_id'],
         'character_id': r['frame_id'][:7] + ':' + r['person'], 'person': r['person'], 'type': r['type'], 'view': r['view'],
         'pose': r['pose'], 'headgear': r['headgear']}
    for k in num:
        d[k] = str(int(round(float(r[k]) * S))) if r[k] else ''
    d['notes'] = r['notes']
    out.append(d)
cols = ['phase','video','frame_id','character_id','person','type','view','pose','headgear'] + num + ['notes']
w = csv.DictWriter(open(sys.argv[2], 'w', newline=''), fieldnames=cols); w.writeheader(); w.writerows(out)
print(len(out), 'rows ->', sys.argv[2])
