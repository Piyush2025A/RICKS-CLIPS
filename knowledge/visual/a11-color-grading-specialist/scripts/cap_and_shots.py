import csv,os,json,numpy as np
R=os.path.expanduser('~/ricks-clips-private/analysis-data/rc30')
T=list(csv.DictReader(open('/home/piyush/RICKS-CLIPS/knowledge/cinematography/a15-transition-specialist/data/transitions_confirmed.csv')))
grp={}
for v in [1,3,4,5,6,7,8,9,10,12,13,14,22,27]: grp[v]='lit3d'
for v in [15,16,17,18,19,20,23,24,25,29,30]: grp[v]='illustrated'
for v in [2,11,21,26,28]: grp[v]='mixed'
cap={}; out={'caption':{}, 'shots':[]}
vid_cap=[]
for n in range(1,31):
    rows=[r for r in csv.DictReader(open(f'{R}/v0.2.0/RC30-{n:02d}/color.csv')) if r['status'].startswith('ok')]
    idx=np.array([int(r['frame_index']) for r in rows])
    F={c:np.array([float(r[c]) for r in rows]) for c in ['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99','L_mean','a_mean','b_mean']}
    m=np.zeros(idx.max()+1,bool)
    for s in csv.DictReader(open(f'{R}/captions/RC30-{n:02d}/caption_segments.csv')): m[int(s['f_start']):int(s['f_end'])+1]=True
    cm=m[idx]
    d={'cap_frac':float(cm.mean())}
    for c in ['luma_p1','luma_p99']:
        d[c+'_with']=float(np.median(F[c][cm])) if cm.sum()>20 else None; d[c+'_without']=float(np.median(F[c][~cm])) if (~cm).sum()>20 else None
    out['caption'][n]=d
    # shots
    pos={int(i):k for k,i in enumerate(idx)}
    for t in T:
        if t['video']!=f'RC30-{n:02d}': continue
        a,b=int(t['cand_start']),int(t['cand_end'])
        pre=[pos[i] for i in range(max(0,a-4),a-0) if i in pos]; post=[pos[i] for i in range(b+1,b+5) if i in pos]
        if len(pre)<2 or len(post)<2: continue
        g=lambda c,s:float(np.mean(F[c][s]))
        dE=float(np.sqrt((g('L_mean',pre)-g('L_mean',post))**2+(g('a_mean',pre)-g('a_mean',post))**2+(g('b_mean',pre)-g('b_mean',post))**2))
        out['shots'].append({'video':n,'grp':grp[n],'type':t['type'],'dE76_mean':dE,'dP50':abs(g('luma_p50',pre)-g('luma_p50',post))/255,'dP1':abs(g('luma_p1',pre)-g('luma_p1',post))/255,'dP99':abs(g('luma_p99',pre)-g('luma_p99',post))/255,'len':b-a+1,
          'overshoot':float(max(0,F['luma_p50'][pre[-1]:post[0]+1].max()-max(g('luma_p50',pre),g('luma_p50',post)))) if post[0]>pre[-1] else 0})
json.dump(out,open('data/native3b_caption_shots.json','w'),indent=1)
cp=out['caption']
for c in ['luma_p1','luma_p99']:
    w=[cp[n][c+'_with']-cp[n][c+'_without'] for n in cp if cp[n][c+'_with'] is not None and cp[n][c+'_without'] is not None]
    print(c,'with-minus-without per video median',np.median(w),np.percentile(w,[25,75]),len(w))
print('cap frac median',np.median([cp[n]['cap_frac'] for n in cp]))
print('without-caption video medians p1',np.median([cp[n]['luma_p1_without'] for n in cp if cp[n]['luma_p1_without'] is not None]),'p99',np.percentile([cp[n]['luma_p99_without'] for n in cp if cp[n]['luma_p99_without'] is not None],[25,50,75]), 'p1 IQR',np.percentile([cp[n]['luma_p1_without'] for n in cp if cp[n]['luma_p1_without'] is not None],[25,75]))
S=out['shots']; print('n transitions',len(S))
from collections import defaultdict
for key in ('type','grp'):
    D=defaultdict(list)
    for s in S: D[s[key]].append(s)
    for k,v in D.items():
        print(key,k,len(v),'dE',np.percentile([s['dE76_mean'] for s in v],[25,50,75,90]).round(1),'dP50',np.percentile([s['dP50'] for s in v],[50,90]).round(3),'dP1',np.percentile([s['dP1'] for s in v],[50,90]).round(3),'dP99',np.percentile([s['dP99'] for s in v],[50,90]).round(3))
