import { readFileSync } from 'node:fs';
import { secondsToFrames } from './time.ts';

const fx = JSON.parse(readFileSync('pipeline/voice/tests/fixtures/frame_conversion_vectors.json', 'utf8')) as {
  cases: { t: string; fps: number; expected: number; note?: string }[];
};
let pass = 0, fail = 0;
const check = (label: string, got: number, want: number): void => {
  if (got === want) pass++; else { fail++; console.error(`FAIL ${label}: got ${got} want ${want}`); }
};
for (const c of fx.cases) check(`${c.t}@${c.fps} (${c.note ?? ''})`, secondsToFrames(Number(c.t), c.fps), c.expected);
console.log(`fixture: ${pass}/${fx.cases.length} cases`);
if (fx.cases.length !== 59) { fail++; console.error(`expected 59 fixture cases, found ${fx.cases.length}`); }
const explicit = pass;
check('2.55@30', secondsToFrames(2.55, 30), 77);
check('0.0625@24', secondsToFrames(0.0625, 24), 2);
check('0.1875@24', secondsToFrames(0.1875, 24), 5);
console.log(`explicit: ${pass - explicit}/3`);
const throws = (label: string, fn: () => unknown): void => {
  try { fn(); fail++; console.error(`FAIL no throw: ${label}`); } catch { pass++; }
};
throws('negative', () => secondsToFrames(-0.001, 24));
throws('NaN', () => secondsToFrames(NaN, 24));
throws('Infinity', () => secondsToFrames(Infinity, 24));
throws('fps 0', () => secondsToFrames(1, 0));
throws('fps -24', () => secondsToFrames(1, -24));
throws('fps 23.5', () => secondsToFrames(1, 23.5));
throws('fps NaN', () => secondsToFrames(1, NaN));
console.log(`total pass=${pass} fail=${fail}`);
if (fail) process.exit(1);
console.log('time contract OK');
