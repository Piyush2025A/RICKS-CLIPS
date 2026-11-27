"""A10 thin-line thickness v1. blackhat(k=15) on gray -> mask (bh>18 & gray<150) -> dist transform -> skeleton -> thickness=2*dt (px, approx FWHM-ish at mask threshold).
Excludes bottom 22% (caption band, y>0.78H) and returns per-region stats."""
import cv2,numpy as np,sys,json
from skimage.morphology import skeletonize
def run(p,regions):
    im=cv2.imread(p); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); H,W=g.shape
    bh=cv2.morphologyEx(g,cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(21,21)))
    m=((bh>18)&(g<170)).astype(np.uint8); m[int(0.78*H):]=0
    dt=cv2.distanceTransform(m,cv2.DIST_L2,5); sk=skeletonize(m>0)
    out={}
    for name,(x0,x1,y0,y1) in regions.items():
        t=2*dt[y0:y1,x0:x1][sk[y0:y1,x0:x1]]
        t=t[(t>=1)&(t<=30)]
        out[name]=dict(n=int(len(t)),median=float(np.median(t)) if len(t) else None,iqr=np.percentile(t,[25,75]).round(2).tolist() if len(t) else None,
          coverage_pct=float(100*m[y0:y1,x0:x1].mean()))
    # core colour: min-luma pixel colour along skeleton
    ys,xs=np.nonzero(sk[:int(0.78*H)]); cols=im[ys,xs][:,::-1]; 
    out["skeleton_rgb_median"]=np.median(cols,axis=0).tolist(); out["skeleton_px"]=int(len(ys))
    return out
if __name__=="__main__":
    A="../a05-3d-world-designer/"
    R25={"all":(0,1080,0,700),"near_right":(780,1080,0,700),"mid":(450,780,100,600),"far_left_center":(250,500,150,500)}
    R29={"all":(0,1080,0,700),"near_tower_left":(640,1080,0,700),"sky_palms":(0,640,0,700)}
    print(json.dumps({"RC30-25-f000519":run(A+"c_25_000519.png",R25),"RC30-29-f000359":run(A+"c_29_000359.png",R29)},indent=1))
