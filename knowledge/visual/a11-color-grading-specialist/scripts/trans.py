import csv,json,glob,os,numpy as np
V=os.path.expanduser("~/ricks-clips-private/analysis-data/rc30/v0.2.0/")
OUT="/home/piyush/RICKS-CLIPS/knowledge/visual/a11-color-grading-specialist/data/"
def rd(p):
    r=list(csv.DictReader(open(p)));return {k:np.array([float(x[k]) for x in r]) for k in r[0] if k not in('frame_id','status')}
res={};allcut=[];allgr=[];fp={}
rows=[]
for d in sorted(glob.glob(V+"RC30-*")):
    key=os.path.basename(d)
    if not os.path.exists(d+"/shot_candidates.json") or not os.path.exists(d+"/color.csv"):continue
    c=rd(d+"/color.csv");sc=json.load(open(d+"/shot_candidates.json"))
    Lab=np.stack([c['L_mean'],c['a_mean'],c['b_mean']],1);n=len(Lab)
    # whole-video native stats (caption included!)
    st=dict(n=n,p1_med=float(np.median(c['luma_p1'])),p50_med=float(np.median(c['luma_p50'])),p99_med=float(np.median(c['luma_p99'])),
       p1_min=float(c['luma_p1'].min()),p99_max=float(c['luma_p99'].max()),frames_p99_ge254=float((c['luma_p99']>=254).mean()),frames_p1_le16=float((c['luma_p1']<=16).mean()),frames_p1_le2=float((c['luma_p1']<=2).mean()),
       contrast_med=float(np.median(c['luma_p95']-c['luma_p5'])))
    ev=[]
    for k in sc['candidates']:
        a,b=k['start'],k['end'];t=k['type']
        if a<2 or b>=n-2:continue
        pre=Lab[a-1];post=Lab[min(b+1,n-1)]
        dE=float(np.linalg.norm(post-pre));dL=float(post[0]-pre[0])
        # monotone-ness in crossfade: is L path between pre and post bounded (no flash)? overshoot
        seg=c['luma_mean'][a-1:b+2];lo,hi=min(seg[0],seg[-1]),max(seg[0],seg[-1])
        over=float(max(seg.max()-hi,lo-seg.min(),0))
        ev.append((t,dE,dL,over,b-a+1))
    st['n_events']=len(ev)
    for t in set(e[0] for e in ev):
        x=[e for e in ev if e[0]==t]
        st[t]=dict(n=len(x),dE_med=float(np.median([e[1] for e in x])),dE_p90=float(np.percentile([e[1] for e in x],90)),overshoot_med=float(np.median([e[3] for e in x])))
    res[key]=st;allcut+= [e[1] for e in ev]
    # whole-frame mean-Lab temporal std per second within non-event areas: skip
print(json.dumps(res,indent=0)[:5000])
json.dump(res,open(OUT+"native_tone_and_transitions_processed.json","w"),indent=1)
a=np.array(allcut);print("all events dE76 across transitions: n",len(a),np.percentile(a,[25,50,75,90]))
