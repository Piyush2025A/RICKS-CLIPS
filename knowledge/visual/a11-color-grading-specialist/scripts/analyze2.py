import csv,json,os,numpy as np
D=os.path.expanduser("~/ricks-clips-private/analysis-data/rc30/agents/a11-color-grading-specialist/")
OUT="/home/piyush/RICKS-CLIPS/knowledge/visual/a11-color-grading-specialist/data/"
def rd(p):
    r=list(csv.DictReader(open(p)));return {k:np.array([float(x[k]) if x[k] not in('','nan') else np.nan for x in r]) for k in r[0]}
q=lambda x,p:float(np.nanpercentile(x,p))
res={};ALL={k:[] for k in ['white_frac','wL','wa','wb','wR','wG','wB','dk_a','dk_b','dk_frac','sat_frac']};YH=[]
for n in range(1,31):
    d=rd(D+f"pass2_{n:02d}.csv")
    res[f"RC30-{n:02d}"]={k:round(float(np.nanmedian(d[k])),3) for k in ['white_frac','wL','wa','wb','wR','wG','wB','dk_a','dk_b','sat_frac']}
    for k in ALL: ALL[k]+=list(d[k])
    YH.append(np.stack([d[f"yh{k:02d}"] for k in range(16)],1))
YH=np.concatenate(YH)
out={"per_video":res,"pooled":{k:[round(q(np.array(v),25),3),round(q(np.array(v),50),3),round(q(np.array(v),75),3)] for k,v in ALL.items()},
 "pooled_luma_hist_16bin_mean":[round(float(x),4) for x in YH.mean(0)],
 "pooled_luma_hist_16bin_median":[round(float(x),4) for x in np.median(YH,0)]}
json.dump(out,open(OUT+"white_card_black_tint_hist.json","w"),indent=1)
print(json.dumps(out["pooled"]));print(out["pooled_luma_hist_16bin_mean"])
vals=np.array([[v['wL'],v['wa'],v['wb']] for v in res.values()]);print(vals.min(0),np.median(vals,0),vals.max(0))
