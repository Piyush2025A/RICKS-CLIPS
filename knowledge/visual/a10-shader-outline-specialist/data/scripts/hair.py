"""A10 hairline scan v1: horizontal scanlines (normal to vertical edges), invert gray, scipy find_peaks prominence>=P, peak_widths rel_height .5 => FWHM px at native (crop native scale). 
Reports FWHM, depth of line (gray drop vs local baseline), core RGB."""
import cv2,numpy as np,json,sys
from scipy.signal import find_peaks,peak_widths
def scan(p,rows,P=20,maxw=14):
    im=cv2.imread(p); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(float); out=[]
    for y in rows:
        pr=255-g[y]; pk,pp=find_peaks(pr,prominence=P)
        if len(pk)==0: continue
        w=peak_widths(pr,pk,rel_height=0.5)[0]
        for x,ww,pm in zip(pk,w,pp["prominences"]):
            if 1<=ww<=maxw: out.append((int(x),y,float(ww),float(pm),im[y,x][::-1].tolist()))
    return out
A="../a05-3d-world-designer/"
res={}
for name,p,rows in (("RC30-25-f000519",A+"c_25_000519.png",range(120,620,12)),("RC30-29-f000359",A+"c_29_000359.png",range(40,600,12))):
    o=scan(p,rows); res[name]=o
    w=np.array([a[2] for a in o]);pm=np.array([a[3] for a in o]);x=np.array([a[0] for a in o])
    print(name,"n",len(o),"FWHM med %.1f IQR %s"%(np.median(w),np.percentile(w,[25,75]).round(1)),"prom med %.0f"%np.median(pm),"rgb med",np.median([a[4] for a in o],axis=0))
    for lo,hi in ((0,360),(360,720),(720,1080)):
        s=(x>=lo)&(x<hi); 
        if s.sum(): print("  x%d-%d n=%d FWHM med %.1f IQR %s"%(lo,hi,s.sum(),np.median(w[s]),np.percentile(w[s],[25,75]).round(1)))
json.dump(res,open("hair.json","w"))
