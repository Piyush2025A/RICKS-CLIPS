import cv2,glob,numpy as np
pick={1:2,2:5,3:4,4:2,5:5,6:2,7:2,8:2,9:3,10:5,11:3,12:1,13:1,14:2,15:2,16:3,17:3,18:2,19:6,20:2,21:3,22:2,23:3,24:1,25:6,26:3,27:4,28:3,29:5,30:2}
ids=sorted(pick); sel=[]
for k in range(0,30,6):
    ims=[]
    for i in ids[k:k+6]:
        f=sorted(glob.glob(f'f/{i:02d}_f*.png'))[pick[i]-1]
        im=cv2.imread(f); c=cv2.resize(im[700:1920],(520,620),interpolation=cv2.INTER_AREA)
        cv2.putText(c,f.split('/')[1][:-4],(4,18),0,0.55,(0,255,255),1); ims.append(c); sel.append(f.split('/')[1][:-4])
    cv2.imwrite(f'c/crop{k//6}.png',np.vstack([np.hstack(ims[:3]),np.hstack(ims[3:])]))
print(sel)
