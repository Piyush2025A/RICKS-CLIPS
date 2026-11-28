"""A21 3B task 4: bed level in voice-free pauses vs adjacent speech, mid & side, per video. numpy only.
Pause = acoustic (mid 300-3400 Hz band, 2-class Otsu on dB, closed 100 ms), run >=150 ms, 50 ms margin trimmed.
Also reports how often caption_segments.csv has gaps >=150 ms (the brief's proposed pause definition)."""
import sys, csv, json, numpy as np
from p3b_feat import EDGES
FD=sys.argv[1]; CAP='/home/piyush/ricks-clips-private/analysis-data/rc30/captions/RC30-%02d/caption_segments.csv'
def db(x): return 10*np.log10(x+1e-14)
def band(b,lo,hi):
    i=[k for k in range(48) if EDGES[k]>=lo-1 and EDGES[k+1]<=hi+1]; return b[:,i].sum(1)
def otsu(v):
    h,e=np.histogram(v,128); c=(e[:-1]+e[1:])/2; w=np.cumsum(h); w2=w[-1]-w
    m=np.cumsum(h*c); mu=m/np.maximum(w,1); mu2=(m[-1]-m)/np.maximum(w2,1)
    return c[np.argmax(w*w2*(mu-mu2)**2)]
def runs(m):
    d=np.diff(np.r_[0,m.astype(int),0]); return list(zip(np.where(d==1)[0],np.where(d==-1)[0]))
def close(m,n):
    m=m.copy()
    for a,b in runs(~m):
        if a>0 and b<len(m) and b-a<=n: m[a:b]=True
    return m
rows=[]; allp={}
for n in range(1,31):
    z=np.load(f'{FD}/v{n:02d}.npz'); bm,bs=z['bm'].astype(float),z['bs'].astype(float)
    v=db(band(bm,300,3400)); th=otsu(v); voiced=close(v>th,10)
    pauses=[(a+5,b-5) for a,b in runs(~voiced) if b-a>=15 and a>0 and b<len(v)]  # interior, >=150 ms
    # caption gaps
    cs=list(csv.DictReader(open(CAP%n))); capgap=sum(float(cs[k+1]['t_start'])-float(cs[k]['t_end'])>=0.15 for k in range(len(cs)-1))
    cb=np.array([float(c['t_start']) for c in cs]+[float(c['t_end']) for c in cs])
    res={'video':n,'n_pause':len(pauses),'pause_s':sum(b-a for a,b in pauses)/100,'cap_gaps150':capgap}
    pm=np.zeros(len(v),bool)
    for a,b in pauses: pm[a:b]=True
    sp=np.zeros(len(v),bool)  # adjacent speech: 300 ms before/after each pause (voiced frames only)
    for a,b in pauses:
        for lo,hi in ((a-5-30,a-5),(b+5,b+5+30)): 
            lo=max(lo,0); hi=min(hi,len(v)); sp[lo:hi]|=voiced[lo:hi]
    for nm,b in (('mid',bm),('side',bs)):
        for bn,(lo,hi) in (('400-2000',(400,2000)),('full',(60,16000)),('sub60-150',(60,150)),('2k-8k',(2000,8000))):
            e=band(b,lo,hi); P=db(e[pm].mean()); S=db(e[sp].mean()); Sall=db(e[voiced].mean())
            res[f'{nm}_{bn}_adj']=S-P; res[f'{nm}_{bn}_all']=Sall-P
            res[f'{nm}_{bn}_floor10']=db(np.percentile(e[pm],10))-P  # flatness of the pause floor
    # decay: first vs last 50 ms of pauses (mid 400-2000)
    e=band(bm,400,2000); f=[db(e[a:a+5].mean())-db(e[b-5:b].mean()) for a,b in pauses if b-a>=12]
    res['mid_pause_head_minus_tail']=float(np.median(f)) if f else np.nan
    # pause starts near caption boundary (+-100 ms)
    st=np.array([a for a,b in pauses])/100+0.0
    res['pause_start_near_capbound']=float(np.mean([np.min(np.abs(cb-t))<=0.1 for t in st])) if len(st) else np.nan
    res['voiced_frac']=float(voiced.mean())
    rows.append(res); print(n,{k:round(v,1) if isinstance(v,float) else v for k,v in res.items() if k in('n_pause','mid_400-2000_adj','side_400-2000_adj','cap_gaps150')},flush=True)
keys=list(rows[0]); w=csv.DictWriter(open(sys.argv[2],'w'),keys); w.writeheader(); w.writerows(rows)
summ={}
for k in keys[1:]:
    a=np.array([r[k] for r in rows],float); a=a[~np.isnan(a)]
    summ[k]=[float(np.median(a)),float(np.percentile(a,25)),float(np.percentile(a,75)),float(a.min()),float(a.max())]
json.dump(summ,open(sys.argv[2].replace('.csv','_summary.json'),'w'),indent=1)
for k,v in summ.items(): print(k,[round(x,2) for x in v])
