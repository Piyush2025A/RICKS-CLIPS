"""A21 3B task 4b: cross-channel reference: mid-speech level minus pause level (mid mean, mid P10 floor, side mean), 400-2000 Hz and full band. Reuses p3b_bed helpers by copy."""
import sys,csv,json,numpy as np
from p3b_feat import EDGES
FD=sys.argv[1]
def db(x): return 10*np.log10(x+1e-14)
def band(b,lo,hi):
    i=[k for k in range(48) if EDGES[k]>=lo-1 and EDGES[k+1]<=hi+1]; return b[:,i].sum(1)
def otsu(v):
    h,e=np.histogram(v,128); c=(e[:-1]+e[1:])/2; w=np.cumsum(h); w2=w[-1]-w
    m=np.cumsum(h*c); mu=m/np.maximum(w,1); mu2=(m[-1]-m)/np.maximum(w2,1); return c[np.argmax(w*w2*(mu-mu2)**2)]
def runs(m):
    d=np.diff(np.r_[0,m.astype(int),0]); return list(zip(np.where(d==1)[0],np.where(d==-1)[0]))
def close(m,n):
    m=m.copy()
    for a,b in runs(~m):
        if a>0 and b<len(m) and b-a<=n: m[a:b]=True
    return m
out=[]
for n in range(1,31):
    z=np.load(f'{FD}/v{n:02d}.npz'); bm,bs=z['bm'].astype(float),z['bs'].astype(float)
    v=db(band(bm,300,3400)); vo=close(v>otsu(v),10)
    pm=np.zeros(len(v),bool)
    for a,b in runs(~vo):
        if b-a>=15 and a>0 and b<len(v): pm[a+5:b-5]=True
    r={'video':n}
    for bn,(lo,hi) in (('400-2000',(400,2000)),('full',(60,16000))):
        em=band(bm,lo,hi); es=band(bs,lo,hi); S=db(em[vo].mean())
        r[f'speech_minus_midpause_{bn}']=S-db(em[pm].mean()); r[f'speech_minus_midP10_{bn}']=S-db(np.percentile(em[pm],10))
        r[f'speech_minus_sidepause_{bn}']=S-db(es[pm].mean()); r[f'midpause_minus_sidepause_{bn}']=db(em[pm].mean())-db(es[pm].mean())
        r[f'speech_minus_sideP10_{bn}']=S-db(np.percentile(es[pm],10))
    out.append(r)
w=csv.DictWriter(open(sys.argv[2],'w'),list(out[0])); w.writeheader(); w.writerows(out)
for k in list(out[0])[1:]:
    a=np.array([r[k] for r in out]); print(k,[round(float(x),1) for x in (np.median(a),*np.percentile(a,[25,75]),a.min(),a.max())])
