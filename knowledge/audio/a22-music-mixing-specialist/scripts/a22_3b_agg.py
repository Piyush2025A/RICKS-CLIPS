import json,glob,numpy as np,csv
R=[json.load(open(f)) for f in sorted(glob.glob("../data/pv3b/*.json"),key=lambda p:int(p.split('/')[-1][:-5]))]
def st(k,sub=None):
    v=np.array([r[k] for r in R if r.get(k) is not None],float); v=v[~np.isnan(v)]
    return f"{np.median(v):.2f} (IQR {np.percentile(v,25):.2f}..{np.percentile(v,75):.2f}; {v.min():.2f}..{v.max():.2f}; n={len(v)})"
for k in R[0]:
    if k in("key",)or isinstance(R[0][k],(list,str)):continue
    print(k,st(k))
print("end swell >ctl p95:",[r["key"] for r in R if r["end_rise"]>r["end_ctl_p95"]])
print("end rise>=10:",[(r["key"],round(r["end_rise"],1),round(r["end_t_peak"],1),round(r["dur_s"],1),r["end_above6_s"]) for r in R if r["end_rise"]>=10])
print("tempo z>3:",[(r["key"],round(r["tempo_bpm"]),round(r["tempo_z"],1)) for r in R if r["tempo_z"]>3])
print("tempo z<=3 count",sum(r["tempo_z"]<=3 for r in R))
print("paired side bass sig (CI excludes 0):",sum(1 for r in R if r.get("paired_bass30_90_ci") and (r["paired_bass30_90_ci"][0]>0 or r["paired_bass30_90_ci"][1]<0)))
print("tempo bpm all",sorted(round(r["tempo_bpm"]) for r in R))
print("chroma min cos",sorted((round(r["chroma_adjwin_cos_min"],2),r["key"]) for r in R)[:6])
with open("../data/bed_level_3B.csv","w") as f:
    w=csv.writer(f);ks=[k for k in R[0] if not isinstance(R[0][k],list)];w.writerow(ks)
    for r in R:w.writerow([r.get(k) for k in ks])
