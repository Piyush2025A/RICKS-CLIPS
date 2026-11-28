"""3B pose-update rate: ink-overlap between consecutive frames after phase-correlation (as iou.py), caption band masked, run-length stats.
usage: iou2.py VIDEO F0 F1 X0 Y0 X1 Y1 [capY0 capY1] [thr]   prints per-pair score, hold runs (score>=0.90), frac>0.9, frac<0.7"""
import cv2,numpy as np,sys
a=sys.argv[1:];n,f0,f1,x0,y0,x1,y1=map(int,a[:7]);c0,c1=(int(a[7]),int(a[8])) if len(a)>8 else (0,0);thr=int(a[9]) if len(a)>9 else 50
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4');cap.set(cv2.CAP_PROP_POS_FRAMES,f0)
prev=None;res=[]
for i in range(f0,f1+1):
    ok,f=cap.read()
    if not ok:break
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    if c1>c0:g[c0:c1,:]=255
    g=cv2.resize(g[y0:y1,x0:x1],None,fx=.5,fy=.5,interpolation=cv2.INTER_AREA);m=(g<thr).astype(np.float32)
    if prev is not None:
        (dx,dy),_=cv2.phaseCorrelate(prev,m);M=np.float32([[1,0,-dx],[0,1,-dy]]);w=cv2.warpAffine(m,M,(m.shape[1],m.shape[0]))
        A=cv2.dilate(prev,np.ones((3,3)));B=cv2.dilate(w,np.ones((3,3)))
        res.append((i,min(np.minimum(prev,B).sum()/max(prev.sum(),1),np.minimum(w,A).sum()/max(w.sum(),1))))
    prev=m
v=np.array([r for _,r in res]);hold=v>=0.9
runs=[];c=0
for h in hold:
    if h:c+=1
    elif c:runs.append(c);c=0
if c:runs.append(c)
print(f'RC30-{n:02d} f{f0}-{f1} n={len(v)} median={np.median(v):.2f} frac>=.9={hold.mean():.2f} frac<.7={(v<.7).mean():.2f} hold_runs(pairs)={runs}')
print(' '.join(f'{i}:{r:.2f}' for i,r in res))
