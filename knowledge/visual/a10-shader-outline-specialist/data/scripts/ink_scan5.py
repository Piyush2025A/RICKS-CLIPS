"""A10 ink_scan5 (3B): perpendicular-profile FWHM of the dark head-edge stroke. Inputs: A03 landmarks (old landmarks.csv + landmarks_3b.csv), native frames from A03's private dirs.
Per head: 7 rows between 12 % and 55 % of head height above chin, both sides; +-45 px window, 0.25 px sampling; FWHM of the dark run at half-depth between core and
inside/outside reference; width multiplied by edge-normal x-component (reject nx<0.6). Reject contrast<40 / outside contrast<25 / w outside 2..45.
Output ink_scan5.json (+ per head table). Run: .venv-analysis/bin/python ink_scan5.py"""
import csv,json,os,collections,numpy as np,cv2
from scipy.ndimage import map_coordinates
R="/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a03-anatomy-proportion-specialist/"
rows=[]
for f,phase in (("landmarks.csv","3A"),("/home/piyush/RICKS-CLIPS/knowledge/character/a03-anatomy-proportion-specialist/data/landmarks_3b.csv","3B")):
    for r in csv.DictReader(open(R+f if phase=="3A" else f)):
        if r.get("view")=="back": continue
        fid=r.get("frame_id")
        for p in (R+"3b/%s.png"%fid,R+"frames/%s.png"%fid):
            if os.path.exists(p): break
        else: continue
        try: rows.append((fid,r["person"],p,int(r["head_l"]),int(r["head_r"]),int(r["chin"]),r["head_top"],phase))
        except: pass
res=[]
for fid,person,p,hl,hr,chin,ht,ph in rows:
    im=cv2.imread(p); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(float); H,W=g.shape
    hw=hr-hl; top=int(ht) if ht else chin-int(1.05*hw)
    if hw<60: continue
    gb=cv2.GaussianBlur(g,(0,0),3); GX=cv2.Sobel(gb,cv2.CV_64F,1,0,ksize=3); GY=cv2.Sobel(gb,cv2.CV_64F,0,1,ksize=3)
    ys=np.linspace(chin-0.12*(chin-top), chin-0.55*(chin-top),7).astype(int)
    for side,x0,sgn in (("L",hl,-1),("R",hr,1)):
        for y in ys:
            xs=np.arange(x0-45,x0+45,0.25)
            if xs[0]<60 or xs[-1]>=W-60 or y<0 or y>=H: continue
            prof=map_coordinates(g,[np.full_like(xs,y),xs],order=1)
            i=int(np.argmin(prof)); core=prof[i]; xc=xs[i]
            if sgn==-1: inside=np.median(g[y,int(xc)+20:int(xc)+50]); outside=np.median(g[y,int(xc)-60:int(xc)-30])
            else: inside=np.median(g[y,int(xc)-50:int(xc)-20]); outside=np.median(g[y,int(xc)+30:int(xc)+60])
            if inside<110 or inside-core<40 or outside-core<25: continue
            hi_in=(core+inside)/2; hi_out=(core+outside)/2
            a,b=(hi_out,hi_in) if sgn==-1 else (hi_in,hi_out)
            l=i
            while l>0 and prof[l]<a: l-=1
            rr=i
            while rr<len(prof)-1 and prof[rr]<b: rr+=1
            w=(rr-l)*0.25
            gx=GX[y,int(xc)]; gy=GY[y,int(xc)]; nx=abs(gx)/(np.hypot(gx,gy)+1e-9)
            if nx<0.6: continue
            w*=nx
            if not(2<=w<=45): continue
            res.append(dict(fid=fid,video=fid[:7],person=person,phase=ph,side=side,y=int(y),w=float(w),core=float(core),head_w=hw))
json.dump(res,open("ink_scan5.json","w"))
by=collections.defaultdict(list)
for r in res: by[(r["fid"],r["person"])].append(r)
tab=[]
for k,v in sorted(by.items()):
    w=np.median([x["w"] for x in v]); tab.append((k[0],k[1],len(v),w,v[0]["head_w"],100*w/v[0]["head_w"]))
    print(k,len(v),"w %.1f hw %d  %.2f%%"%(w,v[0]["head_w"],100*w/v[0]["head_w"]))
t=np.array([(x[3],x[5]) for x in tab])
print("heads",len(tab),"frames",len({x[0] for x in tab}),"videos",len({x[0][:7] for x in tab}),"scans",len(res))
for nm,col in(("px",0),("pct_hw",1)): print(nm,"median %.2f IQR %s range %.1f-%.1f"%(np.median(t[:,col]),np.percentile(t[:,col],[25,75]).round(2),t[:,col].min(),t[:,col].max()))
allw=np.array([r["w"] for r in res]);print("scan-level n",len(allw),np.median(allw),np.percentile(allw,[25,75]))
vid=collections.defaultdict(list)
for x in tab: vid[x[0][:7]].append(x[3])
vm=np.array([np.median(v) for v in vid.values()]);print("per-video medians n",len(vm),np.median(vm),np.percentile(vm,[25,75]))
from scipy.stats import spearmanr
print("spearman w vs head_w",spearmanr([x[3] for x in tab],[x[4] for x in tab]))
json.dump(tab,open("ink_scan5_heads.json","w"))
