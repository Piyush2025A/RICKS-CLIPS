from moves import *
import collections
def models():
    M={'linear':lambda t:np.ones_like(t),
       'sine_inout':lambda t:np.pi/2*np.sin(np.pi*t),
       'smoothstep':lambda t:6*t*(1-t),
       'smootherstep':lambda t:30*t**2*(1-t)**2,
       'easeout_quad':lambda t:2*(1-t),
       'easeout_cubic':lambda t:3*(1-t)**2,
       'easein_quad':lambda t:2*t,
       'easein_cubic':lambda t:3*t**2}
    return M
def cum(f,tt):
    # numerically integrate density f on grid tt -> cumulative normalised
    c=np.cumsum(f(tt)); return c/c[-1]
def fit_move(p):
    n=len(p); tau=(np.arange(n)+0.5)/n
    p=np.maximum(p,0); 
    if p.sum()<=0: return None
    C=np.cumsum(p)/p.sum()
    res={}
    fine=np.linspace(0,1,2001)[1:]
    for nm,f in models().items():
        Cm=np.cumsum(f(fine)); Cm/=Cm[-1]
        pred=np.interp(np.arange(1,n+1)/n,fine,Cm)
        res[nm]=float(np.sqrt(np.mean((pred-C)**2)))
    # exp ease-out family and beta
    best=(9,None)
    for lam in (1,2,3,4,6,8):
        f=lambda t:np.exp(-lam*t); Cm=np.cumsum(f(fine)); Cm/=Cm[-1]
        pred=np.interp(np.arange(1,n+1)/n,fine,Cm); r=float(np.sqrt(np.mean((pred-C)**2)))
        if r<best[0]: best=(r,lam)
    res['exp_out']=best[0]
    bb=(9,None)
    for a in np.arange(0,4.01,0.25):
        for b in np.arange(0,4.01,0.25):
            f=fine**a*(1-fine)**b; Cm=np.cumsum(f); Cm/=Cm[-1]
            pred=np.interp(np.arange(1,n+1)/n,fine,Cm); r=float(np.sqrt(np.mean((pred-C)**2)))
            if r<bb[0]: bb=(r,(a,b))
    res['beta']=bb[0]
    return res,best[1],bb[1]
if __name__=='__main__':
    rows=[]
    for k in keys():
        d,sm,bad,labels,cands,moves=analyse(k)
        bnd=[(c['start'],c['end']) for c in cands]
        for m in moves:
            lo,hi=m['start'],m['end']; s=sm[lo:hi]
            inten=np.maximum.reduce([np.abs(s[:,2])/PEAK_Z,np.hypot(s[:,0],s[:,1])/PEAK_T,np.abs(s[:,3])/0.3])
            m['fast']=bool(m['pkz']>=3 or m['pkt']>=6)
            m['near_cand']=bool(any(lo-15<=e and hi+15>=st for st,e in bnd))
            m['peak_frac']=float((np.argmax(inten)+0.5)/len(inten))
            pk=inten.max(); idx=np.where(inten>=0.1*pk)[0]; i90=np.where(inten>=0.9*pk)[0]
            m['attack']=int(i90[0]-idx[0]); m['release']=int(idx[-1]-i90[-1])
            m['pk_inten']=float(pk)
            if m['dur']>=8:
                out=fit_move(inten)
                if out:
                    r,lam,ab=out; m['fit']=r; m['best']=min((v,kk) for kk,v in r.items() if kk not in('beta','exp_out'))[1]; m['lam']=lam; m['ab']=ab
            rows.append(m)
    json.dump(rows,open('moves_fit.json','w'))
    print(len(rows),'moves; fast',sum(m['fast'] for m in rows),'near_cand',sum(m['near_cand'] for m in rows))
    for nm,sel in (('in-shot',lambda m:not m['fast'] and not m['near_cand']),('boundary-adjacent',lambda m:m['near_cand'] and not m['fast']),('fast',lambda m:m['fast'])):
        sub=[m for m in rows if sel(m)]
        fit=[m for m in sub if 'best' in m]
        print('\n==',nm,len(sub),'videos',len(set(m['key'] for m in sub)),'dur pct25/50/75',np.percentile([m['dur'] for m in sub],[25,50,75]))
        print(' kinds',collections.Counter(m['kind'].replace('+roll','') for m in sub).most_common(8))
        print(' fit n',len(fit),collections.Counter(m['best'] for m in fit).most_common())
        if fit:
            print(' peak_frac pct',np.percentile([m['peak_frac'] for m in fit],[25,50,75]).round(2),'attack',np.percentile([m['attack'] for m in fit],[25,50,75]),'release',np.percentile([m['release'] for m in fit],[25,50,75]))
            ab=np.array([m['ab'] for m in fit]); print(' beta a,b median',np.median(ab,0),'a<b frac',(ab[:,0]<ab[:,1]).mean().round(2),'a>b',(ab[:,0]>ab[:,1]).mean().round(2))
            print(' median rmse by model',{kk:round(float(np.median([m['fit'][kk] for m in fit])),3) for kk in fit[0]['fit']})
