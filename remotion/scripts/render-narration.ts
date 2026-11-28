/**
 * Render NarrationTest to MP4 in out/ (git-ignored). Usage:
 *   npm run render-narration -- --descriptor <path.json> [--beats productions/TEST6S/voice/beats.json] [--out out/narration_test.mp4] [--frames a-b]
 * Verifies narration SHA-256 + plate SHA-256 BEFORE bundling (throws on mismatch), hard-links both into the ignored bundle public dir.
 */
import { createHash } from 'node:crypto';
import { readFileSync, rmSync, mkdirSync, linkSync, copyFileSync } from 'node:fs';
import path from 'node:path';
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import { LIGHTHOUSE_PLATE_V01 } from '../../src/contracts/assets.ts';
import { validateNarrationDescriptor } from '../../src/contracts/narration.ts';
import { verifyNarrationFile } from '../../src/contracts/narration-node.ts';
import { parseBeats } from '../../src/contracts/beats.ts';

const arg = (n: string, d?: string): string => {
  const i = process.argv.indexOf(`--${n}`);
  const v = i >= 0 ? process.argv[i + 1] : d;
  if (!v) throw new Error(`missing --${n}`);
  return v;
};
const root = process.cwd();
const sha = (f: string): string => createHash('sha256').update(readFileSync(f)).digest('hex');
const desc = validateNarrationDescriptor(JSON.parse(readFileSync(arg('descriptor'), 'utf8')));
const audioSrc = verifyNarrationFile(desc, root); // throws loudly on missing / mismatch
const plateSrc = path.resolve(root, LIGHTHOUSE_PLATE_V01.privatePath);
if (sha(plateSrc) !== LIGHTHOUSE_PLATE_V01.sha256) throw new Error('plate sha mismatch');
const beats = parseBeats(JSON.parse(readFileSync(arg('beats', 'productions/TEST6S/voice/beats.json'), 'utf8')));
const beatFrames24 = beats.clauses.map((c) => {
  if (!c.frames_24) throw new Error(`clause ${c.index} lacks frames_24`);
  return [c.frames_24[0], c.frames_24[1]] as const;
});
const outFile = path.resolve(root, arg('out', 'out/narration_test.mp4'));
const publicDir = path.resolve(root, 'out/remotion-public-narration');
const outDir = path.resolve(root, 'out/remotion-bundle-narration');
rmSync(publicDir, { recursive: true, force: true }); mkdirSync(publicDir, { recursive: true });
rmSync(outDir, { recursive: true, force: true });
const serveUrl = await bundle({ entryPoint: path.resolve(root, 'remotion/index.ts'), publicDir, outDir });
const link = (src: string, rel: string): void => {
  const dst = path.join(outDir, 'public', rel);
  mkdirSync(path.dirname(dst), { recursive: true });
  try { linkSync(src, dst); } catch { copyFileSync(src, dst); console.warn(`hardlink failed for ${rel}; copied into git-ignored out/`); }
};
link(plateSrc, LIGHTHOUSE_PLATE_V01.publicPath);
link(audioSrc, desc.publicPath);
const inputProps = { plate: LIGHTHOUSE_PLATE_V01, narration: desc, beatFrames24 };
const browserExecutable = process.env.RC_BROWSER ?? null;
const chromiumOptions = { gl: 'swangle' as const };
const comp = await selectComposition({ serveUrl, id: 'NarrationTest', inputProps, browserExecutable, chromiumOptions });
const fr = process.argv.includes('--frames') ? arg('frames').split('-').map(Number) : null;
const t0 = Date.now();
await renderMedia({
  composition: comp, serveUrl, codec: 'h264', outputLocation: outFile, inputProps, browserExecutable, chromiumOptions,
  overwrite: true, audioCodec: 'aac', colorSpace: 'bt709', ...(fr ? { frameRange: [fr[0]!, fr[1]!] as [number, number] } : {}),
});
console.log(JSON.stringify({
  outFile, durationInFrames: comp.durationInFrames, fps: comp.fps, render_s: (Date.now() - t0) / 1000,
  plateUnchanged: sha(plateSrc) === LIGHTHOUSE_PLATE_V01.sha256, narrationUnchanged: sha(audioSrc) === desc.sha256,
}, null, 1));
