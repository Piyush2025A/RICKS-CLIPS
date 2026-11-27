import json, numpy as np
from load import load
from labels import LAB
k,a=load(); fr,gy,gx,lv,ls,sat,L,ch=a.T
hf=lv/np.maximum(ls,1)**2
sel=json.load(open('montage_sel.json'))
def stats(key,f):
    m=(k==key)&(fr==f); h=hf[m]; s=ls[m]; g=gy[m]; x=gx[m]; l=lv[m]
    tex=s>10
    if tex.sum()<4: return None
    ref=np.percentile(h[tex],90); 
    allr=h[tex]/ref
    top=tex&(g<=2)
    return dict(med_all=float(np.median(allr)), p25_all=float(np.percentile(allr,25)), frac_soft=float((allr<0.1).mean()), lap_med=float(np.median(l)), maxlap=float(l.max()), softmax=float(np.log10(l.max()/max(np.median(l),1))), ntex=int(tex.sum()))
rows=[]
for (key,f),lab in zip(sel,LAB):
    if lab[1] is None: continue
    st=stats(key,f)
    if st: rows.append((lab[1]>=1,st))
def auc(name,sign=1):
    pos=np.array([sign*r[1][name] for r in rows if r[0]]); neg=np.array([sign*r[1][name] for r in rows if not r[0]])
    return np.mean([(p>n)+0.5*(p==n) for p in pos for n in neg])
for n,s in [('med_all',-1),('p25_all',-1),('frac_soft',1),('lap_med',-1),('maxlap',-1),('softmax',1)]:
    print(n,'AUC',round(auc(n,s),3), 'pos med',np.round(np.median([r[1][n] for r in rows if r[0]]),3),'neg med',np.round(np.median([r[1][n] for r in rows if not r[0]]),3))
print(sum(r[0] for r in rows),len(rows))
