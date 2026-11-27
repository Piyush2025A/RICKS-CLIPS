#!/usr/bin/env python3
"""grid.py IN.png OUT.png [x0 y0 x1 y1] : crop (native px) + thin labelled native-coordinate grid, 100 px lines (50 px ticks at edges)."""
import sys, cv2, numpy as np
src, dst = sys.argv[1:3]
im = cv2.imread(src); H, W = im.shape[:2]
crop = len(sys.argv) >= 7
x0, y0, x1, y1 = map(int, sys.argv[3:7]) if crop else (0, 0, W, H)
step = 100 if not crop else 50
c = im[y0:y1, x0:x1].copy()
s = (1500 / max(c.shape[:2])) if crop else min(1.0, 1500 / max(c.shape[:2]))
c = cv2.resize(c, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
o = c.copy()
for x in range((x0 // step + 1) * step, x1, step):
    X = int((x - x0) * s); cv2.line(o, (X, 0), (X, c.shape[0]), (255, 0, 255), 1)
    cv2.putText(o, str(x), (X + 2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 0), 1)
    cv2.putText(o, str(x), (X + 2, c.shape[0] - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 0), 1)
for y in range((y0 // step + 1) * step, y1, step):
    Y = int((y - y0) * s); cv2.line(o, (0, Y), (c.shape[1], Y), (255, 0, 255), 1)
    cv2.putText(o, str(y), (2, Y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 0), 1)
    cv2.putText(o, str(y), (c.shape[1] - 40, Y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 0), 1)
cv2.imwrite(dst, cv2.addWeighted(o, 0.55, c, 0.45, 0))
