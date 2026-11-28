import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { validateNarrationDescriptor, narrationFrames } from './narration.ts';
import { verifyNarrationFile, sha256File } from './narration-node.ts';

const root = process.cwd();
const dir = 'out/narration-test';
rmSync(dir, { recursive: true, force: true });
mkdirSync(dir, { recursive: true });
writeFileSync(`${dir}/x.wav`, Buffer.from('synthetic-bytes'));
const base = {
  id: 't', role: 'vo', production: 'T', privatePath: `${dir}/x.wav`, publicPath: 'audio/T/x.wav',
  sha256: sha256File(`${dir}/x.wav`), duration_s: 7.06, sample_rate: 48000, channels: 1, synthetic: true,
};
let fail = 0;
const expect = (label: string, fn: () => unknown, shouldThrow: boolean): void => {
  let threw = false;
  try { fn(); } catch { threw = true; }
  if (threw !== shouldThrow) { fail++; console.error(`FAIL ${label}`); } else console.log(`ok ${label}`);
};
const d = validateNarrationDescriptor(base);
expect('valid file verifies', () => verifyNarrationFile(d, root), false);
expect('frames 7.06@24 = 169', () => { if (narrationFrames(d, 24) !== 169) throw new Error('x'); }, false);
expect('sha mismatch throws', () => verifyNarrationFile({ ...d, sha256: 'a'.repeat(64) }, root), true);
expect('missing file throws', () => verifyNarrationFile({ ...d, privatePath: `${dir}/nope.wav` }, root), true);
expect('bad role rejected', () => validateNarrationDescriptor({ ...base, role: 'sfx' }), true);
expect('bad sha rejected', () => validateNarrationDescriptor({ ...base, sha256: 'xyz' }), true);
expect('absolute public path rejected', () => validateNarrationDescriptor({ ...base, publicPath: '/etc/x' }), true);
rmSync(dir, { recursive: true, force: true });
if (fail) process.exit(1);
console.log('narration contract OK');
