# a06 flowlayers v0.1: per-window flow clustering. usage: flowlayers.py out.json
import cv2, numpy as np, sys, json, glob
from sklearn.cluster import KMeans
R='/home/piyush/ricks-clips-private/reference-videos/RC30/%d.mp4'
out=[]
for n in range(1,31):
    cap=cv2.VideoCapture(R%n); N=int(cap.get(7)); W=270;H=480
    for s in range(30,N-10,45):
        cap.set(1,s); fr=[]
        for k in range(3):
            ok,f=cap.read()
            if not ok: break
            fr.append(cv2.cvtColor(cv2.resize(f,(W,H),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY))
        if len(fr)<3: continue
        fl=cv2.calcOpticalFlowFarneback(fr[0],fr[2],None,.5,4,21,3,5,1.1,0)
        m=np.ones((H,W),bool); m[int(.58*H):int(.82*H)]=False  # caption band
        g=cv2.GaussianBlur(fr[0],(0,0),1); gx=cv2.Sobel(g,cv2.CV_32F,1,0);gy=cv2.Sobel(g,cv2.CV_32F,0,1)
        tex=(np.hypot(gx,gy)>40)&m
        if tex.sum()<2000: continue
        ys,xs=np.nonzero(tex); v=fl[ys,xs]
        # global affine fit (LS) -> residual
        A=np.c_[xs-W/2,ys-H/2,np.ones(len(xs))]
        cx=np.linalg.lstsq(A,v[:,0],rcond=None)[0];cy=np.linalg.lstsq(A,v[:,1],rcond=None)[0]
        res=v-np.c_[A@cx,A@cy]
        mag=np.hypot(v[:,0],v[:,1])
        sub=np.random.RandomState(0).choice(len(v),min(4000,len(v)),replace=False)
        X=v[sub]; ine=[]; km={}
        for k in (1,2,3,4):
            km[k]=KMeans(k,n_init=3,random_state=0).fit(X); ine.append(km[k].inertia_)
        # stable clusters: k minimising by 50% inertia drop rule, count clusters with >=8% mass and centre sep >0.4px
        k=1
        for kk in (2,3,4):
            if ine[kk-1]<0.6*ine[kk-2] and ine[kk-2]>len(X)*0.15: k=kk
        c=km[k].cluster_centers_; lab=km[k].labels_; frac=np.bincount(lab,minlength=k)/len(lab)
        keep=[i for i in range(k) if frac[i]>=.08]
        sp=sorted(np.hypot(c[i,0],c[i,1]) for i in keep)
        # y-position of clusters (top/bottom) for ground-plane gradient
        out.append(dict(v=n,f=s,medmag=float(np.median(mag)),p90=float(np.percentile(mag,90)),resmed=float(np.median(np.hypot(res[:,0],res[:,1]))),
            k=len(keep),sp=[round(float(x),2) for x in sp],ratio=float(sp[-1]/max(sp[0],.05)) if len(sp)>1 else 1.0,
            scale=float(cx[0]+cy[1]),ntex=int(tex.sum())))
    print(n,len([o for o in out if o['v']==n]),flush=True)
json.dump(out,open(sys.argv[1],'w'))
