import cv2,numpy as np
D='/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a08-prop-texture-designer/nat/'
def L(fid): im=cv2.imread(D+fid+'.png'); return cv2.cvtColor(im.astype(np.float32)/255,cv2.COLOR_BGR2Lab)[...,0]
def fwhm(p):
    """full width at half depth of the darkest dip, sub-pixel, relative to local baseline (median of ends)"""
    i=int(np.argmin(p)); base=np.median(np.r_[p[:3],p[-3:]]); half=(base+p[i])/2
    l=i
    while l>0 and p[l]<half: l-=1
    r=i
    while r<len(p)-1 and p[r]<half: r+=1
    return (r-l-1), float(p[i]),float(base)
tests=[('RC30-16-f000599','h',600,(380,470),'yellow machine edge near (outline)'),
('RC30-16-f000599','h',1000,(660,780),'pink box / roller edge'),
('RC30-16-f000599','v',900,(1140,1230),'machine base horizontal line'),
('RC30-09-f000359','v',300,(470,560),'prison railing/wall line far'),
('RC30-18-f000449','h',1000,(1000,1075),'character stick arm near'),
('RC30-05-f000089','h',700,(560,640),'cave wall crack line'),
('RC30-18-f000449','v',700,(1100,1200),'wallet stitch zone')]
for fid,o,c,(a,b),name in tests:
    l=L(fid); p=l[c,a:b] if o=='h' else l[a:b,c]
    print(name,fid,fwhm(p))
