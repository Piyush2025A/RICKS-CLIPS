from common import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, sys
k=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
d,bad,c,_=load(k,mask_cuts=False); d2,bad2,_,_=load(k)
fig,ax=plt.subplots(4,1,figsize=(16,10),sharex=True)
x=np.arange(len(d))
for i,(nm) in enumerate(['tx %W/f','ty %W/f','scale %/f','rot deg/f']):
    ax[i].plot(x,d[:,i],lw=.6,c='lightgray'); ax[i].plot(x,d2[:,i],lw=.9); ax[i].set_ylabel(nm); ax[i].grid(alpha=.3)
    for cc in c: ax[i].axvspan(cc['start'],cc['end'],color='r' if cc['type']!='gradual_candidate' else 'orange',alpha=.2)
ax[0].set_xlim(a,b); 
for i in range(3): ax[i].set_ylim(-8,8)
ax[2].set_ylim(-6,6)
plt.tight_layout(); plt.savefig(f'plot_{k}_{a}_{b}.png',dpi=60)
