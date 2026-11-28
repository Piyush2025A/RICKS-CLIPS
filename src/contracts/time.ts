/** Time contract (A20 CONTRACT "Units and frame conversion"): seconds are master; frame = floor(t*fps+0.5). */
export const DEV_FPS = 24;
export const FINAL_FPS = 30;

/** Convert seconds to frames BY TIME. Never copy frame numbers across fps values. */
export const secondsToFrames = (seconds: number, fps: number): number => {
  if (!Number.isFinite(seconds) || !Number.isFinite(fps) || fps <= 0) {
    throw new Error(`secondsToFrames: invalid input seconds=${seconds} fps=${fps}`);
  }
  return Math.floor(seconds * fps + 0.5);
};

export const framesToSeconds = (frame: number, fps: number): number => frame / fps;
