"""A10 vignette test v1: keyframe-only decode (ffmpeg -skip_frame nokey), 108x192 gray, temporal MEDIAN image per video (camera/character motion averages out; static screen-space vignette persists).
radial profile r=0 centre..1 corner (normalised ellipse); report ratio corner(r>0.85)/centre(r<0.25) of median image and of per-frame ratios (median+IQR)."""
import subprocess,numpy as np,sys,json
V="/home/piyush/ricks-clips-private/reference-videos/RC30/%d.mp4"
res={}
for n in range(1,31):
    raw=subprocess.run(["ffmpeg","-v","error","-skip_frame","nokey","-i",V%n,"-vf","scale=108:192,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,192,108).astype(float)
    if len(a)<8: res[n]=None; continue
    yy,xx=np.mgrid[:192,:108]; r=np.hypot((xx-53.5)/54,(yy-95.5)/96)/np.sqrt(2)*np.sqrt(2) # 1 at edge midpoint axes; corners ~1.41
    corner=r>1.15; centre=r<0.35
    med=np.median(a,axis=0); pf=[f[corner].mean()/max(f[centre].mean(),1) for f in a]
    # radial slope of temporal mean: luma vs r bins
    mean=a.mean(axis=0); bins=[mean[(r>=lo)&(r<lo+0.2)].mean() for lo in (0,0.2,0.4,0.6,0.8,1.0,1.2)]
    res[n]=dict(frames=len(a),median_img_ratio=float(med[corner].mean()/med[centre].mean()),perframe_ratio_median=float(np.median(pf)),iqr=np.percentile(pf,[25,75]).tolist(),radial=[round(b,1) for b in bins])
    print(n,res[n]["frames"],"median-img corner/centre %.2f perframe %.2f"%(res[n]["median_img_ratio"],res[n]["perframe_ratio_median"]),res[n]["radial"],flush=True)
json.dump(res,open("vig.json","w"),indent=1)
