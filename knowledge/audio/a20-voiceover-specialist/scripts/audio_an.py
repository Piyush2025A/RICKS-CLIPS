import sys, subprocess, json, re, numpy as np
from scipy import signal
import librosa
n=sys.argv[1]
mp4=f"/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4"
out={}
# 1 loudness (native stream)
r=subprocess.run(["ffmpeg","-nostats","-hide_banner","-i",mp4,"-map","0:a","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
s=r[r.rfind("Summary:"):]
g=lambda pat: float(re.search(pat,s).group(1))
out["lufs_i"]=g(r"I:\s+(-?[\d.]+) LUFS"); out["lra"]=g(r"LRA:\s+([\d.]+) LU"); out["tp"]=g(r"Peak:\s+(-?[\d.]+) dBFS")
# 2 stereo from native decode, piped (no temp file)
raw=subprocess.run(["ffmpeg","-v","error","-i",mp4,"-map","0:a","-f","f32le","-ac","2","-ar","44100","-"],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64)
L,R=x[:,0],x[:,1]
db=lambda v:20*np.log10(max(v,1e-12))
rms=lambda v:np.sqrt(np.mean(v**2))
M=(L+R)/2;S=(L-R)/2
out["dur"]=len(L)/44100
out["L_rms_db"]=db(rms(L));out["R_rms_db"]=db(rms(R));out["side_rms_db"]=db(rms(S));out["mid_rms_db"]=db(rms(M))
out["side_minus_mid_db"]=out["side_rms_db"]-out["mid_rms_db"]
out["lr_corr"]=float(np.corrcoef(L,R)[0,1]) if rms(L)>0 and rms(R)>0 else None
# 3 mono 16k for speech analysis (from native 44.1 mid)
y=librosa.resample(M,orig_sr=44100,target_sr=16000,res_type="soxr_hq").astype(np.float32)
sr=16000
def bp(y,lo,hi):
    sos=signal.butter(4,[lo,hi],btype="band",fs=sr,output="sos");return signal.sosfiltfilt(sos,y)
hop=160  # 10 ms
def env_db(z,win=480):
    p=np.convolve(z**2,np.ones(win)/win,mode="same")[::hop]
    return 10*np.log10(p+1e-12)
sp=bp(y,300,3400)
e_sp=env_db(sp,800)  # 50 ms
low=bp(y,35,110); e_low=env_db(low,1600)
hi=bp(y,4000,7500); e_hi=env_db(hi,800)
t=np.arange(len(e_sp))*0.01
# activity threshold: Otsu on dB env
def otsu(v):
    h,b=np.histogram(v,bins=100);c=(b[:-1]+b[1:])/2;w0=np.cumsum(h);w1=w0[-1]-w0
    m0=np.cumsum(h*c)/np.maximum(w0,1);m1=(np.sum(h*c)-np.cumsum(h*c))/np.maximum(w1,1)
    return c[np.argmax(w0*w1*(m0-m1)**2)]
thr=otsu(e_sp[10:-10]); act=e_sp>thr
out["otsu_db"]=float(thr)
out["active_frac"]=float(act.mean())
out["sp_active_db_med"]=float(np.median(e_sp[act]));out["sp_pause_db_med"]=float(np.median(e_sp[~act])) if (~act).any() else None
out["vo_bed_diff_db"]=None if out["sp_pause_db_med"] is None else out["sp_active_db_med"]-out["sp_pause_db_med"]
out["sp_active_p90"]=float(np.percentile(e_sp[act],90));out["sp_pause_p90"]=float(np.percentile(e_sp[~act],90)) if (~act).any() else None
out["low_active_db"]=float(np.median(e_low[act]));out["low_pause_db"]=float(np.median(e_low[~act])) if (~act).any() else None
out["hi_active_db"]=float(np.median(e_hi[act]));out["hi_pause_db"]=float(np.median(e_hi[~act])) if (~act).any() else None
# gaps: runs of ~act, closed-opened with min length 150 ms; ignore leading/trailing
runs=[];i=0;N=len(act)
while i<N:
    if not act[i]:
        j=i
        while j<N and not act[j]:j+=1
        runs.append((i*0.01,(j-i)*0.01,i==0,j==N));i=j
    else:i+=1
gaps=[d for (st,d,a,b) in runs if not a and not b and d>=0.15-1e-9]
out["gaps"]=gaps;out["n_gaps"]=len(gaps)
out["lead_silence"]=runs[0][1] if runs and runs[0][2] else 0.0
out["first_active_s"]=float(np.argmax(act)*0.01)
out["pause_total_gt025"]=float(sum(d for d in gaps if d>0.25))
# syllable-rate proxy: peaks of smoothed speech-band envelope
a=np.sqrt(np.abs(signal.sosfiltfilt(signal.butter(2,10,fs=100,output="sos"),10**(e_sp/20))))
# use linear envelope of speech band: abs then lowpass
ev=np.abs(signal.hilbert(sp)); ev=signal.sosfiltfilt(signal.butter(2,10,fs=sr,output="sos"),ev)[::hop]
ev=np.maximum(ev,0);evdb=20*np.log10(ev+1e-9)
pk,pr=signal.find_peaks(evdb,distance=8,prominence=3.0)
pk=[p for p in pk if act[min(p,N-1)]]
out["syl_peaks"]=len(pk)
out["syl_rate_overall"]=len(pk)/out["dur"]
act_t=act.sum()*0.01
out["syl_rate_active"]=len(pk)/act_t
# modulation spectrum peak 2-10 Hz of linear env in active
e2=ev-ev.mean(); f,P=signal.welch(e2,fs=100,nperseg=512)
sel=(f>=2)&(f<=10); out["mod_peak_hz"]=float(f[sel][np.argmax(P[sel])])
out["peak_times"]=[round(float(p*0.01),2) for p in pk]
# phrases: split at gaps >=0.3 s
act_idx=np.where(act)[0]
phr=[];st=None;prev=None
for i in act_idx:
    if st is None: st=i;prev=i
    elif (i-prev)*0.01>0.3: phr.append((st,prev));st=i;prev=i
    else: prev=i
if st is not None: phr.append((st,prev))
out["phrases"]=[(round(a*0.01,2),round((b-a)*0.01,2),int(sum(1 for p in pk if a<=p<=b))) for a,b in phr]
# LTAS 1/3 oct (active) 100-7000
S_=np.abs(librosa.stft(y,n_fft=1024,hop_length=160))**2
fr=librosa.fft_frequencies(sr=sr,n_fft=1024)
m=min(S_.shape[1],len(act));A=act[:m]
cent=librosa.feature.spectral_centroid(S=np.sqrt(S_),sr=sr)[0][:m]
out["centroid_active_med"]=float(np.median(cent[A]));out["centroid_pause_med"]=float(np.median(cent[~A])) if (~A).any() else None
cen=[100*2**(k/3) for k in range(0,19)]
ltas=[]
for c in cen:
    sel=(fr>=c/2**(1/6))&(fr<c*2**(1/6));ltas.append(float(10*np.log10(S_[sel][:,:m][:,A].mean()+1e-12)))
out["ltas_cf"]=[round(c) for c in cen];out["ltas_active_db"]=ltas
# pitch
yp=y
f0,vf,vp=librosa.pyin(yp,fmin=65,fmax=450,sr=sr,frame_length=1024,hop_length=320,fill_na=np.nan)
tt=np.arange(len(f0))*0.02
ai=np.clip((tt/0.01).astype(int),0,N-1)
good=vf&act[ai]&~np.isnan(f0)
out['f0_voiced_pause_frac']=float((vf&~act[ai]&~np.isnan(f0)).sum()/max(1,(~act[ai]).sum()))
out['pyin_vp_median_active']=float(np.median(vp[act[ai]]))
out["f0_n_frames"]=int(good.sum());out["f0_voiced_active_frac"]=float(good.sum()/max(1,(act[ai]).sum()))
if good.sum()>20:
    ff=f0[good]
    # median filter on the sequence of good frames
    ffm=signal.medfilt(ff,5)
    out["f0_med"]=float(np.median(ffm));out["f0_p10"]=float(np.percentile(ffm,10));out["f0_p90"]=float(np.percentile(ffm,90))
    out["f0_iqr"]=[float(np.percentile(ffm,25)),float(np.percentile(ffm,75))]
    out["f0_range_semitones_p10_p90"]=float(12*np.log2(out["f0_p90"]/out["f0_p10"]))
    out["f0_std_semitones"]=float(np.std(12*np.log2(ffm/np.median(ffm))))
    np.save(f"f0_{n}.npy",np.stack([tt[good],f0[good]]))
json.dump(out,open(f"aud_{n}.json","w"))
print(n,"done",out["lufs_i"],out.get("f0_med"))
