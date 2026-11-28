"""A21 3B task 2: picture-sync labelling + precision/lift vs shuffle. usage: p3b_eval.py CANDS.csv [window_frames]"""
import sys,csv,numpy as np
R='/home/piyush/RICKS-CLIPS/knowledge/'
W=int(sys.argv[2]) if len(sys.argv)>2 else 4
ev={}  # video -> list of (t0,t1,kind)
def add(v,f0,f1,k): ev.setdefault(int(v[-2:]),[]).append(((f0+1)/30,(f1+1)/30,k))
for r in csv.DictReader(open(R+'cinematography/a15-transition-specialist/data/transitions_confirmed.csv')): add(r['video'],int(r['cand_start']),int(r['cand_end']),'A15_'+r['type'])
for r in csv.DictReader(open(R+'visual/a12-vfx-specialist/data/luma_bumps_3B.csv')): add(r['video'],int(r['start']),int(r['end']),'A12_bump')
for r in csv.DictReader(open(R+'visual/a12-vfx-specialist/data/flash_candidates_luma_3B.csv')): add(r['video'],int(r['start']),int(r['end']),'A12_flash')
def label(v,t):
    best=None
    for t0,t1,k in ev.get(v,[]):
        lo,hi=t0-W/30,t1+W/30
        if lo<=t<=hi:
            off=(t-t0)*30 if t<t0+ (t1-t0)/2 else (t-t1)*30
            if best is None or abs(off)<abs(best[0]): best=(off,k)
    return best
def prec(c):
    return np.mean([label(v,t) is not None for v,t in c]) if c else float('nan')
if __name__=='__main__':
    rows=list(csv.DictReader(open(sys.argv[1]))); rng=np.random.default_rng(1)
    dur={v:np.load(f'/tmp/claude-1000/-home-piyush-RICKS-CLIPS/092e9044-5d47-45d7-9b9b-c40b677c0730/scratchpad/feat/v{v:02d}.npz')['dur'] for v in range(1,31)}
    for m in sorted({r['method'] for r in rows}):
        for tier,flt in (('all',lambda r:True),)+tuple((f'strength>={q}',(lambda q:lambda r:float(r['strength'])>=q)(q)) for q in ((0.1,0.15,0.2,0.25,0.4) if m=="M1" else (10,14,18) if m=='M3' else (12,20,30))):
            c=[(int(r['video']),float(r['t'])) for r in rows if r['method']==m and flt(r)]
            if len(c)<5: continue
            p=prec(c); sh=[prec([(v,(t+rng.uniform(5,dur[v]-5))%dur[v]) for v,t in c]) for _ in range(200)]
            print(m,tier,'n',len(c),'videos',len({v for v,_ in c}),'precision %.2f'%p,'chance %.2f (95%% %.2f)'%(np.mean(sh),np.percentile(sh,95)),'lift %.2f'%(p/np.mean(sh)))
