import csv,json,glob,os,numpy as np
D=os.path.expanduser("~/ricks-clips-private/analysis-data/rc30/agents/a11-color-grading-specialist/")
V=os.path.expanduser("~/ricks-clips-private/analysis-data/rc30/v0.2.0/")
OUT="/home/piyush/RICKS-CLIPS/knowledge/visual/a11-color-grading-specialist/data/"
def rd(p):
    r=list(csv.DictReader(open(p)));return {k:np.array([float(x[k]) for x in r]) for k in r[0] if k not in('frame_id','status')}
moods=json.load(open("/home/piyush/RICKS-CLIPS/knowledge/visual/a09-lighting-shadow-specialist/data/mood_classes.json"))
names=list(moods);cent=np.array([[moods[m]['L'][1],moods[m]['a'][1],moods[m]['b'][1]] for m in names])
vids={n:rd(D+f"pass_{n:02d}.csv") for n in range(1,31) if os.path.exists(D+f"pass_{n:02d}.csv")}
pct=lambda x,q:float(np.percentile(x,q))
rows=[];allf={k:[] for k in ['y_p1','y_p5','y_p25','y_p50','y_p75','y_p95','y_p99','clip_lo','clip_hi','near_white','C_p50','C_p90','C_mean','C_cen','C_per','vig','L','a','b','vid','mood']}
for n,d in vids.items():
    X=np.stack([d['L'],d['a'],d['b']],1)
    sc=np.array([1/12.7,1/6,1/13.3])  # per-axis scale (SD-ish)
    mi=np.argmin((((X[:,None,:]-cent[None])*np.array([1/12.7,1/6.0,1/10.0]))**2).sum(2),1)
    for k in allf:
        if k=='vid':allf[k]+= [n]*len(d['t'])
        elif k=='mood':allf[k]+=[names[i] for i in mi]
        else: allf[k]+=list(d[k])
    r=dict(video=f"RC30-{n:02d}",n=len(d['t']))
    for k in ['y_p1','y_p5','y_p50','y_p95','y_p99']: r[k+'_med']=round(pct(d[k],50),4)
    r['contrast_p95_p5_med']=round(pct(d['y_p95']-d['y_p5'],50),4)
    r['clip_lo_frac_frames_gt1pct']=round(float((d['clip_lo']>0.01).mean()),3)
    r['clip_hi_frac_frames_gt1pct']=round(float((d['clip_hi']>0.01).mean()),3)
    r['near_white_med']=round(pct(d['near_white'],50),4)
    r['C_p50_med']=round(pct(d['C_p50'],50),2);r['C_p90_med']=round(pct(d['C_p90'],50),2)
    r['C_cen_over_per_med']=round(pct(d['C_cen']/(d['C_per']+1e-3),50),3)
    r['vig_med']=round(pct(d['vig'],50),3)
    r['L_sd']=round(float(d['L'].std()),2);r['b_sd']=round(float(d['b'].std()),2)
    rows.append(r)
with open(OUT+"per_video_tone_chroma.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
A={k:np.array(v) for k,v in allf.items() if k!='mood'};M=np.array(allf['mood'])
def iqr(x):return [round(pct(x,25),4),round(pct(x,50),4),round(pct(x,75),4)]
summ={"n_frames":int(len(M)),"n_videos":len(vids)}
summ['across_videos_median_of_video_medians']={k:iqr(np.array([r[k] for r in rows])) for k in rows[0] if k not in('video','n')}
# per mood
pm={}
HK=[f"hue{k:02d}" for k in range(12)]
H=np.concatenate([np.stack([vids[n][h] for h in HK],1) for n in vids]);Cw=A['C_mean']
for m in names:
    s=M==m
    if s.sum()<5:continue
    hh=H[s].mean(0);hh=hh/hh.sum()
    pm[m]={"n":int(s.sum()),"videos":int(len(set(A['vid'][s]))),
     **{k:iqr(A[k][s]) for k in ['y_p1','y_p5','y_p25','y_p50','y_p75','y_p95','y_p99','C_p50','C_p90','vig']},
     "clip_hi_gt1pct":round(float((A['clip_hi'][s]>0.01).mean()),3),"clip_lo_gt1pct":round(float((A['clip_lo'][s]>0.01).mean()),3),
     "hue_hist_12bin_30deg_Lab_angle":[round(float(x),3) for x in hh]}
summ['per_mood']=pm
hh=H.mean(0);summ['hue_hist_all']=[round(float(x/hh.sum()),3) for x in hh]
# pooled tone-curve shape: frame-level percentiles
summ['pooled_frame_percentiles']={k:iqr(A[k]) for k in ['y_p1','y_p5','y_p25','y_p50','y_p75','y_p95','y_p99']}
summ['clip_hi_gt1pct_frames']=round(float((A['clip_hi']>0.01).mean()),3);summ['clip_lo_gt1pct_frames']=round(float((A['clip_lo']>0.01).mean()),3)
summ['near_white_frac_iqr']=iqr(A['near_white'])
# bimodality check: per-video p50 spread
summ['p50_video_medians_sorted']=sorted([(r['video'],r['y_p50_med']) for r in rows],key=lambda x:x[1])
json.dump(summ,open(OUT+"tone_chroma_hue_summary.json","w"),indent=1)
# black point colour
bp=[]
for n,d in vids.items():
    bp.append([n]+[round(float(np.median(d[k])*255)) for k in('blk_r','blk_g','blk_b')])
json.dump(bp,open(OUT+"black_point_rgb_per_video.json","w"))
# black tint by mood
bm={}
for m in names:
    s=M==m
    if s.sum()<5:continue
    br=np.concatenate([vids[n]['blk_r'] for n in vids]);bg=np.concatenate([vids[n]['blk_g'] for n in vids]);bb=np.concatenate([vids[n]['blk_b'] for n in vids])
    bm[m]=[round(float(np.median(x[s])*255)) for x in (br,bg,bb)]
json.dump(bm,open(OUT+"black_point_rgb_per_mood.json","w"))
# ----- shot-to-shot (1fps proxy)
dE=[];vd={}
for n,d in vids.items():
    x=np.stack([d['L'],d['a'],d['b']],1);e=np.linalg.norm(np.diff(x,axis=0),axis=1);vd[n]=e;dE+=list(e)
dE=np.array(dE)
summ2={"dE76_1s_steps_all":iqr(dE),"p90":pct(dE,90),"p95":pct(dE,95),
 "per_video_median_dE":{f"{n:02d}":round(pct(e,50),2) for n,e in vd.items()},
 "per_video_p90_dE":{f"{n:02d}":round(pct(e,90),2) for n,e in vd.items()}}
# luma p50 step
dy=np.concatenate([np.abs(np.diff(d['y_p50'])) for d in vids.values()]);summ2['abs_dY50_1s_steps']=iqr(dy);summ2['abs_dY50_p90']=pct(dy,90)
json.dump(summ2,open(OUT+"shot_continuity_1fps.json","w"),indent=1)
print(json.dumps(summ,indent=0)[:6000]);print(json.dumps(summ2)[:1500])
