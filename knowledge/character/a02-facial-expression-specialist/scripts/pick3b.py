# cluster candidate events, pick up to 3 per video spread out, build every-frame strips (private). usage: pick3b.py n
import sys,json,os,subprocess,numpy as np,cv2
n=int(sys.argv[1]);key=f'RC30-{n:02d}';P=os.path.expanduser('~/ricks-clips-private')
D=f'{P}/analysis-data/rc30/agents/a02-facial-expression-specialist/3b'
j=json.load(open(f'{D}/ev_{n:02d}.json'));ev=j['ev'];dens=j['dens']
# keep events with quiet neighbours (local, not camera move): total density small in +-3 frames
cl=[]
for e in ev:
    f=e[0]
    if cl and f-cl[-1][-1][0]<=10 and abs(e[1]-cl[-1][-1][1])<80 and abs(e[2]-cl[-1][-1][2])<80: cl[-1].append(e)
    else: cl.append([e])
# score: >=2 swaps in cluster (a face acting), small
cl=[c for c in cl if 2<=len(c)<=14 and all(max(dens[max(0,x[0]-4):x[0]+3])<2500 for x in c[:1])]
cl.sort(key=lambda c:-len(c))
pick=[];
for c in cl:
    if all(abs(c[0][0]-p[0][0])>90 for p in pick): pick.append(c)
    if len(pick)==3:break
pick.sort(key=lambda c:c[0][0])
json.dump(pick,open(f'{D}/pick_{n:02d}.json','w'))
print(key,len(ev),len(cl),[(c[0][0],c[-1][0],c[0][1:3]) for c in pick])
if not pick: sys.exit()
# decode needed frames at 540x960 via ffmpeg select
v=f'{P}/reference-videos/RC30/{n}.mp4';rng=[]
for c in pick:
    xs=[e[1] for e in c];ys=[e[2] for e in c];xe=[e[1]+e[3] for e in c];ye=[e[2]+e[4] for e in c]
    cx=(min(xs)+max(xe))/2*4;cy=(min(ys)+max(ye))/2*4  # full-res coords
    s=max(max(xe)-min(xs),max(ye)-min(ys))*4+120;s=int(min(max(s,260),700))
    rng.append((max(0,c[0][0]-3),min(c[-1][0]+4,c[0][0]+27),int(cx),int(cy),s))
sel='+'.join(f'between(n\\,{a}\\,{b})' for a,b,*_ in rng)
frames={}
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',v,'-vf',f"select='{sel}'",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
idx=[f for a,b,*_ in rng for f in range(a,b+1)]
for f in idx:
    b=p.stdout.read(1080*1920*3)
    if len(b)<1080*1920*3:break
    frames[f]=np.frombuffer(b,np.uint8).reshape(1920,1080,3)
rows=[]
for a,b,cx,cy,s in rng:
    x0=int(np.clip(cx-s//2,0,1080-s));y0=int(np.clip(cy-s//2,0,1920-s));tiles=[]
    for f in range(a,b+1):
        if f not in frames:continue
        c=cv2.resize(frames[f][y0:y0+s,x0:x0+s],(110,110),interpolation=cv2.INTER_AREA)
        cv2.putText(c,str(f),(1,11),cv2.FONT_HERSHEY_SIMPLEX,.38,(0,255,255),1);tiles.append(c)
    for r in range(0,len(tiles),14):
        row=tiles[r:r+14]
        while len(row)<14:row.append(np.zeros_like(tiles[0]))
        rows.append(np.hstack(row))
    rows.append(np.full((4,14*110,3),255,np.uint8))
cv2.imwrite(f'{D}/strip_{n:02d}.png',np.vstack(rows))
