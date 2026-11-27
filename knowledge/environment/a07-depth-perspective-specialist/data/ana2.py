import json, numpy as np, collections
from load import load
from labels import LAB
k,a=load(); fr,gy,gx,lv,ls,sat,L,ch=a.T
hf=lv/np.maximum(ls,1)**2
sel=json.load(open('montage_sel.json'))
cal=json.load(open('calib_curve.json')); S=np.array(cal['sigma']); R=np.array(cal['ratio_median'])
def sig_from_ratio(r):
    r=min(max(r,1e-4),1.0); return float(np.interp(np.log(r),np.log(R[::-1].clip(1e-5)),S[::-1]))
def frame_metrics(key,f):
    m=(k==key)&(fr==f)
    h=hf[m]; s=ls[m]; g=gy[m]; l=lv[m]
    tex=s>10
    if tex.sum()<3: return None
    ref=np.percentile(h[tex],90)
    top=tex&(g<=1)
    if top.sum()<1: return None
    bgr=np.median(h[top])/max(ref,1e-6)
    return bgr, sig_from_ratio(bgr), ref
out=[]
for (key,f),lab in zip(sel,LAB):
    mm=frame_metrics(key,f)
    out.append((key,f,lab,mm))
for d in (0,1,2):
    v=[o[3][0] for o in out if o[2][1]==d and o[3]]
    s=[o[3][1] for o in out if o[2][1]==d and o[3]]
    print('dof',d,'n',len(v),'bg/ref hf ratio med',np.round(np.median(v),3),'IQR',np.round(np.percentile(v,[25,75]),3),'sigma_eq med',np.round(np.median(s),2),np.round(np.percentile(s,[25,75]),2))
c=collections.Counter((o[2][0],o[2][1]) for o in out if o[2][0]); print(sorted(c.items()))
c2=collections.Counter(o[2][2] for o in out if o[2][2]); print(c2)
hz=[o[2][3] for o in out if o[2][3]]; print('horizon y',sorted(hz), np.median(hz))
json.dump([(o[0],o[1],o[2],o[3]) for o in out],open('labelled_frames.json','w'))
