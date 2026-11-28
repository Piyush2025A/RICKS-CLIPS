"""3B push validation. Native 1080x1920 frames (ffmpeg decode, index n == frame index) downscaled to 360x640 gray.
(a) direct: SIFT start->end, RANSAC similarity (estimateAffinePartial2D) -> true total scale S_direct
(b) chained: Shi-Tomasi+LK per consecutive frame at 360x640, similarity fit -> per-frame scale, product.
Run with .venv-analysis python.  Usage: push3b.py"""
import csv, subprocess, sys, json, random, numpy as np, cv2, os
M='/home/piyush/RICKS-CLIPS/knowledge/cinematography/a13-camera-director/data/moves_table.csv'
V='/home/piyush/ricks-clips-private/reference-videos/RC30/%d.mp4'
OUT='/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a13-camera-director/push3b'
W,H=360,640
rows=list(csv.DictReader(open(M)))
c=[r for r in rows if r['kind'].startswith('push') and r['fast']=='False' and r['near_cand']=='False' and int(r['dur'])>=20 and abs(float(r['R']))<4]
random.seed(13); random.shuffle(c)
sel=[];cnt={}
for r in c:
    if cnt.get(r['key'],0)<2: sel.append(r); cnt[r['key']]=cnt.get(r['key'],0)+1
sel.sort(key=lambda r:(r['key'],int(r['start'])))
def decode(vid,a,b):
    cmd=['ffmpeg','-nostdin','-v','error','-i',V%vid,'-vf',f"select='between(n\\,{a}\\,{b})',scale={W}:{H}:flags=area,format=gray",'-fps_mode','passthrough','-f','rawvideo','-']
    d=subprocess.run(cmd,capture_output=True).stdout
    return np.frombuffer(d,np.uint8).reshape(-1,H,W)
sift=cv2.SIFT_create(2000)
def direct(a,b):
    ka,da=sift.detectAndCompute(a,None); kb,db=sift.detectAndCompute(b,None)
    if da is None or db is None or len(ka)<8 or len(kb)<8: return None
    m=cv2.BFMatcher().knnMatch(da,db,k=2)
    g=[x[0] for x in m if len(x)==2 and x[0].distance<0.75*x[1].distance]
    if len(g)<8: return None
    pa=np.float32([ka[x.queryIdx].pt for x in g]); pb=np.float32([kb[x.trainIdx].pt for x in g])
    T,inl=cv2.estimateAffinePartial2D(pa,pb,method=cv2.RANSAC,ransacReprojThreshold=3)
    if T is None: return None
    s=float(np.hypot(T[0,0],T[1,0])); return s,int(inl.sum()),len(g)
def chain(fr):
    out=[]
    for i in range(1,len(fr)):
        p=cv2.goodFeaturesToTrack(fr[i-1],500,0.01,8)
        if p is None: out.append(np.nan); continue
        q,st,_=cv2.calcOpticalFlowPyrLK(fr[i-1],fr[i],p,None,winSize=(21,21),maxLevel=3)
        ok=st.ravel()==1
        if ok.sum()<8: out.append(np.nan); continue
        T,inl=cv2.estimateAffinePartial2D(p[ok],q[ok],method=cv2.RANSAC,ransacReprojThreshold=2)
        out.append(float(np.hypot(T[0,0],T[1,0])) if T is not None else np.nan)
    return np.array(out)
res=[]
for r in sel:
    k=r['key']; vid=int(k[-2:]); a=int(r['start']); b=int(r['end'])
    fr=decode(vid,a-1,b)
    if len(fr)<b-a+2: print('short',k,a,b,len(fr)); continue
    # start/end frames: window offset +1 because moves table start is first increment? use fr[0] (=a) .. fr[b-a]
    d=direct(fr[0],fr[-1]); ch=chain(fr)
    cum=np.concatenate([[1],np.nancumprod(np.nan_to_num(ch,nan=1.0))])
    np.save(f'{OUT}/{k}_{a}_{b}_cum.npy',cum)
    Z=float(r['Z']); proxy_c=None
    res.append(dict(key=k,start=a,end=b,dur=b-a,Z=Z,S_direct=d[0] if d else None,inl=d[1] if d else None,nm=d[2] if d else None,S_chain=float(cum[-1]),nan_frac=float(np.isnan(ch).mean()),X=r['X'],Y=r['Y'],R=r['R'],best=r['best']))
    print(k,a,b,Z,res[-1]['S_direct'],res[-1]['S_chain'],flush=True)
json.dump(res,open(OUT+'/push3b.json','w'),indent=1)
