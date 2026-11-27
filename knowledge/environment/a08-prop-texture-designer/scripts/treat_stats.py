import csv,numpy as np,json
R='/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0/RC30-%02d/'
grp={'A':[2,26,27],'B':[15,25,29,30],'H':[23,24,28]}
def col(path,c):
    v=[]
    for r in csv.DictReader(open(path)):
        if r.get('status','ok')=='ok' and r[c] not in('','nan'): v.append(float(r[c]))
    return np.array(v)
out={}
for g,ks in grp.items():
    for k in ks:
        d={}
        for f,c in [('sharpness','lap_var'),('sharpness','grad_energy'),('edges','canny_density'),('edges','edge_width_px'),('edges','dark_frac')]:
            v=col(R%k+f+'.csv',c); d[c]=[round(float(np.median(v)),4),round(float(np.percentile(v,25)),4),round(float(np.percentile(v,75)),4),len(v)]
        out[f'{g}-RC30-{k:02d}']=d; print(g,k,{c:d[c][0] for c in d},'n',d['lap_var'][3])
json.dump(out,open('/home/piyush/RICKS-CLIPS/knowledge/environment/a08-prop-texture-designer/data/treatment_hf_energy.json','w'),indent=1) if False else None
json.dump(out,open('/tmp/x','w')) if False else None
json.dump(out,open(__file__.replace('scripts/treat_stats.py','treat_stats.json'),'w'),indent=1)
