# lip-sync test: local-change frames (mouth/face) vs caption onsets. Permutation test with circular shifts of the onsets.
import json,csv,os,numpy as np,sys
P=os.path.expanduser('~/ricks-clips-private/analysis-data/rc30')
D=P+'/agents/a02-facial-expression-specialist/3b'
shots=[(2,743,763),(6,1062,1078),(27,283,310),(27,446,474),(3,761,775),(3,322,341),(12,356,370),(14,1390,1407),(9,381,399),(9,16,36),(5,1074,1093),(15,1333,1353)]
rng=np.random.default_rng(1);out=[]
allobs=[];allnull=[]
for n,a,b in shots:
    ev=json.load(open(f'{D}/ev_{n:02d}.json'))['ev']
    pk=[c for c in json.load(open(f'{D}/pick_{n:02d}.json'))]
    c=[c for c in pk if c[0][0]-4<=a+8 and c[-1][0]+4>=a]
    if not c: print(n,a,'no cluster');continue
    cx,cy=np.mean([e[1] for e in c[0]]),np.mean([e[2] for e in c[0]])
    fr=sorted({e[0] for e in ev if a<=e[0]<=b and abs(e[1]-cx)<70 and abs(e[2]-cy)<70})
    segs=list(csv.DictReader(open(f'{P}/captions/RC30-{n:02d}/caption_segments.csv')))
    ons=np.array([int(s['f_start']) for s in segs])
    on=ons[(ons>=a-2)&(ons<=b+2)]
    if len(fr)<3: print(n,a,'few',fr);continue
    def stat(on_):
        return np.mean([np.min(np.abs(on_-f))<=2 if len(on_) else False for f in fr])
    obs=stat(on)
    # null: place same number of onsets (positions of caption onsets) randomly within window
    nul=[stat(rng.integers(a,b+1,len(on))) for _ in range(2000)] if len(on) else []
    out.append((n,a,b,len(fr),len(on),round(obs,2),round(float(np.mean(nul)),2) if nul else None,round(float(np.mean(np.array(nul)>=obs)),2) if nul else None))
    print(out[-1])
json.dump(out,open(f'{D}/sync_out.json','w'))
