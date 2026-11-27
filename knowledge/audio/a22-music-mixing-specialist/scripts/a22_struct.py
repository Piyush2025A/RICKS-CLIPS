"""novelty (side chroma+MFCC, 20ms hop) vs shot candidates and speech onsets, shuffled controls"""
import json,numpy as np,glob
P="/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a22-music-mixing-specialist/"
R="/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0/"
D="/home/piyush/RICKS-CLIPS/knowledge/audio/a22-music-mixing-specialist/data/"
rng=np.random.default_rng(5); out=[]
for k in range(1,31):
    n=f"{k:02d}"; nov=np.load(P+f"nov_{n}.npy"); act=np.load(P+f"act_{n}.npy")
    import os
    if not os.path.exists(R+f"RC30-{n}/shot_candidates.json"): continue
    sc=json.load(open(R+f"RC30-{n}/shot_candidates.json"))["candidates"]
    ct=[c["pts_time"] for c in sc if c["type"] in("cut_candidate","gradual_candidate")]
    ft=[c["pts_time"] for c in sc if c["type"]=="flash_candidate"]
    T=len(nov); dur=T*0.02
    # novelty peaks (music change events): local max > mean+1.5sd, min 1 s apart
    from scipy.signal import find_peaks
    nn=nov[25:-25]; pk,_=find_peaks(nov,height=nov[25:-25].mean()+1.5*nov[25:-25].std(),distance=50)
    pk=pk*0.02
    def stat(ev,w=0.25):
        ev=[e for e in ev if 1<e<dur-1]
        if len(ev)<3: return None
        f=lambda E:np.mean([nov[int((e-w)/0.02):int((e+w)/0.02)].max() for e in E])
        o=f(ev); c=np.array([f(rng.uniform(1,dur-1,len(ev))) for _ in range(300)])
        return dict(n=len(ev),obs=float(o),ctrl=float(c.mean()),z=float((o-c.mean())/(c.std()+1e-9)),p=float((c>=o).mean()))
    # nearest music-change distance to cut vs random
    def near(ev):
        ev=[e for e in ev if 1<e<dur-1]
        if len(ev)<3 or len(pk)<2: return None
        f=lambda E:np.median([np.min(abs(pk-e)) for e in E])
        o=f(ev); c=np.array([f(rng.uniform(1,dur-1,len(ev))) for _ in range(300)]); return dict(obs=float(o),ctrl=float(c.mean()),p_le=float((c<=o).mean()))
    out.append(dict(key=n,n_peaks=len(pk),peaks_per_10s=len(pk)/dur*10,cuts=stat(ct),flash=stat(ft),near_cut=near(ct),peak_t=pk.round(1).tolist(),cut_t=sorted(round(c,1) for c in ct)))
json.dump(out,open(D+"music_change_vs_cuts.json","w"))
z=[o["cuts"]["z"] for o in out if o["cuts"]]; p=[o["cuts"]["p"] for o in out if o["cuts"]]
print("cuts n videos",len(z),"median z",np.median(z),"IQR",np.percentile(z,[25,75]),"p<0.05:",sum(x<0.05 for x in p),"p>0.95:",sum(x>0.95 for x in p))
nc=[o["near_cut"] for o in out if o["near_cut"]]; print("near-cut median dist obs/ctrl",np.median([a["obs"] for a in nc]),np.median([a["ctrl"] for a in nc]),"p_le<0.05",sum(a["p_le"]<0.05 for a in nc),len(nc))
print("peaks/10s",np.median([o["peaks_per_10s"] for o in out]),np.percentile([o["peaks_per_10s"] for o in out],[25,75]))
fz=[o["flash"]["z"] for o in out if o["flash"]]; print("flash n videos",len(fz),np.median(fz) if fz else None)
