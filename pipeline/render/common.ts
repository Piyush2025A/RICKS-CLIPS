/**
 * A26 shared helpers: bundle preparation (plate hard-linked, never copied), SHA-256, /proc memory sampler.
 * Script version: a26-render v1 (Phase 5A). Run with: node --experimental-strip-types --no-warnings <script>
 */
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, linkSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { bundle } from '@remotion/bundler';
import { LIGHTHOUSE_PLATE_V01 } from '../../src/contracts/assets.ts';

export const SCRIPT_VERSION = 'a26-render-v1';
export const root = process.cwd();
export const A26_OUT = path.resolve(root, 'out/a26');
export const sha = (f: string): string => createHash('sha256').update(readFileSync(f)).digest('hex');
export const plateSrc = path.resolve(root, LIGHTHOUSE_PLATE_V01.privatePath);
export const arg = (n: string, d: string): string => {
  const i = process.argv.indexOf(`--${n}`);
  return i >= 0 && process.argv[i + 1] ? (process.argv[i + 1] as string) : d;
};
export const flag = (n: string): boolean => process.argv.includes(`--${n}`);
export const checkPlate = (): string => {
  const s = sha(plateSrc);
  if (s !== LIGHTHOUSE_PLATE_V01.sha256) throw new Error(`plate sha mismatch: ${s}`);
  return s;
};
export const median = (a: number[]): number => {
  const s = [...a].sort((x, y) => x - y); const m = s.length >> 1;
  return s.length % 2 ? (s[m] as number) : ((s[m - 1] as number) + (s[m] as number)) / 2;
};
export const pct = (a: number[], p: number): number => {
  const s = [...a].sort((x, y) => x - y);
  return s[Math.min(s.length - 1, Math.ceil((p / 100) * s.length) - 1)] as number;
};

/** 0.25 s 440 Hz synthetic WAV (8 kHz mono 16-bit), same as A25 still.ts --audio. */
export const writeToneWav = (file: string): void => {
  const n = 2000, buf = Buffer.alloc(44 + n * 2);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 2, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22); buf.writeUInt32LE(8000, 24); buf.writeUInt32LE(16000, 28);
  buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) buf.writeInt16LE(Math.round(8000 * Math.sin((2 * Math.PI * 440 * i) / 8000)), 44 + i * 2);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, buf);
};

/** Bundle an entry into out/a26/<name> (git-ignored); hard-link plate (A25 method). Returns dir + seconds. */
export const prepareBundle = async (entry: string, name: string, withPlate = true): Promise<{ dir: string; seconds: number }> => {
  const t0 = Date.now();
  const publicDir = path.join(A26_OUT, `public-${name}`);
  rmSync(publicDir, { recursive: true, force: true });
  writeToneWav(path.join(publicDir, 'test/tone.wav'));
  const outDir = path.join(A26_OUT, name);
  rmSync(outDir, { recursive: true, force: true });
  await bundle({ entryPoint: path.resolve(root, entry), publicDir, outDir });
  if (withPlate) {
    mkdirSync(path.join(outDir, 'public/flow'), { recursive: true });
    const dst = path.join(outDir, 'public', LIGHTHOUSE_PLATE_V01.publicPath);
    try { linkSync(plateSrc, dst); } catch { throw new Error('hardlink failed; refusing to copy private plate'); }
  }
  return { dir: outDir, seconds: (Date.now() - t0) / 1000 };
};

/** Memory sampler: peak RSS of this node process and of all descendant processes (chromium), via /proc. */
export const startMemSampler = (intervalMs = 150) => {
  const status = (pid: number): Record<string, number> | null => {
    try {
      const o: Record<string, number> = {};
      for (const l of readFileSync(`/proc/${pid}/status`, 'utf8').split('\n')) {
        const m = /^(VmRSS|VmHWM|PPid):\s+(\d+)/.exec(l); if (m) o[m[1] as string] = Number(m[2]);
      }
      return o;
    } catch { return null; }
  };
  const peak = { nodeHWM_MB: 0, childSumRSS_MB_peak: 0, childMaxHWM_MB: 0, childCountMax: 0, totalSumRSS_MB_peak: 0 };
  const seen = new Map<number, number>(); // child pid -> max HWM kB
  const tick = (): void => {
    const me = status(process.pid); if (me) peak.nodeHWM_MB = Math.max(peak.nodeHWM_MB, (me.VmHWM ?? 0) / 1024);
    const parent = new Map<number, number>(); const rss = new Map<number, number>();
    for (const d of readdirSync('/proc')) {
      if (!/^\d+$/.test(d)) continue; const s = status(Number(d)); if (!s) continue;
      parent.set(Number(d), s.PPid ?? 0); rss.set(Number(d), s.VmRSS ?? 0);
      if (s.VmHWM !== undefined) seen.set(Number(d), Math.max(seen.get(Number(d)) ?? 0, s.VmHWM));
    }
    const desc = (p: number): boolean => { for (let q = parent.get(p); q; q = parent.get(q)) if (q === process.pid) return true; return false; };
    let sum = 0, n = 0; const kids: number[] = [];
    for (const [p, r] of rss) if (desc(p)) { sum += r; n++; kids.push(p); }
    peak.childSumRSS_MB_peak = Math.max(peak.childSumRSS_MB_peak, sum / 1024);
    peak.childCountMax = Math.max(peak.childCountMax, n);
    peak.totalSumRSS_MB_peak = Math.max(peak.totalSumRSS_MB_peak, (sum + (me?.VmRSS ?? 0)) / 1024);
    for (const k of kids) peak.childMaxHWM_MB = Math.max(peak.childMaxHWM_MB, (seen.get(k) ?? 0) / 1024);
  };
  const h = setInterval(tick, intervalMs); tick();
  return { stop: () => { clearInterval(h); tick(); return Object.fromEntries(Object.entries(peak).map(([k, v]) => [k, Math.round(v)])); } };
};
export { existsSync };
