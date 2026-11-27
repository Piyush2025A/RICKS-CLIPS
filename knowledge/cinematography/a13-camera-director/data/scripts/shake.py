from moves import *
from scipy.signal import welch
import collections
rows=[];events=[]
for k in keys():
    d,sm,bad,labels,cands,moves=analyse(k)
    ok=~bad
    hp=np.full_like(d,np.nan)
    for a,b in runs(ok,15):
        hp[a:b]=d[a:b]-uniform_filter1d(d[a:b],5,axis=0,mode='nearest')
    quiet=(labels=='hold')|(labels=='creep')
    h=hp[quiet]
    rms=np.sqrt(np.nanmean(h**2,0))      # tx,ty %W ; scale %; rot deg
    # lag-1 autocorr of hp in quiet runs (negative = alternating jitter)
    # power >5Hz fraction
    fr=[];
    for a,b in runs(quiet,48):
        x=d[a:b,0]-np.mean(d[a:b,0]); f,P=welch(x,fs=30,nperseg=32); fr.append(P[f>=5].sum()/max(P.sum(),1e-12))
    # events: |hp tx| or ty > 0.8 %W with >=3 sign alternations in 12 frames, all frames
    ev=0
    mag=np.hypot(hp[:,0],hp[:,1])
    i=0
    while i<len(d)-12:
        w=hp[i:i+12,:2]
        if np.isnan(w).any(): i+=1; continue
        found=False
        for c in (0,1):
            sg=np.sign(w[:,c])*(np.abs(w[:,c])>0.5)
            ch=np.sum(sg[1:]*sg[:-1]<0)
            if ch>=3 and np.abs(w[:,c]).max()>=1.0: found=True
        if found:
            events.append((k,i,i+12,float(np.abs(w).max()))); i+=12
        else: i+=1
    rows.append(dict(key=k,quiet_frames=int(quiet.sum()),rms_tx_pctW=float(rms[0]),rms_ty_pctW=float(rms[1]),rms_scale=float(rms[2]),rms_rot=float(rms[3]),hf5_frac_med=float(np.median(fr)) if fr else None,n_psd=len(fr),n_events=sum(1 for e in events if e[0]==k)))
    print(rows[-1])
json.dump(rows,open('shake_summary.json','w')); json.dump(events,open('shake_events.json','w'))
r=np.array([[x['rms_tx_pctW'],x['rms_ty_pctW'],x['rms_scale'],x['rms_rot']] for x in rows])
print('rms median',np.median(r,0),'iqr',np.percentile(r,[25,75],axis=0)); print('native px per frame tx',np.median(r[:,0])*10.8)
print('events total',len(events), 'videos',len(set(e[0] for e in events)))
