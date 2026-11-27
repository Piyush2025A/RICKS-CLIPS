"""A10 whole-frame line-width histogram v1: horizontal scanlines rows 60..0.68H step 6 (caption band 0.68-0.80H and bottom excluded), peaks of inverted gray with prominence>=30 (dark line on lighter ground), FWHM via peak_widths(.5), keep 1..40 px. 
Classes: hair <=5.0 px ; heavy >=8 px. Heavy = character ink (also dark masses, hair). Per-frame medians reported."""
import cv2,numpy as np,sys,os,json
from scipy.signal import find_peaks,peak_widths
out={}
for p in sorted(sys.argv[1:]):
    g=cv2.cvtColor(cv2.imread(p),cv2.COLOR_BGR2GRAY).astype(float); H,W=g.shape; ws=[];core=[]
    for y in range(60,int(.68*H),6):
        pr=255-cv2.GaussianBlur(g[y:y+1],(0,0),0.6)[0]; pk,pp=find_peaks(pr,prominence=30)
        if len(pk)==0: continue
        w=peak_widths(pr,pk,rel_height=.5)[0]
        for x,ww in zip(pk,w):
            if 1<=ww<=40: ws.append(ww); core.append(g[y,x])
    ws=np.array(ws); k=os.path.basename(p)[:-4]
    if len(ws)==0: continue
    out[k]=dict(n=len(ws),hair_share=float((ws<=5).mean()),heavy_share=float((ws>=8).mean()),hair_med=float(np.median(ws[ws<=5])) if (ws<=5).any() else None,heavy_med=float(np.median(ws[ws>=8])) if (ws>=8).any() else None,all_med=float(np.median(ws)))
    print(k,{a:(round(b,2) if b is not None else None) for a,b in out[k].items()})
json.dump(out,open("lines_all.json","w"),indent=1)
