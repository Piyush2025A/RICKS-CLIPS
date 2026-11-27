"""A22 per-video music/mix analysis, native 44.1k stereo decoded in memory. usage: a22_an.py NN  -> data/pv/NN.json"""
import sys, subprocess, json, numpy as np, librosa
from scipy import signal
n=sys.argv[1]; SR=44100
mp4=f"/home/piyush/ricks-clips-private/reference-videos/RC30/{int(n)}.mp4"
raw=subprocess.run(["ffmpeg","-v","error","-i",mp4,"-map","0:a","-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64)
L,R=x[:,0],x[:,1]; M=(L+R)/2; S=(L-R)/2
out={"key":n,"dur":len(M)/SR,"stft_db_offset_to_dbfs_ms":-58.96}
db=lambda v:20*np.log10(max(v,1e-12))
rms=lambda v:np.sqrt(np.mean(v**2))
# crest / peak
out["mid_rms_db"]=db(rms(M)); out["mid_peak_db"]=db(np.abs(M).max()); out["crest_db"]=out["mid_peak_db"]-out["mid_rms_db"]
out["samplepeak_lr_db"]=db(max(np.abs(L).max(),np.abs(R).max()))
# fraction of samples within 0.5 dB of the peak (limiter flat-tops)
pk=np.abs(M).max(); out["near_peak_frac"]=float(np.mean(np.abs(M)>pk*10**(-0.5/20)))
# --- 22.05k working signals
M2=librosa.resample(M,orig_sr=SR,target_sr=22050,res_type="soxr_hq"); S2=librosa.resample(S,orig_sr=SR,target_sr=22050,res_type="soxr_hq"); sr=22050
hop=441  # 20 ms
def stft_pow(z): return np.abs(librosa.stft(z,n_fft=2048,hop_length=hop,center=True))**2
PM=stft_pow(M2); PS=stft_pow(S2)
f=librosa.fft_frequencies(sr=sr,n_fft=2048); T=PM.shape[1]; t=np.arange(T)*hop/sr
# speech activity (A20-style): 300-3400 Hz band power of mid, 50ms smoothing, Otsu
bi=(f>=300)&(f<=3400)
e_sp=10*np.log10(np.convolve(PM[bi].sum(0),np.ones(3)/3,mode="same")+1e-12)
def otsu(v):
    h,b=np.histogram(v,bins=100);c=(b[:-1]+b[1:])/2;w0=np.cumsum(h);w1=w0[-1]-w0
    m0=np.cumsum(h*c)/np.maximum(w0,1);m1=(np.sum(h*c)-np.cumsum(h*c))/np.maximum(w1,1)
    return c[np.argmax(w0*w1*(m0-m1)**2)]
thr=otsu(e_sp[5:-5]); act=e_sp>thr
# close tiny holes <100ms, drop blips
from scipy.ndimage import binary_closing, binary_opening
act=binary_opening(binary_closing(act,np.ones(5)),np.ones(3))
out["active_frac"]=float(act.mean())
# onsets/offsets
d=np.diff(act.astype(int)); ons=np.where(d==1)[0]+1; offs=np.where(d==-1)[0]+1
out["n_on"]=int(len(ons)); out["n_off"]=int(len(offs))
# gap mask: inactive frames in runs >=150ms (>=8 frames), not head/tail
gap=np.zeros(T,bool); i=0
while i<T:
    if not act[i]:
        j=i
        while j<T and not act[j]: j+=1
        if i>0 and j<T and (j-i)>=8: gap[i+1:j-1]=True
        i=j
    else: i+=1
out["gap_frames"]=int(gap.sum())
# band levels (dB re full-scale-ish) in mid and side: sub<100, low 100-400, mid 400-2k, hi 2k-8k
bands={"sub":(30,100),"low":(100,400),"mid":(400,2000),"hi":(2000,8000)}
def bl(P,mask,lo,hi):
    b=(f>=lo)&(f<hi); return 10*np.log10(P[b][:,mask].sum(0).mean()+1e-15)
for nm,(lo,hi) in bands.items():
    for ch,P in (("M",PM),("S",PS)):
        out[f"{ch}_{nm}_act"]=bl(P,act,lo,hi)
        out[f"{ch}_{nm}_gap"]=bl(P,gap,lo,hi) if gap.any() else None
out["M_full_act"]=10*np.log10(PM[:,act].sum(0).mean()+1e-15); out["M_full_gap"]=10*np.log10(PM[:,gap].sum(0).mean()+1e-15) if gap.any() else None
out["S_full_act"]=10*np.log10(PS[:,act].sum(0).mean()+1e-15); out["S_full_gap"]=10*np.log10(PS[:,gap].sum(0).mean()+1e-15) if gap.any() else None
# side timeline 1 s
sdb=10*np.log10(PS.sum(0)+1e-15); mdb=10*np.log10(PM.sum(0)+1e-15)
nsec=int(T*hop/sr)
sec_side=[float(np.median(sdb[int(k*sr/hop):int((k+1)*sr/hop)])) for k in range(nsec)]
sec_mid=[float(np.median(mdb[int(k*sr/hop):int((k+1)*sr/hop)])) for k in range(nsec)]
out["sec_side_db"]=sec_side; out["sec_mid_db"]=sec_mid
ss=np.array(sec_side); out["side_med_db"]=float(np.median(ss)); out["side_p10"]=float(np.percentile(ss,10)); out["side_p90"]=float(np.percentile(ss,90))
out["side_frac_below_-90dB"]=float(np.mean(sdb<-31))
# side tonal-ness: spectral flatness of side in frames above -80
ok=sdb>-21
fl=librosa.feature.spectral_flatness(S=np.sqrt(PS),n_fft=2048)[0]
out["side_flat_med"]=float(np.median(fl[ok])) if ok.any() else None
out["side_ok_frac"]=float(ok.mean())
# ---- tempo / loop on side (and mid-gap fallback not meaningful)
def tempo_feat(z,label):
    o=librosa.onset.onset_strength(y=z,sr=sr,hop_length=hop,n_fft=2048)
    if o.std()<1e-9: return None
    tempo,beats=librosa.beat.beat_track(onset_envelope=o,sr=sr,hop_length=hop,start_bpm=100)
    tempo=float(np.atleast_1d(tempo)[0])
    # autocorr of onset env -> BPM peaks, confidence = peak/mean in 40-200 bpm
    oc=o-o.mean(); ac=np.correlate(oc,oc,"full")[len(oc)-1:]; ac/=ac[0]+1e-12
    lags=np.arange(len(ac))*hop/sr
    sel=(lags>=60/200)&(lags<=60/40)
    k=np.argmax(ac[sel]); lag=lags[sel][k]; conf=float(ac[sel][k])
    # beat regularity
    bt=librosa.frames_to_time(beats,sr=sr,hop_length=hop)
    ibi=np.diff(bt); reg=float(np.std(ibi)/np.mean(ibi)) if len(ibi)>3 else None
    return {"beat_tempo":tempo,"ac_bpm":float(60/lag),"ac_conf":conf,"n_beats":int(len(beats)),"ibi_cv":reg,"onset_mean":float(o.mean())}
out["tempo_side"]=tempo_feat(S2,"side")
# chroma from side
C=librosa.feature.chroma_stft(S=PS,sr=sr,n_fft=2048,hop_length=hop,tuning=0.0)
w=(sdb>-21)
out["chroma_n_frames"]=int(w.sum())
if w.sum()>50:
    cm=C[:,w].mean(1); cm=cm/cm.sum(); out["chroma_mean"]=cm.tolist()
    maj=np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); mnr=np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
    best=[]
    for mode,p in (("maj",maj),("min",mnr)):
        for k in range(12): best.append((np.corrcoef(cm,np.roll(p,k))[0,1],k,mode))
    best.sort(reverse=True); out["key_top"]=[(float(a),int(b),c) for a,b,c in best[:3]]
    # chroma self-similarity loop: autocorr of chroma frames (1-12 s), smooth to 100 ms
    Cs=librosa.util.normalize(C,axis=0); Cs=Cs[:,:]
    Cd=Cs-Cs.mean(1,keepdims=True)
    # autocorrelation via FFT
    F=np.fft.rfft(Cd,n=2*Cd.shape[1],axis=1); acc=np.fft.irfft(F*np.conj(F),axis=1)[:,:Cd.shape[1]].sum(0)
    acc=acc/ (acc[0]+1e-12)
    lg=np.arange(len(acc))*hop/sr; sel=(lg>=1.0)&(lg<=min(15,out["dur"]/2))
    pk,_=signal.find_peaks(acc[sel],prominence=0.03)
    cand=sorted([(float(acc[sel][p]),float(lg[sel][p])) for p in pk],reverse=True)[:4]
    out["loop_cands"]=cand
    # timbre
    cen=librosa.feature.spectral_centroid(S=np.sqrt(PS),sr=sr,n_fft=2048)[0]
    out["side_centroid_med"]=float(np.median(cen[w]))
    ro=librosa.feature.spectral_rolloff(S=np.sqrt(PS),sr=sr,roll_percent=0.85)[0]; out["side_rolloff85_med"]=float(np.median(ro[w]))
    # percussive vs harmonic on side STFT
    Sc=librosa.stft(S2,n_fft=2048,hop_length=hop); H,Pc=librosa.decompose.hpss(np.abs(Sc),margin=1.0)
    out["side_hp_ratio_db"]=float(10*np.log10((H[:,w]**2).sum()/((Pc[:,w]**2).sum()+1e-15)))
    # onset sharpness: median onset-strength peak/ mean
    o=librosa.onset.onset_strength(S=librosa.power_to_db(PS+1e-12),sr=sr); out["side_onset_peak_over_mean"]=float(np.percentile(o[w[:len(o)]],95)/(o[w[:len(o)]].mean()+1e-9)) if w.sum()>0 else None
# ---- ducking: event-triggered average of side level (dB) around speech onsets/offsets vs shuffled control
rng=np.random.default_rng(22)
win=np.arange(-25,26)  # +-0.5s at 20ms
def eta(sig,ev):
    ev=[e for e in ev if e+win[0]>=0 and e+win[-1]<len(sig)]
    if len(ev)<5: return None
    A=np.array([sig[e+win] for e in ev]); A=A-A[:,:10].mean(1,keepdims=True)  # baseline: -500..-300ms
    return A.mean(0)
# pre-event baselines relative; for onsets baseline is the gap (pre) so effect = post-pre
# low-voice-leak signals: side full band; mid low band 35-150
bl_low=10*np.log10(PM[(f>=35)&(f<150)].sum(0)+1e-15)
res={}
for nm,sig in (("side",sdb),("midlow",bl_low)):
    for evn,ev in (("on",ons),("off",offs)):
        e=eta(sig,list(ev))
        if e is None: continue
        ctrl=[]
        for _ in range(100):
            fake=rng.integers(30,T-30,size=len(ev)); c=eta(sig,list(fake)); 
            if c is not None: ctrl.append(c)
        ctrl=np.array(ctrl)
        res[f"{nm}_{evn}"]={"eta":e.tolist(),"ctrl_mean":ctrl.mean(0).tolist(),"ctrl_sd":ctrl.std(0).tolist(),"n":int(len(ev))}
out["eta"]=res
# scalar duck: side level during speech vs gap (same video), in dB; and mid-low
out["side_act_minus_gap_db"]=(10*np.log10(PS[:,act].sum(0).mean()+1e-15)-10*np.log10(PS[:,gap].sum(0).mean()+1e-15)) if gap.any() else None
# ---- novelty on side chroma+mfcc -> peaks (times)
mf=librosa.feature.mfcc(S=librosa.power_to_db(librosa.feature.melspectrogram(S=PS,sr=sr)+1e-12),n_mfcc=13)
Z=np.vstack([librosa.util.normalize(C,axis=0)*3,(mf-mf.mean(1,keepdims=True))/(mf.std(1,keepdims=True)+1e-9)])
Z=signal.savgol_filter(Z,9,1,axis=1)
k=25; nov=np.zeros(Z.shape[1])
for i in range(k,Z.shape[1]-k): nov[i]=np.linalg.norm(Z[:,i:i+k].mean(1)-Z[:,i-k:i].mean(1))
out["nov"]=[float(v) for v in nov[::5]]  # 100ms
np.save(f"/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a22-music-mixing-specialist/nov_{n}.npy",nov)
np.save(f"/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a22-music-mixing-specialist/act_{n}.npy",act)
# ---- ending: last 3 s mid & side level vs median
tail=int(3*sr/hop); out["end_mid_db"]=float(np.median(mdb[-tail:])); out["end_side_db"]=float(np.median(sdb[-tail:]))
out["last_voice_t"]=float(t[np.where(act)[0][-1]]) if act.any() else None
# ---- LTAS mid (Welch), 1/3 octave bands dB rel total
fw,pw=signal.welch(M,fs=SR,nperseg=8192)
cf=[31.5*2**(k/3) for k in range(0,25) if 31.5*2**(k/3)<18000]
tot=pw.sum()
out["ltas_third"]={f"{c:.0f}":float(10*np.log10(pw[(fw>=c/2**(1/6))&(fw<c*2**(1/6))].sum()/tot+1e-15)) for c in cf}
fw,pw=signal.welch(S,fs=SR,nperseg=8192)
out["ltas_side_third"]={f"{c:.0f}":float(10*np.log10(pw[(fw>=c/2**(1/6))&(fw<c*2**(1/6))].sum()/tot+1e-15)) for c in cf}
import os; os.makedirs("/home/piyush/RICKS-CLIPS/knowledge/audio/a22-music-mixing-specialist/data/pv",exist_ok=True)
json.dump(out,open(f"/home/piyush/RICKS-CLIPS/knowledge/audio/a22-music-mixing-specialist/data/pv/{n}.json","w"))
print(n,"ok",round(out["dur"],1),out["side_med_db"],out.get("key_top",[None])[0],out["tempo_side"])
