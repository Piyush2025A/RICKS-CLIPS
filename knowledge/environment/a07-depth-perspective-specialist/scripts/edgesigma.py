"""A07 3B v1: edge-spread blur sigma per grid cell on native frames. sigma = contrast/(2.507*peak_grad) at Canny edge points,
contrast = max-min of profile +-10 px along gradient. Usage: edgesigma.py <video.mp4> <key> <step> <outdir>"""
import sys, subprocess, numpy as np, cv2, json
from scipy.ndimage import map_coordinates
W,H=1080,1920
ROWS=[(0,.20),(.20,.40),(.40,.58),(.82,1.0)]; COLS=3
def sig_points(g):
    gb=cv2.GaussianBlur(g,(0,0),0.6)
    gx=cv2.Sobel(gb,cv2.CV_32F,1,0,ksize=3)/8; gy=cv2.Sobel(gb,cv2.CV_32F,0,1,ksize=3)/8
    mag=np.hypot(gx,gy)
    e=cv2.Canny(np.clip(g,0,255).astype(np.uint8),40,100)
    ys,xs=np.nonzero(e)
    if len(ys)>6000:
        idx=np.random.RandomState(0).choice(len(ys),6000,replace=False); ys,xs=ys[idx],xs[idx]
    m=mag[ys,xs]; ok=m>2; ys,xs,m=ys[ok],xs[ok],m[ok]
    ux=gx[ys,xs]/m; uy=gy[ys,xs]/m
    t=np.arange(-10,11)[None,:]
    prof=map_coordinates(g,[ (ys[:,None]+uy[:,None]*t), (xs[:,None]+ux[:,None]*t)],order=1,mode='nearest')
    c=prof.max(1)-prof.min(1)
    s=c/(2.507*m)
    return ys,xs,s,c
def cells(g):
    ys,xs,s,c=sig_points(g); out=[]
    for r,(a,b) in enumerate(ROWS):
        for k in range(COLS):
            sel=(ys>=a*H)&(ys<b*H)&(xs>=k*W/COLS)&(xs<(k+1)*W/COLS)&(c>25)
            out.append((r,k,int(sel.sum()),float(np.median(s[sel])) if sel.sum()>=40 else float('nan')))
    return out
def frames(path,step,tag=None):
    cmd=['ffmpeg','-nostdin','-v','error','-i',path,'-vf',f"select='not(mod(n\\,{step}))'",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE); n=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield n*step,np.frombuffer(b,np.uint8).reshape(H,W,3); n+=1
if __name__=='__main__':
    path,key,step,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
    res=[]
    for fi,img in frames(path,step):
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)
        cv2.imwrite(f"{out}/jpg/{key}-f{fi:06d}.jpg",cv2.resize(img,(540,960),interpolation=cv2.INTER_AREA),[cv2.IMWRITE_JPEG_QUALITY,88])
        res.append({'f':fi,'cells':cells(g)})
    json.dump(res,open(f"{out}/{key}_sigma.json",'w'))
