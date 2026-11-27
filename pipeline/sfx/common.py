"""A21 shared audio helpers (read-only on native audio; decodes to memory, writes nothing to the source)."""
import subprocess, numpy as np, librosa
SR = 44100
def load_stereo(path):
    p = subprocess.run(["ffmpeg","-v","error","-i",path,"-vn","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True)
    x = np.frombuffer(p.stdout,dtype=np.float32).reshape(-1,2)
    return x
def stft_db(m, n_fft=2048, hop=441):
    S = np.abs(librosa.stft(m, n_fft=n_fft, hop_length=hop, center=True))**2
    f = librosa.fft_frequencies(sr=SR, n_fft=n_fft)
    return S, f
BANDS = {"sub":(25,100),"low":(100,300),"voice":(300,3400),"pres":(3400,7000),"air":(7000,16000)}
def band_db(S,f):
    out={}
    for k,(a,b) in BANDS.items():
        i=(f>=a)&(f<b)
        out[k]=10*np.log10(S[i].sum(0)+1e-12)
    return out
