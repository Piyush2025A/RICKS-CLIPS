#!/usr/bin/env python3
"""A21 SFX candidate detector v0.1 (conservative, lower-bound). Input: features npz dir; output events CSV + per-video JSON.
Usage: detect.py FEATDIR OUTDIR
Event classes (band-energy shape rules; see knowledge/audio/a21-sound-effects-specialist/FINDINGS.md for validation):
 boom   : sub(30-85Hz) rises >=12 dB over speech voice-band, sub-low(85-300) >= -8 dB, attack
 tonal  : stationary narrowband partials 1.8-10 kHz >= 12 dB over local median, >=120 ms (chime/sparkle/riser tone)
 sweep  : air (8-16k) >= +12 dB over local median for >=250 ms (whoosh/riser noise); rising/falling by envelope peak position
 click  : top(12-20k) >= +18 dB over local median, <=60 ms (transient; ambiguous with plosive/sibilant)
 bedstep: 1 s floor of low/sub changes >=8 dB persistently (ambience/music/drone start or stop)"""
import sys, os, glob, json, csv, numpy as np, scipy.ndimage as ndi
from scipy.signal import find_peaks
VER="a21-sfx-0.1"
def exc(x,w=301): return x-ndi.median_filter(x,size=w,mode='nearest')
def runs(mask):
    m=np.concatenate([[0],mask.astype(int),[0]]); d=np.diff(m); return list(zip(np.where(d==1)[0],np.where(d==-1)[0]))
def detect(d):
    n=len(d['sub']); T=n/100
    vox=d['voice']; act=vox>np.percentile(vox,60); vref=float(np.median(vox[act]))
    full=d['full']; fullref=float(np.median(full[act]))
    ev=[]
    # boom
    s=ndi.uniform_filter1d(d['sub']-vox,3); ok=(d['sub']-d['low'])>=-8
    pk,_=find_peaks(np.where(ok,s,-99),height=-13,distance=40,prominence=8)  # sub-voice >= -13 dB (speech median ~ -20..-25)
    for i in pk:
        base=np.min(d['sub'][max(0,i-30):i+1]); j=i
        while j>0 and d['sub'][j]>base+0.5*(d['sub'][i]-base): j-=1
        ev.append(dict(cls="boom",onset=j/100,peak=i/100,dur=float(((d['sub'][i:i+60]>d['sub'][i]-6).sum())/100),band_db=float(d['sub'][i]),ref_db=float(np.median(d['sub'][act]))))
    # tonal
    e=exc(d['tonal']); frac=d['tonal']-d['hi_all']
    for a,b in runs((ndi.uniform_filter1d(e,5)>=12)&(frac>=-3)):
        if b-a>=12:
            i=a+int(np.argmax(e[a:b])); ev.append(dict(cls="tonal",onset=a/100,peak=i/100,dur=(b-a)/100,band_db=float(d['tonal'][i]),ref_db=float(np.median(d['tonal']))))
    # sweep + click on air/top
    ea=ndi.uniform_filter1d(exc(d['air']),5)
    for a,b in runs(ea>=12):
        if b-a>=25:
            i=a+int(np.argmax(ea[a:b])); ev.append(dict(cls="sweep",onset=a/100,peak=i/100,dur=(b-a)/100,band_db=float(d['air'][i]),ref_db=float(np.median(d['air'])),shape="rising" if (i-a)>0.6*(b-a) else ("falling" if (i-a)<0.4*(b-a) else "swell")))
    et=exc(d['top'])
    for a,b in runs(et>=18):
        if b-a<=6 and not any(abs(a/100-x['onset'])<0.15 for x in ev if x['cls']=='sweep'):
            i=a+int(np.argmax(et[a:b])); ev.append(dict(cls="click",onset=a/100,peak=i/100,dur=(b-a)/100,band_db=float(d['top'][i]),ref_db=float(np.median(d['top']))))
    # bed steps
    for k in ('sub','low'):
        fl=ndi.percentile_filter(d[k],10,size=101,mode='nearest'); fl=ndi.uniform_filter1d(fl,51)
        D=np.array([fl[min(n-1,i+100):min(n,i+150)].mean()-fl[max(0,i-150):max(1,i-100)].mean() if 100<i<n-150 else 0 for i in range(n)])
        pk,_=find_peaks(np.abs(D),height=8,distance=300)
        for i in pk: ev.append(dict(cls="bedstep",onset=i/100,peak=i/100,dur=0.0,band_db=float(D[i]),ref_db=float(np.median(fl)),shape=("up_"+k) if D[i]>0 else ("down_"+k)))
    # short-term level of SFX: 400 ms full-band window max around peak vs speech-active median
    mom=10*np.log10(ndi.uniform_filter1d(10**(full/10),40,mode='nearest')+1e-12)
    for x in ev:
        i=int(x['peak']*100); x['rel_level_lu']=float(mom[max(0,i-30):i+40].max()-np.median(mom[act])); x['rel_band_db']=x['band_db']-x['ref_db']
    ev.sort(key=lambda x:x['onset'])
    return ev,T,vref
if __name__=="__main__":
    fd,od=sys.argv[1:3]; os.makedirs(od,exist_ok=True); rows=[]
    for p in sorted(glob.glob(fd+"/f*.npz")):
        k=int(p[-6:-4]); d=np.load(p); ev,T,vref=detect(d)
        for x in ev: x.update(key=f"RC30-{k:02d}",frame=int(round(x['onset']*30-1))); rows.append(x)
        c={}
        for x in ev: c[x['cls']]=c.get(x['cls'],0)+1
        print(k,f"{T:.0f}s",c, f"per10s={(len([x for x in ev if x['cls']!='bedstep']))/T*10:.2f}")
    keys=["key","cls","onset","peak","dur","frame","band_db","ref_db","rel_band_db","rel_level_lu","shape"]
    with open(od+"/events.csv","w",newline="") as f:
        w=csv.DictWriter(f,keys,extrasaction="ignore"); w.writeheader(); [w.writerow({k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()}) for r in rows]
