"""A21 3B: M1 threshold grid (side channel bands 0-35, bed = rolling median 1.0..0.2 s). precision vs picture labels (window W=4 f), lift vs shuffle, synthetic-burst recall. usage: p3b_grid.py FEATDIR"""
import sys,csv,numpy as np
from p3b_util import *
FD=sys.argv[1]; sys.argv=['x','x']; import p3b_eval as e
def rise_of(bs):
    Es=np.maximum(db(bs)[:,:36],-100); sm=np.array([np.convolve(Es[:,k],np.ones(3)/3,'same') for k in range(36)]).T
    bed=rollmed_past(sm); fmax=np.maximum.reduce([np.roll(sm,-s,axis=0) for s in (0,1,2,3,4)]); return fmax-bed
R={};D={}
for v in range(1,31):
    z=np.load(f'{FD}/v{v:02d}.npz'); bs=z['bs'].astype(float); R[v]=rise_of(bs); D[v]=float(z['dur'])
rng=np.random.default_rng(5)
# synthetic burst set: 12 videos x 6
inj={}
for v in range(1,31,2):
    bs=np.load(f'{FD}/v{v:02d}.npz')['bs'].astype(float); ts=rng.integers(200,len(bs)-200,6); inj[v]=(ts,bs)
rr={X:{} for X in (6,12,18)}
for X in rr:
    for v,(ts,bs) in inj.items():
        b2=bs.copy()
        for t in ts: b2[t:t+8,:36]*=10**(X/10)
        rr[X][v]=rise_of(b2)
out=[]
print('rise_db frac | n_events videos precision chance lift | synth recall +6/+12/+18 dB | events/min')
for rdb in (10,14,18,24):
  for fr in (0.3,0.5,0.7):
    c=[]
    for v in R:
        f=(R[v]>rdb).mean(1); f[:30]=0; f[-30:]=0
        c+= [(v,t/100) for t in peaks(f,fr,25)]
    if len(c)<5: print(rdb,fr,'n',len(c)); continue
    p=e.prec(c); sh=[e.prec([(v,(t+rng.uniform(5,D[v]-5))%D[v]) for v,t in c]) for _ in range(100)]
    rec=[]
    for X in rr:
        d=0;n=0
        for v,(ts,bs) in inj.items():
            f=(rr[X][v]>rdb).mean(1); f[:30]=0; f[-30:]=0
            for t in ts: d+= f[t-5:t+10].max()>=fr; n+=1
        rec.append(d/n)
    line=f'{rdb} {fr} | n={len(c)} v={len({v for v,_ in c})} P={p:.2f} ch={np.mean(sh):.2f} lift={p/np.mean(sh):.2f} | '+'/'.join('%.2f'%x for x in rec)+f' | {len(c)/sum(D.values())*60:.2f}'
    print(line); out.append((rdb,fr,len(c),p,np.mean(sh),*rec))
