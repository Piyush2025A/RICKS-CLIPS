import cv2,numpy as np,sys,json
from skimage.feature import graycomatrix,graycoprops
D='/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a08-prop-texture-designer/nat/'
def stats(fid,box,name):
    im=cv2.imread(D+fid+'.png'); x0,y0,x1,y1=box; p=im[y0:y1,x0:x1]
    lab=cv2.cvtColor(p.astype(np.float32)/255,cv2.COLOR_BGR2Lab)
    L,a,b=lab[...,0],lab[...,1],lab[...,2]; C=np.hypot(a,b)
    hp=L-cv2.GaussianBlur(L,(0,0),2.0)       # high-pass: removes scales > ~sigma 2 px
    mu=cv2.blur(L,(7,7)); sd=np.sqrt(np.maximum(cv2.blur(L*L,(7,7))-mu*mu,0))
    g=np.clip(L/100*31,0,31).astype(np.uint8)
    gl=graycomatrix(g,[2],[0,np.pi/2],32,symmetric=True,normed=True)
    lap=cv2.Laplacian(L,cv2.CV_32F).var()
    r=dict(fid=fid,name=name,box=box,n_px=int(L.size),L_med=round(float(np.median(L)),1),L_p10=round(float(np.percentile(L,10)),1),L_p90=round(float(np.percentile(L,90)),1),
      C_med=round(float(np.median(C)),1),hue_deg=round(float(np.degrees(np.arctan2(np.median(b),np.median(a)))),0),
      L_std=round(float(L.std()),2),localstd7_med=round(float(np.median(sd)),2),hp_std=round(float(hp.std()),2),lap_var=round(float(lap),1),glcm_contrast=round(float(graycoprops(gl,'contrast').mean()),2))
    return r
if __name__=='__main__':
    P=json.load(open(sys.argv[1])); out=[stats(*p) for p in P]
    for r in out: print(r)
    json.dump(out,open(sys.argv[2],'w'),indent=1)
