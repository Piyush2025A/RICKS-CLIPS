import React from 'react';
import { Composition } from 'remotion';
import { EngineTest, engineTestDefaults, WIDTH, HEIGHT } from './EngineTest.tsx';

export const FPS = 24; // dev rate (CLAUDE.md rule 6); durations elsewhere are authored in seconds

export const RemotionRoot: React.FC = () => (
  <Composition
    id="EngineTest"
    component={EngineTest}
    width={WIDTH}
    height={HEIGHT}
    fps={FPS}
    durationInFrames={48}
    defaultProps={engineTestDefaults}
  />
);
