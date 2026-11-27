from moves import *
import json
ev=json.load(open('/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a20-voiceover-specialist/capev.json'))
rows=json.load(open('moves_fit.json'))
rng=np.random.default_rng(0)
def lags(starts,evs,maxd=15):
    evs=np.array(evs); return np.array([ (s-evs[np.argmin(np.abs(evs-s))]) for s in starts])
out={}
for tier,sel in (('in-shot (non-fast, not near cut cand)',lambda m:not m['fast'] and not m['near_cand']),('all non-fast',lambda m:not m['fast']),('fast',lambda m:m['fast'])):
    L=[];B=[];nv=set()
    for k in keys():
        n=k.split('-')[1].lstrip('0'); 
        if n not in ev: continue
        e=ev[n]; ms=[m for m in rows if m['key']==k and sel(m)]
        if not ms: continue
        nv.add(k)
        st=np.array([m['start'] for m in ms]); en=np.array([m['end'] for m in ms]);
        L+=list(lags(st,e)); 
        nframes=len(csv_len) if False else int(max(e))+30
        for _ in range(200):
            rs=rng.integers(5,nframes,len(st)); B+=list(lags(rs,e))
    L=np.array(L);B=np.array(B)
    f=lambda x,w:float((np.abs(x)<=w).mean())
    out[tier]=dict(n=len(L),videos=len(nv),within3=f(L,3),base3=f(B,3),within6=f(L,6),base6=f(B,6),med_lag=float(np.median(L)),med_abs=float(np.median(np.abs(L))),base_med_abs=float(np.median(np.abs(B))))
    print(tier,out[tier])
# move vs shot boundary candidates (start-to-nearest-candidate start / end)
for tier,sel in (('non-fast',lambda m:not m['fast']),('fast',lambda m:m['fast'])):
    L=[];Bs=[]
    for k in keys():
        c=json.load(open(f'{R}/{k}/shot_candidates.json'))['candidates']; ends=np.array([x['end'] for x in c]); 
        ms=[m for m in rows if m['key']==k and sel(m)]
        for m in ms: L.append(m['start']-ends[np.argmin(np.abs(ends-m['start']))])
        for _ in range(len(ms)*20): Bs.append(rng.integers(5,1800)-ends[np.argmin(np.abs(ends-rng.integers(5,1800)))])
    L=np.array(L); print(tier,'move start - nearest cand end: n',len(L),'within 6f',(np.abs(L)<=6).mean().round(2),'within 15',(np.abs(L)<=15).mean().round(2),'median',np.median(L))
json.dump(out,open('sync_summary.json','w'))
