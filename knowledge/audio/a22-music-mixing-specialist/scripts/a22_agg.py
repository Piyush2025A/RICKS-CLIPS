import json,glob,numpy as np,csv,sys
D="/home/piyush/RICKS-CLIPS/knowledge/audio/a22-music-mixing-specialist/data/"
V=[json.load(open(p)) for p in sorted(glob.glob(D+"pv/*.json"))]
OFF=-58.96
a20={r["key"] if "key" in r else None:r for r in []}
def q(x):
    x=np.array([v for v in x if v is not None and np.isfinite(v)]); 
    return (len(x),round(float(np.median(x)),2),round(float(np.percentile(x,25)),2),round(float(np.percentile(x,75)),2),round(float(x.min()),2),round(float(x.max()),2)) if len(x) else None
rows=[]
for v in V:
    ss=np.array(v["sec_side_db"])+OFF; mm=np.array(v["sec_mid_db"])+OFF
    pres=float(np.mean(ss>-75)); 
    r=dict(key=v["key"],dur=round(v["dur"],1),side_med_dbfs=round(float(np.median(ss)),1),side_p10=round(float(np.percentile(ss,10)),1),side_p90=round(float(np.percentile(ss,90)),1),
      side_minus_mid_db=round(float(np.median(ss-mm)),1),frac_sec_side_gt_m75=round(pres,2),side_flat=v["side_flat_med"],
      tempo_beat=(v["tempo_side"] or {}).get("beat_tempo"),ac_bpm=(v["tempo_side"] or {}).get("ac_bpm"),ac_conf=(v["tempo_side"] or {}).get("ac_conf"),ibi_cv=(v["tempo_side"] or {}).get("ibi_cv"),
      key_top=str(v.get("key_top",[None])[0]),loop=str(v.get("loop_cands",[None])[:2]),centroid=v.get("side_centroid_med"),hp_db=v.get("side_hp_ratio_db"),
      M_gap_minus_act=None if v["M_full_gap"] is None else round(v["M_full_act"]-v["M_full_gap"],1),
      S_act_minus_gap=None if v["side_act_minus_gap_db"] is None else round(v["side_act_minus_gap_db"],1),
      bed_vs_vo=None if v["S_full_gap"] is None else round(v["M_full_act"]-v["S_full_gap"],1),
      crest=round(v["crest_db"],1),near_peak=v["near_peak_frac"],mid_rms=round(v["mid_rms_db"],1),end_side_minus_med=round(v["end_side_db"]-v["side_med_db"],1),active=round(v["active_frac"],2))
    rows.append(r)
with open(D+"music_per_video.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for k in ["side_med_dbfs","side_minus_mid_db","frac_sec_side_gt_m75","side_flat","tempo_beat","ac_conf","M_gap_minus_act","S_act_minus_gap","bed_vs_vo","crest","near_peak","end_side_minus_med","centroid","hp_db"]:
    print(k,q([r[k] for r in rows]))
# ETA pooled
for nm in ["side_on","side_off","midlow_on","midlow_off"]:
    E=[];C=[];Z=[]
    for v in V:
        e=v["eta"].get(nm)
        if not e: continue
        E.append(e["eta"]);C.append(e["ctrl_mean"]); Z.append((np.array(e["eta"])-np.array(e["ctrl_mean"]))/ (np.array(e["ctrl_sd"])+1e-9))
    E=np.array(E);C=np.array(C);Z=np.array(Z)
    t=np.arange(-25,26)*0.02
    d=E-C
    print(nm,len(E),"median diff dB @ -0.2,0,+0.1,+0.2,+0.4:",[round(float(np.median(d[:,int(np.argmin(abs(t-x)))])),2) for x in (-0.2,0,0.1,0.2,0.4)],"min med diff",round(float(np.median(d,0).min()),2),"at",round(float(t[np.argmin(np.median(d,0))]),2),"n videos |z|>2 at peak:",int((np.abs(Z).max(1)>3).sum()))
    json.dump({"t":t.tolist(),"median_eta":np.median(E,0).tolist(),"median_ctrl":np.median(C,0).tolist(),"median_diff":np.median(d,0).tolist(),"p25_diff":np.percentile(d,25,0).tolist(),"p75_diff":np.percentile(d,75,0).tolist(),"n":len(E)},open(D+f"eta_{nm}.json","w"))
# LTAS
ks=list(V[0]["ltas_third"]); L=np.array([[v["ltas_third"][k] for k in ks] for v in V]); Sd=np.array([[v["ltas_side_third"][k] for k in ks] for v in V])
with open(D+"ltas_third_octave.csv","w") as f:
    f.write("freq_hz,mid_med,mid_p25,mid_p75,side_med\n")
    for i,k in enumerate(ks): f.write(f"{k},{np.median(L[:,i]):.1f},{np.percentile(L[:,i],25):.1f},{np.percentile(L[:,i],75):.1f},{np.median(Sd[:,i]):.1f}\n")
print(open(D+"ltas_third_octave.csv").read())
