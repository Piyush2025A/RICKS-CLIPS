import csv, json, numpy as np
from scipy.ndimage import uniform_filter1d
V='/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0/'
out={}
for k in [15,23,25,27,28,30]:
    d=f'{V}RC30-{k}/'
    lv=np.array([float(r['lap_var']) if r['status']=='ok' else np.nan for r in csv.DictReader(open(d+'sharpness.csv'))])
    cands=json.load(open(d+'shot_candidates.json'))['candidates']
    cut=np.zeros(len(lv),bool)
    for c in cands:
        cut[max(0,c['start']-4):c['end']+5]=True
    l=np.log(np.nan_to_num(lv,nan=np.nanmedian(lv))+1)
    s=uniform_filter1d(l,5)
    ev=[]
    W=20
    i=0
    while i<len(s)-W:
        seg=s[i:i+W+1]; dl=seg[-1]-seg[0]
        if abs(dl)>0.9 and not cut[i:i+W+1].any() and (np.diff(seg)*np.sign(dl)>-0.05).mean()>0.85:
            ev.append((i,i+W,round(float(np.exp(dl)),2))); i+=W
        else: i+=1
    out[k]={'n_frames':len(lv),'lapvar_median':float(np.nanmedian(lv)),'lapvar_iqr':[float(np.nanpercentile(lv,25)),float(np.nanpercentile(lv,75))],'ramps':ev}
    print(k,len(lv),'med',round(float(np.nanmedian(lv)),1),'ramps',len(ev),ev[:12])
json.dump(out,open('rack_candidates.json','w'))
