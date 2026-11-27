import csv,json,numpy as np,collections,sys
K="/home/piyush/RICKS-CLIPS/knowledge/"
PV="/home/piyush/ricks-clips-private/analysis-data/rc30/"
OUT=K+"cinematography/a16-editing-pacing-specialist/data/"
rng=np.random.default_rng(16)
gaps=json.load(open(PV+"agents/a16-editing-pacing-specialist/gaps.json"))
def cev(a,thr=200):  # A20 detector (capev.py): spike >= thr, local max +-3, 3-frame refractory
    d=a[:,2];ev=[i for i in range(1,len(d)) if d[i]>=thr and d[i]==d[max(0,i-3):i+4].max()];o=[]
    for i in ev:
        if not o or i-o[-1]>=3:o.append(i)
    return o
caps={str(n):np.array(cev(np.load(PV+f"agents/a20-voiceover-specialist/capser_{n}.npy"))) for n in range(1,31)}
rows=list(csv.DictReader(open(K+"cinematography/a15-transition-specialist/data/transitions_confirmed.csv")))
tr=collections.defaultdict(list)
for r in rows:
    if r["type"]=="FP":continue
    tr[r["video"]].append((int(r["cand_start"]),int(r["cand_end"]),r["type"]))
def nframes(k):
    with open(PV+f"v0.2.0/{k}/frames.csv") as f: return sum(1 for _ in f)-1
edl={}
for k in sorted(tr):
    L=sorted(tr[k]);m=[]
    for s,e,t in L:
        if m and s-m[-1][1]<=15: m[-1]=(m[-1][0],max(m[-1][1],e),m[-1][2]+"+"+t)
        else: m.append((s,e,t))
    edl[k]=dict(n=nframes(k),tr=m)
# shots
def shots(k):
    n=edl[k]["n"];c=[(s+e)/2 for s,e,_ in edl[k]["tr"]]
    b=[0]+c+[n];return np.diff(b)
res={"videos":list(edl)}
# 1 shot lengths per act (normalised 0-.25,.25-.65,.65-1 and absolute first 3 s) and cut rate per decile
out=[];dec=np.zeros(10);decT=np.zeros(10)
actl={"A1":[], "A2":[], "A3":[]}
for k in edl:
    n=edl[k]["n"];c=np.array([(s+e)/2 for s,e,_ in edl[k]["tr"]])/n
    sl=shots(k)/30
    first3=sum(1 for x in c*n if x<90)
    cnt=[((c<.25)).sum(),((c>=.25)&(c<.65)).sum(),(c>=.65).sum()]
    dur=[.25*n/30,.4*n/30,.35*n/30]
    h,_=np.histogram(c,bins=10,range=(0,1));dec+=h;decT+=1
    # shot lengths by act using shot midpoint
    b=np.r_[0,c,1];mid=(b[:-1]+b[1:])/2;ln=np.diff(b)*n/30
    for a,(lo,hi) in zip(["A1","A2","A3"],[(0,.25),(.25,.65),(.65,1.01)]):
        actl[a]+=list(ln[(mid>=lo)&(mid<hi)])
    out.append(dict(key=k,dur_s=round(n/30,2),n_trans=len(c),shots=len(c)+1,median_shot_s=round(float(np.median(sl)),2),first_trans_s=round(c[0]*n/30,2) if len(c) else None,
        trans_first3s=first3,rate_A1=round(cnt[0]/dur[0]*10,2),rate_A2=round(cnt[1]/dur[1]*10,2),rate_A3=round(cnt[2]/dur[2]*10,2),max_shot_s=round(float(sl.max()),2),
        last_shot_s=round(float(sl[-1]),2),first_shot_s=round(float(sl[0]),2)))
with open(OUT+"shots_per_video.csv","w") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
q=lambda a:[round(float(x),2) for x in np.percentile(a,[25,50,75])]
res["act_shot_len_s"]={a:dict(n=len(v),q25_50_75=q(v),mean=round(float(np.mean(v)),2)) for a,v in actl.items()}
res["cuts_per_decile_pooled"]=[int(x) for x in dec]
# per-video decile rate rank test: A1 vs A3 rate
r1=np.array([o["rate_A1"] for o in out]);r2=np.array([o["rate_A2"] for o in out]);r3=np.array([o["rate_A3"] for o in out])
from scipy import stats
res["rate_per10s"]=dict(A1=q(r1),A2=q(r2),A3=q(r3),wilcoxon_A1_vs_A3_p=float(stats.wilcoxon(r1,r3).pvalue),A3_gt_A1=int((r3>r1).sum()),A3_lt_A1=int((r3<r1).sum()),friedman_p=float(stats.friedmanchisquare(r1,r2,r3).pvalue))
# slope of cut position vs normalised time: spearman of shot length vs shot midpoint, per video
rho=[]
for k in edl:
    n=edl[k]["n"];c=np.array([(s+e)/2 for s,e,_ in edl[k]["tr"]])/n;b=np.r_[0,c,1];mid=(b[:-1]+b[1:])/2;ln=np.diff(b)
    if len(mid)>=6: rho.append(stats.spearmanr(mid,ln)[0])
res["spearman_shotlen_vs_pos"]=dict(n=len(rho),q=q(rho),pos=int((np.array(rho)>0).sum()),neg=int((np.array(rho)<0).sum()))
# first 3 s
res["trans_first3s"]=dict(values=[o["trans_first3s"] for o in out],first_shot_s=q([o["first_shot_s"] for o in out]),last_shot_s=q([o["last_shot_s"] for o in out]))
# 2 beat-to-shot mapping
def nearest(x,arr):
    d=np.abs(arr[None,:]-x[:,None]);return d.min(1)
def circ_null(c,n,arr,B=500):
    # circular shift of the whole transition list
    ms=[]
    for _ in range(B):
        s=rng.uniform(0,n);cc=(c+s)%n;ms.append(np.median(nearest(cc,arr)))
    return np.array(ms)
off=[];summ=[]
allobs={"gapc":[],"gap_edge":[],"cap":[]};allnull={"gapc":[],"gap_edge":[],"cap":[]}
for k in edl:
    n=edl[k]["n"];ts=np.array(edl[k]["tr"],dtype=object)
    cs=np.array([(s+e)/2 for s,e,_ in edl[k]["tr"]]);ss=np.array([s for s,e,_ in edl[k]["tr"]],float);ee=np.array([e for s,e,_ in edl[k]["tr"]],float)
    g=np.array(gaps[k]["gaps"])*30
    gc=(g[:,0]+g[:,1])/2
    # distance from transition centre to nearest gap interval (0 if inside)
    def dgap(x):
        d=np.maximum(np.maximum(g[:,0][None,:]-x[:,None],x[:,None]-g[:,1][None,:]),0);return d.min(1)
    cap=np.array(caps[k.split("-")[1].lstrip("0")])
    # observed
    inside_c=dgap(cs)==0;inside_any=np.array([(dgap(np.arange(s,e+1,dtype=float))==0).any() for s,e in zip(ss,ee)])
    dc=nearest(cs,cap);ds=nearest(ss,cap);de=nearest(ee,cap)
    # null: circular shift 500x
    nin=[];nany=[];ncap=[]
    for _ in range(500):
        s0=rng.uniform(0,n);c2=(cs+s0)%n;nin.append((dgap(c2)==0).mean())
        ncap.append(np.median(nearest(c2,cap)))
        s2=(ss+s0)%n;e2=s2+(ee-ss);nany.append(np.mean([(dgap(np.arange(a,b+1,dtype=float))==0).any() for a,b in zip(s2,e2)]))
    # gap-centre distance
    dgc=nearest(cs,gc);ngc=[np.median(nearest((cs+rng.uniform(0,n))%n,gc)) for _ in range(500)]
    summ.append(dict(key=k,n_tr=len(cs),centre_in_gap=round(float(inside_c.mean()),3),null_centre_in_gap=round(float(np.mean(nin)),3),
        span_overlaps_gap=round(float(inside_any.mean()),3),null_span_overlaps_gap=round(float(np.mean(nany)),3),
        med_dist_gapcentre_f=round(float(np.median(dgc)),1),null_med_dist_gapcentre_f=round(float(np.mean(ngc)),1),
        med_dist_capchange_centre_f=round(float(np.median(dc)),1),null_med_dist_cap_f=round(float(np.mean(ncap)),1),
        med_dist_cap_start_f=round(float(np.median(ds)),1),med_dist_cap_end_f=round(float(np.median(de)),1)))
    allobs["gapc"]+=list(dgc)
    off+=[dict(key=k,centre=float(c),start=float(a),end=float(b),dist_gap_f=float(dgap(np.array([c]))[0]),dist_cap_f=float(x)) for c,a,b,x in zip(cs,ss,ee,dc)]
with open(OUT+"boundary_offsets_per_video.csv","w") as f:
    w=csv.DictWriter(f,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
S=lambda f:np.array([s[f] for s in summ])
res["beat_alignment"]={f:dict(med_over_videos=round(float(np.median(S(f))),3)) for f in S.__code__.co_consts[0:0]} if False else {}
for a,b in [("centre_in_gap","null_centre_in_gap"),("span_overlaps_gap","null_span_overlaps_gap"),("med_dist_gapcentre_f","null_med_dist_gapcentre_f"),("med_dist_capchange_centre_f","null_med_dist_cap_f")]:
    x,y=S(a),S(b)
    res["beat_alignment"][a]=dict(obs_median=round(float(np.median(x)),3),null_median=round(float(np.median(y)),3),videos_obs_gt_null=int((x>y).sum()),videos_obs_lt_null=int((x<y).sum()),wilcoxon_p=float(stats.wilcoxon(x,y).pvalue))
dgp=np.array([o["dist_gap_f"] for o in off]);dcp=np.array([o["dist_cap_f"] for o in off])
res["pooled"]=dict(n_trans=len(off),dist_to_gap_f_q=q(dgp),frac_centre_in_gap=round(float((dgp==0).mean()),3),dist_to_capchange_f_q=q(dcp),
    frac_within3f_cap=round(float((dcp<=3).mean()),3))
# signed offset of transition centre to nearest gap START/END (for placement rule)
sg=[]
for k in edl:
    g=np.array(gaps[k]["gaps"])*30
    for s,e,_ in edl[k]["tr"]:
        c=(s+e)/2;allg=np.r_[g[:,0],g[:,1]];i=np.argmin(np.abs(allg-c));sg.append(c-allg[i])
res["signed_offset_to_nearest_gap_edge_f_q"]=q(sg)
# phrases / shot: gaps>=0.3 s per shot, caption tokens per shot
ph=[];tk=[];per=[]
for k in edl:
    n=edl[k]["n"];c=np.r_[0,[(s+e)/2 for s,e,_ in edl[k]["tr"]],n];g=np.array([x for x in gaps[k]["gaps"] if x[1]-x[0]>=0.3])*30
    cap=np.array(caps[k.split("-")[1].lstrip("0")])
    p=[];t=[]
    for a,b in zip(c[:-1],c[1:]):
        ng=((g[:,0]>a)&(g[:,1]<b)).sum() if len(g) else 0
        # phrases = pause-split segments intersecting the shot, approximated as gaps inside +1 (fractional)
        p.append(ng+(b-a)/30/3.9*0)  # integer gap count
        t.append(((cap>=a)&(cap<b)).sum())
    ph+=p;tk+=t;per.append(dict(key=k,pauses_ge03_per_shot_med=float(np.median(p)),tokens_per_shot_med=float(np.median(t))))
res["per_shot"]=dict(n_shots=len(ph),pauses_ge03_q=q(ph),tokens_q=q(tk),shots_with_zero_internal_pause_ge03=round(float(np.mean(np.array(ph)==0)),3),tokens_per_shot_mean=round(float(np.mean(tk)),1))
# pause-phrase per shot: phrases = internal gaps +1 (a shot spanning n gaps touches n+1 phrases)
res["per_shot"]["phrases_touched_q"]=q(np.array(ph)+1)
# sensitivity: window around gap: also share of transitions within +-0.25 s of a gap >=0.3 s
w=[]
for k in edl:
    g=np.array([x for x in gaps[k]["gaps"] if x[1]-x[0]>=0.3])*30
    for s,e,_ in edl[k]["tr"]:
        c=(s+e)/2;w.append(bool((np.maximum(np.maximum(g[:,0]-c,c-g[:,1]),0)<=7.5).any()))
nullw=[]
for _ in range(200):
    m=[]
    for k in edl:
        n=edl[k]["n"];g=np.array([x for x in gaps[k]["gaps"] if x[1]-x[0]>=0.3])*30;s0=rng.uniform(0,n)
        for s,e,_ in edl[k]["tr"]:
            c=((s+e)/2+s0)%n;m.append(bool((np.maximum(np.maximum(g[:,0]-c,c-g[:,1]),0)<=7.5).any()))
    nullw.append(np.mean(m))
res["within_0p25s_of_pause_ge0p3"]=dict(obs=round(float(np.mean(w)),3),null_mean=round(float(np.mean(nullw)),3),null_p95=round(float(np.percentile(nullw,95)),3))
json.dump(res,open(OUT+"pacing_summary.json","w"),indent=1)
json.dump({k:dict(n_frames=v["n"],transitions=v["tr"]) for k,v in edl.items()},open(OUT+"edit_lists_from_a15.json","w"))
print(json.dumps(res,indent=1))
