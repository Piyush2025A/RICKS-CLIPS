import numpy as np
from p3b_feat import EDGES
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
def rollmed_past(E,lo=100,hi=20):
    """per-band median over frames [t-lo, t-hi] (10 ms frames); E (T,B)"""
    T=E.shape[0]; out=np.zeros_like(E)
    for t in range(T):
        a=max(0,t-lo); b=max(a+1,t-hi); out[t]=np.median(E[a:b],axis=0)
    return out
def peaks(x,thr,refr):
    idx=[]; 
    for t in np.where(x>=thr)[0]:
        if idx and t-idx[-1]<=refr:
            if x[t]>x[idx[-1]]: idx[-1]=t
        else: idx.append(t)
    return idx
def rise_of(bs):
    """side bands 0-35 (<~3.9 kHz) rise vs rolling-median bed (dB)"""
    Es=np.maximum(db(bs)[:,:36],-100); sm=np.array([np.convolve(Es[:,k],np.ones(3)/3,'same') for k in range(36)]).T
    bed=rollmed_past(sm); fmax=np.maximum.reduce([np.roll(sm,-s,axis=0) for s in (0,1,2,3,4)]); return fmax-bed
