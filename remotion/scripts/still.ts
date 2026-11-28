/**
 * Render one still of EngineTest to out/ (git-ignored). Usage:
 *   npm run still -- [--frame 24] [--gl swangle|angle|swiftshader|angle-egl] [--out out/still.png] [--audio]
 * Serves the private plate via a git-ignored public dir (out/remotion-public) (plate hard-linked into the bundle, never copied); the original
 * is never copied or modified. Verifies SHA-256 of the plate before and after.
 */
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, rmSync, linkSync, copyFileSync, writeFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition } from '@remotion/renderer';
import { LIGHTHOUSE_PLATE_V01 } from '../../src/contracts/assets.ts';

const arg = (n: string, d: string): string => {
  const i = process.argv.indexOf(`--${n}`);
  return i >= 0 && process.argv[i + 1] ? (process.argv[i + 1] as string) : d;
};
const root = process.cwd();
const frame = Number(arg('frame', '24'));
const gl = arg('gl', 'swangle') as 'swangle' | 'angle' | 'swiftshader' | 'angle-egl';
const outFile = path.resolve(root, arg('out', 'out/engine_test_still.png'));
const withAudio = process.argv.includes('--audio');
const sha = (f: string): string => createHash('sha256').update(readFileSync(f)).digest('hex');

const plateSrc = path.resolve(root, LIGHTHOUSE_PLATE_V01.privatePath);
const before = sha(plateSrc);
if (before !== LIGHTHOUSE_PLATE_V01.sha256) throw new Error(`plate sha mismatch: ${before}`);

const publicDir = path.resolve(root, 'out/remotion-public');
rmSync(publicDir, { recursive: true, force: true });
mkdirSync(path.join(publicDir, 'flow'), { recursive: true });
// NOTE: Remotion's bundler copies publicDir and DROPS symlinks (observed), so the plate is linked into the
// git-ignored bundle dir after bundling (below). No private bytes are ever copied.
if (withAudio) {
  // tiny synthetic 8 kHz mono 16-bit WAV, 0.25 s of 440 Hz (generated, git-ignored)
  const n = 2000, buf = Buffer.alloc(44 + n * 2);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 2, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22); buf.writeUInt32LE(8000, 24); buf.writeUInt32LE(16000, 28);
  buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) buf.writeInt16LE(Math.round(8000 * Math.sin((2 * Math.PI * 440 * i) / 8000)), 44 + i * 2);
  mkdirSync(path.join(publicDir, 'test'), { recursive: true });
  writeFileSync(path.join(publicDir, 'test/tone.wav'), buf);
}

const browserExecutable = process.env.RC_BROWSER ?? null; // e.g. /opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
const t0 = Date.now();
const outDir = path.resolve(root, 'out/remotion-bundle');
rmSync(outDir, { recursive: true, force: true });
const serveUrl = await bundle({ entryPoint: path.resolve(root, 'remotion/index.ts'), publicDir, outDir });
mkdirSync(path.join(outDir, 'public/flow'), { recursive: true });
const linkDst = path.join(outDir, 'public', LIGHTHOUSE_PLATE_V01.publicPath);
// Remotion's serve-handler runs with symlinks disabled (observed: 404), so use a HARD LINK (same inode, zero byte copy,
// read-only source). Falls back to a byte copy inside git-ignored out/ only if linking fails (e.g. other filesystem).
try { linkSync(plateSrc, linkDst); } catch { copyFileSync(plateSrc, linkDst); console.warn('hardlink failed; copied into git-ignored out/'); }
const tBundle = Date.now();
const inputProps = { plate: LIGHTHOUSE_PLATE_V01, audio: withAudio ? 'test/tone.wav' : undefined, captions: false };
const chromiumOptions = { gl };
const comp = await selectComposition({ serveUrl, id: 'EngineTest', inputProps, browserExecutable, chromiumOptions });
mkdirSync(path.dirname(outFile), { recursive: true });
const t1 = Date.now();
await renderStill({ composition: comp, serveUrl, output: outFile, frame, inputProps, browserExecutable, chromiumOptions, imageFormat: 'png', overwrite: true });
const t2 = Date.now();

const after = sha(plateSrc);
console.log(JSON.stringify({
  frame, gl, browserExecutable, outFile, bytes: statSync(outFile).size, outSha256: sha(outFile),
  bundle_s: (tBundle - t0) / 1000, select_s: (t1 - tBundle) / 1000, still_s: (t2 - t1) / 1000,
  plateShaBefore: before, plateShaAfter: after, plateUnchanged: before === after && existsSync(outFile),
}, null, 1));
