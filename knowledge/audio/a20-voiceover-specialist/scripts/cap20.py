import sys,subprocess,numpy as np,cv2
n=sys.argv[1]
mp4=f"/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4"
W,H=960,400
p=subprocess.Popen(["ffmpeg","-v","error","-i",mp4,"-vf",f"crop={W}:{H}:60:1150,format=gray","-f","rawvideo","-"],stdout=subprocess.PIPE,bufsize=W*H*4)
rows=[];prev=None;i=0
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H:break
    g=np.frombuffer(b,np.uint8).reshape(H,W)
    m=(g>=245).astype(np.uint8)
    s=cv2.resize(m,(240,100),interpolation=cv2.INTER_AREA).astype(np.float32)
    cnt=float(s.sum());d=float(np.abs(s-prev).sum()) if prev is not None else 0.
    cols=np.where(s.sum(0)>0.5)[0]
    xmin,xmax=(int(cols[0]),int(cols[-1])) if len(cols) else (-1,-1)
    rows.append((i,cnt,d,xmin,xmax));prev=s;i+=1
np.save(f"capser_{n}.npy",np.array(rows,dtype=np.float32));print(n,i)
