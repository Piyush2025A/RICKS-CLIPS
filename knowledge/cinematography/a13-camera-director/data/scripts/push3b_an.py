"""Analyse push3b.json: bias, easing fits. Run with .venv-analysis python."""
import json,csv,numpy as np
from scipy.optimize import least_squares
OUT='/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a13-camera-director/push3b'
R='/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0'
res=json.load(open(OUT+'/push3b.json'))
rows=[]
for r in res:
    mo=list(csv.DictReader(open(f"{R}/{r['key']}/motion.csv")))
    sc=np.array([float(x['scale']) for x in mo])
    seg=sc[r['start']:r['end']+1]; seg=np.nan_to_num(seg,nan=1.0)
    r['proxy_comp']=(np.prod(seg)-1)*100; r['proxy_sum']=float(np.sum((seg-1)*100))
    r['chain_pct']=(r['S_chain']-1)*100
    r['direct_pct']=(r['S_direct']-1)*100 if r['S_direct'] and r['S_direct']>0.5 else None
    # easing on native chained cumulative log-scale
    cum=np.load(f"{OUT}/{r['key']}_{r['start']}_{r['end']}_cum.npy")
    y=np.log(cum); y=(y-y[0])/(y[-1]-y[0]) if y[-1]!=y[0] else y
    t=np.linspace(0,1,len(y))
    fits={'smoothstep':3*t**2-2*t**3,'linear':t,'easeout_quad':1-(1-t)**2,'easeout_cubic':1-(1-t)**3,'easein_quad':t**2,'smootherstep':6*t**5-15*t**4+10*t**3}
    rm={k:float(np.sqrt(np.mean((v-y)**2))) for k,v in fits.items()}
    r['ease_rmse']=rm; r['ease_best']=min(rm,key=rm.get)
    # peak time of per-frame speed (smoothed)
    sp=np.diff(np.log(cum)); k=np.ones(5)/5; sps=np.convolve(sp,k,'same'); r['peak_t']=float(np.argmax(sps)/len(sps))
    r['attack_ratio']=float(sps[:len(sps)//4].mean()/max(sps.mean(),1e-9))
    rows.append(r)
json.dump(rows,open(OUT+'/push3b_an.json','w'),indent=1)
def q(x): x=np.array(x,float); return f"{np.median(x):.1f} (IQR {np.percentile(x,25):.1f}-{np.percentile(x,75):.1f}) n={len(x)}"
ok=[r for r in rows if r['direct_pct'] is not None]
print('moves',len(rows),'videos',len({r['key'] for r in rows}),'direct ok',len(ok),'videos',len({r['key'] for r in ok}))
for r in rows: print(r['key'],r['start'],r['end'],'sum %.1f comp %.1f chain %.1f direct %s inl %s best %s pk %.2f'%(r['proxy_sum'],r['proxy_comp'],r['chain_pct'],None if r['direct_pct'] is None else round(r['direct_pct'],1),r['inl'],r['ease_best'],r['peak_t']))
print('direct',q([r['direct_pct'] for r in ok])); print('proxy sum (same moves)',q([r['proxy_sum'] for r in ok])); print('proxy comp',q([r['proxy_comp'] for r in ok])); print('chain',q([r['chain_pct'] for r in ok])); print('chain all',q([r['chain_pct'] for r in rows]))
for a,b in (('direct_pct','proxy_sum'),('direct_pct','proxy_comp'),('chain_pct','proxy_comp'),('direct_pct','chain_pct')):
    ra=np.array([r[a]/r[b] for r in ok if abs(r[b])>3]); print(a,'/',b,'ratio',q(ra*1)) 
# log-scale ratios
lr=np.array([np.log(1+r['direct_pct']/100)/np.log(1+r['proxy_comp']/100) for r in ok if r['proxy_comp']>3]); print('log ratio direct/proxy_comp',q(lr))
from collections import Counter
e=[r for r in rows if abs(r['chain_pct'])>15 and r['dur']>=20]; print('ease n',len(e),Counter(r['ease_best'] for r in e),'peak_t',q([r['peak_t'] for r in e]))
print('rmse medians',{k:round(float(np.median([r['ease_rmse'][k] for r in e])),3) for k in e[0]['ease_rmse']})
