"""ducking test on bass band (30-90 Hz, mid) and side band 300-3000, onsets/offsets of speech vs shuffled controls; 20 ms hop"""
import sys,subprocess,json,numpy as np,librosa
n=sys.argv[1]; SR=44100
P="/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a22-music-mixing-specialist/"
raw=subprocess.run(["ffmpeg","-v","error","-i",f"/home/piyush/ricks-clips-private/reference-videos/RC30/{int(n)}.mp4","-map","0:a","-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64); M=(x[:,0]+x[:,1])/2; S=(x[:,0]-x[:,1])/2
act=np.load(P+f"act_{n}.npy"); hop=441
f=librosa.fft_frequencies(sr=SR,n_fft=4096)
def band(z,lo,hi):
    P_=np.abs(librosa.stft(z,n_fft=4096,hop_length=hop))**2; b=(f>=lo)&(f<hi); return 10*np.log10(P_[b].sum(0)+1e-15)
T=min(len(act),band(M,30,90).shape[0]); act=act[:T]
d=np.diff(act.astype(int)); ons=np.where(d==1)[0]+1; offs=np.where(d==-1)[0]+1
win=np.arange(-50,51); rng=np.random.default_rng(7)
def eta(sig,ev):
    ev=[e for e in ev if e+win[0]>=0 and e+win[-1]<T]
    if len(ev)<5:return None
    A=np.array([sig[e+win] for e in ev]); return (A-A[:,:15].mean(1,keepdims=True)).mean(0)
out={"key":n}
for nm,sig in (("bass_M",band(M,30,90)),("side_mid",band(S,300,3000)),("side_bass",band(S,30,150))):
    sig=sig[:T]
    out[f"lev_act_minus_gap_{nm}"]=float(10*np.log10((10**(sig[act]/10)).mean())-10*np.log10((10**(sig[~act]/10)).mean()))
    for evn,ev in (("on",ons),("off",offs)):
        e=eta(sig,list(ev))
        if e is None: continue
        c=np.array([eta(sig,list(rng.integers(60,T-60,len(ev)))) for _ in range(100)])
        out[f"{nm}_{evn}"]={"eta":e.tolist(),"ctrl_mean":c.mean(0).tolist(),"ctrl_sd":c.std(0).tolist(),"n":len(ev)}
# dropout fraction of side bed: 1 s windows below median-6 dB
sd=band(S,100,4000)[:T]; sec=np.array([np.median(sd[i:i+50]) for i in range(0,T-50,50)])
out["side_dropout_frac_6dB"]=float(np.mean(sec<np.median(sec)-6)); out["side_sec_sd"]=float(sec.std())
json.dump(out,open(f"/home/piyush/RICKS-CLIPS/knowledge/audio/a22-music-mixing-specialist/data/pv/duck_{n}.json","w")); print(n,"ok")
