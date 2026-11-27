# a07 regions v0.1: every 10th native frame, 3x3 grid (caption band y 58-82% excluded by using rows 0-58% and 82-100% only -> 4 rows)
import cv2, numpy as np, sys, json, csv
step=int(sys.argv[2]) if len(sys.argv)>2 else 10
def sig_match(ref, target_lv):
    # sigma of gaussian blur on ref patch s.t. lapvar ~= target
    lo,hi=0.0,12.0
    base=cv2.Laplacian(ref,cv2.CV_32F).var()
    if target_lv>=base: return 0.0
    for _ in range(12):
        m=(lo+hi)/2
        b=cv2.GaussianBlur(ref,(0,0),m) if m>0.05 else ref
        v=cv2.Laplacian(b,cv2.CV_32F).var()
        if v>target_lv: lo=m
        else: hi=m
    return (lo+hi)/2
out=open(f'regions_{sys.argv[1]}.csv','w'); w=csv.writer(out)
w.writerow(['key','frame','gy0','gx0','lapv','lstd','sat','L','chroma'])
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{int(sys.argv[1])}.mp4')
i=0
while True:
    ok=cap.grab()
    if not ok: break
    if i%step==0:
        ok,f=cap.retrieve()
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
        hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
        lab=cv2.cvtColor(f,cv2.COLOR_BGR2LAB).astype(np.float32)
        H,W=g.shape
        rows=[(0,int(.2*H)),(int(.2*H),int(.4*H)),(int(.4*H),int(.58*H)),(int(.82*H),H)]
        for ri,(a,b) in enumerate(rows):
            for ci in range(3):
                x0,x1=ci*W//3,(ci+1)*W//3
                p=g[a:b,x0:x1]
                lv=cv2.Laplacian(p,cv2.CV_32F).var()
                w.writerow([f'RC30-{int(sys.argv[1]):02d}',i,ri,ci,round(float(lv),2),round(float(p.std()),2),round(float(hsv[a:b,x0:x1,1].mean()),1),round(float(lab[a:b,x0:x1,0].mean()),1),round(float(np.hypot(lab[a:b,x0:x1,1]-128,lab[a:b,x0:x1,2]-128).mean()),1)])
    i+=1
out.close()
