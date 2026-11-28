#!/usr/bin/env python3
"""3B round 2: explicit native boxes (x,y,w,h) chosen on grid composites + plank seam FWHM. usage: patch3b_xy.py natdir out.json montage.png"""
import cv2,numpy as np,json,sys
from skimage import color
from scipy.ndimage import uniform_filter
nat,outj,mont=sys.argv[1:4]
P=[("12-f000209",(330,1050,100,100),"fabric_bedspread"),("12-f000209",(600,1290,100,100),"wood_planks_b"),("12-f000209",(590,395,90,60),"skin_forehead_fill"),
("21-f000329",(300,1030,90,90),"metal_bell_grey"),("21-f000329",(30,150,100,100),"stone_pillar"),("25-f000419",(400,1470,80,80),"glass_pill_cap"),
("20-f000299",(780,1130,100,100),"enamel_fridge_face"),("04-f000539",(30,1330,100,100),"paint_red_b"),("17-f000749",(250,280,100,100),"wood_siding_b")]
res=[];tiles=[]
for fid,(x,y,w,h),m in P:
    im=cv2.imread(f"{nat}/RC30-{fid}.png"); p=im[y:y+h,x:x+w]; lab=color.rgb2lab(p[:,:,::-1].copy()/255.)
    L=lab[:,:,0]; C=np.hypot(lab[:,:,1],lab[:,:,2]); hh=np.degrees(np.arctan2(np.median(lab[:,:,2]),np.median(lab[:,:,1])))%360
    ls=np.sqrt(np.maximum(uniform_filter(L*L,7)-uniform_filter(L,7)**2,0))
    gx=cv2.Sobel(L.astype(np.float32),cv2.CV_32F,1,0);gy=cv2.Sobel(L.astype(np.float32),cv2.CV_32F,0,1);gm=np.hypot(gx,gy)/8
    res.append(dict(frame="RC30-"+fid,box=[x,y,w,h],material=m,L_med=round(float(np.median(L)),1),L_p10=round(float(np.percentile(L,10)),1),L_p90=round(float(np.percentile(L,90)),1),C_med=round(float(np.median(C)),1),hue=round(float(hh)),local_std_med=round(float(np.median(ls)),2),strong_grad_frac=round(float((gm>12).mean()),3)))
    t=cv2.resize(p,(240,240),interpolation=cv2.INTER_NEAREST);cv2.putText(t,m[:16],(3,14),0,0.45,(0,0,255),2);tiles.append(t)
# plank seam FWHM
im=cv2.imread(f"{nat}/RC30-12-f000209.png");lab=color.rgb2lab(im[:,:,::-1].copy()/255.)[:,:,0]
strip=lab[1330:1420,450:1000]; prof=np.median(strip,axis=0); base=uniform_filter(prof,41)
d=base-prof; seams=[]
from scipy.signal import find_peaks
pk,_=find_peaks(d,height=2.0,distance=15)
for k in pk:
    half=d[k]/2; a=k
    while a>0 and d[a]>half:a-=1
    b=k
    while b<len(d)-1 and d[b]>half:b+=1
    seams.append(dict(x=int(k+450),depth_L=round(float(d[k]),1),fwhm_px=int(b-a)))
res.append(dict(seams=seams,note="column-median L* over rows 1330-1420 minus 41-px running mean; dips = plank seams (perspective-tilted so FWHM overestimates)"))
json.dump(res,open(outj,"w"),indent=1)
while len(tiles)%5:tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(mont,np.vstack([np.hstack(tiles[i:i+5]) for i in range(0,len(tiles),5)]))
for d in res:print(d)
