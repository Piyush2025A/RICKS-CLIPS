import cv2,numpy as np,json,sys
P=json.load(open('pairs.json'))
def lin(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
tiles=[];rows=[]
for p in P:
    im=cv2.imread(f"f/{p['id']}.png")
    rgb=im[:,:,::-1].astype(float)/255
    out=[]
    for k in ('lit','shade'):
        x,y=p[k]; out.append(np.median(rgb[y-20:y+20,x-20:x+20].reshape(-1,3),axis=0))
    Y=lambda c: lin(c)@np.array([.2126,.7152,.0722])
    lab=lambda c: cv2.cvtColor((c.reshape(1,1,3)*255).astype(np.uint8)[:,:,::-1].copy(),cv2.COLOR_BGR2LAB).reshape(3).astype(float)-[0,128,128]
    la,sh=lab(out[0]),lab(out[1])
    print(p['id'],p['mat'],'lit',np.round(out[0]*255).astype(int),'shade',np.round(out[1]*255).astype(int),'Yratio',round(Y(out[1])/Y(out[0]),3),'db*',round(sh[2]-la[2],1))
    for k,c in (('lit',(0,255,0)),('shade',(0,0,255))):
        x,y=p[k]; cv2.rectangle(im,(x-20,y-20),(x+20,y+20),c,6)
    tiles.append(cv2.resize(im[700:],(432,508)))
while len(tiles)%3: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite('c/pairs.png',np.vstack([np.hstack(tiles[i:i+3]) for i in range(0,len(tiles),3)]))
