import cv2,sys,numpy as np,json
v,key=sys.argv[1:3]
cap=cv2.VideoCapture(v); prev=None; res=[]; i=0
while True:
    ok,f=cap.read()
    if not ok:break
    r=f[1150:1550,60:1020]
    g=cv2.cvtColor(r,cv2.COLOR_BGR2GRAY)
    m=(g>=245).astype(np.uint8)
    m=cv2.resize(m,(240,100),interpolation=cv2.INTER_AREA) 
    cnt=float(m.sum())
    if prev is not None:
        a=np.abs(m.astype(int)-prev.astype(int)).sum()
        res.append((i,cnt,float(a)))
    else: res.append((i,cnt,0.))
    prev=m;i+=1
json.dump(res,open(f'cap_{key}.json','w'))
