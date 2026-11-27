import cv2,sys,numpy as np,json
v,s,n,x,y,w,h=sys.argv[1],*map(int,sys.argv[2:7+1])
cap=cv2.VideoCapture(v);i=0;prev=None;out=[]
while i<s+n:
    ok,f=cap.read()
    if not ok:break
    if i>=s-1:
        r=cv2.cvtColor(f[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY).astype(float)
        dark=float((r<70).mean())
        d=0 if prev is None else float(np.abs(r-prev).mean())
        if i>=s: out.append((i,round(dark,3),round(d,2)))
        prev=r
    i+=1
print(json.dumps(out))
