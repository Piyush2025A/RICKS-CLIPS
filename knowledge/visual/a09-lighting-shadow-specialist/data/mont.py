import cv2,numpy as np,sys,glob
S=sys.argv[1]
def crop(n,k,y0=250,h=620,w=620,x0=230):
    im=cv2.imread(f"{S}/nat/RC30-{n:02d}_{k}.png"); 
    if im is None: return np.zeros((h//2,w//2,3),np.uint8)
    c=im[y0:y0+h,x0:x0+w].copy(); c=cv2.resize(c,(w//2,h//2),interpolation=cv2.INTER_AREA)
    cv2.putText(c,f"{n:02d}.{k}",(5,22),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2); return c
for part,rng in enumerate([range(1,11),range(11,21),range(21,31)]):
    rows=[np.hstack([crop(n,1) for n in list(rng)[:5]]),np.hstack([crop(n,1) for n in list(rng)[5:]])]
    cv2.imwrite(f"{S}/mont_scen_{part}.png",np.vstack(rows))
