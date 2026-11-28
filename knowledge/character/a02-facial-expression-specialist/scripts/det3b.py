# local-change (face-swap candidate) detector. usage: det3b.py <n>  -> private 3b/ev_nn.json
import sys,subprocess,numpy as np,cv2,json,csv,os
n=int(sys.argv[1]);key=f'RC30-{n:02d}';W,H=270,480
P=os.path.expanduser('~/ricks-clips-private')
v=f'{P}/reference-videos/RC30/{n}.mp4'
segs=list(csv.DictReader(open(f'{P}/analysis-data/rc30/captions/{key}/caption_segments.csv')))
cm=np.zeros((len(segs),4))
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',v,'-vf',f'scale={W}:{H}:flags=area,format=gray','-f','rawvideo','-'],stdout=subprocess.PIPE)
prev=None;i=0;ev=[];dens=[]
capmask=np.zeros((H,W),np.uint8)
caps=[(int(s['f_start']),int(s['f_end']),int(s['x0'])//4-6,int(s['x1'])//4+6,int(s['y0'])//4-6,int(s['y1'])//4+6) for s in segs]
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H:break
    g=np.frombuffer(b,np.uint8).reshape(H,W)
    if prev is not None:
        d=(np.abs(g.astype(int)-prev.astype(int))>40).astype(np.uint8)
        for a,bb,x0,x1,y0,y1 in caps:
            if a-1<=i<=bb+1: d[max(0,y0):y1,max(0,x0):x1]=0
        tot=d.sum();dens.append(int(tot))
        if 25<tot<2500:
            dd=cv2.dilate(d,np.ones((9,9),np.uint8))
            nl,lab,st,_=cv2.connectedComponentsWithStats(dd)
            if nl>1:
                k=1+np.argmax(st[1:,4]);x,y,w,h,a=st[k]
                if w<130 and h<130 and a>150: ev.append((i,int(x),int(y),int(w),int(h),int(tot)))
        else: pass
    prev=g;i+=1
json.dump({'n':i,'ev':ev,'dens':dens},open(f'{P}/analysis-data/rc30/agents/a02-facial-expression-specialist/3b/ev_{n:02d}.json','w'))
print(key,i,len(ev))
