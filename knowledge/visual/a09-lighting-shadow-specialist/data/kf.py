import cv2,glob,numpy as np,json,sys
def lin(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
res={}
B=8
for f in sorted(glob.glob('f/[0-3][0-9]_f*.png')):
    v=int(f.split('/')[1][:2]); fid=f.split('/')[1][:-4]
    im=cv2.imread(f)[:,:,::-1]; im=cv2.resize(im,(270,480),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    lab=cv2.cvtColor((im*255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32); L=lab[...,0]*100/255; a=lab[...,1]-128; b=lab[...,2]-128
    Y=(lin(im)@np.array([.2126,.7152,.0722]))
    H,W=480//B,270//B
    def bl(x): return x[:H*B,:W*B].reshape(H,B,W,B)
    mY=bl(Y).mean((1,3)); sY=bl(Y).std((1,3))/(mY+0.02)
    ma=bl(a).mean((1,3)); mb=bl(b).mean((1,3)); 
    flat=sY<0.08
    for dirn in ('h','v'):
        for i in range(H if dirn=='h' else H-3):
            for j in range(W-3 if dirn=='h' else W):
                idx=[(i,j+k) for k in range(4)] if dirn=='h' else [(i+k,j) for k in range(4)]
                ys=[mY[p] for p in idx]
                if not all(flat[p] for p in idx): continue
                r0=idx[0][0]*B/480
                if 0.64<r0<0.76 : continue
                lit=(ys[0]+ys[1])/2; sh=(ys[2]+ys[3])/2
                if min(ys[0],ys[1])<0.7*max(ys[0],ys[1]) or min(ys[2],ys[3])<0.7*max(ys[2],ys[3]): continue
                r=sh/lit
                if not (0.05<r<0.7) or lit<0.05: continue
                da=(ma[idx[2]]+ma[idx[3]]-ma[idx[0]]-ma[idx[1]])/2; db=(mb[idx[2]]+mb[idx[3]]-mb[idx[0]]-mb[idx[1]])/2
                # same-material proxy: lit/shade chroma vector change small in hue angle
                if np.hypot(da,db)>25: continue
                res.setdefault(fid,[]).append((float(r),float(db)))
json.dump({k:v for k,v in res.items()},open('kf.json','w'))
per={}
for k,v in res.items():
    per.setdefault(int(k[:2]),[]).extend(v)
out=[]
for v in sorted(per):
    r=np.array([x[0] for x in per[v]]); out.append((v,len(r),float(np.median(r))))
    print(v,len(r),round(np.median(r),3),round(np.percentile(r,25),3),round(np.percentile(r,75),3))
m=np.array([o[2] for o in out if o[1]>=10]); print('videos',len(m),'median of video medians',np.median(m),np.percentile(m,[25,75]))
