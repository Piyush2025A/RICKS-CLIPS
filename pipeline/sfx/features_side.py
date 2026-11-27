#!/usr/bin/env python3
"""A21 side-channel features: S=(L-R)/2 isolates non-centre content (narration is centre-panned, side ~ -20..-32 dB re mid).
Per 10 ms: band dB of side and of mid (mono mix), side flatness/tonal share. Usage: features_side.py OUTDIR [keys]
Limitation: only stereo-wide SFX/music are visible; centre-panned (mono) SFX are masked by/identical to the voice channel."""
import sys, os, numpy as np, scipy.ndimage as ndi
sys.path.insert(0, os.path.dirname(__file__))
from common import *
SRC=os.path.expanduser("~/ricks-clips-private/reference-videos/RC30")
BD={"sub":(30,100),"low":(100,300),"lmid":(300,1500),"mid":(1500,4000),"pres":(4000,8000),"air":(8000,16000)}
def bands(S,f): return {k:10*np.log10(S[(f>=a)&(f<b)].sum(0)+1e-12) for k,(a,b) in BD.items()}
def run(path):
    x=load_stereo(path); mid=(x[:,0]+x[:,1])/2; side=(x[:,0]-x[:,1])/2
    out={}
    Sm,f=stft_db(mid); Ss,_=stft_db(side)
    for k,v in bands(Sm,f).items(): out["m_"+k]=v
    for k,v in bands(Ss,f).items(): out["s_"+k]=v
    out["m_full"]=10*np.log10(Sm.sum(0)+1e-12); out["s_full"]=10*np.log10(Ss.sum(0)+1e-12)
    sel=(f>=100)&(f<12000); Sw=Ss[sel]
    out["s_flat"]=np.exp(np.log(Sw+1e-12).mean(0))/(Sw.mean(0)+1e-12)
    H=ndi.median_filter(Sw,size=(1,15)); V=ndi.median_filter(Sw,size=(15,1))
    out["s_tonal"]=10*np.log10((H*(H>2*V)).sum(0)+1e-12)   # stationary-line (music) energy
    out["s_resid"]=10*np.log10(np.maximum(Sw.sum(0)-(H*(H>2*V)).sum(0),1e-12))  # non-tonal (broadband/transient) energy
    Ls=np.log1p(1e3*np.sqrt(Ss)); out["s_flux"]=np.maximum(np.diff(Ls,axis=1,prepend=Ls[:,:1]),0).sum(0)
    out["dur"]=np.array([len(mid)/SR]); return out
if __name__=="__main__":
    o=sys.argv[1]; os.makedirs(o,exist_ok=True)
    for k in (sys.argv[2:] or [str(i) for i in range(1,31)]):
        np.savez_compressed(f"{o}/s{int(k):02d}.npz",**run(f"{SRC}/{int(k)}.mp4")); print("done",k,flush=True)
