import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';

/**
 * Placeholder geometry (NOT a character). Pure function of useCurrentFrame(): no useFrame, Math.random, Date.
 * Times authored in seconds and converted via fps so 24 dev / 30 final play the same motion.
 */
export const PlaceholderCard: React.FC<{ viewHeight: number }> = ({ viewHeight }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const total = durationInFrames / fps;
  const x = interpolate(t, [0, total], [-0.18, 0.18], { easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) * viewHeight;
  const rotY = t * Math.PI * 0.5; // 90 deg per second
  const s = viewHeight * 0.16;
  return (
    <mesh position={[x, -viewHeight * 0.05, 0.5]} rotation={[0.25, rotY, 0]}>
      <boxGeometry args={[s, s * 1.4, s * 0.1]} />
      <meshStandardMaterial color="#e8a33d" roughness={0.6} metalness={0} />
    </mesh>
  );
};
