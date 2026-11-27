import numpy as np,json,subprocess,sys
from scipy import signal
sys.path.insert(0,'.')
from capev import events
res={}
rng=np.random.default_rng(0)
for n in range(1,31):
    mp4=f"/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4"
    raw=subprocess.run(["ffmpeg","-v","error","-i",mp4,"-map","0:a","-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
    y=np.frombuffer(raw,dtype=np.float32).astype(np.float64);sr=16000
    sos=signal.butter(4,[300,3400],btype="band",fs=sr,output="sos");sp=signal.sosfiltfilt(sos,y)
    env=signal.sosfiltfilt(signal.butter(2,30,fs=sr,output="sos"),np.abs(sp))[::160]  # 100 Hz
    le=np.log(np.maximum(env,1e-5)); on=np.maximum(np.diff(le,prepend=le[0]),0)
    on=signal.sosfiltfilt(signal.butter(2,15,fs=100,output="sos"),on); on=(on-on.mean())/on.std()
    a=np.load(f"capser_{n}.npy");ev=events(a)
    T=len(on);tr=np.zeros(T)
    for e in ev:
        t=int(round((e+0.5)/30*100))  # frame e center -> 10ms index (pts=(i+1)/30; audio starts 0): use (e+1)/30
        t=int(round((e+1)/30*100))
        if t<T: tr[t]=1
    lags=np.arange(-40,81)  # -400..+800ms: caption time = audio time + lag
    def cc(tr):
        out=[]
        for L in lags:
            # onset at time t+L paired with caption at t
            idx=np.where(tr>0)[0];j=idx+L;j=j[(j>=0)&(j<T)]
            out.append(on[j].mean())
        return np.array(out)
    c=cc(tr)
    # null: random circular shifts
    nulls=np.array([cc(np.roll(tr,int(rng.integers(300,T-300)))) for _ in range(20)])
    z=(c-nulls.mean(0))/nulls.std(0).mean()
    k=int(np.argmax(c));res[n]=dict(peak_lag_ms=int(lags[k]*10),peak_val=float(c[k]),peak_z=float(z[k]),n_events=len(ev),curve=[round(float(v),3) for v in c[::5]])
    print(n,res[n]['peak_lag_ms'],round(res[n]['peak_val'],2),round(res[n]['peak_z'],1),flush=True)
json.dump(res,open("xcorr.json","w"))
