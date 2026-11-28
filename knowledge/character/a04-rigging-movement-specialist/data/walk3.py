"""3B walk metrics. usage: walk3.py VIDEO F0 F1 X0 Y0 X1 Y1 [thr] [dark_only_sat]
Per frame: ink mask (gray<thr) in ROI, bbox, leg spread (x-std of ink in lower 40% of bbox), top-y of ink, centroid.
Outputs series + dominant period of leg-spread (autocorr) and bob (top-y p2p / bbox height, after linear detrend)."""
import cv2,numpy as np,sys
n,f0,f1=map(int,sys.argv[1:4]);x0,y0,x1,y1=map(int,sys.argv[4:8]);thr=int(sys.argv[8]) if len(sys.argv)>8 else 60
cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4');cap.set(cv2.CAP_PROP_POS_FRAMES,f0)
R=[]
for i in range(f0,f1+1):
    ok,f=cap.read()
    if not ok:break
    c=f[y0:y1,x0:x1];g=cv2.cvtColor(c,cv2.COLOR_BGR2GRAY);hs=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)
    m=((g<thr)&(hs[...,1]<130)).astype(np.uint8);m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    ys,xs=np.nonzero(m)
    if len(ys)<50:R.append((i,np.nan,np.nan,np.nan,np.nan,np.nan,0));continue
    top,bot=np.percentile(ys,1),np.percentile(ys,99);h=bot-top
    low=ys>top+0.6*h
    spread=xs[low].std() if low.sum()>20 else np.nan
    R.append((i,spread,top,bot,xs.mean(),ys.mean(),len(ys)))
A=np.array(R)
def per(s):
    s=s[~np.isnan(s)];s=s-np.polyval(np.polyfit(np.arange(len(s)),s,2),np.arange(len(s)))
    ac=np.correlate(s,s,'full')[len(s)-1:];ac/=ac[0]
    pk=[k for k in range(4,min(40,len(s)//2)) if ac[k]>ac[k-1] and ac[k]>=ac[k+1]]
    return pk[:3],[round(ac[k],2) for k in pk[:3]]
sp=A[:,1];print('frames',f0,f1,'n',len(A))
print('spread',' '.join(f'{int(a)}:{v:.1f}' for a,v in zip(A[:,0],sp)))
print('spread period(acf peaks,height)',per(sp.copy()))
top=A[:,2]-np.nanmean(A[:,2]);h=np.nanmedian(A[:,3]-A[:,2])
d=top-np.polyval(np.polyfit(np.arange(len(top)),np.nan_to_num(top),2),np.arange(len(top)))
print('bbox h px',round(h),'top-y detrended p2p',round(np.nanpercentile(d,95)-np.nanpercentile(d,5),1),'=',round(100*(np.nanpercentile(d,95)-np.nanpercentile(d,5))/h,1),'% h; top period',per(d.copy()))
# peaks of spread
s=sp;pk=[int(A[k,0]) for k in range(1,len(s)-1) if s[k]>s[k-1] and s[k]>=s[k+1] and s[k]>np.nanmedian(s)]
print('spread maxima frames',pk,'intervals',np.diff(pk).tolist())
