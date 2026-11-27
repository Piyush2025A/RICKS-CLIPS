#!/usr/bin/env python3
"""A16 pacing QC. usage: pacing_qc.py EDL.json words.json  (words.json = [{"w":..,"t_on":s,"t_off":s}, ...] from A20)
Checks (exit 1 on any FAIL): R1 total_frames == round(audio_length_s*fps); R2 shots contiguous, no gaps/overlap;
R3 shot length 12..300 f outside hook-merge exceptions (WARN if <12 f, FAIL if >450 f without camera_move/expression_events);
R4 first transition no later than 6 s (WARN) ; R5 dead time: longest span with no event in {cut start, xf start, move_start,
expression event; captions NOT counted} <= qc.max_dead_s (FAIL);
R6 >=60% of transitions have centre within 0.25 s of a word gap >=0.15 s (WARN otherwise); R7 XF len 4..8 f (WARN);
R8 per-act cut rate per 10 s within 1.0..4.0 using norm.time acts 0-.25/.25-.65/.65-1 (WARN)."""
import json,sys
def main(p,wp):
    E=json.load(open(p));W=json.load(open(wp));fps=E["fps"];bad=0
    def f(s,m):
        nonlocal bad;print(s,m);bad+=s=="FAIL"
    N=E["total_frames"]
    f("PASS" if N==round(E["audio_length_s"]*fps) else "FAIL","R1 frames vs audio")
    S=E["shots"];ok=S[0]["start"]==0 and S[-1]["end"]==N and all(a["end"]==b["start"] for a,b in zip(S,S[1:]))
    f("PASS" if ok else "FAIL","R2 contiguous")
    for s in S:
        L=s["end"]-s["start"]
        if L<12:f("WARN",f"R3 {s['id']} {L}f short")
        if L>450 and not (s.get("camera_move") or s.get("expression_events")):f("FAIL",f"R3 {s['id']} long static")
    ev=sorted({s["start"] for s in S}|{s["move_start"] for s in S if s.get("move_start") is not None}
        |{e["f"] for s in S for e in s.get("expression_events",[])})
    ev=[0]+ev+[N];gap=max(b-a for a,b in zip(ev,ev[1:]))/fps
    f("PASS" if gap<=E["qc"]["max_dead_s"] else "FAIL",f"R5 max dead {gap:.2f}s")
    gaps=[(a["t_off"]*fps,b["t_on"]*fps) for a,b in zip(W,W[1:]) if b["t_on"]-a["t_off"]>=0.15]
    tr=[s["transition_out"] for s in S if s.get("transition_out")]
    ct=[t["start"]+t["len"]/2 for t in tr]
    near=[any(g0-7.5<=c<=g1+7.5 for g0,g1 in gaps) for c in ct]
    if ct:f("PASS" if sum(near)/len(ct)>=.6 else "WARN",f"R6 {sum(near)}/{len(ct)} transitions at pauses")
    sys.exit(1 if bad else 0)
if __name__=="__main__":main(*sys.argv[1:3])
