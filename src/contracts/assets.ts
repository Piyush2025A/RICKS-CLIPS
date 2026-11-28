/**
 * Engine-side view of the A24 asset provenance facts (pipeline/assets/schemas/asset-provenance.schema.json).
 * Only the fields the engine needs. Files stay private (outside git); the engine serves them through a
 * git-ignored public dir and verifies SHA-256 before use.
 */
export type AssetKind =
  | 'character' | 'expression' | 'parts' | 'prop' | 'texture' | 'environment' | 'audio' | 'other';

export interface ImageAssetRef {
  readonly id: string;
  readonly kind: AssetKind;
  /** Path relative to Remotion's public dir (use staticFile(publicPath)). */
  readonly publicPath: string;
  /** Private-store path of the byte-exact original (never modified or copied into tracked paths). */
  readonly privatePath: string;
  readonly sha256: string;
  readonly width: number;
  readonly height: number;
  readonly hasAlpha: boolean;
  /** A24 recorded a visible provider watermark; engine must not crop/hide it in the source. */
  readonly visibleWatermark: boolean;
  readonly c2pa: boolean;
}

const isHex64 = (s: unknown): s is string => typeof s === 'string' && /^[0-9a-f]{64}$/.test(s);

export const validateImageAssetRef = (v: unknown): ImageAssetRef => {
  const o = v as Record<string, unknown>;
  const fail = (m: string): never => {
    throw new Error(`ImageAssetRef invalid: ${m}`);
  };
  if (typeof o !== 'object' || o === null) return fail('not an object');
  if (typeof o.id !== 'string' || !o.id) fail('id');
  if (typeof o.publicPath !== 'string' || o.publicPath.startsWith('/')) fail('publicPath must be relative');
  if (typeof o.privatePath !== 'string') fail('privatePath');
  if (!isHex64(o.sha256)) fail('sha256');
  if (!Number.isInteger(o.width) || (o.width as number) <= 0) fail('width');
  if (!Number.isInteger(o.height) || (o.height as number) <= 0) fail('height');
  if (typeof o.hasAlpha !== 'boolean') fail('hasAlpha');
  return o as unknown as ImageAssetRef;
};

/** The verified Flow lighthouse plate (A24 intake; values from the director's brief). */
export const LIGHTHOUSE_PLATE_V01: ImageAssetRef = {
  id: 'lighthouse_plate_v01',
  kind: 'environment',
  publicPath: 'flow/lighthouse_plate_v01.png',
  privatePath: 'assets/private/flow/lighthouse_plate_v01.png',
  sha256: 'bd4fac1d3593467ed7583b42146712b6ee7d8d622edcd1d8a9056ed3d62a7a3a',
  width: 768,
  height: 1376,
  hasAlpha: true,
  visibleWatermark: true,
  c2pa: true,
};
