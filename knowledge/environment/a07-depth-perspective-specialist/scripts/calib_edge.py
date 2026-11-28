import sys,numpy as np,cv2,json
sys.path.insert(0,'.')
from edgesigma import *
path,fl=sys.argv[1],[int(x) for x in sys.argv[2].split(',')]
out={}
for fi,img in frames(path,1) if False else []: pass
import subprocess
for f in fl:
    cmd=['ffmpeg','-nostdin','-v','error','-i',path,'-vf',f"select='eq(n\\,{f})'",'-frames:v','1','-f','rawvideo','-pix_fmt','bgr24','-']
    b=subprocess.run(cmd,capture_output=True).stdout
    img=np.frombuffer(b,np.uint8).reshape(H,W,3); g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)
    for s in [0,1,2,3,4,6,8,12,16]:
        gg=g if s==0 else cv2.GaussianBlur(g,(0,0),s)
        c=cells(gg); v=[x[3] for x in c if x[3]==x[3]]
        out.setdefault(s,[]).append(float(np.median(v)))
    print(f,{s:round(out[s][-1],2) for s in out},flush=True)
json.dump(out,open(sys.argv[3],'w'))
