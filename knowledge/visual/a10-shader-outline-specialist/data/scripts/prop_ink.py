"""A10 3B: width of dark ink strokes on props: horizontal rows over a prop edge; FWHM of darkest run vs half-depth of local background (gray). Frames from ffmpeg (n=300). Args: frames_dir"""
import sys,cv2,numpy as np,json
D=sys.argv[1]
def run(v,xr,yr,name):
    g=cv2.cvtColor(cv2.imread(f"{D}/RC30-{v:02d}_1.png"),cv2.COLOR_BGR2GRAY).astype(float); ws=[];cores=[]
    for y in range(*yr,6):
        p=g[y,xr[0]:xr[1]]; i=int(np.argmin(p)); c=p[i]
        if c>90: continue
        ref=max(np.median(p[:max(1,i-30)]) if i>30 else 255, np.median(p[i+30:]) if i+30<len(p) else 255)
        h=(c+min(ref,np.median(p[i+25:]) if i+25<len(p) else ref))/2
        l=i
        while l>0 and p[l]<h:l-=1
        r=i
        while r<len(p)-1 and p[r]<h:r+=1
        ws.append(r-l);cores.append(c)
    print(name,"n",len(ws),"median %.1f"%np.median(ws),"IQR",np.percentile(ws,[25,75]),"core",np.median(cores))
    return ws
run(19,(225,345),(760,880),"19 clock rim (x225-345,y760-880)")
run(28,(225,345),(690,810),"28 porthole ring (x225-345,y690-810)")
