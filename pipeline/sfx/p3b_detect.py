"""A21 3B tasks 1-2 (a21-sfx-0.7): bed-subtracted SFX candidate detectors; writes candidates CSV. numpy only.
M1 side-channel broadband rise over per-band rolling-median bed (past 1.0..0.2 s)
M2 mid rise inside acoustic pauses (floor = pause P10), full band
M3 mid sub(60-150)+air(7-16k) joint rise vs rolling-median bed with voice band (300-3400) flat (<4 dB)
usage: p3b_detect.py FEATDIR OUT.csv"""
import sys,csv,numpy as np
from p3b_util import *
FD=sys.argv[1]; rows=[]
for n in range(1,31):
    z=np.load(f'{FD}/v{n:02d}.npz'); bm,bs=z['bm'].astype(float),z['bs'].astype(float); T=len(bm)
    # M1
    Es=db(bs)[:,:36]; Es=np.maximum(Es,-100)  # side carries signal only below ~3.9 kHz (AAC); bands 0-35
    sm=np.array([np.convolve(Es[:,k],np.ones(3)/3,'same') for k in range(36)]).T
    bed=rollmed_past(sm); fut=np.array([np.convolve(sm[:,k],np.ones(1),'same') for k in range(36)]).T
    fmax=np.maximum.reduce([np.roll(sm,-s,axis=0) for s in (0,1,2,3,4)])
    rise=fmax-bed; ok=bed>np.percentile(Es,10,axis=0)  # bands above their own floor
    frac=(rise>6).mean(1); frac[:30]=0; frac[-30:]=0   # edge frames (np.roll wrap / stream end) excluded
    amp=np.median(rise,1); np.save(f"{FD}/frac{n:02d}.npy",frac)
    for t in peaks(frac,float(__import__("os").environ.get("M1THR","0.25")),25): rows.append(dict(video=n,method='M1',t=t/100,strength=float(frac[t]),amp_db=float(amp[t]),in_pause=0))
    # pauses / voiced
    v=db(band(bm,300,3400)); vo=close(v>otsu(v),10)
    pa=[(a+5,b-5) for a,b in runs(~vo) if b-a>=15 and a>0 and b<T]
    pm=np.zeros(T,bool)
    for a,b in pa: pm[a:b]=True
    # M2
    full=db(band(bm,60,16000))
    for a,b in pa:
        fl=np.percentile(full[a:b],10); r=full[a:b]-fl
        k=np.where((r[:-1]>=12)&(r[1:]>=12))[0]
        if len(k): 
            t=a+k[0]; rows.append(dict(video=n,method='M2',t=t/100,strength=float(r[k[0]]),amp_db=float(r.max()),in_pause=1))
    # M3
    sub=db(band(bm,60,150)); air=db(band(bm,7000,16000)); vb=v
    def rr(e): 
        s=np.convolve(e,np.ones(3)/3,'same'); b=rollmed_past(s[:,None])[:,0]; f=np.maximum.reduce([np.roll(s,-q) for q in (0,1,2,3,4)]); return f-b
    rs,ra,rv=rr(sub),rr(air),rr(vb)
    s3=np.minimum(rs,ra); s3[:30]=0; s3[-30:]=0

    for t in peaks(np.where(rv<4,s3,0),8,25): rows.append(dict(video=n,method='M3',t=t/100,strength=float(s3[t]),amp_db=float(rv[t]),in_pause=int(pm[t])))
    print(n,{m:sum(1 for r in rows if r['video']==n and r['method']==m) for m in('M1','M2','M3')},flush=True)
w=csv.DictWriter(open(sys.argv[2],'w'),list(rows[0])); w.writeheader(); w.writerows(rows)
