from common import *
from scipy.ndimage import uniform_filter1d
from scipy.optimize import curve_fit
import json, sys
FPS=30
def runs(ok,minlen):
    out=[];i=0;n=len(ok)
    while i<n:
        if not ok[i]: i+=1; continue
        j=i
        while j<n and ok[j]: j+=1
        if j-i>=minlen: out.append((i,j))
        i=j
    return out
PEAK_Z=0.6; PEAK_T=1.2   # %/frame zoom, %W/frame translation: min peak to count as a "move"
HOLD_Z=0.10; HOLD_T=0.20
def analyse(k):
    d,bad,cands,fid=load(k); n=len(d)
    ok=~bad
    sm=np.full_like(d,np.nan)
    moves=[]; labels=np.full(n,'x',dtype='<U6')
    for (a,b) in runs(ok,12):
        s=uniform_filter1d(d[a:b],3,axis=0,mode='nearest')   # light 3-frame smoothing
        sm[a:b]=s
        z=s[:,2]; tx=s[:,0]; ty=s[:,1]; rot=s[:,3]
        spd=np.hypot(tx,ty)
        # per-frame class
        for i in range(b-a):
            zz=abs(z[i]); tt=spd[i]
            if zz<HOLD_Z and tt<HOLD_T and abs(rot[i])<0.05: labels[a+i]='hold'
            elif zz<PEAK_Z*0.5 and tt<PEAK_T*0.5 and abs(rot[i])<0.15: labels[a+i]='creep'
            else: labels[a+i]='move'
        # move detection by peaks of normalised intensity
        inten=np.maximum.reduce([np.abs(z)/PEAK_Z, spd/PEAK_T, np.abs(rot)/0.3])
        m=inten>=0.5
        for (i,j) in runs(m,4):
            # extend while > 0.15 peak
            pk=inten[i:j].max()
            lo=i
            while lo>0 and inten[lo-1]>0.15*pk and inten[lo-1]<inten[lo]*1.5+0.2: lo-=1
            hi=j
            while hi<len(inten) and inten[hi]>0.15*pk: hi+=1
            if pk<1.0: continue
            seg=s[lo:hi]
            Z=seg[:,2].sum(); X=seg[:,0].sum(); Y=seg[:,1].sum(); Rr=seg[:,3].sum()
            # component dominance (normalised by thresholds)
            cz=abs(seg[:,2]).max()/PEAK_Z; ct=np.hypot(seg[:,0],seg[:,1]).max()/PEAK_T; cr=abs(seg[:,3]).max()/0.3
            kinds=[]
            if cz>=1: kinds.append('push' if Z>0 else 'pull')
            if ct>=1: kinds.append(('pan' if abs(X)>=abs(Y) else 'tilt')+('+' if (X if abs(X)>=abs(Y) else Y)>0 else '-'))
            if cr>=1: kinds.append('roll')
            kind='+'.join(kinds) if kinds else 'minor'
            moves.append(dict(key=k,start=a+lo,end=a+hi,dur=hi-lo,kind=kind,Z=Z,X=X,Y=Y,R=Rr,
               pkz=float(np.abs(seg[:,2]).max()),pkt=float(np.hypot(seg[:,0],seg[:,1]).max()),pkr=float(np.abs(seg[:,3]).max())))
    return d,sm,bad,labels,cands,moves
if __name__=='__main__':
    allm=[]; summ=[]
    for k in keys():
        d,sm,bad,labels,cands,moves=analyse(k)
        n=len(d); valid=(labels!='x').sum()
        sh={c:float((labels==c).sum()/valid) for c in ('hold','creep','move')}
        allm+=moves
        summ.append(dict(key=k,frames=n,valid=int(valid),hold=sh['hold'],creep=sh['creep'],move=sh['move'],n_moves=len(moves),
              moves_per_min=len(moves)/(valid/FPS/60)))
        print(k,'valid',valid,{a:round(b,2) for a,b in sh.items()},'moves',len(moves),'/min %.1f'%summ[-1]['moves_per_min'])
    json.dump(allm,open('moves_all.json','w')); json.dump(summ,open('summary.json','w'))
    import collections
    c=collections.Counter(m['kind'] for m in allm); print(c.most_common(20))
    for kind in ('push','pull'):
        dd=[m['dur'] for m in allm if m['kind']==kind]; zz=[abs(m['Z']) for m in allm if m['kind']==kind]
        if dd: print(kind,len(dd),'dur med/IQR',np.percentile(dd,[25,50,75]),'total scale% ',np.percentile(zz,[25,50,75]).round(1))
