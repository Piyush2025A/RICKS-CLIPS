/**
 * A26 diagnostic entry (own bundle; does NOT touch A25 files). Logs WebGL/WebGL2 context info via console
 * (captured by renderer onBrowserLog). Bundle with: render.ts prepare --entry pipeline/render/diag/index.tsx --name diag --noplate
 */
import React from 'react';
import { Composition, registerRoot, AbsoluteFill } from 'remotion';

const Diag: React.FC = () => {
  const info: Record<string, unknown> = { ua: navigator.userAgent };
  for (const kind of ['webgl2', 'webgl'] as const) {
    try {
      const c = document.createElement('canvas'); c.width = 64; c.height = 64;
      const g = c.getContext(kind) as WebGL2RenderingContext | null;
      if (!g) { info[kind] = null; continue; }
      const ext = g.getExtension('WEBGL_debug_renderer_info');
      info[kind] = {
        version: g.getParameter(g.VERSION), glsl: g.getParameter(g.SHADING_LANGUAGE_VERSION), vendor: g.getParameter(g.VENDOR), renderer: g.getParameter(g.RENDERER),
        unmaskedVendor: ext ? g.getParameter(ext.UNMASKED_VENDOR_WEBGL) : null, unmaskedRenderer: ext ? g.getParameter(ext.UNMASKED_RENDERER_WEBGL) : null,
        maxTextureSize: g.getParameter(g.MAX_TEXTURE_SIZE), maxRenderbuffer: g.getParameter(g.MAX_RENDERBUFFER_SIZE), maxViewport: Array.from(g.getParameter(g.MAX_VIEWPORT_DIMS) as Int32Array),
        maxAnisotropy: (() => { const a = g.getExtension('EXT_texture_filter_anisotropic'); return a ? g.getParameter(a.MAX_TEXTURE_MAX_ANISOTROPY_EXT) : null; })(),
        samples: kind === 'webgl2' ? g.getParameter(g.MAX_SAMPLES) : null, extCount: g.getSupportedExtensions()?.length ?? 0,
        floatRT: !!g.getExtension('EXT_color_buffer_float'),
      };
    } catch (e) { info[kind] = `error: ${String(e)}`; }
  }
  console.log('A26DIAG ' + JSON.stringify(info));
  return <AbsoluteFill style={{ background: '#222' }} />;
};
registerRoot(() => <Composition id="Diag" component={Diag} width={360} height={640} fps={24} durationInFrames={1} />);
