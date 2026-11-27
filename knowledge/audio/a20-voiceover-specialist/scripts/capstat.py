import numpy as np,json,csv,sys
sys.path.insert(0,'.')
from capev import events
x=json.load(open('xcorr.json'))
WPT=1.16
rows=[]
for n in range(1,31):
    a=np.load(f"capser_{n}.npy");ev=np.array(events(a));au=json.load(open(f'aud_{n}.json'))
    t=(ev+1)/30; dt=np.diff(t)
    span=t[-1]-t[0]
    rate=(len(ev)-1)/span
    # tokens in first 3 s
    f3=int(((t>=0)&(t<3)).sum())
    # syl peaks within same span
    pk=np.array(au['peak_times']);ns=int(((pk>=t[0])&(pk<=t[-1])).sum())
    rows.append(dict(key=f"RC30-{n:02d}",events=len(ev),first_event_s=round(t[0],2),last_event_s=round(t[-1],2),tokens_per_s=round(rate,2),words_per_s_est=round(rate*WPT,2),
      token_dt_med_ms=int(np.median(dt)*1000),token_dt_p25_ms=int(np.percentile(dt,25)*1000),token_dt_p75_ms=int(np.percentile(dt,75)*1000),token_dt_p90_ms=int(np.percentile(dt,90)*1000),
      events_first3s=f3,syl_peaks_per_s_same_span=round(ns/span,2),syl_per_token=round(ns/(len(ev)-1),2),
      cap_lead_audio_ms=x[str(n)]['peak_lag_ms'],xcorr_z=round(x[str(n)]['peak_z'],1)))
w=csv.DictWriter(open('/home/piyush/RICKS-CLIPS/knowledge/audio/a20-voiceover-specialist/data/caption_tokens_per_video.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def st(k):
    v=np.array([r[k] for r in rows],float);return k,[round(float(q),2) for q in (np.median(v),np.percentile(v,25),np.percentile(v,75),v.min(),v.max())]
for k in ['events','first_event_s','tokens_per_s','words_per_s_est','token_dt_med_ms','token_dt_p90_ms','events_first3s','syl_peaks_per_s_same_span','syl_per_token','cap_lead_audio_ms','xcorr_z']:print(st(k))
r=np.corrcoef([r['tokens_per_s'] for r in rows],[r['syl_peaks_per_s_same_span'] for r in rows])[0,1];print('corr tokens/s vs syl/s',r)
alldt=np.concatenate([np.diff((np.array(events(np.load(f"capser_{n}.npy")))+1)/30) for n in range(1,31)])
print(len(alldt),np.percentile(alldt,[5,10,25,50,75,90,95,99]).round(3))
print([(r['key'],r['tokens_per_s']) for r in rows if r['tokens_per_s']>3.2 or r['tokens_per_s']<2.4])
