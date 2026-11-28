"""3B: two shot units. edit shot (A15 real rows) vs visual beat (edits + camera-driven FP rows + own window detector).
Run: .venv-analysis/bin/python knowledge/cinematography/a16-editing-pacing-specialist/scripts/units3b.py"""
import csv,json,re,numpy as np,collections
from scipy.signal import find_peaks
K="/home/piyush/RICKS-CLIPS/knowledge/";PV="/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0/"
OUT=K+"cinematography/a16-editing-pacing-specialist/data/"
rows=list(csv.DictReader(open(K+"cinematography/a15-transition-specialist/data/transitions_confirmed.csv")))
CAM=re.compile(r"camera|pull|push|zoom|fly|descent|pan\b|tilt|follow|whip|continuous",re.I)
def feat(k):
    r=list(csv.DictReader(open(PV+f"{k}/color.csv")))
    f=np.array([[float(x[c]) for c in ["hue%02d"%i for i in range(12)]+["L_mean","a_mean","b_mean","sat_mean"]] for x in r])
    f[:,12]/=100;f[:,13]/=60;f[:,14]/=60  # scale
    return f
def dwin(f,w0=4,w1=12):
    n=len(f);d=np.zeros(n)
    c=np.cumsum(np.vstack([np.zeros(f.shape[1]),f]),0)
    def m(a,b):a=max(a,0);b=min(b,n);return (c[b]-c[a])/max(b-a,1)
    for t in range(w1,n-w1):
        d[t]=np.abs(m(t+w0,t+w1)-m(t-w1,t-w0)).sum()
    return d
def merge(L,g=15):
    L=sorted(L);m=[]
    for s,e in L:
        if m and s-m[-1][1]<=g:m[-1]=(m[-1][0],max(m[-1][1],e))
        else:m.append((s,e))
    return [(a+b)/2 for a,b in m]
vids=["RC30-%02d"%i for i in range(1,31)]
N={k:sum(1 for _ in open(PV+f"{k}/frames.csv"))-1 for k in vids}
real={k:[] for k in vids};camfp={k:[] for k in vids};cand={k:[] for k in vids}
for r in rows:
    k=r["video"];s,e=int(r["cand_start"]),int(r["cand_end"])
    if r["type"]!="FP":real[k].append((s,e))
    elif CAM.search(r["notes"]):camfp[k].append((s,e))
D={};F={}
for k in vids:
    F[k]=feat(k);D[k]=dwin(F[k])
# calibrate: d at real edits
dr=[]
for k in vids:
    for c in merge(real[k]):
        i=int(c);dr.append(D[k][max(0,i-3):i+4].max())
dr=np.array(dr);print("d at real edits n",len(dr),"pcts",np.percentile(dr,[10,25,50,75]))
dall=np.concatenate([D[k][12:-12] for k in vids]);print("d all pcts",np.percentile(dall,[50,90,95,99]))
import sys
THR=float(sys.argv[1]) if len(sys.argv)>1 else 0.7
out=[];detail={}
for k in vids:
    n=N[k];dur=n/30
    ed=merge(real[k]);cf=merge(camfp[k])
    pk,_=find_peaks(D[k],height=THR,distance=12)
    own=[int(p) for p in pk]
    # beats = union: edits; camera FP rows; own peaks not within 15 f of any of those
    base=list(ed)
    cfx=[c for c in cf if all(abs(c-b)>15 for b in base)]
    b2=sorted(base+cfx)
    ownx=[p for p in own if all(abs(p-b)>15 for b in b2)]
    b3=sorted(b2+ownx)
    def shots(b):
        x=np.diff([0]+list(b)+[n])/30;return x
    se,sb2,sb3=shots(sorted(ed)),shots(b2),shots(b3)
    rec=dict(key=k,dur_s=round(dur,2),edits=len(ed),edit_shots=len(se),edit_median_s=round(float(np.median(se)),2),edits_per10s=round(len(ed)/dur*10,2),
      camfp_rows=len(cf),camfp_new=len(cfx),beatsB_n=len(b2),beatsB_median_s=round(float(np.median(sb2)),2),beatsB_per10s=round(len(b2)/dur*10,2),
      own_peaks=len(own),own_extra=len(ownx),beatsC_n=len(b3),beatsC_median_s=round(float(np.median(sb3)),2),beatsC_per10s=round(len(b3)/dur*10,2),
      own_recall_of_edits=round(float(np.mean([any(abs(p-c)<=10 for p in own) for c in ed])),2) if ed else "")
    out.append(rec);detail[k]=dict(edits=ed,camfp=cfx,own_extra=ownx)
json.dump(detail,open(OUT+"beats_events_3b.json","w"))
with open(OUT+"shots_two_units_3b.csv","w") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
def S(x):x=np.array(x,float);return f"{np.median(x):.2f} (IQR {np.percentile(x,25):.2f}-{np.percentile(x,75):.2f})"
for c in ["edit_median_s","beatsB_median_s","beatsC_median_s","edits_per10s","beatsB_per10s","beatsC_per10s"]:print(c,S([r[c] for r in out]))
# pooled shot lengths
for name,key in [("edit","edits"),("B","B"),("C","C")]:
    pass
print("recall own of edits",np.nanmean([r["own_recall_of_edits"] for r in out if r["own_recall_of_edits"]!=""]))
print("totals edits",sum(r["edits"] for r in out),"camfp new",sum(r["camfp_new"] for r in out),"own extra",sum(r["own_extra"] for r in out))
for r in out:print(r["key"],r["edits_per10s"],r["beatsB_per10s"],r["beatsC_per10s"],r["own_peaks"],r["own_recall_of_edits"])
# pooled shot-length statistics
def pooled(key):
    L=[]
    for k in vids:
        d=detail[k];n=N[k]
        if key=="edit":b=sorted(d["edits"])
        elif key=="B":b=sorted(d["edits"]+d["camfp"])
        else:b=sorted(d["edits"]+d["camfp"]+d["own_extra"])
        L+=list(np.diff([0]+b+[n])/30)
    return L
for key in ["edit","B","C"]:
    L=pooled(key);print("pooled",key,len(L),S(L))
