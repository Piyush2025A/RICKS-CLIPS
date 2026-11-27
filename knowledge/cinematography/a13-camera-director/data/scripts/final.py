from moves import *
import json, collections, csv as C
rows=json.load(open('moves_fit.json')); rng=np.random.default_rng(1)
K=keys(); out={}
# cut-sync baseline
for tier,sel in (('non-fast',lambda m:not m['fast']),('fast',lambda m:m['fast'])):
    L=[];B=[]
    for k in K:
        c=json.load(open(f'{R}/{k}/shot_candidates.json'))['candidates']; ends=np.array([x['end'] for x in c]); nfr=len(load(k)[0])
        ms=[m for m in rows if m['key']==k and sel(m)]
        for m in ms: L.append(m['start']-ends[np.argmin(np.abs(ends-m['start']))])
        for _ in range(len(ms)*50):
            r=rng.integers(5,nfr); B.append(r-ends[np.argmin(np.abs(ends-r))])
    L=np.array(L);B=np.array(B)
    out[tier]=dict(n=len(L),w6=float((abs(L)<=6).mean()),b6=float((abs(B)<=6).mean()),w15=float((abs(L)<=15).mean()),b15=float((abs(B)<=15).mean()))
    print('cut-sync',tier,out[tier])
# per video table
tab=[]
summ={s['key']:s for s in json.load(open('summary.json'))}
for k in K:
    ms=[m for m in rows if m['key']==k]; nf=[m for m in ms if not m['fast']]
    kinds=collections.Counter()
    for m in nf:
        kk=m['kind'].replace('+roll','')
        pri='push' if kk.startswith('push') else 'pull' if kk.startswith('pull') else 'pan/tilt' if kk.startswith(('pan','tilt')) else 'roll' if kk=='roll' else 'other'
        kinds[pri]+=1
    tab.append([k,summ[k]['frames'],summ[k]['valid'],round(summ[k]['hold'],3),round(summ[k]['creep'],3),round(summ[k]['move'],3),len(ms),len(nf),len(ms)-len(nf),kinds['push'],kinds['pull'],kinds['pan/tilt'],kinds['roll']+kinds['other'],
        round(float(np.median([m['dur'] for m in nf])) if nf else 0,1)])
with open('/home/piyush/RICKS-CLIPS/knowledge/cinematography/a13-camera-director/data/camera_per_video.csv','w') as f:
    w=C.writer(f); w.writerow(['key','frames','valid_frames','hold_share','creep_share','move_share','n_moves','n_nonfast','n_fast','nf_push','nf_pull','nf_pantilt','nf_other','nf_median_dur_f']); w.writerows(tab)
# magnitudes by kind for non-fast
for kind in ('push','pull'):
    sub=[m for m in rows if not m['fast'] and m['kind'].replace('+roll','').startswith(kind)]
    z=[abs(m['Z']) for m in sub]; d=[m['dur'] for m in sub]; pk=[m['pkz'] for m in sub]
    print(kind,len(sub),'videos',len(set(m['key'] for m in sub)),'|Z|%',np.percentile(z,[25,50,75]).round(1),'dur',np.percentile(d,[25,50,75]),'peak %/f',np.percentile(pk,[25,50,75]).round(2),'rate %/f mean',np.percentile([a/b for a,b in zip(z,d)],[25,50,75]).round(2))
sub=[m for m in rows if not m['fast'] and m['kind'].replace('+roll','').startswith(('pan','tilt')) or (not m['fast'] and 'pan' in m['kind'])]
t=[np.hypot(m['X'],m['Y']) for m in sub]; print('translation total %W',np.percentile(t,[25,50,75]).round(1),len(sub))
print('roll peak deg/f (non-fast with roll)',np.percentile([m['pkr'] for m in rows if not m['fast']],[50,90,99]).round(3),'cum roll deg',np.percentile([abs(m['R']) for m in rows if not m['fast']],[50,90,99]).round(1))
print('roll-only/flagged',sum('roll' in m['kind'] for m in rows if not m['fast']),'of',sum(1 for m in rows if not m['fast']))
# push vs pull ratio and taxonomy shares non-fast
c=collections.Counter(); 
for m in rows:
    if m['fast']: continue
    kk=m['kind'].replace('+roll','').rstrip('+-')
    c[kk]+=1
print(c.most_common())
# hold/creep/move overall
s=np.array([[summ[k]['hold'],summ[k]['creep'],summ[k]['move']] for k in K]); print('hold/creep/move median',np.median(s,0).round(3),'IQR',np.percentile(s,[25,75],axis=0).round(3))
# fast moves detail: signature candidates: total scale factor
sig=[]
for m in rows:
    f=np.exp(m['Z']/100) if abs(m['Z'])<200 else None
    sig.append(m)
big=[m for m in rows if abs(m['Z'])>=40 or np.hypot(m['X'],m['Y'])>=100]
print('big moves',len(big))
json.dump(big,open('big_moves.json','w'))
json.dump(out,open('cutsync.json','w'))
