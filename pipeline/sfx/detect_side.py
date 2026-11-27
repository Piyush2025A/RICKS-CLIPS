#!/usr/bin/env python3
"""A21 side-channel SFX detector v0.5 (script version a21-sfx-0.5). Usage: detect_side.py FEAT_S OUTCSV
v0.5: events = peaks of non-tonal side energy (s_resid, smoothed 3 fr) >= 12 dB (weak) / >= 18 dB (strong) over +-1.5 s median, >= 200 ms apart.
Obsolete v0.4 notes follow. Candidates (side channel (L-R)/2, 10 ms hop; narration is centre so it is largely absent):
  T  transient : s_flux (smoothed 3 fr) peak >= FLUX_THR (450; hand-calibrated on 12 labelled candidates, see FINDINGS) -> click/tick/burst
  B  thud      : s_sub (30-100 Hz) rise >= 15 dB over its +-1.5 s median within 5 frames (attack), peaks >= 300 ms apart
  W  swell     : non-tonal side energy >= +10 dB over median for >= 250 ms -> whoosh/swell/riser-noise
Merged when onsets <150 ms apart. Music note changes (narrow tonal lines, flux < 400) are not counted as SFX."""
import sys, glob, csv, numpy as np, scipy.ndimage as ndi
from scipy.signal import find_peaks
FLUX_THR=450.0  # unused in v0.5 (flux kept as a descriptor)
def exc(x,w=301): return x-ndi.median_filter(x,size=w,mode='nearest')
def runs(m):
    m=np.concatenate([[0],m.astype(int),[0]]); d=np.diff(m); return list(zip(np.where(d==1)[0],np.where(d==-1)[0]))
def onset_back(r,i,frac=0.5,maxb=40):
    lo=r[max(0,i-maxb):i+1].min(); j=i
    while j>max(0,i-maxb) and r[j-1]>lo+frac*(r[i]-lo): j-=1
    return j
def detect(d, thr=12.0):
    r=ndi.uniform_filter1d(d["s_resid"],3); e=exc(r); ev=[]
    pk,_=find_peaks(e,height=thr,distance=20)
    for i in pk:
        ev.append(dict(src="R",onset=onset_back(r,i,0.5,30)/100,peak=i/100,excess_db=float(e[i]),flux=float(d["s_flux"][max(0,i-8):i+4].max())))
    mg=ev
    mref=float(np.median(d["m_full"][d["m_full"]>np.percentile(d["m_full"],60)])); out=[]
    for x in mg:
        i=int(x["peak"]*100); o=int(x["onset"]*100); sl=slice(max(0,o),o+30)
        bandmax={k:float(d["s_"+k][sl].max()) for k in ["sub","low","lmid","mid","pres","air"]}
        r=d["s_resid"]; dur=float((r[i:i+150]>r[i]-6).sum()/100)
        lowdom=max(bandmax["sub"],bandmax["low"])>=max(bandmax["mid"],bandmax["pres"],bandmax["air"])+3
        hidom=max(bandmax["pres"],bandmax["air"])>=max(bandmax["sub"],bandmax["low"])-3
        if dur>=0.8: c="riser_swell"
        elif dur>=0.25 and not lowdom: c="whoosh_noise"
        elif lowdom: c="impact_thud"
        elif dur<0.12 and hidom: c="click_tick"
        elif hidom: c="burst_hf"
        else: c="burst_mid"
        x.update(cls=c,dur=dur,tier=("strong" if x["excess_db"]>=18 else "weak"),side_db=float(d["s_full"][max(0,i-5):i+10].max()),
          rel_level_db=float(10*np.log10(np.mean(10**(d["s_full"][max(0,i-15):i+25]/10)))-mref),**{"b_"+k:v for k,v in bandmax.items()})
    return mg
if __name__=="__main__":
    fd,fo=sys.argv[1:3]; rows=[]
    for p in sorted(glob.glob(fd+"/s*.npz")):
        k=int(p[-6:-4]); d=np.load(p); T=float(d["dur"][0]); ev=detect(d); c={}
        for x in ev: x["key"]=f"RC30-{k:02d}"; x["frame"]=int(round(x["onset"]*30-1)); x["T"]=T; rows.append(x); c[x["cls"]]=c.get(x["cls"],0)+1
        print(k,f"{T:.0f}s n={len(ev)} per10s={len(ev)/T*10:.2f}",c)
    ks=["key","cls","tier","excess_db","flux","onset","peak","dur","frame","side_db","rel_level_db","b_sub","b_low","b_lmid","b_mid","b_pres","b_air"]
    with open(fo,"w",newline="") as f:
        w=csv.DictWriter(f,ks,extrasaction="ignore"); w.writeheader(); [w.writerow({k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()}) for r in rows]
