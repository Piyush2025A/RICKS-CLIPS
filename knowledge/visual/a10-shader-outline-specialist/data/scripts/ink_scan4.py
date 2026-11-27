"""A10 ink_scan v1: horizontal scanlines across head left/right edge using A03 landmarks (head_l/head_r/chin) on native frames.
Per scan: window +-45 px around landmark; profile = gray; core = min; inside = median gray 20..50px inside head; outside = median gray 30..60px outside.
FWHM of the dark line = run of profile below (core+ref)/2 where ref = max(inside,outside)... uses sub-pixel linear interp. Reject if contrast<40 or width>60."""
import sys,csv,json,glob,os,numpy as np,cv2
from scipy.ndimage import map_coordinates
A="/home/piyush/ricks-clips-private/analysis-data/rc30/agents/"
rows=[]
for r in csv.DictReader(open(A+"a03-anatomy-proportion-specialist/landmarks.csv")):
    if r["view"]=="back": continue
    p=A+"a03-anatomy-proportion-specialist/frames/%s.png"%r["frame_id"]
    if os.path.exists(p): rows.append((r["frame_id"],r["person"],p,int(r["head_l"]),int(r["head_r"]),int(r["chin"]),r["head_top"]))
def fwhm(prof):
    # prof sampled at 0.25 px; return width, core idx
    i=int(np.argmin(prof)); core=prof[i]
    return i,core
import cv2 as _c
B={"RC30-09-f000299":(560,830),"RC30-12-f000269":(600,880),"RC30-01-f000509":(480,600),"RC30-20-f000569":(760,830),"RC30-22-f000089":(730,880),"RC30-03-f000389":(640,700),"RC30-05-f000209":(540,900)}
for k,seed in B.items():
    p=A+"a01-character-designer/%s.png"%k; im0=_c.imread(p); g0=_c.cvtColor(im0,_c.COLOR_BGR2GRAY)
    n,lab=_c.connectedComponents((g0>150).astype(np.uint8)); l=lab[seed[1],seed[0]]
    if l==0: continue
    face=_c.morphologyEx((lab==l).astype(np.uint8),_c.MORPH_CLOSE,np.ones((41,41),np.uint8)); ys,xs=np.nonzero(face)
    rows.append((k,"a01",p,int(xs.min()),int(xs.max()),int(ys.max()),str(int(ys.min()))))
res=[]
for fid,person,p,hl,hr,chin,ht in rows:
    im=cv2.imread(p); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(float); H,W=g.shape
    lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(float)
    hw=hr-hl; top=int(ht) if ht else chin-int(1.05*hw)
    ys=np.linspace(chin-0.12*(chin-top), chin-0.55*(chin-top),7).astype(int)  # mid-lower face rows (avoid hat/hair)
    for side,x0,sgn in (("L",hl,-1),("R",hr,1)):
        for y in ys:
            xs=np.arange(x0-45,x0+45,0.25); 
            if xs[0]<0 or xs[-1]>=W: continue
            prof=map_coordinates(g,[np.full_like(xs,y),xs],order=1)
            i=int(np.argmin(prof)); core=prof[i]; xc=xs[i]
            ins=np.median(g[y,int(xc-sgn*-1*0)+ (20 if sgn==-1 else -50): int(xc)+(50 if sgn==-1 else -20)]) if False else None
            if sgn==-1: inside=np.median(g[y,int(xc)+20:int(xc)+50]); outside=np.median(g[y,int(xc)-60:int(xc)-30])
            else: inside=np.median(g[y,int(xc)-50:int(xc)-20]); outside=np.median(g[y,int(xc)+30:int(xc)+60])
            if inside<110 or inside-core<40 or outside-core<25: continue
            hi_in=(core+inside)/2; hi_out=(core+outside)/2
            ia,ib=(i,i)
            if sgn==-1: hl_,hr_=hi_out,hi_in
            else: hl_,hr_=hi_in,hi_out
            l=i
            while l>0 and prof[l]<hl_: l-=1
            rr=i
            while rr<len(prof)-1 and prof[rr]<hr_: rr+=1
            w=(rr-l)*0.25
            gb=cv2.GaussianBlur(g,(0,0),3); gx=cv2.Sobel(gb,cv2.CV_64F,1,0,ksize=3)[y,int(xc)]; gy=cv2.Sobel(gb,cv2.CV_64F,0,1,ksize=3)[y,int(xc)]
            nx=abs(gx)/(np.hypot(gx,gy)+1e-9)
            if nx<0.6: continue
            w=w*nx
            if not(2<=w<=45): continue
            c=im[y,int(round(xc))][::-1].tolist(); lb=lab[y,int(round(xc))]
            lb=[lb[0]*100/255,lb[1]-128,lb[2]-128]
            res.append(dict(fid=fid,person=person,side=side,y=int(y),w=float(w),core_luma=float(core),inside=float(inside),outside=float(outside),rgb=c,lab=lb,head_w=hw,chin=chin))
json.dump(res,open("ink_scan4.json","w"))
import collections
by=collections.defaultdict(list)
for r in res: by[(r["fid"],r["person"])].append(r)
print("frames/persons",len(by),"scans",len(res),"videos",len({k[0][:7] for k in by}))
tab=[]
for k,v in by.items():
    w=[x["w"] for x in v]; print(k,len(v),"w med %.1f iqr %s head_w %d  w/hw %.3f core %.0f rgb %s"%(np.median(w),np.percentile(w,[25,75]).round(1),v[0]["head_w"],np.median(w)/v[0]["head_w"],np.median([x["core_luma"] for x in v]),np.median([x["rgb"] for x in v],axis=0).astype(int)))
    tab.append((np.median(w),v[0]["head_w"],v[0]["chin"]))
t=np.array(tab); print("corr w vs head_w",np.corrcoef(t[:,0],t[:,1])[0,1],"spearman",__import__("scipy.stats").stats.spearmanr(t[:,0],t[:,1]))
allw=np.array([r["w"] for r in res]);print("ALL n",len(allw),"median",np.median(allw),"IQR",np.percentile(allw,[25,75]))
