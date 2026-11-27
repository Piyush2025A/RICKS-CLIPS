"""A10 shading profile v1: inside head box (landmarks A03), face-fill pixels = gray>150 & saturation low-ish; report luma p5/p50/p95, Lab L std, and horizontal gradient: corr of fill luma with x (lit side) ; terminator test: share of |dL/dx| (blurred s=2) between 0.3 and 3 per px (smooth ramp) vs >6 (hard step)."""
import csv,cv2,numpy as np,json,collections
A="/home/piyush/ricks-clips-private/analysis-data/rc30/agents/"
out=[]
for r in csv.DictReader(open(A+"a03-anatomy-proportion-specialist/landmarks.csv")):
    if r["view"]=="back": continue
    im=cv2.imread(A+"a03-anatomy-proportion-specialist/frames/%s.png"%r["frame_id"]); hl,hr,chin=int(r["head_l"]),int(r["head_r"]),int(r["chin"]); hw=hr-hl
    y0=max(0,chin-int(0.75*hw)); y1=chin-int(0.08*hw); x0=hl+int(0.12*hw); x1=hr-int(0.12*hw)
    roi=im[y0:y1,x0:x1]; g=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY).astype(float); gb=cv2.GaussianBlur(g,(0,0),2)
    lab=cv2.cvtColor(roi,cv2.COLOR_BGR2LAB).astype(float)
    m=(g>150); 
    if m.sum()<2000: continue
    gx=cv2.Sobel(gb,cv2.CV_64F,1,0,ksize=3)/8; gy=cv2.Sobel(gb,cv2.CV_64F,0,1,ksize=3)/8
    mag=np.hypot(gx,gy)[m & (cv2.erode(m.astype(np.uint8),np.ones((9,9)))>0)]
    L=g[m]
    out.append(dict(fid=r["frame_id"],person=r["person"],n=int(m.sum()),p5=float(np.percentile(L,5)),p50=float(np.median(L)),p95=float(np.percentile(L,95)),
       bins16=int((np.bincount((L//4).astype(int),minlength=64)>0.01*len(L)).sum()),smooth=float(((mag>0.15)&(mag<3)).mean()),hard=float((mag>=6).mean()),flat=float((mag<=0.15).mean())))
for o in out: print(o["fid"],o["person"],"p5/50/95 %.0f/%.0f/%.0f"%(o["p5"],o["p50"],o["p95"]),"bins>1%%: %d"%o["bins16"],"flat %.2f smooth %.2f hard %.3f"%(o["flat"],o["smooth"],o["hard"]))
print("median p95-p5",np.median([o["p95"]-o["p5"] for o in out]),"median flat",np.median([o["flat"] for o in out]),"median smooth",np.median([o["smooth"] for o in out]),"median hard",np.median([o["hard"] for o in out]),len(out))
json.dump(out,open("shade.json","w"))
