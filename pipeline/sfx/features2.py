#!/usr/bin/env python3
"""A21 features v2: harmonicity (autocorr 70-400 Hz), wideband noise band levels, 10 ms hop. Usage: features2.py OUTDIR [keys]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import *
SRC=os.path.expanduser("~/ricks-clips-private/reference-videos/RC30")
def f2(path):
    m=load_stereo(path).mean(1); S,f=stft_db(m,2048,441)
    n=S.shape[1]
    b=lambda a,c:10*np.log10(S[(f>=a)&(f<c)].sum(0)+1e-12)
    d={"lo300_1500":b(300,1500),"mid1500_4000":b(1500,4000),"hi4_12":b(4000,12000)}
    Sw=S[(f>=300)&(f<12000)]; d["flat_wide"]=np.exp(np.log(Sw+1e-12).mean(0))/(Sw.mean(0)+1e-12)
    # harmonicity: normalized autocorr of 40 ms frames
    N=1764; h=np.zeros(n); pad=np.pad(m,(N//2,N//2))
    for i in range(n):
        s=pad[i*441:i*441+N]; s=s-s.mean(); e=(s*s).sum()
        if e<1e-9: continue
        X=np.fft.rfft(s,2*N); ac=np.fft.irfft(X*np.conj(X))[:N]; 
        h[i]=ac[110:630].max()/ac[0]
    d["harm"]=h
    return d
if __name__=="__main__":
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    for k in (sys.argv[2:] or [str(i) for i in range(1,31)]):
        np.savez_compressed(f"{out}/g{int(k):02d}.npz",**f2(f"{SRC}/{int(k)}.mp4")); print("done",k,flush=True)
