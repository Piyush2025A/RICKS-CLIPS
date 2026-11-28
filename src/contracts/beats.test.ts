import { readFileSync } from 'node:fs';
import { parseBeats, beatFrames } from './beats.ts';
import { secondsToFrames } from './time.ts';

const beats = parseBeats(JSON.parse(readFileSync('productions/TEST6S/voice/beats.json', 'utf8')));
let bad = 0;
let n = 0;
for (const fps of [24, 30]) {
  for (const [name, list] of [['sentence', beats.sentences], ['clause', beats.clauses]] as const) {
    for (const b of list) {
      const f = beatFrames(b, fps);
      const ref = fps === 24 ? b.frames_24 : b.frames_30;
      if (!ref) { bad++; console.error(`${name} ${b.index} fps=${fps}: beats.json has no frames_${fps}`); continue; }
      n++;
      const ok = ref[0] === f[0] && ref[1] === f[1]; // exact, no tolerance (A20 half-up rule, D-5A)
      if (!ok) bad++;
      console.log(`${name} ${b.index} fps=${fps} t=[${b.t_on},${b.t_off}] -> [${f}] A20=[${ref}] ${ok ? 'OK' : 'MISMATCH'}`);
    }
  }
}
if (bad) { console.error(`${bad} mismatches vs A20 frames`); process.exit(1); }
console.log(`beats parity OK: ${n}/${n} spans exact`);
