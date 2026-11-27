import cv2,numpy as np,sys
O='/home/piyush/ricks-clips-private/analysis-data/rc30/overview/RC30-%02d_overview_1.png'
def tile(k,t):
    im=cv2.imread(O%k); i=t-1; r,c=divmod(i,8); return im[r*320:(r+1)*320,c*180:(c+1)*180]
def mont(keys,ts,out):
    rows=[]
    tiles=[tile(k,t) for k in keys for t in ts]
    while len(tiles)%8: tiles.append(np.zeros_like(tiles[0]))
    for i in range(0,len(tiles),8): rows.append(np.hstack(tiles[i:i+8]))
    cv2.imwrite(out,np.vstack(rows))
A=[1,3,4,6,7,8,10,11,12,14,15,17]; B=[19,20,21,23,24,25,26,28]
mont(A,[10,20],'mont1.png'); mont(B,[10,20,30],'mont2.png')
