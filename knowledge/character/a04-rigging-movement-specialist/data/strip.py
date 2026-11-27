import cv2,numpy as np,sys,os
n=int(sys.argv[1]);f0=int(sys.argv[2]);f1=int(sys.argv[3]);step=int(sys.argv[4]);cols=int(sys.argv[5])
crop=tuple(map(int,sys.argv[6:10])) if len(sys.argv)>9 else (0,0,1080,1920)
tw=int(sys.argv[10]) if len(sys.argv)>10 else 200
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES,f0); tiles=[]
for i in range(f0,f1+1):
    ok,f=cap.read()
    if not ok:break
    if (i-f0)%step: continue
    x0,y0,x1,y1=crop; f=f[y0:y1,x0:x1]
    s=tw/f.shape[1]; f=cv2.resize(f,(tw,int(f.shape[0]*s)),interpolation=cv2.INTER_AREA)
    cv2.putText(f,str(i),(3,14),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),1)
    tiles.append(f)
rows=[]
for r in range(0,len(tiles),cols):
    row=tiles[r:r+cols]
    while len(row)<cols: row.append(np.zeros_like(tiles[0]))
    rows.append(np.hstack(row))
out=f'/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a04-rigging-movement-specialist/s_{n}_{f0}_{f1}.png'
os.makedirs(os.path.dirname(out),exist_ok=True)
cv2.imwrite(out,np.vstack(rows));print(out)
