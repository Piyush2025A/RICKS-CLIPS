"""Composite tiles from every-frame sheets. usage: comp3b.py out.png cols label KEY:f0:f1:stride [KEY:f0:f1:stride ...]
Tiles cropped from RC30 sheets (private); output stays under private agent folder."""
import sys,cv2,numpy as np
PV="/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0/"
HDR=1292-6*213
def tile(k,i):
    s=i//48;f0=s*48;f1=f0+47
    im=cv2.imread(PV+f"{k}/sheets/{k}_sheet_f{f0:06d}-f{f1:06d}.png")
    if im is None: return np.zeros((213,120,3),np.uint8)
    p=i-f0;r,c=p//8,p%8
    y=im.shape[0]-(6-r)*213 if False else HDR+r*213
    return im[y:y+213,c*120:(c+1)*120].copy()
def build(out,cols,specs,lab=True):
    tiles=[]
    for sp in specs:
        k,a,b,st=sp.split(":");a,b,st=int(a),int(b),int(st)
        for i in range(a,b+1,st):
            t=tile(k,i)
            if lab:cv2.putText(t,f"{k[-2:]}:{i}",(2,205),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255),1,cv2.LINE_AA)
            tiles.append(t)
    rows=[]
    for j in range(0,len(tiles),cols):
        r=tiles[j:j+cols]
        while len(r)<cols:r.append(np.zeros((213,120,3),np.uint8))
        rows.append(np.hstack(r))
    cv2.imwrite(out,np.vstack(rows))
if __name__=="__main__":
    build(sys.argv[1],int(sys.argv[2]),sys.argv[4:])
