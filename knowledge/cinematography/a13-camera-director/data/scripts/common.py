import csv, json, glob, numpy as np, os
R='/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0'
def keys(): return sorted(os.path.basename(os.path.dirname(f)) for f in glob.glob(R+'/RC30-*/motion.csv'))
def load(k, mask_cuts=True, pad=2):
    r=list(csv.DictReader(open(f'{R}/{k}/motion.csv')))
    n=len(r)
    a=np.array([[float(x[c]) for c in ('tx','ty','scale','rot_deg')] for x in r])
    conf=np.array([x['confidence'] for x in r])
    d=np.zeros((n,4)); d[:,0]=a[:,0]/320*100; d[:,1]=a[:,1]/320*100; d[:,2]=(a[:,2]-1)*100; d[:,3]=a[:,3]
    bad=(conf=='low')|(conf=='none')|np.isnan(d).any(1)
    cands=json.load(open(f'{R}/{k}/shot_candidates.json'))['candidates']
    cm=np.zeros(n,bool)
    for c in cands:
        s,e=c['start'],c['end']; cm[max(0,s-pad):min(n,e+pad+1)]=True
    if mask_cuts: bad=bad|cm
    d[bad]=np.nan
    return d,bad,cands,[x['frame_id'] for x in r]
