import sys,subprocess,numpy as np,cv2,os,csv
W,H=270,480
def run(n):
    src=os.path.expanduser(f"~/ricks-clips-private/reference-videos/RC30/{n}.mp4")
    cmd=["ffmpeg","-v","error","-threads","1","-i",src,"-vf",f"fps=1,scale={W}:{H}:flags=area:in_range=limited:out_range=full:in_color_matrix=bt709","-pix_fmt","rgb24","-f","rawvideo","-"]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
    yy,xx=np.mgrid[0:H,0:W];cap=np.ones((H,W),bool);cap[int(.60*H):int(.76*H),:]=False
    rows=[];i=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3:break
        rgb=np.frombuffer(b,np.uint8).reshape(H,W,3)
        lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32)
        L=lab[...,0]*100/255;a=lab[...,1]-128;bb=lab[...,2]-128;C=np.hypot(a,bb)
        w=cap&(L>82)&(C<12)
        r=dict(t=i,white_frac=float(w.sum()/cap.sum()))
        if w.sum()>200:
            r.update(wL=float(np.median(L[w])),wa=float(np.median(a[w])),wb=float(np.median(bb[w])),
              wR=float(np.median(rgb[...,0][w])),wG=float(np.median(rgb[...,1][w])),wB=float(np.median(rgb[...,2][w])),
              wmax=float(np.percentile(L[w],95)))
        else: r.update(wL=np.nan,wa=np.nan,wb=np.nan,wR=np.nan,wG=np.nan,wB=np.nan,wmax=np.nan)
        # saturated mid-tone pixels: C>40 hue histogram share warm/cool
        s=cap&(C>35);r['sat_frac']=float(s.sum()/cap.sum())
        r['sat_hue_med']=float(np.degrees(np.arctan2(np.median(bb[s]),np.median(a[s])))%360) if s.sum()>200 else np.nan
        # dark pixel (L<15) tint
        dk=cap&(L<12)
        r['dk_frac']=float(dk.sum()/cap.sum())
        r['dk_a']=float(np.median(a[dk])) if dk.sum()>200 else np.nan
        r['dk_b']=float(np.median(bb[dk])) if dk.sum()>200 else np.nan
        # quantised tone histogram 16 bins of Y
        Y=(0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2])
        hy=np.histogram(Y[cap],bins=16,range=(0,256))[0]/cap.sum()
        for k in range(16):r[f"yh{k:02d}"]=float(hy[k])
        rows.append(r);i+=1
    p.wait()
    with open(f"pass2_{n:02d}.csv","w",newline="") as fh:
        w_=csv.DictWriter(fh,fieldnames=list(rows[0]));w_.writeheader();w_.writerows(rows)
    print(n,len(rows),flush=True)
for n in map(int,sys.argv[1:]):run(n)
