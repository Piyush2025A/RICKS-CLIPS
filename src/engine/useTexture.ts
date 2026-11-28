import { useEffect, useState } from 'react';
import { useThree } from '@react-three/fiber';
import { cancelRender, continueRender, delayRender } from 'remotion';
import { LinearMipmapLinearFilter, LinearFilter, SRGBColorSpace, Texture, TextureLoader } from 'three';

/**
 * Deterministic texture loading: the frame is not captured until the image has decoded (delayRender/continueRender).
 * Colour management is explicit: colour images are sRGB-tagged. Mipmaps on (minified at 360p), no anisotropy tricks.
 */
export const useRemotionTexture = (url: string): Texture | null => {
  const advance = useThree((st) => st.advance);
  const [texture, setTexture] = useState<Texture | null>(null);
  const [handle] = useState(() => delayRender(`texture ${url}`, { timeoutInMilliseconds: 60000 }));

  useEffect(() => {
    let cancelled = false;
    new TextureLoader().load(
      url,
      (tex) => {
        if (cancelled) return;
        tex.colorSpace = SRGBColorSpace;
        tex.generateMipmaps = true;
        tex.minFilter = LinearMipmapLinearFilter;
        tex.magFilter = LinearFilter;
        tex.needsUpdate = true;
        setTexture(tex);
      },
      undefined,
      (err) => cancelRender(err instanceof Error ? err : new Error(`texture load failed: ${url}`)),
    );
    return () => {
      cancelled = true;
    };
  }, [url, handle]);

  // During rendering <ThreeCanvas> uses frameloop="never" and only advances when the frame number changes, so a
  // late-arriving texture does not trigger a redraw by itself (observed: black plate). After React committed the mesh
  // (2 animation frames) we advance the R3F loop once explicitly and then release the delay. Deterministic: no useFrame.
  useEffect(() => {
    if (!texture) return;
    let r2 = 0;
    const r1 = requestAnimationFrame(() => {
      r2 = requestAnimationFrame(() => {
        advance(performance.now());
        continueRender(handle);
      });
    });
    return () => {
      cancelAnimationFrame(r1);
      cancelAnimationFrame(r2);
    };
  }, [texture, handle, advance]);

  return texture;
};
