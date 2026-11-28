/**
 * Time contract (A20 pipeline/voice/CONTRACT.md "Units and frame conversion"; Python twin: common.seconds_to_frame).
 * Seconds are master. Canonical rule, bit-for-bit with Python: round half up on integer microseconds.
 *   us = floor(t*1e6 + 0.5);  frame = floor((us*fps + 500000) / 1e6)   (exact integer arithmetic, BigInt)
 */
export const DEV_FPS = 24;
export const FINAL_FPS = 30;

/** Convert seconds to frames BY TIME. Never copy frame numbers across fps values. */
export const secondsToFrames = (seconds: number, fps: number): number => {
  if (typeof seconds !== 'number' || !Number.isFinite(seconds) || seconds < 0) {
    throw new Error(`secondsToFrames: t must be a finite number >= 0, got ${seconds}`);
  }
  if (typeof fps !== 'number' || !Number.isInteger(fps) || fps <= 0) {
    throw new Error(`secondsToFrames: fps must be a positive integer, got ${fps}`);
  }
  const us = Math.floor(seconds * 1_000_000 + 0.5); // same IEEE double ops as Python
  if (!Number.isFinite(us)) throw new Error(`secondsToFrames: t too large: ${seconds}`);
  return Number((BigInt(us) * BigInt(fps) + 500_000n) / 1_000_000n); // BigInt division floors for non-negative values
};

/**
 * Composition/clip duration that must CONTAIN media (D039): smallest integer N with N/fps >= t,
 * on integer microseconds (us = floor(t*1e6+0.5); N = ceil(us*fps/1e6), exact BigInt). t=0 -> 0.
 * Event timestamps keep secondsToFrames (nearest, half-up).
 */
export const durationFramesCovering = (seconds: number, fps: number): number => {
  if (typeof seconds !== 'number' || !Number.isFinite(seconds) || seconds < 0) {
    throw new Error(`durationFramesCovering: t must be a finite number >= 0, got ${seconds}`);
  }
  if (typeof fps !== 'number' || !Number.isInteger(fps) || fps <= 0) {
    throw new Error(`durationFramesCovering: fps must be a positive integer, got ${fps}`);
  }
  const us = Math.floor(seconds * 1_000_000 + 0.5);
  if (!Number.isFinite(us)) throw new Error(`durationFramesCovering: t too large: ${seconds}`);
  return Number((BigInt(us) * BigInt(fps) + 999_999n) / 1_000_000n);
};

export const framesToSeconds= (frame: number, fps: number): number => frame / fps;
