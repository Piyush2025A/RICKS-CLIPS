import cv2,numpy as np,sys
def run(n,f0,f1,roi,tag):
    cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4')
    cap.set(cv2.CAP_PROP_POS_FRAMES,f0)
    x0,y0,x1,y1=roi; prev=None; res=[]
    for i in range(f0,f1):
        ok,f=cap.read()
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)[y0:y1,x0:x1]
        g=cv2.resize(g,None,fx=.35,fy=.35,interpolation=cv2.INTER_AREA).astype(np.float32)
        if prev is not None:
            W=np.eye(2,3,dtype=np.float32)
            try:
                _,W=cv2.findTransformECC(prev,g,W,cv2.MOTION_TRANSLATION,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,60,1e-5),None,5)
                w=cv2.warpAffine(g,W,(g.shape[1],g.shape[0]),flags=cv2.INTER_LINEAR+cv2.WARP_INVERSE_MAP)
                m=cv2.warpAffine(np.ones_like(g),W,(g.shape[1],g.shape[0]),flags=cv2.INTER_NEAREST+cv2.WARP_INVERSE_MAP)>0
                r=np.abs(w-prev)[m].mean()
                raw=np.abs(g-prev).mean()
            except cv2.error: r=-1;raw=-1
            res.append((i,round(float(r),2),round(float(raw),2)))
        prev=g
    print(tag,n,' '.join(f'{i}:{r}/{a}' for i,r,a in res))
if __name__=='__main__':
    a=sys.argv; run(int(a[1]),int(a[2]),int(a[3]),tuple(map(int,a[4:8])),a[8])
