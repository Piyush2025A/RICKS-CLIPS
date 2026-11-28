import { createHash } from 'node:crypto';
import { existsSync, readFileSync, statSync } from 'node:fs';
import type { NarrationDescriptor } from './narration.ts';

/** Node-only helpers (kept out of narration.ts so the Remotion browser bundle never imports node:*). */
export const sha256File = (file: string): string => createHash('sha256').update(readFileSync(file)).digest('hex');

/** Fail loudly (throw) if the file is missing or its SHA-256 / size differs from the descriptor. Returns the absolute path. */
export const verifyNarrationFile = (d: NarrationDescriptor, repoRoot: string): string => {
  const abs = `${repoRoot.replace(/\/$/, '')}/${d.privatePath}`;
  if (!existsSync(abs)) {
    throw new Error(`NARRATION MISSING: ${d.privatePath} not found. Transfer it per ENGINE.md "Accepting private narration".`);
  }
  if (d.bytes !== undefined && statSync(abs).size !== d.bytes) {
    throw new Error(`NARRATION SIZE MISMATCH: ${d.privatePath} is ${statSync(abs).size} B, descriptor says ${d.bytes} B`);
  }
  const got = sha256File(abs);
  if (got !== d.sha256) {
    throw new Error(`NARRATION SHA-256 MISMATCH: ${d.privatePath} is ${got}, descriptor says ${d.sha256}. Refusing to render.`);
  }
  return abs;
};
