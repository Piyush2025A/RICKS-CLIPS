import cv2, numpy as np, random, json
from load import load
k,a=load()
random.seed(7)
sel=[]
for key in sorted(set(k)):
    fr=sorted(set(int(x) for x in a[k==key][:,0]))
    fr=[f for f in fr if f%30==0 and f>=60 and f<=max(fr)-30]
    random.shuffle(fr)
    for f in sorted(fr[:4]): sel.append((key,f))
json.dump(sel,open('montage_sel.json','w'))
random.shuffle(sel)
json.dump(sel,open('montage_sel.json','w'))
caps={}
def get(key,f):
    n=int(key[-2:])
    cap=cv2.VideoCapture(f'/home/piyush/ricks-clips-private/reference-videos/RC30/{n}.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,f); ok,im=cap.read(); return im
for mi in range(3):
    tiles=[]
    for key,f in sel[mi*40:(mi+1)*40]:
        im=get(key,f); t=cv2.resize(im,(180,320),interpolation=cv2.INTER_AREA)
        cv2.rectangle(t,(0,0),(180,14),(0,0,0),-1)
        cv2.putText(t,f'{key[-2:]}-f{f}',(3,11),cv2.FONT_HERSHEY_SIMPLEX,0.42,(0,255,255),1)
        tiles.append(t)
    rows=[np.hstack(tiles[i:i+8]) for i in range(0,40,8)]
    cv2.imwrite(f'mont{mi+1}.png',np.vstack(rows))
