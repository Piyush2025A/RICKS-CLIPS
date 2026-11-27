# A09 FAILED
1. `pair.py` first runs: swapped/wrong-region pairs (RC30-09-f000629 floor gave 1.05; RC30-12-f000059 lit/shade
   inverted). Fixed by re-picking against the viewed frame — always view and confirm patch positions.
2. uint8 overflow in an inline Lab print → nonsense L*a*b* for face stats; RGB from that run valid (reported RGB only);
   `pair.py` uses a float Lab path.
3. `edge.py` on low-range profiles (Y range < 0.1) gave a bogus 140 px; profiles with range < 0.2 excluded ("no edge" guard).
4. First mood rule (`a* >= 14`) lumped violet-night, red-orange and pink; split by b*.
5. Class switches/min (14.6) measures cut rate, not lighting beats — not usable as a beat metric.
6. A27 `color.csv` existed for 8 videos only at start → own 1 fps pass for all 30; cross-check on those 8 open.
7. `get_frames.py` slow under load: RC30-02-f000659, RC30-04-f000179, RC30-12-f000749, RC30-17-f000959 not viewed.
8. Write tool refused the three deliverables; texts returned in the hand-off.
