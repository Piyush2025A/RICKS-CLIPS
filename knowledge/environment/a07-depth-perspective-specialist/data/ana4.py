import json, numpy as np, collections
from load import load
from labels import LAB
k,a=load(); fr,gy,gx,lv,ls,sat,L,ch=a.T
sel=json.load(open('montage_sel.json'))
lab=[(s[0],s[1])+tuple(l) for s,l in zip(sel,LAB)]
valid=[x for x in lab if x[3] is not None]
n=len(valid); print('valid',n,'videos',len(set(x[0] for x in valid)))
def wil(p,n,z=1.96):
    d=1+z*z/n; c=p+z*z/(2*n); r=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n)); return round((c-r)/d,3),round((c+r)/d,3)
for dofmin in (1,2):
    x=sum(1 for v in valid if v[3]>=dofmin); print('dof>=',dofmin,x,n,round(x/n,3),wil(x/n,n))
    print(' videos with >=1:',len(set(v[0] for v in valid if v[3]>=dofmin)))
for t in 'CMWX':
    s=[v for v in valid if v[2]==t]; x=sum(1 for v in s if v[3]>=1); y=sum(1 for v in s if v[3]>=2)
    print(t,len(s),'share',round(len(s)/n,2),'dof>=1',x,round(x/len(s),2),wil(x/len(s),len(s)),'dof2',y)
for c in 'ELH': print(c,sum(1 for v in valid if v[4]==c),round(sum(1 for v in valid if v[4]==c)/n,2))
hz=[v[5] for v in valid if v[5]]; print('horizon',len(hz),np.median(hz),np.percentile(hz,[25,75]),'videos',len(set(v[0] for v in valid if v[5])))
# horizon vs cam
for c in 'ELH':
    h=[v[5] for v in valid if v[5] and v[4]==c]; print(c,h)
# row stats per video medians
vids=sorted(set(k)); R={r:[] for r in range(4)}
rowstat=[]
for v in vids:
    m=k==v; row=[]
    for r in range(4):
        s=m&(gy==r); row.append((np.median(sat[s]),np.median(L[s]),np.median(ch[s]),np.median(ls[s])))
    rowstat.append(row)
rs=np.array(rowstat) # v,row,stat
for si,nm in enumerate(['sat','L','chroma','lstd']):
    print(nm,'row medians across videos',np.round(np.median(rs[:,:,si],0),1),'IQR row0',np.round(np.percentile(rs[:,0,si],[25,75]),1),'row3',np.round(np.percentile(rs[:,3,si],[25,75]),1),'videos row0<row3:',int((rs[:,0,si]<rs[:,3,si]).sum()))
# dof by video frequency
per=collections.defaultdict(lambda:[0,0])
for v in valid: per[v[0]][0]+=1; per[v[0]][1]+= v[3]>=1
print({kk:tuple(vv) for kk,vv in sorted(per.items())})
h=json.load(open('haze_cases.json'))
far=np.array([c['dE_far_to_sky'] for c in h]); near=np.array([c['dE_near_to_sky'] for c in h]); mid=np.array([c['dE_mid_to_sky'] for c in h])
print('far',np.median(far),np.percentile(far,[25,75]),'mid',np.median(mid),'near',np.median(near),np.percentile(near,[25,75]),'haze_delta(near-far)',np.median(near-far),np.percentile(near-far,[25,75]),'ratio far/near',np.round(np.median(far/near),2),np.round(np.percentile(far/near,[25,75]),2))
