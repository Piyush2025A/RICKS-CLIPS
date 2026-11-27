import csv,json,numpy as np
from scipy.ndimage import median_filter
from lib import *
K="/home/piyush/RICKS-CLIPS/knowledge/";OUT=K+"cinematography/a16-editing-pacing-specialist/data/"
edl=json.load(open(OUT+"edit_lists_from_a15.json"))
mv={}
for r in csv.DictReader(open(K+"cinematography/a13-camera-director/data/moves_table.csv")):
    mv.setdefault(r["key"],[]).append((int(r["start"]),int(r["end"]),r["fast"]=="True"))
def spikes(k,n,fac):
    m=col(k,"shot_features.csv","mad");m=np.nan_to_num(m,nan=np.nanmedian(m))
    base=median_filter(m,size=15,mode="nearest");d=np.abs(m-base);sig=1.4826*np.median(np.abs(d-np.median(d)))+1e-6
    ev=[i for i in range(1,len(m)-1) if d[i]>fac*sig and d[i]>=d[max(0,i-2):i+3].max()]
    o=[]
    for i in ev:
        if not o or i-o[-1]>=6:o.append(i)
    return np.array(o)
def maxgap(ev,n):
    e=np.r_[0,np.sort(ev),n];g=np.diff(e);i=int(g.argmax());return g.max()/30,e[i]
rows=[];sens=[]
for k,v in edl.items():
    n=v["n_frames"];T=n/30
    tr=np.array([(s+e)/2 for s,e,_ in v["transitions"]])
    mvs=np.array([s for s,e,f in mv.get(k,[])]);mve=np.array([e for s,e,f in mv.get(k,[])])
    d1=maxgap(tr,n)
    row=dict(key=k,dur_s=round(T,1),max_gap_transitions_s=round(d1[0],2),at_f=int(d1[1]))
    if len(mvs):
        # moves occupy a span: change continuously during move; gap = frames not in any transition/move span
        cov=np.zeros(n,bool)
        for s,e,_ in mv[k]:cov[s:e+1]=True
        for s,e,_ in v["transitions"]:cov[max(0,s-1):e+2]=True
        # longest run uncovered
        run=best=0;end=0
        for i,c in enumerate(cov):
            run=0 if c else run+1
            if run>best:best=run;end=i
        row.update(max_gap_trans_moves_s=round(best/30,2),at_f2=end-best+1,frames_covered_frac=round(float(cov.mean()),3))
        # camera static: |tx|,|ty|<0.5 px per frame, |scale-1|<.002 and conf high/med
        tx=col(k,"motion.csv","tx");ty=col(k,"motion.csv","ty");sc=col(k,"motion.csv","scale")
        still=(np.abs(tx)<0.5)&(np.abs(ty)<0.5)&(np.abs(sc-1)<0.002)
        row["static_cam_frac"]=round(float(np.nanmean(still)),3)
        run=best=0
        for c in still:
            run=run+1 if c else 0;best=max(best,run)
        row["longest_static_cam_s"]=round(best/30,2)
    else: row.update(max_gap_trans_moves_s=None)
    for fac in (3,4,6):
        sp=spikes(k,n,fac)
        evs=np.r_[tr,sp]
        if len(mvs):evs=np.r_[evs,mvs]
        g=maxgap(evs,n)
        row[f"max_gap_all_f{fac}_s"]=round(g[0],2);row[f"events_per10s_f{fac}"]=round(len(np.unique(evs.astype(int)))/T*10,1)
        row[f"at_f_f{fac}"]=int(g[1])
        row[f"spike_per10s_f{fac}"]=round(len(sp)/T*10,1)
        row[f"med_interval_f{fac}_s"]=round(float(np.median(np.diff(np.sort(evs))))/30,2) if len(evs)>2 else None
    rows.append(row)
with open(OUT+"change_rate_deadtime.csv","w") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
q=lambda a:[round(float(x),2) for x in np.nanpercentile([x for x in a if x is not None],[25,50,75])]
for c in ["max_gap_transitions_s","max_gap_trans_moves_s","static_cam_frac","longest_static_cam_s","max_gap_all_f3_s","max_gap_all_f4_s","max_gap_all_f6_s","events_per10s_f3","events_per10s_f4","events_per10s_f6","spike_per10s_f4","med_interval_f4_s"]:
    print(c,q([r.get(c) for r in rows]),"max",max(r[c] for r in rows if r.get(c) is not None))
for r in rows:print(r["key"],r["max_gap_transitions_s"],r.get("max_gap_trans_moves_s"),r.get("at_f2"),r.get("longest_static_cam_s"),r["max_gap_all_f4_s"],r["at_f_f4"],r["events_per10s_f4"])
