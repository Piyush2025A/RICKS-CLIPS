#!/usr/bin/env python3
"""A21 detector v0.2 — non-speech-evidence rules (harmonicity + duration). Usage: detect2.py FEAT FEAT2 OUTCSV
Classes: noise_long (>=300 ms unvoiced broadband noise, harm<0.3, hi4-12 excess) => whoosh/riser/crash candidate;
         boom (sub 30-85 Hz sustained >=120 ms, sub-low >= -8 dB, harm low) => impact/thud/rumble candidate;
         tonal (stationary partials >=150 ms, tonal share high) => chime/sparkle/riser-tone/pad candidate.
Duration gates exclude fricatives (typically <=200 ms) and plosives (<=60 ms). Precision measured separately by hand check."""
import sys, glob, os, csv, numpy as np, scipy.ndimage as ndi
from detect import exc, runs
def detect2(d,g):
    n=len(d['sub']); ev=[]
    vox=d['voice']; act=vox>np.percentile(vox,60); full=d['full']
    mom=10*np.log10(ndi.uniform_filter1d(10**(full/10),40,mode='nearest')+1e-12); mref=float(np.median(mom[act]))
    harm=ndi.uniform_filter1d(g['harm'],5)
    # noise_long: hi4-12 high & unvoiced & low-mid band also non-empty (broadband), sustained
    hi=g['hi4_12']; e_hi=exc(hi)
    m=(harm<0.3)&(e_hi>=8)&(g['lo300_1500']>=hi-25)
    m=ndi.binary_closing(m,np.ones(6)); 
    for a,b in runs(m):
        if b-a>=30:
            seg=e_hi[a:b]; i=a+int(np.argmax(seg)); half=a+(b-a)//2
            sh="rising" if seg[(b-a)//2:].mean()>seg[:(b-a)//2].mean()+3 else ("falling" if seg[:(b-a)//2].mean()>seg[(b-a)//2:].mean()+3 else "flat")
            ev.append(dict(cls="noise_long",onset=a/100,peak=i/100,dur=(b-a)/100,band_db=float(hi[i]),ref_db=float(np.median(hi)),shape=sh,mean_harm=float(harm[a:b].mean())))
    # boom
    sub=d['sub']; es=exc(sub)
    mb=(es>=10)&((sub-d['low'])>=-8)
    mb=ndi.binary_closing(mb,np.ones(5))
    for a,b in runs(mb):
        if b-a>=12:
            i=a+int(np.argmax(sub[a:b])); ev.append(dict(cls="boom",onset=a/100,peak=i/100,dur=(b-a)/100,band_db=float(sub[i]),ref_db=float(np.median(sub)),shape="",mean_harm=float(harm[a:b].mean())))
    # tonal
    et=ndi.uniform_filter1d(exc(d['tonal']),5); frac=d['tonal']-d['hi_all']
    for a,b in runs((et>=12)&(frac>=-3)):
        if b-a>=15:
            i=a+int(np.argmax(et[a:b])); ev.append(dict(cls="tonal",onset=a/100,peak=i/100,dur=(b-a)/100,band_db=float(d['tonal'][i]),ref_db=float(np.median(d['tonal'])),shape="",mean_harm=float(harm[a:b].mean())))
    for x in ev:
        i=int(x['peak']*100); x['rel_level_lu']=float(mom[max(0,i-30):i+40].max()-mref); x['rel_band_db']=x['band_db']-x['ref_db']
    ev.sort(key=lambda x:x['onset']); return ev,n/100
if __name__=="__main__":
    fd,gd,out=sys.argv[1:4]; rows=[]
    for p in sorted(glob.glob(fd+"/f*.npz")):
        k=int(p[-6:-4]); d=np.load(p); g=np.load(f"{gd}/g{k:02d}.npz"); ev,T=detect2(d,g)
        c={}
        for x in ev: x['key']=f"RC30-{k:02d}"; x['frame']=int(round(x['onset']*30-1)); rows.append(x); c[x['cls']]=c.get(x['cls'],0)+1
        print(k,f"{T:.0f}s",c,f"per10s={len(ev)/T*10:.2f}")
    keys=["key","cls","onset","peak","dur","frame","band_db","ref_db","rel_band_db","rel_level_lu","shape","mean_harm"]
    with open(out,"w",newline="") as f:
        w=csv.DictWriter(f,keys,extrasaction="ignore"); w.writeheader(); [w.writerow({k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()}) for r in rows]
