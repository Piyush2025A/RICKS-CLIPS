"""A21 3B: positive control for M1. Inject a synthetic broadband burst (all 48 bands, 8 frames = 80 ms) into real side-channel band power at X dB above the local per-band bed (x power gain) at 6 random times per video (12 videos, away from edges); report detection rate of M1 (frac>=0.1 within +-0.1 s). usage: p3b_sens.py FEATDIR"""
import sys,numpy as np
from p3b_util import *
FD=sys.argv[1]; rng=np.random.default_rng(3); vids=list(range(1,31,2))[:12]
def m1(bs):
    Es=np.maximum(db(bs)[:,:36],-100); sm=np.array([np.convolve(Es[:,k],np.ones(3)/3,'same') for k in range(36)]).T
    bed=rollmed_past(sm); fmax=np.maximum.reduce([np.roll(sm,-s,axis=0) for s in (0,1,2,3,4)])
    fr=((fmax-bed)>6).mean(1); fr[:30]=0; fr[-30:]=0; return fr
for X in (0,3,6,12):
    det=0;n=0
    for v in vids:
        bs=np.load(f'{FD}/v{v:02d}.npz')['bs'].astype(float); T=len(bs)
        ts=rng.integers(200,T-200,6); b2=bs.copy()
        for t in ts: b2[t:t+8,:36]*=10**(X/10)
        fr=m1(b2)
        for t in ts: det+= fr[t-5:t+10].max()>=0.1; n+=1
    print('burst +%d dB over bed: detected %d/%d = %.2f'%(X,det,n,det/n),flush=True)
