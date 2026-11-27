import json,csv,numpy as np
OUT="/home/piyush/RICKS-CLIPS/knowledge/cinematography/a16-editing-pacing-specialist/data/"
edl=json.load(open(OUT+"edit_lists_from_a15.json"))
W=[("hook_0-3s",None),("setup_3s-25%",(0,.25)),("escalation_25-55%",(.25,.55)),("reveal_55-85%",(.55,.85)),("punch_85-100%",(.85,1.01))]
L={w:[] for w,_ in W};cnt={w:[] for w,_ in W};rate={w:[] for w,_ in W}
for k,v in edl.items():
    if k in("RC30-03","RC30-22"):continue   # A15 list undercounts (see FINDINGS F-a16-002); kept in separate run
    n=v["n_frames"];T=n/30;c=np.array([(s+e)/2 for s,e,_ in v["transitions"]]);b=np.r_[0,c,n];mid=(b[:-1]+b[1:])/2;ln=np.diff(b)/30
    for w,r in W:
        if r is None:
            m=mid<90;cc=((c<90).sum());d=3.0
        else:
            m=(mid>=r[0]*n)&(mid<r[1]*n);cc=((c>=max(r[0]*n,90))&(c<r[1]*n)).sum();d=(r[1]*n/30 if r[1]<1 else T)-max(r[0]*T,3.0) if r[0]==0 else (min(r[1],1)-r[0])*T
        L[w]+=list(ln[m]);cnt[w].append(int(cc));rate[w].append(cc/d*10)
res={}
for w,_ in W:
    a=np.array(L[w]);res[w]=dict(n_shots=len(a),shot_len_s_q25_50_75=[round(float(x),2) for x in np.percentile(a,[25,50,75])],cuts_per_video_med=float(np.median(cnt[w])),cuts_per10s_q25_50_75=[round(float(x),2) for x in np.percentile(rate[w],[25,50,75])])
last=[ (np.diff(np.r_[0,[(s+e)/2 for s,e,_ in v["transitions"]],v["n_frames"]])[-1]/30) for k,v in edl.items()]
res["last_shot_s_q"]=[round(float(x),2) for x in np.percentile(last,[25,50,75])]
# shots per 'act' (25/65 split) per video
sh=[]
for k,v in edl.items():
    n=v["n_frames"];c=np.array([(s+e)/2 for s,e,_ in v["transitions"]])/n
    sh.append(((c<.25).sum(),((c>=.25)&(c<.65)).sum(),(c>=.65).sum()))
sh=np.array(sh);res["transitions_per_act_med_A1_A2_A3"]=[float(x) for x in np.median(sh,0)]
res["excluded_from_beats"]=["RC30-03","RC30-22"];res["n_videos"]=len(edl)-2
json.dump(res,open(OUT+"beat_windows.json","w"),indent=1);print(json.dumps(res,indent=1))
