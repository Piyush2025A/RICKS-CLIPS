import cv2,numpy as np,sys
n,f0,f1=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]); x0,y0,x1,y1=map(int,sys.argv[4:8])
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,f0)
prev=None;res=[]
for i in range(f0,f1):
    ok,f=cap.read(); g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)[y0:y1,x0:x1]
    g=cv2.resize(g,None,fx=.5,fy=.5,interpolation=cv2.INTER_AREA)
    m=(g<50).astype(np.float32)
    if prev is not None:
        (dx,dy),_=cv2.phaseCorrelate(prev,m)
        M=np.float32([[1,0,-dx],[0,1,-dy]]); w=cv2.warpAffine(m,M,(m.shape[1],m.shape[0]))
        a=cv2.dilate(prev,np.ones((3,3)));b=cv2.dilate(w,np.ones((3,3)))
        iou=(np.minimum(prev,b).sum())/max(prev.sum(),1)  # fraction of prev ink covered by dilated cur
        iou2=(np.minimum(w,a).sum())/max(w.sum(),1)
        res.append((i,min(iou,iou2),dx,dy))
    prev=m
print(' '.join(f'{i}:{v:.2f}' for i,v,_,_ in res))
vals=np.array([v for _,v,_,_ in res]);print('median',np.median(vals),'frac>0.9',(vals>0.9).mean(),'frac<0.7',(vals<.7).mean())
