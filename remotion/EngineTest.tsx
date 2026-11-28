import React from 'react';
import { AbsoluteFill, Audio, staticFile } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { NoToneMapping, SRGBColorSpace } from 'three';
import { PlateCard, PlaceholderCard } from '../src/engine/index.ts';
import { LIGHTHOUSE_PLATE_V01, type ImageAssetRef } from '../src/contracts/assets.ts';

export type EngineTestProps = {
  plate: ImageAssetRef;
  /** Public-dir relative audio path; undefined = no audio. */
  audio?: string;
  /** Rendered captions are OPTIONAL and OFF by default (D036). No caption component exists in the engine yet. */
  captions: boolean;
};

export const engineTestDefaults: EngineTestProps = { plate: LIGHTHOUSE_PLATE_V01, audio: undefined, captions: false };

export const WIDTH = 360;
export const HEIGHT = 640;
const FOV = 50;
const CAM_Z = 10;
// world units: visible height at z=0 is 2*CAM_Z*tan(FOV/2)
const VIEW_H = 2 * CAM_Z * Math.tan((FOV * Math.PI) / 360);
const VIEW_W = (VIEW_H * WIDTH) / HEIGHT;

export const EngineTest: React.FC<EngineTestProps> = ({ plate, audio }) => (
  <AbsoluteFill style={{ backgroundColor: '#000' }}>
    <ThreeCanvas
      width={WIDTH}
      height={HEIGHT}
      camera={{ fov: FOV, position: [0, 0, CAM_Z], near: 0.1, far: 100 }}
      flat
      onCreated={({ gl }) => {
        gl.outputColorSpace = SRGBColorSpace;
        gl.toneMapping = NoToneMapping;
      }}
    >
      <ambientLight intensity={0.8} />
      <directionalLight position={[3, 5, 8]} intensity={2.2} />
      <PlateCard asset={plate} viewWidth={VIEW_W} viewHeight={VIEW_H} />
      <PlaceholderCard viewHeight={VIEW_H} />
    </ThreeCanvas>
    {audio ? <Audio src={staticFile(audio)} /> : null}
  </AbsoluteFill>
);
