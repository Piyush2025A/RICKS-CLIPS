"""A21 3B: ending side-channel swell census. Level of side 60-1000 Hz (dB re mean-power) in 0.5 s windows: max over the last 4 s (ending at dur-0.3) minus median of the body (2..dur-5 s). Control: same statistic on random 4 s windows of the body (200 draws, per video). usage: p3b_end.py FEATDIR OUT.csv"""
import sys,csv,numpy as np
from p3b_util import *
FD=sys.argv[1]; rng=np.random.default_rng(7); rows=[]
for v in range(1,31):
    z=np.load(f'{FD}/v{v:02d}.npz'); s=band(z['bs'].astype(float),60,1000); T=len(s)
    w=50; e=db(np.convolve(s,np.ones(w)/w,'valid'))  # 0.5 s windows
    body=e[200:T-500-w]; med=np.median(body)
    last=e[T-30-400:T-30-w]; stat=last.max()-med
    ctl=[]
    for _ in range(200):
        a=rng.integers(200,T-500-w-400); ctl.append(e[a:a+400-w].max()-med)
    rows.append(dict(video=v,end_rise_db=stat,ctl_median=np.median(ctl),ctl_p95=np.percentile(ctl,95),t_peak=(T-30-400+int(np.argmax(last)))/100))
w=csv.DictWriter(open(sys.argv[2],'w'),list(rows[0])); w.writeheader(); w.writerows(rows)
a=np.array([r['end_rise_db'] for r in rows]); ex=sum(r['end_rise_db']>r['ctl_p95'] for r in rows)
print('end rise median %.1f IQR %.1f-%.1f; > control p95 in %d/30; >=6 dB in %d/30; >=10 dB in %d'%(np.median(a),*np.percentile(a,[25,75]),ex,(a>=6).sum(),(a>=10).sum()))
print([ (r['video'],round(r['end_rise_db'],1),round(r['t_peak'],1)) for r in rows if r['end_rise_db']>r['ctl_p95']])
