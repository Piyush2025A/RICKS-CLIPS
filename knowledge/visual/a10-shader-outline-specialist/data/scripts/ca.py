"""A10 chromatic-aberration test v1. Per frame, patches 192x192 at centre and 4 corners (rows 0..0.75H only). In each patch, find sub-pixel shift of R-channel vs B-channel
gradient magnitude via phase-correlation (cv2.phaseCorrelate on Hann-windowed Sobel mags). CA => shift vector points radially and grows with radius.
Report radial component (px, + = R further from centre than B) per corner and centre."""
import cv2,numpy as np,sys,os,json
def patch_shift(im,x,y,s=192):
    p=im[y:y+s,x:x+s].astype(np.float32); 
    def gm(c):
        c=cv2.GaussianBlur(c,(0,0),0.8); return np.hypot(cv2.Sobel(c,cv2.CV_32F,1,0),cv2.Sobel(c,cv2.CV_32F,0,1))
    r=gm(p[:,:,2]); b=gm(p[:,:,0])
    if r.std()<8 or b.std()<8: return None
    w=cv2.createHanningWindow((s,s),cv2.CV_32F); (dx,dy),resp=cv2.phaseCorrelate(b,r,w)
    return dx,dy,resp
out={}
for p in sorted(sys.argv[1:]):
    im=cv2.imread(p); H,W=im.shape[:2]; cx,cy=W/2,H*0.375
    pts={"TL":(0,0),"TR":(W-192,0),"ML_L":(0,int(H*.375)-96),"ML_R":(W-192,int(H*.375)-96),"BL":(0,int(.75*H)-192),"BR":(W-192,int(.75*H)-192),"C":(W//2-96,int(H*.375)-96)}
    row={}
    for k,(x,y) in pts.items():
        s=patch_shift(im,x,y)
        if s is None: continue
        dx,dy,resp=s; px,py=x+96-cx,y+96-cy; n=np.hypot(px,py)
        rad=(dx*px+dy*py)/n if n>50 else None
        row[k]=dict(dx=round(dx,2),dy=round(dy,2),resp=round(float(resp),2),radial=None if rad is None else round(float(rad),2))
    out[os.path.basename(p)[:-4]]=row
json.dump(out,open("ca.json","w"),indent=1)
rads=[v["radial"] for r in out.values() for k,v in r.items() if k!="C" and v["radial"] is not None and v["resp"]>0.1]
cs=[np.hypot(v["dx"],v["dy"]) for r in out.values() for k,v in r.items() if k=="C" and v["resp"]>0.1]
print("corner/edge radial shifts n",len(rads),"median %.2f IQR %s"%(np.median(rads),np.percentile(rads,[25,75]).round(2)),"share |r|>0.5:",np.mean(np.abs(rads)>0.5),"share>0 %.2f"%np.mean(np.array(rads)>0))
print("centre shift magnitude n",len(cs),"median %.2f"%np.median(cs))
