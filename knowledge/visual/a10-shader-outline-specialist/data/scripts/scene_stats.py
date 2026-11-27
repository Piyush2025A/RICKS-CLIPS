"""A10 scene shading stats v1 (whole native frame, rows 0..0.75H to skip captions; characters included -> relative comparison only).
flat/smooth/hard = share of px with blurred(s=1.5) |grad| <0.15 / 0.15-3 / >=6 per px ; grain = std of (gray - blur s=1.2) in pixels where 15x15-window blurred grad <0.5 (flat zones); dark_thin = share black-hat(k=9, gray<80 & bh>25) i.e. thin dark lines; clip_hi = share gray>=250; bloom_proxy = luma mean ratio of heavy blur(s=25) of >235 px mask... (mean of blurred bright mask in non-bright px)"""
import cv2,numpy as np,glob,sys,json,os
def stats(p):
    im=cv2.imread(p); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32); H,W=g.shape; g=g[:int(.75*H)]
    gb=cv2.GaussianBlur(g,(0,0),1.5); gx=cv2.Sobel(gb,cv2.CV_32F,1,0,ksize=3)/8; gy=cv2.Sobel(gb,cv2.CV_32F,0,1,ksize=3)/8; mag=np.hypot(gx,gy)
    fl=(mag<.15).mean(); sm=((mag>=.15)&(mag<3)).mean(); hd=(mag>=6).mean()
    res=g-cv2.GaussianBlur(g,(0,0),1.2); loc=cv2.blur(mag,(15,15)); z=loc<0.5
    grain=float(res[z].std()) if z.sum()>5000 else None
    bh=cv2.morphologyEx(g.astype(np.uint8),cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))); dt=((bh>25)&(g<80)).mean()
    hi=(g>=250); glow=cv2.GaussianBlur((g>235).astype(np.float32),(0,0),25); bl=float(glow[g<200].mean())
    lum=g/255.; vig=float(lum[:, :W//6].mean()/max(lum[:, W//3:2*W//3].mean(),1e-3)) # side/centre luma ratio
    return dict(flat=float(fl),smooth=float(sm),hard=float(hd),grain=grain,dark_thin=float(dt),clip_hi=float(hi.mean()),glow_halo=bl,corner_over_centre=float(
        (lum[:H//6,:W//5].mean()+lum[H//2-H//6:H//2,:W//5].mean()+lum[:H//6,-W//5:].mean())/3/max(lum[H//6:H//2-H//6,W//3:2*W//3].mean(),1e-3)),side_over_centre=vig)
if __name__=="__main__":
    out={}
    for p in sorted(sys.argv[1:]):
        k=os.path.basename(p)[:-4]; out[k]=stats(p)
        s=out[k]; print(k,"flat %.2f smooth %.2f hard %.3f grain %s dark_thin %.4f clip %.3f glow %.3f corner/centre %.2f"%(s["flat"],s["smooth"],s["hard"],"%.2f"%s["grain"] if s["grain"] else "-",s["dark_thin"],s["clip_hi"],s["glow_halo"],s["corner_over_centre"]))
    json.dump(out,open("scene_stats_%s.json"%sys.argv[0].split("/")[-1][:-3] if False else "scene_stats.json","w"),indent=1)
