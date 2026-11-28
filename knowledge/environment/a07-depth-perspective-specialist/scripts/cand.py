import numpy as np,csv
R='/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0'
out=[]
for k in range(1,31):
    key=f'RC30-{k:02d}'; rows=list(csv.DictReader(open(f'{R}/{key}/motion.csv')))
    f=lambda c:np.array([float(r[c]) if r[c] not in('nan','') else np.nan for r in rows])
    tx,sc,res,ni=f('tx'),f('scale'),f('res_mean_mag'),f('n_inliers')
    ok=np.array([r['confidence']=='high' for r in rows])&(ni>=40)
    tx=np.where(ok,tx,np.nan); L=10; c=[]
    for s in range(1,len(rows)-L,5):
        w=tx[s:s+L]
        if np.isnan(w).any(): continue
        ds=np.nansum(sc[s:s+L]-1)
        if abs(w.sum())>5 and abs(ds)<0.05 and (np.sign(w)==np.sign(w.sum())).mean()>0.8 and np.nanmean(res[s:s+L])<3:
            c.append((key,s,s+L,round(w.sum(),1),round(ds,3),round(np.nanmean(res[s:s+L]),2)))
    c.sort(key=lambda r:-abs(r[3])); sel=[]
    for r in c:
        if all(abs(r[1]-q[1])>40 for q in sel): sel.append(r)
        if len(sel)==3: break
    out+=sel
print(len(out),len({o[0] for o in out}))
for o in out: print(*o)
csv.writer(open('par_cand.csv','w')).writerows(out)
