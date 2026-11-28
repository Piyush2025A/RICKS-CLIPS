"""A21 3B task 3: picture-event-triggered side-broadband evidence vs shuffled controls (statistical, not per-event).
For each picture event kind: fraction of events with side broadband frac>=THR within [-3f,+10f] of event start, vs shuffled times (200 draws/video). Also recall of M1 candidates. usage: p3b_eta.py FEATDIR"""
import sys,csv,numpy as np
sys.argv_save=sys.argv; FD=sys.argv[1]; sys.argv=['x','x']
import p3b_eval as e
from p3b_util import rise_of
rng=np.random.default_rng(2)
fr={}
for v in range(1,31):
    f=(rise_of(np.load(f'{FD}/v{v:02d}.npz')['bs'].astype(float))>18).mean(1); f[:30]=0; f[-30:]=0; fr[v]=f  # strict M1: rise>18 dB in >=thr of 36 bands
def hit(v,t,thr,lo=-3,hi=10):
    a=int(round(t*100+lo/0.3)); b=int(round(t*100+hi/0.3)); a=max(a,31); b=min(b,len(fr[v])-31)
    return b>a and fr[v][a:b].max()>=thr
for thr in (0.5,0.7):
  print('THR',thr)
  kinds={}
  for v,L in e.ev.items():
    for t0,t1,k in L: kinds.setdefault(k.split('_')[0]+'_'+k.split('_')[1] if k.startswith('A15') else k,[]).append((v,t0))
  allk=[('ALL_A15',[x for k,l in kinds.items() if k.startswith('A15') for x in l]),('ALL_A12',[x for k,l in kinds.items() if k.startswith('A12') for x in l])]
  for k,l in sorted(kinds.items())+allk:
    if len(l)<8: continue
    r=np.mean([hit(v,t,thr) for v,t in l]); 
    ch=[]
    for _ in range(200): ch.append(np.mean([hit(v,rng.uniform(2,len(fr[v])/100-2),thr) for v,t in l]))
    vids=len({v for v,_ in l}); 
    print(f'{k:12s} n={len(l):3d} videos={vids:2d} hit={r:.2f} chance={np.mean(ch):.2f} 95%={np.percentile(ch,95):.2f} p_ge={np.mean(np.array(ch)>=r):.3f}')
