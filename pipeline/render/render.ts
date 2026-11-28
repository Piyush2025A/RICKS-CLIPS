/**
 * A26 render harness (dev profile 360x640 @ 24 fps, Remotion renderer, gl swangle by default).
 *   node --experimental-strip-types --no-warnings pipeline/render/render.ts <mode> [options]
 * Modes:
 *   prepare [--entry remotion/index.ts --name bundle]   bundle into out/a26/<name> (hard-linked plate)
 *   still   --frame N --out file.png [--gl X]            one still, fresh process
 *   stills  --frames 24,24,5,5 --outdir d [--gl X]       several stills in ONE process (per-still seconds reported)
 *   seq     --concurrency C --outdir d [--format png|jpeg]   48-frame image sequence (renderFrames)
 *   mp4     --concurrency C --out f.mp4 [--audio]        H.264 MP4 (renderMedia, crf 18, yuv420p)
 *   diag    --gl X                                       WebGL context info (own diagnostic composition)
 * Common: --bundle out/a26/bundle  --id EngineTest  --browser <exe>  --gl swangle
 * Output: one JSON line on stdout. Never writes outside out/a26 (git-ignored). Verifies plate SHA-256 before/after.
 */
import { mkdirSync, readdirSync, statSync, rmSync } from 'node:fs';
import path from 'node:path';
import { renderStill, renderFrames, renderMedia, selectComposition, getCompositions } from '@remotion/renderer';
import { LIGHTHOUSE_PLATE_V01 } from '../../src/contracts/assets.ts';
import { A26_OUT, SCRIPT_VERSION, arg, flag, sha, checkPlate, median, pct, prepareBundle, startMemSampler, root } from './common.ts';

const mode = process.argv[2] ?? '';
const gl = arg('gl', 'swangle') as 'swangle' | 'angle' | 'swiftshader' | 'angle-egl';
const browserExecutable = (process.env.RC_BROWSER ?? (arg('browser', '') || null));
const bundleDir = path.resolve(root, arg('bundle', 'out/a26/bundle'));
const id = arg('id', 'EngineTest');
const concurrency = Number(arg('concurrency', '1'));
const imageFormat = arg('format', 'png') as 'png' | 'jpeg';
const withAudio = flag('audio');
const chromiumOptions = { gl };
const inputProps = { plate: LIGHTHOUSE_PLATE_V01, audio: withAudio ? 'test/tone.wav' : undefined, captions: false };
const logs: string[] = [];
const onBrowserLog = (l: { text: string }): void => { logs.push(l.text); };
const out = (o: Record<string, unknown>): void => console.log(JSON.stringify({ script: SCRIPT_VERSION, mode, gl, concurrency, ...o }));

const plateBefore = checkPlate();
if (mode === 'prepare') {
  const r = await prepareBundle(arg('entry', 'remotion/index.ts'), arg('name', 'bundle'), !flag('noplate'));
  out({ bundle_s: r.seconds, dir: r.dir, plateUnchanged: checkPlate() === plateBefore });
  process.exit(0);
}

const mem = startMemSampler();
const t0 = Date.now();
const comp = await selectComposition({ serveUrl: bundleDir, id, inputProps, browserExecutable, chromiumOptions, onBrowserLog });
const select_s = (Date.now() - t0) / 1000;
const finish = (extra: Record<string, unknown>): void => {
  out({ select_s, ...extra, mem: mem.stop(), plateUnchanged: checkPlate() === plateBefore, browserLogsSample: logs.slice(0, 5) });
};

if (mode === 'still') {
  const o = path.resolve(root, arg('out', 'out/a26/still.png')); mkdirSync(path.dirname(o), { recursive: true });
  const t1 = Date.now();
  await renderStill({ composition: comp, serveUrl: bundleDir, output: o, frame: Number(arg('frame', '24')), inputProps, browserExecutable, chromiumOptions, imageFormat, overwrite: true, scale: 1, onBrowserLog });
  finish({ frame: Number(arg('frame', '24')), still_s: (Date.now() - t1) / 1000, file: o, sha256: sha(o) });
} else if (mode === 'stills') {
  const d = path.resolve(root, arg('outdir', 'out/a26/stills')); mkdirSync(d, { recursive: true });
  const frames = arg('frames', '24,24').split(',').map(Number);
  const res: { frame: number; s: number; sha256: string }[] = [];
  for (const [i, f] of frames.entries()) {
    const o = path.join(d, `${String(i).padStart(2, '0')}_f${f}.png`); const t = Date.now();
    await renderStill({ composition: comp, serveUrl: bundleDir, output: o, frame: f, inputProps, browserExecutable, chromiumOptions, imageFormat, overwrite: true, scale: 1 });
    res.push({ frame: f, s: (Date.now() - t) / 1000, sha256: sha(o) });
  }
  const ts = res.map((r) => r.s);
  finish({ results: res, still_median_s: median(ts), still_p90_s: pct(ts, 90), still_min_s: Math.min(...ts), still_max_s: Math.max(...ts) });
} else if (mode === 'seq') {
  const d = path.resolve(root, arg('outdir', 'out/a26/seq')); rmSync(d, { recursive: true, force: true }); mkdirSync(d, { recursive: true });
  const t1 = Date.now();
  const r = await renderFrames({ composition: comp, serveUrl: bundleDir, inputProps, browserExecutable, chromiumOptions, imageFormat, concurrency, outputDir: d, scale: 1, onStart: () => undefined, onFrameUpdate: () => undefined, onBrowserLog });
  const s = (Date.now() - t1) / 1000;
  const files = readdirSync(d).filter((f) => f.endsWith(`.${imageFormat}`)).sort();
  finish({ frames: r.frameCount, files: files.length, seq_s: s, fps: r.frameCount / s, sec_per_frame: s / r.frameCount, hashes: Object.fromEntries(files.map((f) => [f, sha(path.join(d, f))])) });
} else if (mode === 'mp4') {
  const o = path.resolve(root, arg('out', 'out/a26/test.mp4')); mkdirSync(path.dirname(o), { recursive: true });
  const t1 = Date.now();
  await renderMedia({ composition: comp, serveUrl: bundleDir, outputLocation: o, codec: 'h264', crf: 18, pixelFormat: 'yuv420p', imageFormat: 'jpeg', jpegQuality: 100, concurrency, inputProps, browserExecutable, chromiumOptions, overwrite: true, scale: 1, onBrowserLog });
  const s = (Date.now() - t1) / 1000;
  finish({ mp4_s: s, fps: 48 / s, file: o, bytes: statSync(o).size, sha256: sha(o), audio: withAudio });
} else if (mode === 'diag') {
  const t1 = Date.now(); const o = path.resolve(root, 'out/a26/diag.png');
  await renderStill({ composition: comp, serveUrl: bundleDir, output: o, frame: 0, inputProps, browserExecutable, chromiumOptions, imageFormat: 'png', overwrite: true, onBrowserLog });
  finish({ still_s: (Date.now() - t1) / 1000, diagLogs: logs.filter((l) => l.includes('A26DIAG')) });
} else { console.error('unknown mode'); process.exit(2); }
void getCompositions;
