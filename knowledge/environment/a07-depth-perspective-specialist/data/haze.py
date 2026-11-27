import cv2, numpy as np, json
cases=[(4,209,.35),(4,179,.33),(8,1830,.50),(24,540,.43),(12,420,.20),(29,840,.50),(10,1560,.40),(6,89,.27),(24,450,.45)]
out=[];tiles=[]
for n,ix,hy in cases:
    cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,ix); ok,f=cap.read()
    H,W=f.shape[:2]
    lab=cv2.cvtColor(f,cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[...,1:]-=128
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
    # refine horizon: strongest vertical luma step in rows hy-0.08..hy+0.08, averaged over all columns
    prof=cv2.GaussianBlur(g,(0,0),3).mean(1)
    lo,hi=int((hy-.08)*H),int((hy+.08)*H)
    hz=lo+int(np.argmax(np.abs(np.diff(prof[lo:hi]))))
    def band(a,b):
        return lab[a:b,:,:].reshape(-1,3).mean(0), g[a:b].std()
    sky,_=band(hz-80,hz-20)
    far,sf=band(hz+15,hz+75); mid,sm=band(hz+int(.1*H),hz+int(.1*H)+60); near,sn=band(H-int(.25*H),H-int(.25*H)+60)
    de=lambda x,y: float(np.linalg.norm(x-y))
    out.append(dict(key=f'RC30-{n:02d}',frame=ix,horizon_y_frac=round(hz/H,3),dE_far_to_sky=round(de(far,sky),1),dE_mid_to_sky=round(de(mid,sky),1),dE_near_to_sky=round(de(near,sky),1),chroma_far=round(float(np.hypot(*far[1:])),1),chroma_near=round(float(np.hypot(*near[1:])),1),lstd_far=round(float(sf),1),lstd_near=round(float(sn),1)))
    t=cv2.resize(f,(180,320),interpolation=cv2.INTER_AREA); y=int(hz/H*320); cv2.line(t,(0,y),(180,y),(0,0,255),1); cv2.putText(t,f'{n}-f{ix}',(3,11),cv2.FONT_HERSHEY_SIMPLEX,.4,(0,255,255),1); tiles.append(t)
for o in out: print(o)
cv2.imwrite('haze_check.png',np.hstack(tiles))
json.dump(out,open('haze_cases.json','w'),indent=1)
