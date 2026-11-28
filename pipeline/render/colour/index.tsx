/**
 * A26 colour-patch diagnostic (Phase 5A colour correction). CSS flat patches, full coverage, 360x640 @ 24 fps, 6 frames.
 * Layout: 2 columns x 7 rows of 180x~91 px cells. Patch list is mirrored in pipeline/render/colour/measure.py (keep in sync).
 * Last cell (index 13) is a WebGL (three.js-free, raw WebGL2) clear-colour patch to confirm the canvas path.
 * Bundle: render.ts prepare --entry pipeline/render/colour/index.tsx --name colour --noplate
 */
import React, { useEffect, useRef } from 'react';
import { Composition, registerRoot, AbsoluteFill } from 'remotion';

export const PATCHES: [number, number, number][] = [
  [0, 0, 0], [255, 255, 255], [128, 128, 128], [255, 0, 0], [0, 255, 0], [0, 0, 255],
  [224, 172, 138], [141, 85, 36], [135, 206, 235], [70, 130, 180], [32, 32, 32], [200, 200, 200],
  [224, 172, 138], // 12: skin again, reference for WebGL comparison
  [224, 172, 138], // 13: WebGL canvas with same colour (index 12 is CSS)
];
const W = 360, H = 640, COLS = 2, ROWS = 7;
const GL_INDEX = 13;

const Gl: React.FC<{ rgb: [number, number, number] }> = ({ rgb }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const c = ref.current as HTMLCanvasElement;
    const g = c.getContext('webgl2') as WebGL2RenderingContext;
    g.clearColor(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, 1); g.clear(g.COLOR_BUFFER_BIT);
  }, [rgb]);
  return <canvas ref={ref} width={W / COLS} height={Math.floor(H / ROWS)} style={{ width: '100%', height: '100%', display: 'block' }} />;
};

const Patches: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    {PATCHES.map((p, i) => {
      const x = (i % COLS) * (W / COLS), y = Math.floor(i / COLS) * Math.floor(H / ROWS);
      return (
        <div key={i} style={{ position: 'absolute', left: x, top: y, width: W / COLS, height: Math.floor(H / ROWS), background: `rgb(${p[0]},${p[1]},${p[2]})` }}>
          {i === GL_INDEX ? <Gl rgb={p} /> : null}
        </div>
      );
    })}
  </AbsoluteFill>
);
registerRoot(() => <Composition id="Patches" component={Patches} width={W} height={H} fps={24} durationInFrames={6} />);
