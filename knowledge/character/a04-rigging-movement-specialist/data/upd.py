import cv2,numpy as np,sys
n,f0,f1=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
x0,y0,x1,y1=map(int,sys.argv[4:8])   # char roi
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,f0)
prev=None;out=[]
for i in range(f0,f1):
    ok,f=cap.read(); g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
    g=cv2.GaussianBlur(g,(0,0),1.5)[y0:y1,x0:x1]
    if prev is not None:
        d=np.abs(g-prev); out.append((i,d.mean(),(d>12).mean()*100))
    prev=g
print(' '.join(f'{i}:{m:.1f}/{p:.1f}' for i,m,p in out))
