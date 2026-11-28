"""A21 Phase 3B (a21-sfx-0.6): per-video features, numpy-only (no librosa/scipy in this env).
Decode native stream in memory -> mid=(L+R)/2, side=(L-R)/2 -> STFT 2048/hop 441 (10 ms) -> saves npz of band dB.
usage: python3 p3b_feat.py OUTDIR [video numbers...]"""
import sys, subprocess, numpy as np, os
SR=44100; NF=2048; HOP=441
VID=os.path.expanduser('~/ricks-clips-private/reference-videos/RC30/%d.mp4')
def load(n):
    p=subprocess.run(["ffmpeg","-nostdin","-v","error","-i",VID%n,"-vn","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True)
    return np.frombuffer(p.stdout,dtype=np.float32).reshape(-1,2).astype(np.float64)
def stft_pow(x):
    w=np.hanning(NF); x=np.pad(x,(NF//2,NF//2),mode='reflect')
    nfr=1+(len(x)-NF)//HOP
    idx=np.arange(NF)[None,:]+HOP*np.arange(nfr)[:,None]
    return np.abs(np.fft.rfft(x[idx]*w,axis=1))**2/ (w**2).sum()
F=np.fft.rfftfreq(NF,1/SR)
EDGES=np.geomspace(60,16000,49)  # 48 log bands
def logbands(P):
    out=np.zeros((P.shape[0],48))
    for k in range(48):
        i=(F>=EDGES[k])&(F<EDGES[k+1]); out[:,k]=P[:,i].sum(1)
    return out  # linear power
def main(od,vids):
    for n in vids:
        x=load(n); mid=(x[:,0]+x[:,1])/2; side=(x[:,0]-x[:,1])/2
        Pm=stft_pow(mid); Ps=stft_pow(side)
        np.savez_compressed(f'{od}/v{n:02d}.npz',bm=logbands(Pm).astype(np.float32),bs=logbands(Ps).astype(np.float32),dur=len(mid)/SR)
        print(n,len(mid)/SR,flush=True)
if __name__=='__main__':
    od=sys.argv[1]; vids=[int(a) for a in sys.argv[2:]] or range(1,31); main(od,vids)
