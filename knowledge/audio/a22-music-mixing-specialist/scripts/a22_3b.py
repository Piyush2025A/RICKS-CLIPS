"""A22 Phase 3B: bed level (3 pause definitions), K-weighted LU, bass/air ducking, end swell, tempo null, track change.
usage: a22_3b.py NN -> data/pv3b/NN.json   (native stream decoded to 48 kHz f32 in memory)"""
import sys,subprocess,json,numpy as np,librosa
from scipy import signal
from scipy.ndimage import binary_closing,binary_opening
n=sys.argv[1]; SR=48000; H=480  # 10 ms
raw=subprocess.run(["ffmpeg","-v","error","-i",f"/home/piyush/ricks-clips-private/reference-videos/RC30/{int(n)}.mp4","-map","0:a","-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64); M=x.mean(1); S=(x[:,0]-x[:,1])/2
# K-weighting (BS.1770, 48 kHz coefficients)
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]
b2=[1,-2,1]; a2=[1,-1.99004745483398,0.99007225036621]
kw=lambda z: signal.lfilter(b2,a2,signal.lfilter(b1,a1,z))
K=[kw(x[:,0]),kw(x[:,1])]
nb=len(M)//H
ms=lambda z:(z[:nb*H].reshape(nb,H)**2).mean(1)
Kms=ms(K[0])+ms(K[1])   # BS.1770 channel sum
# 400 ms blocks (hop 10 ms) loudness
def lufs(p): return -0.691+10*np.log10(p+1e-14)
nfft=2048
P=lambda z:np.abs(librosa.stft(z,n_fft=nfft,hop_length=H,center=False))**2
PM=P(M); PS=P(S); f=librosa.fft_frequencies(sr=SR,n_fft=nfft); T=min(PM.shape[1],nb); PM=PM[:,:T]; PS=PS[:,:T]; Kms=Kms[:T]
bd=lambda Pw,lo,hi:Pw[(f>=lo)&(f<hi)].sum(0)
sp=10*np.log10(np.convolve(bd(PM,300,3400),np.ones(5)/5,'same')+1e-14)
def otsu(v):
    h,b=np.histogram(v,bins=100);c=(b[:-1]+b[1:])/2;w0=np.cumsum(h);w1=w0[-1]-w0
    m0=np.cumsum(h*c)/np.maximum(w0,1);m1=(np.sum(h*c)-np.cumsum(h*c))/np.maximum(w1,1)
    return c[np.argmax(w0*w1*(m0-m1)**2)]
thr=otsu(sp[10:-10]); act=binary_opening(binary_closing(sp>thr,np.ones(9)),np.ones(5))
def runs(mask,minlen):
    out=[];i=0
    while i<len(mask):
        if mask[i]:
            j=i
            while j<len(mask) and mask[j]:j+=1
            if j-i>=minlen: out.append((i,j))
            i=j
        else:i+=1
    return out
# definitions: A old (Otsu, inactive runs>=150ms, untrimmed, excluding head/tail 0.3 s);
# B trimmed 50 ms each side; C strict: sp < speech-median - 20 dB, runs>=150 ms, trimmed 30 ms
def mk(runs_,trim):
    m=np.zeros(T,bool)
    for a,b in runs_:
        a+=trim;b-=trim
        if b>a:m[a:b]=True
    m[:30]=False;m[-30:]=False;return m
inact=~act
gA=mk(runs(inact,15),0); gB=mk(runs(inact,15),5)
spmed=np.median(sp[act]); gC=mk(runs(sp<spmed-15,15),3)
vo=act.copy()
# eroded voiced (30 ms inside)
from scipy.ndimage import binary_erosion
vo=binary_erosion(act,np.ones(7))
mp=lambda z,m:10*np.log10(z[m].mean()+1e-14) if m.sum()>3 else np.nan
out={"key":n,"dur":len(M)/SR,"thr":float(thr),"active_frac":float(act.mean()),"speech_med_db":float(spmed)}
bands={"mid400_2000":(PM,400,2000),"bass30_90":(PM,30,90),"bass30_150":(PM,30,150),"air4k_8k":(PM,4000,8000),"mid150_400":(PM,150,400),"side400_2000":(PS,400,2000),"side_bass30_150":(PS,30,150),"mid_full":(PM,30,20000),"side_full":(PS,30,3900)}
for dn,g in (("A",gA),("B",gB),("C",gC)):
    out[f"n_pause_{dn}"]=len(runs(g,1)); out[f"pause_s_{dn}"]=float(g.sum()/100)
    for bn,(Pw,lo,hi) in bands.items():
        s=bd(Pw,lo,hi); out[f"{bn}_vo_minus_pause_{dn}"]=float(mp(s,vo)-mp(s,g))
        if dn=="B": out[f"{bn}_pauseP10_{dn}"]=float(mp(s,vo)-10*np.log10(np.percentile(s[g],10)+1e-14))
# cross channel
sm=bd(PM,400,2000);ss=bd(PS,400,2000)
out["vo_mid_minus_side_pause_B"]=float(mp(sm,vo)-mp(ss,gB))
# K-weighted LU: speech-active vs pause (B) vs integrated (ungated mean) ; 400 ms smoothing for stability not needed with mean power
out["K_speech_LUFS"]=float(lufs(Kms[vo].mean())); out["K_pause_LUFS_B"]=float(lufs(Kms[gB].mean()) if gB.sum()>3 else np.nan)
out["K_pause_LUFS_C"]=float(lufs(Kms[gC].mean()) if gC.sum()>3 else np.nan); out["K_all_LUFS_ungated"]=float(lufs(Kms.mean()))
# ducking on voice-free bands: per-pause local contrast: pause vs 300 ms voiced neighbours (paired), bass and air
def paired(s,g):
    d=[]
    for a,b in runs(g,1):
        L=act[max(0,a-35):max(0,a-5)];R=act[b+5:b+35]
        if L.all() and len(L)==30 and R.all() and len(R)==30:
            v=np.r_[s[a-35:a-5],s[b+5:b+35]].mean(); d.append(10*np.log10(v+1e-14)-10*np.log10(s[a:b].mean()+1e-14))
    return d
for bn in ("bass30_90","bass30_150","air4k_8k","side400_2000","side_bass30_150"):
    Pw=bands[bn][0];s=bd(Pw,bands[bn][1],bands[bn][2]); d=paired(s,gB)
    out[f"paired_{bn}_n"]=len(d); out[f"paired_{bn}_med"]=float(np.median(d)) if d else None
    out[f"paired_{bn}_mean"]=float(np.mean(d)) if d else None
    out[f"paired_{bn}_ci"]=[float(np.percentile(np.random.default_rng(1).choice(d,(1000,len(d))).mean(1),q)) for q in (2.5,97.5)] if len(d)>=5 else None
# end swell: side 60-1000 Hz, 100 ms frames (10 hop avg), last 4 s max minus body median; control: random 4 s windows
s=10*np.log10(np.convolve(bd(PS,60,1000),np.ones(10)/10,'same')+1e-14)[::10]; tt=np.arange(len(s))/10
body=np.median(s[(tt>3)&(tt<tt[-1]-4.5)]); last=s[tt>tt[-1]-4]; out["end_rise"]=float(last.max()-body); out["end_t_peak"]=float(tt[tt>tt[-1]-4][np.argmax(last)]); out["dur_s"]=float(tt[-1])
rng=np.random.default_rng(3); ctl=[]
for _ in range(300):
    a=rng.uniform(3,tt[-1]-8.5); w=s[(tt>=a)&(tt<a+4)]; ctl.append(w.max()-body)
out["end_ctl_p95"]=float(np.percentile(ctl,95)); out["end_last1s_minus_body"]=float(np.median(s[tt>tt[-1]-1])-body)
# duration of the swell: time above body+6 dB near the end
hi=s>body+6; e=np.where(hi&(tt>tt[-1]-4))[0]; out["end_above6_s"]=float(len(e)/10)
# tempo with block-shuffle null (side onset env, 10 ms)
Ssm=librosa.feature.melspectrogram(S=PS[:, :],sr=SR,n_mels=40) if False else None
oenv=librosa.onset.onset_strength(S=librosa.power_to_db(librosa.feature.melspectrogram(S=PS,sr=SR,n_mels=64,fmin=100,fmax=3900)),sr=SR,hop_length=H)
def acpk(o):
    o=o-o.mean(); a=np.correlate(o,o,'full')[len(o)-1:]; a/=a[0]+1e-12
    lag=np.arange(len(a))*0.01; m=(lag>=60/140)&(lag<=60/60); i=np.argmax(a[m]); return float(a[m][i]),float(60/lag[m][i])
pk,bpm=acpk(oenv); blk=100; nulls=[]
for _ in range(100):
    bl=[oenv[i:i+blk] for i in range(0,len(oenv),blk)]; rng.shuffle(bl); nulls.append(acpk(np.concatenate(bl))[0])
out["tempo_ac_peak"]=pk; out["tempo_bpm"]=bpm; out["tempo_null_mean"]=float(np.mean(nulls)); out["tempo_null_sd"]=float(np.std(nulls)); out["tempo_z"]=float((pk-np.mean(nulls))/(np.std(nulls)+1e-9))
# track change: side chroma over 6 s windows; cosine of adjacent window means
ch=librosa.feature.chroma_stft(S=PS[:,:],sr=SR,n_fft=nfft,hop_length=H) if False else librosa.feature.chroma_stft(S=PS,sr=SR)
W=600;mv=[ch[:,i:i+W].mean(1) for i in range(0,ch.shape[1]-W+1,W)]
cs=[float(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b)) for a,b in zip(mv[:-1],mv[1:])]
out["chroma_adjwin_cos_min"]=float(min(cs)) if cs else None; out["chroma_adjwin_cos_med"]=float(np.median(cs)) if cs else None
import os; os.makedirs("../data/pv3b",exist_ok=True); json.dump(out,open(f"../data/pv3b/{n}.json","w"),default=float); print(n,"ok")
