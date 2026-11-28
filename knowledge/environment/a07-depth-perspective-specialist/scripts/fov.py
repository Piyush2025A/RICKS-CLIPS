import cv2,glob,numpy as np,json
rng=np.random.RandomState(1)
lsd=cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD)
def vp_ransac(L,iters=600,thr=0.035):
    # L: Nx3 homogeneous lines normalised; segments mid, dir
    best=None
    N=len(L)
    for _ in range(iters):
        i,j=rng.choice(N,2,replace=False)
        v=np.cross(L[i],L[j])
        if abs(v[2])<1e-9: v=v/ (np.linalg.norm(v)+1e-9)*1e9
        inl=consist(v,L,thr)
        if best is None or inl.sum()>best[1].sum(): best=(v,inl)
    return best
def consist(v,S,thr):
    # S: rows (mx,my,dx,dy); angle between segment dir and direction to vp
    mx,my,dx,dy=S.T
    vx,vy,vw=v
    if abs(vw)<1e-9: tx,ty=vx*np.ones_like(mx),vy*np.ones_like(my)
    else: tx,ty=vx/vw-mx,vy/vw-my
    n=np.hypot(tx,ty)+1e-9; c=np.abs((tx*dx+ty*dy)/n)
    return c>np.cos(thr)
def run(im):
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); H,W=g.shape
    ln=lsd.detect(g)[0]
    if ln is None: return None
    ln=ln.reshape(-1,4); ln=ln[np.hypot(ln[:,2]-ln[:,0],ln[:,3]-ln[:,1])>35]
    my=(ln[:,1]+ln[:,3])/2; ln=ln[~((my>.55*H)&(my<.85*H))]  # caption band
    if len(ln)<40: return None
    dx=ln[:,2]-ln[:,0]; dy=ln[:,3]-ln[:,1]; n=np.hypot(dx,dy); dx/=n; dy/=n
    S=np.stack([(ln[:,0]+ln[:,2])/2,(ln[:,1]+ln[:,3])/2,dx,dy],1)
    Ls=np.array([np.cross([a,b,1],[a+c,b+d,1]) for a,b,c,d in S]); Ls/=np.linalg.norm(Ls[:,:2],axis=1,keepdims=True)
    def fit(idx,iters=800):
        best=(None,np.zeros(len(idx),bool))
        for _ in range(iters):
            i,j=rng.choice(len(idx),2,replace=False); v=np.cross(Ls[idx[i]],Ls[idx[j]])
            if np.linalg.norm(v)<1e-9: continue
            v=v/np.linalg.norm(v)
            inl=consist(v,S[idx],0.03)
            if inl.sum()>best[1].sum(): best=(v,inl)
        return best
    idx=np.arange(len(S)); v1,i1=fit(idx)
    if v1 is None or i1.sum()<12: return None
    idx2=idx[~i1]
    if len(idx2)<12: return None
    v2,i2=fit(idx2)
    if v2 is None or i2.sum()<12: return None
    cx,cy=W/2,H/2
    def pt(v): return (v[0]/v[2],v[1]/v[2]) if abs(v[2])>1e-6 else (v[0]*1e6,v[1]*1e6)
    p1,p2=pt(v1),pt(v2)
    f2=-((p1[0]-cx)*(p2[0]-cx)+(p1[1]-cy)*(p2[1]-cy))
    return dict(n=len(S),n1=int(i1.sum()),n2=int(i2.sum()),p1=p1,p2=p2,f2=float(f2),f=float(np.sqrt(f2)) if f2>0 else None,H=H)
if __name__=='__main__':
    out={}
    for p in sorted(glob.glob('jpg/*.jpg')):
        r=run(cv2.imread(p))
        if r and r['f'] and r['n1']>=25 and r['n2']>=20:
            r['vfov']=float(2*np.degrees(np.arctan(r['H']/2/r['f']))); out[p[4:-4]]=r
    json.dump(out,open('fov.json','w'))
    v=np.array([r['vfov'] for r in out.values()]); print(len(out),len({k[:7] for k in out}),np.percentile(v,[10,25,50,75,90]))
    for k,r in sorted(out.items(),key=lambda kv:-(kv[1]['n1']+kv[1]['n2']))[:30]: print(k,r['n1'],r['n2'],round(r['vfov'],1),[round(x) for x in r['p1']],[round(x) for x in r['p2']])
