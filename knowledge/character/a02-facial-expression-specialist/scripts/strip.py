import cv2,sys,numpy as np
v,key,start,n,x,y,w,h,out=sys.argv[1:10]
start,n,x,y,w,h=map(int,(start,n,x,y,w,h)); cols=int(sys.argv[10]) if len(sys.argv)>10 else 8
tw=int(sys.argv[11]) if len(sys.argv)>11 else 150
cap=cv2.VideoCapture(v); tiles=[]
for i in range(start+n):
    ok,f=cap.read()
    if not ok:break
    if i>=start:
        c=cv2.resize(f[y:y+h,x:x+w],(tw,int(tw*h/w)),interpolation=cv2.INTER_AREA)
        cv2.putText(c,str(i),(2,14),cv2.FONT_HERSHEY_SIMPLEX,.45,(0,255,255),1)
        tiles.append(c)
th=tiles[0].shape[0]
rows=[]
for r in range(0,len(tiles),cols):
    row=tiles[r:r+cols]
    while len(row)<cols: row.append(np.zeros_like(tiles[0]))
    rows.append(np.hstack(row))
cv2.imwrite(out,np.vstack(rows))
