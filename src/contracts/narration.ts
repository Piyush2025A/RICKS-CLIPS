import { secondsToFrames } from './time.ts';

/**
 * Private narration descriptor (role "vo"). The audio bytes live OUTSIDE tracked paths, by convention under
 * assets/private/audio/<production>/ (git-ignored; check: git check-ignore -v <path>). Never modified or copied
 * into tracked paths; served to Remotion by hard link into the ignored bundle public dir.
 */
export interface NarrationDescriptor {
  readonly id: string;
  readonly role: 'vo';
  readonly production: string;
  /** Repo-relative private path of the byte-exact file. */
  readonly privatePath: string;
  /** Path relative to Remotion's public dir (used with staticFile). */
  readonly publicPath: string;
  readonly sha256: string;
  readonly duration_s: number;
  readonly sample_rate: number;
  readonly channels: number;
  readonly bytes?: number;
  readonly loudness_lufs?: number;
  readonly true_peak_dbtp?: number;
  /** True for generated stand-ins; never use a synthetic descriptor for a real render. */
  readonly synthetic?: boolean;
}

const isHex64 = (s: unknown): s is string => typeof s === 'string' && /^[0-9a-f]{64}$/.test(s);

export const validateNarrationDescriptor = (v: unknown): NarrationDescriptor => {
  const o = v as Record<string, unknown>;
  const fail = (m: string): never => { throw new Error(`NarrationDescriptor invalid: ${m}`); };
  if (typeof o !== 'object' || o === null) return fail('not an object');
  if (o.role !== 'vo') fail('role must be "vo"');
  for (const k of ['id', 'production', 'privatePath', 'publicPath'] as const) {
    if (typeof o[k] !== 'string' || !o[k]) fail(k);
  }
  if ((o.publicPath as string).startsWith('/') || (o.publicPath as string).includes('..')) fail('publicPath must be relative');
  if ((o.privatePath as string).startsWith('/') || (o.privatePath as string).includes('..')) fail('privatePath must be repo-relative');
  if (!isHex64(o.sha256)) fail('sha256');
  if (typeof o.duration_s !== 'number' || !Number.isFinite(o.duration_s) || o.duration_s <= 0) fail('duration_s');
  if (!Number.isInteger(o.sample_rate) || (o.sample_rate as number) <= 0) fail('sample_rate');
  if (!Number.isInteger(o.channels) || (o.channels as number) <= 0) fail('channels');
  for (const k of ['loudness_lufs', 'true_peak_dbtp', 'bytes'] as const) {
    if (o[k] !== undefined && (typeof o[k] !== 'number' || !Number.isFinite(o[k] as number))) fail(k);
  }
  return o as unknown as NarrationDescriptor;
};

export const narrationFrames = (d: NarrationDescriptor, fps: number): number => secondsToFrames(d.duration_s, fps);
