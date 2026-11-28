import React from 'react';
import { staticFile } from 'remotion';
import type { ImageAssetRef } from '../contracts/assets.ts';
import { useRemotionTexture } from './useTexture.ts';

/**
 * Full-frame background card at z=0, "cover"-scaled to the visible frustum (no cropping in the source file;
 * cover may trim a sliver of the plate edge when aspect ratios differ). Unlit (MeshBasicMaterial, toneMapped=false)
 * so the plate's colours reach the output unchanged.
 */
export const PlateCard: React.FC<{ asset: ImageAssetRef; viewWidth: number; viewHeight: number }> = ({
  asset,
  viewWidth,
  viewHeight,
}) => {
  const tex = useRemotionTexture(staticFile(asset.publicPath));
  if (!tex) return null;
  const plateAspect = asset.width / asset.height;
  const frameAspect = viewWidth / viewHeight;
  const w = plateAspect >= frameAspect ? viewHeight * plateAspect : viewWidth;
  const h = plateAspect >= frameAspect ? viewHeight : viewWidth / plateAspect;
  return (
    <mesh position={[0, 0, 0]}>
      <planeGeometry args={[w, h]} />
      <meshBasicMaterial map={tex} toneMapped={false} />
    </mesh>
  );
};
