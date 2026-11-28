"""3B openers table: eye judgements (every-3rd-frame composites f0-f87, ledger) + computed columns. Run from repo root."""
import csv,json,numpy as np
K="/home/piyush/RICKS-CLIPS/knowledge/";P="/home/piyush/ricks-clips-private/analysis-data/rc30/"
det=json.load(open(K+"cinematography/a16-editing-pacing-specialist/data/beats_events_3b.json"))
# eye: key: (edits_eye, beats_eye, f0, slow_camera_move_in_3s, note)
E={1:(1,1,"posed-gesture","y","ZT pull-back out of porthole f38-44"),2:(1,2,"mid-action","y","fast push to face f60-75; XF to cross-section f77-86"),
3:(0,1,"mid-action","y","camera snaps to rolling bomb/wide f27-38"),4:(0,1,"mid-action","y","pan from tree to road f33-50"),
5:(1,3,"posed","y","push-in f18-27, macro gun f30, cut to miner ~f58"),6:(0,3,"posed","y","fast zoom f33, camera-driven change to drill f42, fast pan to castle f59-78 (A15 FP camera pan; read first as cuts)"),
7:(1,1,"mid-action","n","cut car interior to exterior f39"),8:(1,2,"mid-action","y","pull-back f38-45; XF f81-89"),
9:(0,1,"mid-action","y","whip to wall poster f72-80"),10:(1,2,"mid-action","y","apparent hard cut f63-66 (A15 lists none; possible missed HC, unconfirmed); pull-back f83"),
11:(0,2,"mid-action","y","pan down to sea f35-45; whip to ship f68-75"),12:(0,2,"posed","n","piggy smash VFX f38-47, camera whip to horses ~f50; A15 XF horse->hall at f98-109 is outside 3 s"),
13:(0,0,"posed","n","static two-shot, expression changes only"),14:(1,3,"mid-action","y","flash XF f30 to bullet; reveal street f48; push f78"),
15:(0,2,"posed","y","fast push to ticket f27-33; pull to stranger f55"),16:(0,1,"posed","y","push to cards f14-20"),
17:(0,2,"posed","y","descent into grave f20-35; pan to bell f68-90"),18:(0,2,"posed","y","push to ticket f36-45; pull f75"),
19:(1,3,"mid-action","y","hammer-wipe style change f37 to chair man (A15 FP in-shot hammer); XF f69-76 to boss"),20:(2,2,"posed","n","XF f52-62; XF f80-90"),
21:(1,2,"posed","y","push to dragon f22-30; ZT pull-back to throne room f64-70"),22:(1,4,"mid-action","y","whip f50-62; cut f68; cut f75"),
23:(0,0,"posed","y","slow push-in only"),24:(0,0,"posed","n","static wide"),25:(0,1,"posed","y","slow push f0-40; reframe snap f63-66"),
26:(1,1,"mid-action","n","XF to wide street f64-70"),27:(0,1,"posed","y","macro reels, pull-back reveal f24-35"),
28:(0,0,"mid-action","y","continuous fall follow, no scene change"),29:(0,1,"mid-action","y","pull-back reveal f8-27"),30:(0,0,"posed","y","slow pull-back f0-30, then static")}
rows=[];ev=json.load(open(K+"cinematography/a15-transition-specialist/data/transitions_confirmed.csv".replace("transitions_confirmed.csv","transitions_confirmed.csv"))) if False else None
a15=list(csv.DictReader(open(K+"cinematography/a15-transition-specialist/data/transitions_confirmed.csv")))
for n in range(1,31):
    k="RC30-%02d"%n
    cap=list(csv.DictReader(open(P+f"captions/{k}/caption_segments.csv")))
    f1=int(cap[0]["f_start"]);ncap3=sum(1 for c in cap if int(c["f_start"])<90)
    a15e=sum(1 for r in a15 if r["video"]==k and r["type"]!="FP" and int(r["cand_start"])<90)
    a15c=sum(1 for r in a15 if r["video"]==k and r["type"]=="FP" and int(r["cand_start"])<90)
    # detector peaks <90 (all peaks incl. edits) from beats_events: edits + camfp + own_extra
    d=det[k];dp=sum(1 for x in d["edits"]+d["camfp"]+d["own_extra"] if 12<=x<90)
    e,b,f0,sl,note=E[n]
    rows.append(dict(key=k,a15_edits_0_3s=a15e,a15_FP_rows_0_3s=a15c,eye_edits_0_3s=e,eye_beats_0_3s=b,frame0=f0,slow_camera_move=sl,
     first_caption_f=f1,first_caption_t=round((f1+1)/30,3),caption_at_f0_or_f1=int(f1<=1),captions_started_0_3s=ncap3,detector_events_0_3s=dp,
     a19_mode="stage" if n in (13,14,15,16,23,24,25,27,28,29,30) else "quick",note=note))
with open(K+"cinematography/a16-editing-pacing-specialist/data/openers_3b.csv","w") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def S(x):x=np.array(x,float);return f"median {np.median(x):.1f} IQR {np.percentile(x,25):.1f}-{np.percentile(x,75):.1f}"
for c in ["a15_edits_0_3s","eye_edits_0_3s","eye_beats_0_3s","first_caption_f","captions_started_0_3s","detector_events_0_3s"]:print(c,S([r[c] for r in rows]))
import collections
print("beats dist",collections.Counter(r["eye_beats_0_3s"] for r in rows),"edits dist",collections.Counter(r["eye_edits_0_3s"] for r in rows))
print("edits>=1",sum(r["eye_edits_0_3s"]>=1 for r in rows),"beats>=1",sum(r["eye_beats_0_3s"]>=1 for r in rows),"beats>=2",sum(r["eye_beats_0_3s"]>=2 for r in rows))
print("cap f<=1",sum(r["caption_at_f0_or_f1"] for r in rows),"f0 mid-action",sum(r["frame0"]=="mid-action" for r in rows))
for m in("quick","stage"):
    s=[r for r in rows if r["a19_mode"]==m];print(m,len(s),"edits",S([r["eye_edits_0_3s"] for r in s]),"beats",S([r["eye_beats_0_3s"] for r in s]),"beats>=1",sum(r["eye_beats_0_3s"]>=1 for r in s),"beats>=2",sum(r["eye_beats_0_3s"]>=2 for r in s),"a15edits>=1",sum(r["a15_edits_0_3s"]>=1 for r in s))
print("disagree a15 vs eye edits",[(r["key"],r["a15_edits_0_3s"],r["eye_edits_0_3s"]) for r in rows if r["a15_edits_0_3s"]!=r["eye_edits_0_3s"]])
print("quick-mode with B>=1 vs stage",sum(r["eye_beats_0_3s"]>=1 for r in rows if r["a19_mode"]=="quick"))
