import { secondsToFrames } from './time.ts';

/** A20 beats.json (pipeline/voice/beats.py). Only the fields the engine reads; extra fields are ignored. */
export interface BeatSpan {
  readonly index: number;
  readonly t_on: number;
  readonly t_off: number;
  readonly frames_24?: readonly [number, number];
  readonly frames_30?: readonly [number, number];
}
export interface Beats {
  readonly voiced: readonly [number, number];
  readonly sentences: readonly BeatSpan[];
  readonly clauses: readonly BeatSpan[];
}

const span = (v: unknown, where: string): BeatSpan => {
  const o = v as Record<string, unknown>;
  if (typeof o?.index !== 'number' || typeof o.t_on !== 'number' || typeof o.t_off !== 'number') {
    throw new Error(`beats: bad span at ${where}`);
  }
  if (o.t_off < o.t_on) throw new Error(`beats: t_off < t_on at ${where}`);
  return o as unknown as BeatSpan;
};

export const parseBeats = (json: unknown): Beats => {
  const o = json as Record<string, unknown>;
  const voiced = o?.voiced as unknown[] | undefined;
  if (!Array.isArray(voiced) || voiced.length !== 2) throw new Error('beats: voiced');
  if (!Array.isArray(o.sentences) || !Array.isArray(o.clauses)) throw new Error('beats: sentences/clauses');
  return {
    voiced: [Number(voiced[0]), Number(voiced[1])],
    sentences: o.sentences.map((s, i) => span(s, `sentences[${i}]`)),
    clauses: o.clauses.map((s, i) => span(s, `clauses[${i}]`)),
  };
};

/** Frame span for a beat at the given fps. frame_in inclusive, frame_out inclusive (matches A20 frames_NN). */
export const beatFrames = (b: BeatSpan, fps: number): [number, number] => [
  secondsToFrames(b.t_on, fps),
  secondsToFrames(b.t_off, fps),
];
