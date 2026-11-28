"""3B: static-camera walker via background subtraction. usage: bgsub.py VIDEO BG0 BG1 F0 F1 X0 Y0 X1 Y1 [thr]
Foreground = |frame-median bg|>thr within ROI (caption band must be outside ROI or accepted). Per frame: bbox, lower-40% width, top y, centroid x."""
import cv2,numpy as np,sys
n,b0,b1,f0,f1,x0,y0,x1,y1=map(int,sys.argv[1:10]);thr=int(sys.argv[10]) if len(sys.argv)>10 else 45
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4');cap.set(cv2.CAP_PROP_POS_FRAMES,b0)
bg=[];fr={}
for i in range(b0,f1+1):
    ok,f=cap.read()
    if not ok:break
    c=f[y0:y1,x0:x1].astype(np.int16)
    if i<=b1:bg.append(c)
    if i>=f0:fr[i]=c
B=np.median(np.array(bg),0)
print('f cx topy boty h width lowwidth')
rows=[]
for i,c in fr.items():
    d=np.abs(c-B).max(2)>thr;d=cv2.morphologyEx(d.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    ys,xs=np.nonzero(d)
    if len(ys)<200:print(i,'none');continue
    t,b=np.percentile(ys,1),np.percentile(ys,99);h=b-t;low=ys>t+0.65*h
    lw=np.percentile(xs[low],95)-np.percentile(xs[low],5) if low.sum()>20 else np.nan
    rows.append((i,xs.mean(),t,b,h,lw));print(i,round(xs.mean()),round(t),round(b),round(h),round(lw))
np.save('/tmp/claude-1000/-home-piyush-RICKS-CLIPS/092e9044-5d47-45d7-9b9b-c40b677c0730/scratchpad/bg_%d.npy'%n,np.array(rows))
