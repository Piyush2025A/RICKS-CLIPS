#!/usr/bin/env python3
"""3B native patch stats. usage: patch3b.py <natdir> <outjson> <montage.png>  (run with .venv-analysis python -I)
Patch = central 120x120 of a 180x192 grid cell (grid 6x10 on 1080x1920). Metrics: L*,C*,h (CIELAB), local std 7x7 of L*,
strong-gradient fraction (contamination flag), high-frequency power ratio (FFT, radius > 1/8 cycles/px vs all non-DC)."""
import cv2,numpy as np,json,sys
from skimage import color
from scipy.ndimage import uniform_filter
nat,outj,mont=sys.argv[1:4]
P=[("04-f000539","E8","grass","A"),("04-f000539","A5","paint_red","A"),("04-f000539","E5","metal_painted_white","A"),("04-f000539","A9","gravel_road","A"),
("07-f000419","E8","grass","A"),("07-f000419","B1","siding_plastic","A"),("07-f000419","F5","paint_red_car","A"),("07-f000419","C6","fabric_sheet","A"),("07-f000419","E0","sky","A"),
("10-f000629","D9","gravel_ballast","A"),("10-f000629","A6","orange_earth","A"),("10-f000629","B1","sky","A"),
("12-f000209","C8","wood_planks","A"),("12-f000209","D6","fabric_striped","A"),("12-f000209","D2","skin_flat_head","A"),
("14-f000209","C8","sand","A"),("14-f000209","B0","sky","A"),
("08-f000629","E8","grass_night","A"),("08-f000629","B0","sky_night","A"),
("15-f000809","C2","mesh_pattern","B"),("15-f000809","E9","floor_tile","B"),
("17-f000749","A1","wood_siding_snow","B"),("17-f000749","A8","snow_ground","B"),
("20-f000299","E5","enamel_fridge","B"),("20-f000299","A8","checker_tile","B"),("20-f000299","A1","wall_flat_yellow","B"),
("21-f000329","C5","metal_bell","B"),("21-f000329","F8","carpet_floor","B"),
("23-f000299","B9","ground_dirt","B"),("23-f000299","E4","card_paper","B"),
("26-f000869","E7","plastic_crate","B"),("26-f000869","A1","wall_dark","B"),
("03-f000839","D6","wood_barrel","A"),("03-f000839","E9","dirt","A"),
("25-f000419","B1","flesh_wall","B"),("25-f000419","D9","floor_red","B")]
# the 25/26 frame ids: 25 f419 and 26 f869 exist in natdir
res=[];tiles=[]
for fid,cell,mat,tr in P:
    k=fid[:2]; im=cv2.imread(f"{nat}/RC30-{fid}.png")
    if im is None: print("missing",fid);continue
    c="ABCDEF".index(cell[0]); r=int(cell[1]); x=180*c+30;y=192*r+36
    p=im[y:y+120,x:x+120]; lab=color.rgb2lab(p[:,:,::-1].copy()/255.)
    L=lab[:,:,0]; C=np.hypot(lab[:,:,1],lab[:,:,2]); h=np.degrees(np.arctan2(np.median(lab[:,:,2]),np.median(lab[:,:,1])))%360
    ls=np.sqrt(np.maximum(uniform_filter(L*L,7)-uniform_filter(L,7)**2,0))
    g=cv2.Laplacian(L.astype(np.float32),cv2.CV_32F); gx=cv2.Sobel(L.astype(np.float32),cv2.CV_32F,1,0);gy=cv2.Sobel(L.astype(np.float32),cv2.CV_32F,0,1)
    gm=np.hypot(gx,gy)/8
    F=np.abs(np.fft.fftshift(np.fft.fft2(L-L.mean())))**2; yy,xx=np.indices(F.shape);rad=np.hypot(yy-60,xx-60)/120
    hf=F[rad>1/8].sum()/max(F[rad>0.005].sum(),1e-9)
    res.append(dict(frame=f"RC30-{fid}",cell=cell,material=mat,treat=tr,L_med=round(float(np.median(L)),1),L_p10=round(float(np.percentile(L,10)),1),L_p90=round(float(np.percentile(L,90)),1),C_med=round(float(np.median(C)),1),hue=round(float(h)),local_std_med=round(float(np.median(ls)),2),L_std=round(float(L.std()),2),strong_grad_frac=round(float((gm>12).mean()),3),hf_ratio=round(float(hf),4)))
    t=cv2.resize(p,(240,240),interpolation=cv2.INTER_NEAREST); cv2.putText(t,f"{mat[:14]}",(3,14),0,0.45,(0,0,255),2); cv2.putText(t,f"{fid[:2]}{cell}",(3,235),0,0.45,(0,255,255),1); tiles.append(t)
json.dump(res,open(outj,"w"),indent=1)
while len(tiles)%6:tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(mont,np.vstack([np.hstack(tiles[i:i+6]) for i in range(0,len(tiles),6)]))
for d in res: print(d["frame"][5:],d["cell"],d["material"],d["L_med"],d["C_med"],d["hue"],d["local_std_med"],d["strong_grad_frac"],d["hf_ratio"])
