import cv2,numpy as np
from skimage.morphology import skeletonize
from scipy import ndimage as ndi
D='/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a08-prop-texture-designer/nat/'
def lw(fid,box,name,drop=12):
    im=cv2.imread(D+fid+'.png'); x0,y0,x1,y1=box
    L=cv2.cvtColor(im.astype(np.float32)/255,cv2.COLOR_BGR2Lab)[...,0]
    bl=cv2.GaussianBlur(L,(0,0),6); m=(L<bl-drop)[y0:y1,x0:x1]
    m=ndi.binary_opening(m,np.ones((2,2)))
    sk=skeletonize(m); dt=ndi.distance_transform_edt(m)
    w=2*dt[sk]; 
    if len(w)<20: return (fid,name,'n/a',len(w))
    return dict(fid=fid,name=name,n_skel=int(len(w)),width_px_med=round(float(np.median(w)),1),p25=round(float(np.percentile(w,25)),1),p75=round(float(np.percentile(w,75)),1))
for t in [('RC30-16-f000599',(480,900,1080,1500),'B machine props, near-mid'),
 ('RC30-16-f000599',(0,1560,1080,1800),'B conveyor cabinet'),
 ('RC30-18-f000449',(60,860,980,1200),'B wallet+licence'),
 ('RC30-09-f000359',(0,380,1080,1050),'hybrid prison wall/doors/rails (far)'),
 ('RC30-05-f000449',(100,60,1000,400),'A cliff w/ cracks'),
 ('RC30-27-f000209',(60,480,1080,900),'A slot marquee'),
 ('RC30-09-f000209',(0,180,780,420),'hybrid planks')]:
    print(lw(*t))
