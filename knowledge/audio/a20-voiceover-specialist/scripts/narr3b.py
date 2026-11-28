"""A20 Phase 3B: narration verification from private caption transcripts + A27 audio_env.csv.
Writes private caption_timeline.csv per video and committed data/narration_stats_3b.csv (numbers only).
Run: python3 narr3b.py"""
import csv,re,os,numpy as np,json
R=os.path.expanduser("~/ricks-clips-private/analysis-data/rc30")
OUT="/home/piyush/RICKS-CLIPS/knowledge/audio/a20-voiceover-specialist/data/narration_stats_3b.csv"
dur={r['key']:float(r['dur_s']) for r in csv.DictReader(open("/home/piyush/RICKS-CLIPS/knowledge/audio/a20-voiceover-specialist/data/audio_per_video.csv"))}
rows=[];pool={'sent_words':[],'gaps_final':[],'gaps_other':[],'lead':[]}
def q(a,p): return float(np.percentile(a,p)) if len(a) else float('nan')
for n in range(1,31):
    k=f"RC30-{n:02d}";p=f"{R}/captions/{k}"
    seg=list(csv.DictReader(open(p+"/caption_segments.csv")))
    txt={r['seg']:r['text'] for r in csv.DictReader(open(p+"/caption_text.csv"))}
    tl=[]
    for r in seg:
        t=txt.get(r['seg'],'?');a=float(r['t_start']);b=float(r['t_end'])
        if t.strip() in('?','#NONCAPTION'): tl.append([r['seg'],a,b,t,0]);continue
        if tl and tl[-1][3]==t and abs(a-tl[-1][2])<=0.04: tl[-1][2]=b;continue
        tl.append([r['seg'],a,b,t,len(t.split())])
    with open(p+"/caption_timeline.csv","w",newline="") as f:
        w=csv.writer(f);w.writerow("seg t_start t_end text words".split());w.writerows(tl)
    good=[x for x in tl if x[4]>0]
    W=sum(x[4] for x in good);t0=good[0][1];t1=good[-1][2];span=t1-t0
    gaps=[];fin=[];oth=[]
    for x,y in zip(good,good[1:]):
        g=y[1]-x[2];gaps.append(g)
        (fin if re.search(r'[.?!]["\']?$',x[3]) else oth).append(g)
    # sentences
    sw=[];c=0
    for x in good:
        c+=x[4]
        if re.search(r'[.?!]["\']?$',x[3]): sw.append(c);c=0
    if c: sw.append(c)
    # caption start-to-start interval
    st=np.diff([x[1] for x in good])
    # audio
    d=np.genfromtxt(f"{R}/v0.2.0/{k}/audio_env.csv",delimiter=",",names=True)
    on=d['onset_strength'].copy();on=on-np.convolve(on,np.ones(201)/201,'same');on/=on.std()
    T=len(on);ev=np.array([int(round(x[1]*100)) for x in good])
    lags=np.arange(-30,31)  # audio index = caption + lag ; positive lag => audio later
    def cc(ev):
        o=[]
        for L in lags:
            j=ev+L;j=j[(j>=0)&(j<T)];o.append(on[j].mean())
        return np.array(o)
    c0=cc(ev);rng=np.random.default_rng(1)
    nl=np.array([cc((ev+int(rng.integers(300,T-300)))%T) for _ in range(40)])
    z=(c0-nl.mean(0))/nl.std(0).mean();kk=int(np.argmax(c0))
    # centroid of positive part of curve within -10..+30 as robust alt
    lead_ms=int(lags[kk]*10)
    rows.append(dict(key=k,dur_s=dur[k],n_captions=len(good),words=W,words_per_caption=round(W/len(good),3),
      first_word_s=round(t0,3),first_word_frame=int(round(t0*30)),last_caption_end_s=round(t1,3),tail_s=round(dur[k]-t1,3),
      span_s=round(span,3),wps_span=round(W/span,3),wpm_span=round(W/span*60,1),
      caption_interval_med_ms=int(np.median(st)*1000),caption_dur_med_ms=int(np.median([x[2]-x[1] for x in good])*1000),
      gap_med_ms=int(np.median(gaps)*1000),frac_gap_gt100ms=round(float(np.mean(np.array(gaps)>0.1)),3),
      frac_gap_gt250ms=round(float(np.mean(np.array(gaps)>0.25)),3),pause_gt250_total_s=round(float(sum(g for g in gaps if g>0.25)),2),
      n_sentences=len(sw),sent_words_med=float(np.median(sw)),sent_words_max=max(sw),
      n_gap_after_final=len(fin),gap_after_final_med_ms=int(np.median(fin)*1000) if fin else -1,
      gap_other_med_ms=int(np.median(oth)*1000) if oth else -1,
      xcorr_peak_lag_ms=lead_ms,xcorr_z=round(float(z[kk]),1)))
    pool['sent_words']+=sw;pool['gaps_final']+=fin;pool['gaps_other']+=oth
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def S(c):
    a=np.array([r[c] for r in rows],float);return f"{c}: med {np.median(a):.3f} IQR {q(a,25):.3f}-{q(a,75):.3f} range {a.min():.3f}-{a.max():.3f}"
for c in ['n_captions','words','words_per_caption','first_word_s','first_word_frame','tail_s','wps_span','wpm_span','caption_interval_med_ms','caption_dur_med_ms','gap_med_ms','frac_gap_gt100ms','frac_gap_gt250ms','pause_gt250_total_s','n_sentences','sent_words_med','gap_after_final_med_ms','gap_other_med_ms','xcorr_peak_lag_ms','xcorr_z']: print(S(c))
sw=np.array(pool['sent_words']);print("pooled sentences",len(sw),np.median(sw),q(sw,25),q(sw,75),sw.min(),sw.max())
gf=np.array(pool['gaps_final']);go=np.array(pool['gaps_other']);print("pooled gaps final",len(gf),np.median(gf),q(gf,25),q(gf,75),q(gf,90),"other",len(go),np.median(go),q(go,25),q(go,75),q(go,90))
print("gap>0.1 final",np.mean(gf>0.1),"other",np.mean(go>0.1),"gap>0.25 final",np.mean(gf>0.25),"other",np.mean(go>0.25))
print("total words",sum(r['words'] for r in rows))
