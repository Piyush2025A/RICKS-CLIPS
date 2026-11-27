#!/usr/bin/env python3
"""A21 feature extraction: per-10ms band/tonal/flux tracks per video -> npz (private). Usage: features.py OUTDIR [keys...]
Native 44.1k decode in memory (stereo for side/mid, mono mix for features). Script version a21-sfx-0.1."""
import sys, os, numpy as np, scipy.ndimage as ndi
sys.path.insert(0, os.path.dirname(__file__))
from common import *
SRC = os.path.expanduser("~/ricks-clips-private/reference-videos/RC30")
def feats(path):
    x = load_stereo(path); m = x.mean(1)
    side = 10*np.log10((((x[:,0]-x[:,1])/2)**2).mean()/(((x[:,0]+x[:,1])/2)**2).mean()+1e-12)
    S, f = stft_db(m)
    bd = {"sub":(30,85),"low":(85,300),"voice":(300,3400),"pres":(3400,8000),"air":(8000,16000),"top":(12000,20000)}
    d = {k: 10*np.log10(S[(f>=a)&(f<b)].sum(0)+1e-12) for k,(a,b) in bd.items()}
    # tonal (stationary line) energy above 1.8 kHz: horizontal vs vertical median
    hi = (f>=1800)&(f<10000); Sh = S[hi]
    H = ndi.median_filter(Sh, size=(1,15)); V = ndi.median_filter(Sh, size=(15,1))
    mask = H > 2.0*V
    d["tonal"] = 10*np.log10((H*mask).sum(0)+1e-12)
    d["hi_all"] = 10*np.log10(Sh.sum(0)+1e-12)
    # spectral flatness 1.8-10k and centroid
    d["flat"] = np.exp(np.log(Sh+1e-12).mean(0))/(Sh.mean(0)+1e-12)
    d["full"] = 10*np.log10(S.sum(0)+1e-12)
    # positive spectral flux on log-mag (whole spectrum) for generic onset
    L = np.log1p(1e3*np.sqrt(S)); d["flux"] = np.maximum(np.diff(L,axis=1,prepend=L[:,:1]),0).sum(0)
    d["side_db"] = np.array([side]); d["dur"] = np.array([len(m)/SR])
    return d
if __name__=="__main__":
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    keys=sys.argv[2:] or [str(i) for i in range(1,31)]
    for k in keys:
        np.savez_compressed(f"{out}/f{int(k):02d}.npz", **feats(f"{SRC}/{int(k)}.mp4")); print("done",k,flush=True)
