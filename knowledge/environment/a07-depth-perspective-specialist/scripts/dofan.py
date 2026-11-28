import json,glob,numpy as np
B=1.65  # in-focus baseline (calib): measured median sigma at native for sharp frames
rows=[]
for p in sorted(glob.glob('RC30-*_sigma.json')):
    key=p[:7]
    for fr in json.load(open(p)):
        c=fr['cells']; s=np.array([x[3] for x in c],float); n=np.array([x[2] for x in c])
        valid=n>=40
        if valid.sum()<3: rows.append((key,fr['f'],np.nan,np.nan,np.nan,valid.sum(),np.nan));continue
        sv=np.where(valid,s,np.nan)
        # nan with few edges: unmeasurable
        ref=np.nanpercentile(sv,20); mx=np.nanmax(sv)
        top=np.nanmedian(sv[0:6]) if np.isfinite(sv[0:6]).any() else np.nan
        mid=np.nanmedian(sv[6:9]) if np.isfinite(sv[6:9]).any() else np.nan
        rows.append((key,fr['f'],ref,mx,top,valid.sum(),mid))
import csv; csv.writer(open('dof_frames.csv','w')).writerows(rows)
a=np.array([(r[2],r[3]) for r in rows if r[2]==r[2]])
print(len(rows),'frames; ref median',np.median(a[:,0]),'max-cell excess ratio median',np.median(a[:,1]/a[:,0]))
ratio=a[:,1]/a[:,0]; print(np.percentile(ratio,[10,25,50,75,90,95]))
