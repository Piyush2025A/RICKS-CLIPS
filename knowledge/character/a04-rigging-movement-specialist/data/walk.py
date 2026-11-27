import cv2,numpy as np
cap=cv2.VideoCapture('/home/piyush/ricks-clips-private/reference-videos/RC30/14.mp4')
f0,f1=656,740
cap.set(cv2.CAP_PROP_POS_FRAMES,f0)
rows=[]
for i in range(f0,f1):
    ok,f=cap.read()
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)[1060:1420,200:850]
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)[1060:1420,200:850]
    m=(g<55)&(hsv[...,1]<120)
    ys,xs=np.nonzero(m)
    rows.append((i,m.sum(),xs.mean() if len(xs) else -1, xs.std() if len(xs) else -1, ys.mean() if len(ys) else -1))
a=np.array(rows)
for r in a: print(int(r[0]),int(r[1]),round(r[2]),round(r[3],1),round(r[4]))
