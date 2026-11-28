"""Native 1080x1920 decode of 4 frames/video (20/40/60/80 %): p1/p99 with and without caption band (y 0.64-0.76 masked),
top-end histogram (roll-off), vignette (corner 10% boxes / centre box). Gray = cv2 BGR2GRAY. Stats only, nothing saved."""
import subprocess,os,json,numpy as np,cv2
R=os.path.expanduser('~/ricks-clips-private'); H,W=1920,1080
out={}
for n in range(1,31):
    nf=len([1 for _ in open(f'{R}/analysis-data/rc30/v0.2.0/RC30-{n:02d}/color.csv')])-1
    fr=[int(nf*f) for f in (.2,.4,.6,.8)]
    sel='+'.join(f'eq(n\\,{i})' for i in fr)
    p=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',f'{R}/reference-videos/RC30/{n}.mp4','-vf',f"select='{sel}'",'-fps_mode','passthrough','-frames:v','4','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True)
    a=np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3)
    rec=[]
    for f in a:
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY); m=np.ones(H,bool); m[int(.64*H):int(.76*H)]=False
        gm=g[m]
        c=lambda x:[float(v) for v in np.percentile(x,[1,5,50,95,99])]
        h=np.bincount(gm.ravel(),minlength=256)/gm.size
        cen=g[int(.35*H):int(.65*H),int(.3*W):int(.7*W)].mean(); k=int(.12*H); kw=int(.12*W)
        cor=np.mean([g[:k,:kw].mean(),g[:k,-kw:].mean(),g[-k:,:kw].mean(),g[-k:,-kw:].mean()])
        rec.append({'full':c(g),'masked':c(gm),'share_eq255':float(h[255]),'share_ge250':float(h[250:].sum()),'share_235_249':float(h[235:250].sum()),'share_220_234':float(h[220:235].sum()),'share_le2':float((gm<=2).mean()),'share_le10':float((gm<=10).mean()),'share_le16':float((gm<=16).mean()),'min_gray':int(gm.min()),'vig':float(cor/max(cen,1e-6))})
    out[n]=rec; print(n,len(rec),[round(r['full'][0]-r['masked'][0]) for r in rec],[round(r['full'][4]-r['masked'][4]) for r in rec],flush=True)
json.dump(out,open('data/native3b_mask_rolloff_vignette.json','w'),indent=1)
