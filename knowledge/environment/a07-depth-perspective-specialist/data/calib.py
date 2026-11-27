import cv2, numpy as np, json
sig=[0,0.5,1,1.5,2,3,4,6,8,12]
res=[]
for n,idxs in [(4,[300,600,900]),(21,[200,700,1000]),(10,[300,800]),(19,[300,900])]:
    cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4')
    for ix in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES,ix); ok,f=cap.read()
        if not ok: continue
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32); H,W=g.shape
        for (a,b) in [(0,int(.2*H)),(int(.2*H),int(.4*H)),(int(.4*H),int(.58*H)),(int(.82*H),H)]:
            for ci in range(3):
                p=g[a:b,ci*W//3:(ci+1)*W//3]
                if p.std()<20: continue
                row=[]
                for s in sig:
                    q=cv2.GaussianBlur(p,(0,0),s) if s>0 else p
                    row.append(cv2.Laplacian(q,cv2.CV_32F).var()/max(q.std(),1)**2)
                res.append(np.array(row)/row[0])
r=np.array(res); print(len(r))
med=np.median(r,0); print(dict(zip(sig,np.round(med,4)))); print(np.round(np.percentile(r,25,0),4),np.round(np.percentile(r,75,0),4))
json.dump({'sigma':sig,'ratio_median':med.tolist()},open('calib_curve.json','w'))
