import json,csv,os,numpy as np
def mannwhitneyu(a,b,N=20000):
    rng=np.random.default_rng(0); a=np.array(a);b=np.array(b); obs=abs(np.median(a)-np.median(b)); z=np.concatenate([a,b]); c=0
    for _ in range(N):
        rng.shuffle(z); c+=abs(np.median(z[:len(a)])-np.median(z[len(a):]))>=obs
    class R: pass
    r=R(); r.pvalue=(c+1)/(N+1); return r
R=os.path.expanduser('~/ricks-clips-private/analysis-data/rc30/v0.2.0')
d=json.load(open('data/native3b_black_white_groups.json'))
cols=['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99','sat_mean','chroma_frac','a_mean','b_mean','L_std']
vm={}
for n in range(1,31):
    rows=[r for r in csv.DictReader(open(f'{R}/RC30-{n:02d}/color.csv')) if r['status'].startswith('ok')]
    vm[n]={c:float(np.nanmedian([float(r[c]) for r in rows if r[c] not in('','nan')])) for c in cols}
    vm[n]['contrast']=vm[n]['luma_p95']-vm[n]['luma_p5']
    # warm share hue01+hue02 vs blue hue07+hue08
    for k in ('hue01','hue07'): vm[n][k]=float(np.nanmean([float(r[k]) for r in rows]))
L=[v for v in d['per_group']['lit3d']['videos']]; I=d['per_group']['illustrated']['videos']; M=d['per_group']['mixed']['videos']
lowkey=[1,7,8,27]
print('test lit3d(n=%d) vs illustrated(n=%d), video medians, permutation test on difference of medians'%(len(L),len(I)))
res={}
for c in cols+['contrast','hue01','hue07']:
    a=[vm[v][c] for v in L]; b=[vm[v][c] for v in I]; a2=[vm[v][c] for v in L if v not in lowkey]
    p=mannwhitneyu(a,b).pvalue; p2=mannwhitneyu(a2,b).pvalue
    res[c]={'lit_med':np.median(a),'ill_med':np.median(b),'p':p,'lit_no_lowkey_med':np.median(a2),'p_no_lowkey':p2}
    print(c,{k:round(float(v),3) for k,v in res[c].items()})
json.dump({k:{a:float(b) for a,b in v.items()} for k,v in res.items()},open('data/native3b_group_tests.json','w'),indent=1)
