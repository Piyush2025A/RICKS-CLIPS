# speech gaps (>=150 ms, Otsu on 50 ms speech-band dB env, same method as A20 audio_an.py) -> json with gap start/end times
import sys,subprocess,json,numpy as np
from scipy import signal
import librosa
out={}
for n in range(1,31):
    mp4=f"/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4"
    raw=subprocess.run(["ffmpeg","-v","error","-i",mp4,"-map","0:a","-f","f32le","-ac","2","-ar","44100","-"],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64);M=x.mean(1)
    y=librosa.resample(M,orig_sr=44100,target_sr=16000,res_type="soxr_hq").astype(np.float32)
    sos=signal.butter(4,[300,3400],btype="band",fs=16000,output="sos");sp=signal.sosfiltfilt(sos,y)
    p=np.convolve(sp**2,np.ones(800)/800,mode="same")[::160];e=10*np.log10(p+1e-12)
    v=e[10:-10];h,b=np.histogram(v,bins=100);c=(b[:-1]+b[1:])/2;w0=np.cumsum(h);w1=w0[-1]-w0
    m0=np.cumsum(h*c)/np.maximum(w0,1);m1=(np.sum(h*c)-np.cumsum(h*c))/np.maximum(w1,1)
    thr=c[np.argmax(w0*w1*(m0-m1)**2)];act=e>thr
    g=[];i=0;N=len(act)
    while i<N:
        if not act[i]:
            j=i
            while j<N and not act[j]:j+=1
            if i>0 and j<N and (j-i)*0.01>=0.15-1e-9:g.append((round(i*0.01,2),round(j*0.01,2)))
            i=j
        else:i+=1
    out[f"RC30-{n:02d}"]={"dur":len(y)/16000,"gaps":g}
    print(n,len(g),flush=True)
json.dump(out,open("/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a16-editing-pacing-specialist/gaps.json","w"))
