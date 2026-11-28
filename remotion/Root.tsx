import React from 'react';
import { LIGHTHOUSE_PLATE_V01 } from '../src/contracts/assets.ts';
import { Composition } from 'remotion';
import { NarrationTest, narrationCalcMetadata, NARRATION_FPS, type NarrationTestProps } from './NarrationTest.tsx';
import { EngineTest, engineTestDefaults, WIDTH, HEIGHT } from './EngineTest.tsx';

export const FPS = 24; // dev rate (CLAUDE.md rule 6); durations elsewhere are authored in seconds

// Placeholder default narration so the composition registers; real renders pass inputProps (see render-narration.ts).
const placeholderNarration: NarrationTestProps['narration'] = {
  id: 'unset', role: 'vo', production: 'unset', privatePath: 'unset', publicPath: 'unset',
  sha256: '0'.repeat(64), duration_s: 1, sample_rate: 48000, channels: 1,
};

export const RemotionRoot: React.FC = () => (
  <>
  <Composition
    id="EngineTest"
    component={EngineTest}
    width={WIDTH}
    height={HEIGHT}
    fps={FPS}
    durationInFrames={48}
    defaultProps={engineTestDefaults}
  />
  <Composition
    id="NarrationTest"
    component={NarrationTest}
    width={WIDTH}
    height={HEIGHT}
    fps={NARRATION_FPS}
    durationInFrames={24}
    calculateMetadata={narrationCalcMetadata}
    defaultProps={{ plate: LIGHTHOUSE_PLATE_V01, narration: placeholderNarration, beatFrames24: [] } satisfies NarrationTestProps}
  />
  </>
);
