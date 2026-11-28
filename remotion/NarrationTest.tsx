import React from 'react';
import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { NoToneMapping, SRGBColorSpace } from 'three';
import { PlateCard } from '../src/engine/index.ts';
import { LIGHTHOUSE_PLATE_V01, type ImageAssetRef } from '../src/contracts/assets.ts';
import { secondsToFrames } from '../src/contracts/time.ts';
import { validateNarrationDescriptor, type NarrationDescriptor } from '../src/contracts/narration.ts';
import { WIDTH, HEIGHT } from './EngineTest.tsx';

export type NarrationTestProps = {
  plate: ImageAssetRef;
  narration: NarrationDescriptor;
  /** Beat spans [in, out] inclusive in frames at 24 fps, taken from beats.json frames_24 (clauses). */
  beatFrames24: readonly (readonly [number, number])[];
};

export const NARRATION_FPS = 24;
const FOV = 50, CAM_Z = 10;
const VIEW_H = 2 * CAM_Z * Math.tan((FOV * Math.PI) / 360);
const VIEW_W = (VIEW_H * WIDTH) / HEIGHT;

/** durationInFrames = secondsToFrames(narration duration, 24); validated here so a bad descriptor fails the render. */
export const narrationCalcMetadata = ({ props }: { props: NarrationTestProps }) => {
  const d = validateNarrationDescriptor(props.narration);
  return { durationInFrames: secondsToFrames(d.duration_s, NARRATION_FPS), fps: NARRATION_FPS, width: WIDTH, height: HEIGHT };
};

/** Minimal placeholder (NOT a character): a box that is large and warm inside a beat span, small and dim outside. Pure f(frame). */
const BeatBox: React.FC<{ spans: readonly (readonly [number, number])[]; viewHeight: number }> = ({ spans, viewHeight }) => {
  const frame = useCurrentFrame();
  const active = spans.some(([a, b]) => frame >= a && frame <= b);
  const s = viewHeight * (active ? 0.2 : 0.12);
  return (
    <mesh position={[0, -viewHeight * 0.05, 0.5]} rotation={[0.25, 0.4, 0]}>
      <boxGeometry args={[s, s * 1.4, s * 0.1]} />
      <meshStandardMaterial color={active ? '#e8a33d' : '#4a5a70'} roughness={0.6} metalness={0} />
    </mesh>
  );
};

export const NarrationTest: React.FC<NarrationTestProps> = ({ plate, narration, beatFrames24 }) => (
  <AbsoluteFill style={{ backgroundColor: '#000' }}>
    <ThreeCanvas
      width={WIDTH}
      height={HEIGHT}
      camera={{ fov: FOV, position: [0, 0, CAM_Z], near: 0.1, far: 100 }}
      flat
      onCreated={({ gl }) => { gl.outputColorSpace = SRGBColorSpace; gl.toneMapping = NoToneMapping; }}
    >
      <ambientLight intensity={0.8} />
      <directionalLight position={[3, 5, 8]} intensity={2.2} />
      <PlateCard asset={plate} viewWidth={VIEW_W} viewHeight={VIEW_H} />
      <BeatBox spans={beatFrames24} viewHeight={VIEW_H} />
    </ThreeCanvas>
    <Audio src={staticFile(narration.publicPath)} />
  </AbsoluteFill>
);

export const narrationTestDefaults: Omit<NarrationTestProps, 'narration'> = { plate: LIGHTHOUSE_PLATE_V01, beatFrames24: [] };
