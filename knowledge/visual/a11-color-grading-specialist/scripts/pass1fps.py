import sys,subprocess,numpy as np,cv2,json,os
W,H=270,480
def run(n):
    src=os.path.expanduser(f"~/ricks-clips-private/reference-videos/RC30/{n}.mp4")
    cmd=["ffmpeg","-v","error","-threads","2","-i",src,"-vf",f"fps=1,scale={W}:{H}:flags=area:in_range=limited:out_range=full:in_color_matrix=bt709","-pix_fmt","rgb24","-f","rawvideo","-"]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
    rows=[];i=0
    yy,xx=np.mgrid[0:H,0:W]
    cap=np.ones((H,W),bool); cap[int(.60*H):int(.76*H),:]=False   # caption band mask (provisional)
    cen=((xx>W*.25)&(xx<W*.75)&(yy>H*.25)&(yy<H*.75))&cap
    per=(~((xx>W*.15)&(xx<W*.85)&(yy>H*.15)&(yy<H*.85)))&cap
    corner=(((xx<W*.2)|(xx>W*.8))&((yy<H*.15)|(yy>H*.85)))
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3:break
        rgb=np.frombuffer(b,np.uint8).reshape(H,W,3)
        f=rgb.astype(np.float32)/255
        Y=(0.2126*f[...,0]+0.7152*f[...,1]+0.0722*f[...,2])  # gamma-coded Y'
        lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32)
        L=lab[...,0]*100/255;a=lab[...,1]-128;bb=lab[...,2]-128
        C=np.hypot(a,bb);h=(np.degrees(np.arctan2(bb,a)))%360
        m=cap
        y=Y[m]
        pc=np.percentile(y,[1,2,5,25,50,75,95,98,99])
        c=C[m]
        r=dict(t=i,y_p1=pc[0],y_p2=pc[1],y_p5=pc[2],y_p25=pc[3],y_p50=pc[4],y_p75=pc[5],y_p95=pc[6],y_p98=pc[7],y_p99=pc[8],
          clip_lo=float((y<=2/255).mean()),clip_hi=float((y>=253/255).mean()),near_white=float((y>=235/255).mean()),
          L=float(L[m].mean()),a=float(a[m].mean()),b=float(bb[m].mean()),
          C_p50=float(np.percentile(c,50)),C_p90=float(np.percentile(c,90)),C_mean=float(c.mean()),
          C_cen=float(C[cen].mean()),C_per=float(C[per].mean()),Y_cen=float(Y[cen].mean()),Y_per=float(Y[per].mean()),
          vig=float(Y[corner].mean()/(Y[cen].mean()+1e-6)),
          blk_r=float(np.median(f[...,0][m][y<=pc[0]]) if (y<=pc[0]).any() else 0),
          blk_g=float(np.median(f[...,1][m][y<=pc[0]]) if (y<=pc[0]).any() else 0),
          blk_b=float(np.median(f[...,2][m][y<=pc[0]]) if (y<=pc[0]).any() else 0))
        # chroma-weighted hue hist 12 bins, chroma>8 only
        sel=m&(C>8)
        hh=np.histogram(h[sel],bins=12,range=(0,360),weights=C[sel])[0]
        s=hh.sum()
        for k in range(12): r[f"hue{k:02d}"]=float(hh[k]/s) if s>0 else 0.0
        r["chroma_frac"]=float(sel.sum()/m.sum())
        # hue of centre vs periphery (circular mean of chroma>8)
        rows.append(r);i+=1
    p.wait()
    import csv
    with open(f"pass_{n:02d}.csv","w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(n,len(rows),flush=True)
if __name__=="__main__":
    for n in map(int,sys.argv[1:]): run(n)
