#!/usr/bin/env python3
"""A11 3B: black/white points + per-treatment grade from A27 native color.csv (all frames, 30 videos).
Luma = cv2 BGR2GRAY (BT.601 weights) on swscale-decoded bgr24 = limited->full expanded 8-bit (probe: color_range tv, bt709).
Values /255 = normalised full range; limited-range code = 16+219*v. Run: python3 native3b.py"""
import csv, json, glob, os, numpy as np
R=os.path.expanduser('~/ricks-clips-private/analysis-data/rc30/v0.2.0')
LIT=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,22,27]; ILL=[15,16,17,18,19,20,23,24,25,29,30]; MIX=[2,11,21,26,28]
LIT=[v for v in LIT if v not in MIX]; 
grp={}
for v in LIT: grp[v]='lit3d'
for v in ILL: grp[v]='illustrated'
for v in MIX: grp[v]='mixed'
cols=['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99','luma_mean','L_mean','a_mean','b_mean','sat_mean','chroma_frac']+[f'hue{k:02d}' for k in range(12)]
out={'per_video':{}, 'per_group':{}, 'per_toneclass':{}}
allrows={}
def q(x,p): return [float(np.percentile(x,k)) for k in p]
for n in range(1,31):
    rows=list(csv.DictReader(open(f'{R}/RC30-{n:02d}/color.csv')))
    ok=[r for r in rows if r['status'].startswith('ok')]
    A={c:np.array([float(r[c]) if r[c] not in('','nan') else np.nan for r in ok]) for c in cols}
    A['n_all']=len(rows)
    allrows[n]=A
    d={'n_frames':len(rows),'n_ok':len(ok),'group':grp[n]}
    for c in ['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99']:
        d[c+'_med_of_frames']=float(np.nanmedian(A[c])); d[c+'_iqr']=q(A[c][~np.isnan(A[c])],[25,75])
    d['frac_frames_p1_le2']=float(np.mean(A['luma_p1']<=2)); d['frac_frames_p1_le4']=float(np.mean(A['luma_p1']<=4)); d['frac_p99_ge254']=float(np.mean(A['luma_p99']>=254))
    out['per_video'][n]=d
# per group pooled frames
def pool(vs,c): return np.concatenate([allrows[v][c] for v in vs])
G={'lit3d':LIT,'illustrated':ILL,'mixed':MIX}
for g,vs in G.items():
    o={'videos':vs,'n_frames':int(sum(len(allrows[v]['luma_p1']) for v in vs))}
    for c in ['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99','luma_std' if False else 'luma_mean','L_mean','sat_mean','chroma_frac','a_mean','b_mean']:
        x=pool(vs,c); x=x[~np.isnan(x)]; o[c]={'p25_p50_p75':q(x,[25,50,75])}
        # per-video medians
        pm=[float(np.nanmedian(allrows[v][c])) for v in vs]; o[c]['video_median_of_medians']=float(np.median(pm)); o[c]['video_med_iqr']=q(pm,[25,75]); o[c]['video_med_range']=[min(pm),max(pm)]
    o['contrast_p95_p5']=q(pool(vs,'luma_p95')-pool(vs,'luma_p5'),[25,50,75])
    hh=np.array([np.nanmean(pool(vs,f'hue{k:02d}')) for k in range(12)]); o['hue_hist_12bin_HSV30deg_mean']=(hh/hh.sum()).tolist()
    o['frac_frames_p1_le2']=float(np.mean(pool(vs,'luma_p1')<=2)); o['frac_p99_ge254']=float(np.mean(pool(vs,'luma_p99')>=254))
    out['per_group'][g]=o
# overall
vs=list(range(1,31)); o={}
for c in ['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99']:
    x=pool(vs,c); pm=[float(np.nanmedian(allrows[v][c])) for v in vs]
    o[c]={'pooled_frame_p25_50_75':q(x,[25,50,75]),'video_med':float(np.median(pm)),'video_iqr':q(pm,[25,75]),'video_range':[min(pm),max(pm)]}
out['all30']=o
# tone class by frame p50: dark<64, mid 64-140, bright>140 (8-bit)
for g,vs in list(G.items())+[('all',list(range(1,31)))]:
    p50=pool(vs,'luma_p50'); res={}
    for name,m in [('dark_p50<64',p50<64),('mid_64-140',(p50>=64)&(p50<140)),('bright_p50>=140',p50>=140)]:
        r={'n':int(m.sum())}
        for c in ['luma_p1','luma_p5','luma_p95','luma_p99']:
            x=pool(vs,c)[m]; r[c]=q(x,[25,50,75])
        r['frac_p1_le2']=float(np.mean(pool(vs,'luma_p1')[m]<=2))
        res[name]=r
    out['per_toneclass'][g]=res
json.dump(out,open('data/native3b_black_white_groups.json','w'),indent=1)
# print summary
print('ALL30',json.dumps({k:(round(v['video_med']),[round(i) for i in v['video_iqr']],[round(i) for i in v['video_range']]) for k,v in o.items()}))
for n in range(1,31):
    d=out['per_video'][n]; print(n,d['group'][:3],*[round(d[c+'_med_of_frames']) for c in ['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99']],round(d['frac_frames_p1_le2'],2),round(d['frac_p99_ge254'],2))
for g,o in out['per_group'].items():
    print(g,o['videos'],o['n_frames'])
    for c in ['luma_p1','luma_p5','luma_p50','luma_p95','luma_p99','sat_mean','chroma_frac','a_mean','b_mean']:
        print('  ',c,[round(i,3) for i in o[c]['p25_p50_p75']],'vid-med',round(o[c]['video_median_of_medians'],3),[round(i,3) for i in o[c]['video_med_iqr']])
    print('  contrast',[round(i) for i in o['contrast_p95_p5']],'hue',[round(i,3) for i in o['hue_hist_12bin_HSV30deg_mean']],o['frac_frames_p1_le2'],o['frac_p99_ge254'])
for g,r in out['per_toneclass'].items():
    print(g)
    for k,v in r.items(): print('  ',k,v['n'],{c:[round(i) for i in v[c]] for c in ['luma_p1','luma_p5','luma_p95','luma_p99']},round(v['frac_p1_le2'],2))
