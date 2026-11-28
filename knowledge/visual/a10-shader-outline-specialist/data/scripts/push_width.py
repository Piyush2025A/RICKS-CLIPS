"""A10 3B: ink width vs head size along push-in moves (A13 moves_table). Face = connected bright (gray>170) component nearest manual seed; head_w = bbox width (closed);
rows at 35-75 % of component height; same FWHM-of-dark-stroke x normal-correction as ink_scan5. Usage: push_width.py <frames_dir>"""
import sys,cv2,numpy as np,json
from scipy.ndimage import map_coordinates
D=sys.argv[1]
seeds={(16,1):(480,920),(16,2):(640,600),(28,1):(330,760),(28,2):(250,500),(17,1):(820,840),(17,2):(620,1000),(17,3):(640,1160),(26,2):(680,1480),(26,1):(250,1250),(30,3):(560,540),(30,4):(540,860)}
out={}
for (v,k),(sx,sy) in seeds.items():
    im=cv2.imread(f"{D}/RC30-{v:02d}_{k}.png"); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(float); H,W=g.shape
    m=(g>170).astype(np.uint8); n,lab,st,_=cv2.connectedComponentsWithStats(m)
    ys,xs=np.nonzero(m); i=np.argmin((xs-sx)**2+(ys-sy)**2); l=lab[ys[i],xs[i]]
    f=cv2.morphologyEx((lab==l).astype(np.uint8),cv2.MORPH_CLOSE,np.ones((31,31),np.uint8)); yy,xx=np.nonzero(f)
    hl,hr,t,b=xx.min(),xx.max(),yy.min(),yy.max(); hw=hr-hl
    gb=cv2.GaussianBlur(g,(0,0),3); GX=cv2.Sobel(gb,cv2.CV_64F,1,0,ksize=3); GY=cv2.Sobel(gb,cv2.CV_64F,0,1,ksize=3)
    ws=[]
    for y in np.linspace(t+0.35*(b-t),t+0.75*(b-t),9).astype(int):
        for x0,sg in ((hl,-1),(hr,1)):
            xs_=np.arange(x0-0.2*hw-12,x0+0.2*hw+12,0.25)
            if xs_[0]<40 or xs_[-1]>W-40: continue
            p=map_coordinates(g,[np.full_like(xs_,y),xs_],order=1); j=int(np.argmin(p)); c=p[j]; xc=xs_[j]
            if abs(xc-x0)>0.12*hw+10: continue
            L=max(8,int(0.1*hw)); 
            if sg==-1: ins=np.median(g[y,int(xc)+L:int(xc)+2*L]); out_=np.median(g[y,int(xc)-2*L:int(xc)-L])
            else: ins=np.median(g[y,int(xc)-2*L:int(xc)-L]); out_=np.median(g[y,int(xc)+L:int(xc)+2*L])
            if ins-c<40 or abs(out_-c)<25: continue
            a,bb=(c+out_)/2,(c+ins)/2
            if sg==1: a,bb=bb,a
            l_=j
            while l_>0 and p[l_]<a: l_-=1
            r_=j
            while r_<len(p)-1 and p[r_]<bb: r_+=1
            gx=GX[y,int(xc)];gy=GY[y,int(xc)];nx=abs(gx)/(np.hypot(gx,gy)+1e-9)
            if nx<0.6: continue
            ws.append((r_-l_)*0.25*nx)
    out[f"{v}.{k}"]=(int(hw),len(ws),float(np.median(ws)) if ws else None)
    print(v,k,"head_w",hw,"n",len(ws),"w",np.median(ws).round(1) if ws else None, "pct", (100*np.median(ws)/hw).round(2) if ws else None)
json.dump(out,open("push_width.json","w"))
