import { readFileSync } from 'node:fs';
import { durationFramesCovering, secondsToFrames } from './time.ts';

const fx = JSON.parse(readFileSync('pipeline/voice/tests/fixtures/frame_conversion_vectors.json', 'utf8')) as {
  cases: { t: string; fps: number; expected: number; note?: string }[];
  duration_cases?: { t: string; fps: number; expected: number; note?: string }[];
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
const dc: [number, number, number][] = [
  [7.058875, 24, 170], [2.0, 24, 48], [1.0, 30, 30], [7.0, 30, 210], [0, 24, 0], [0, 30, 0],
  [2.000001, 24, 49], [1.000001, 30, 31], [0.000001, 24, 1], [0.000001, 30, 1], [0.04, 24, 1],
  [0.041667, 24, 2], [0.041666, 24, 1], [600, 24, 14400], [600, 30, 18000], [600.000001, 30, 18001],
  [7.058875, 30, 212], [2.55, 30, 77],
];
for (const [t, f, e] of dc) check(`covering ${t}@${f}`, durationFramesCovering(t, f), e);
for (const c of fx.duration_cases ?? []) check(`fixture covering ${c.t}@${c.fps}`, durationFramesCovering(Number(c.t), c.fps), c.expected);
console.log(`covering: ${dc.length} explicit + ${fx.duration_cases?.length ?? 0} fixture cases`);
throws('covering negative', () => durationFramesCovering(-0.001, 24));
throws('covering NaN', () => durationFramesCovering(NaN, 24));
throws('covering Infinity', () => durationFramesCovering(Infinity, 24));
throws('covering fps 0', () => durationFramesCovering(1, 0));
throws('covering fps 23.5', () => durationFramesCovering(1, 23.5));
console.log(`total pass=${pass} fail=${fail}`);
if (fail) process.exit(1);
console.log('time contract OK');
