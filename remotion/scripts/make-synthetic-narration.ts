/**
 * Generate a SYNTHETIC narration stand-in (NOT real voice): 7.06 s, 48 kHz mono 24-bit WAV, 220 Hz tone gated by beats.json voiced
 * span, plus its descriptor. Output (git-ignored): assets/private/audio/TEST6S/synthetic/. Usage: npm run synth-narration
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import type { NarrationDescriptor } from '../../src/contracts/narration.ts';
import { sha256File } from '../../src/contracts/narration-node.ts';

const dir = 'assets/private/audio/TEST6S/synthetic';
const SR = 48000, DUR = 7.06, n = Math.round(SR * DUR);
const buf = Buffer.alloc(44 + n * 3);
buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 3, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16);
buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22); buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 3, 28);
buf.writeUInt16LE(3, 32); buf.writeUInt16LE(24, 34); buf.write('data', 36); buf.writeUInt32LE(n * 3, 40);
for (let i = 0; i < n; i++) {
  const t = i / SR;
  const gate = t > 0.08 && t < 6.79 ? 1 : 0;
  const v = Math.round(0.2 * gate * Math.sin(2 * Math.PI * 220 * t) * 8388607);
  buf.writeIntLE(v, 44 + i * 3, 3);
}
mkdirSync(dir, { recursive: true });
const wav = path.join(dir, 'SYNTHETIC_narration_standin.wav');
writeFileSync(wav, buf);
const d: NarrationDescriptor = {
  id: 'TEST6S_vo_SYNTHETIC', role: 'vo', production: 'TEST6S', synthetic: true,
  privatePath: wav, publicPath: 'audio/TEST6S/SYNTHETIC_narration_standin.wav',
  sha256: sha256File(wav), duration_s: n / SR, sample_rate: SR, channels: 1, bytes: buf.length,
};
writeFileSync(path.join(dir, 'narration.descriptor.json'), JSON.stringify(d, null, 2) + '\n');
console.log(JSON.stringify(d, null, 1));
