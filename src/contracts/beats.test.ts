import { readFileSync } from 'node:fs';
import { parseBeats, beatFrames } from './beats.ts';
import { secondsToFrames } from './time.ts';

const beats = parseBeats(JSON.parse(readFileSync('productions/TEST6S/voice/beats.json', 'utf8')));
let bad = 0;
for (const fps of [24, 30]) {
  for (const [name, list] of [['sentence', beats.sentences], ['clause', beats.clauses]] as const) {
    for (const b of list) {
      const f = beatFrames(b, fps);
      const ref = fps === 24 ? b.frames_24 : b.frames_30;
      const same = !ref || (ref[0] === f[0] && ref[1] === f[1]);
      // A20 beats.py uses Python round() (half-to-even); CONTRACT.md says floor(t*fps+0.5). They differ only on exact .5 ties.
      const tie = [b.t_on, b.t_off].some((t) => Math.abs((t * fps) % 1 - 0.5) < 1e-9);
      const ok = same || (tie && ref !== undefined && Math.abs(ref[0] - f[0]) <= 1 && Math.abs(ref[1] - f[1]) <= 1);
      if (!ok) bad++;
      console.log(`${name} ${b.index} fps=${fps} t=[${b.t_on},${b.t_off}] -> frames [${f}] A20=${ref ? `[${ref}]` : 'n/a'} ${same ? 'OK' : ok ? 'TIE-DIVERGENCE (half-even vs half-up)' : 'MISMATCH'}`);
    }
  }
}
console.log('0.2333s @24 =', secondsToFrames(0.2333, 24), '@30 =', secondsToFrames(0.2333, 30));
if (bad) { console.error(`${bad} mismatches vs A20 frames`); process.exit(1); }
console.log('beats contract OK');
