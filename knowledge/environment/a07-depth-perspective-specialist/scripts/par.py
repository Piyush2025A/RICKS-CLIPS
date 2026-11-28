import csv,glob,subprocess,numpy as np,cv2,json
W,H=1080,1920
wins=[(r[0],int(r[1]),int(r[2])) for r in csv.reader(open('par_cand.csv'))]
A=list(csv.DictReader(open(glob.glob('/home/piyush/RICKS-CLIPS/knowledge/*/a13*/data/moves_table.csv')[0])))
pans=[x for x in A if x['kind'] in('pan-','pan+') and int(x['dur'])>=8 and abs(float(x['X']))>60]
pans.sort(key=lambda x:-abs(float(x['X'])))
for x in pans[:10]: wins.append((x['key'],int(x['start']),int(x['end'])))
# A13 lateral push+pan with small Z
for x in A:
    if x['kind'] in ('push+pan+','push+pan-','pull+pan+','pull+pan-') and 12<=int(x['dur'])<=40 and abs(float(x['X']))>150 and abs(float(x['Z']))<25: wins.append((x['key'],int(x['start']),int(x['end'])))
seen={};out=[]
wins=[w for w in wins]
byv={}
for w in wins:
    if sum(1 for q in byv.get(w[0],[]))>=2: continue
    byv.setdefault(w[0],[]).append(w)
res=[];sav=[]
for key,ws in sorted(byv.items()):
    k=int(key[5:]); need=set()
    for (_,s,e) in ws:
        for n in (s,s+(e-s)//2,e): need.add(n)
    sel='+'.join(f'eq(n\\,{n})' for n in sorted(need))
    p=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',f'/home/piyush/ricks-clips-private/reference-videos/RC30/{k}.mp4','-vf',f"select='{sel}',scale=540:960",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
    ims=np.frombuffer(p,np.uint8).reshape(-1,960,540,3); fm=dict(zip(sorted(need),ims))
    for (_,s,e) in ws:
        m=s+(e-s)//2
        for a,b in ((s,m),(m,e)):
            if a not in fm or b not in fm: continue
            g1=cv2.cvtColor(fm[a],cv2.COLOR_BGR2GRAY);g2=cv2.cvtColor(fm[b],cv2.COLOR_BGR2GRAY)
            fl=cv2.calcOpticalFlowFarneback(g1,g2,None,0.5,4,25,5,7,1.5,0)
            gx=cv2.Sobel(g1,cv2.CV_32F,1,0);gy=cv2.Sobel(g1,cv2.CV_32F,0,1); tex=np.hypot(gx,gy)>40
            tex[int(.58*960):int(.82*960)]=False
            dx=fl[...,0][tex]; sg=np.sign(np.median(dx)) or 1; d=dx*sg
            top=fl[:int(.35*960),:,0][tex[:int(.35*960)]]*sg; bot=fl[int(.82*960):,:,0][tex[int(.82*960):]]*sg
            p10,p50,p90=np.percentile(d,[10,50,90])
            res.append(dict(key=key,a=a,b=b,n=int(tex.sum()),p10=float(p10),p50=float(p50),p90=float(p90),top=float(np.median(top)) if len(top)>50 else None,bot=float(np.median(bot)) if len(bot)>50 else None,disp_native=float(p50*2)))
            if len(sav)<12 and abs(p50)>1.5:
                hm=np.clip((fl[...,0]*sg+2*max(abs(p50),1))/(4*max(abs(p50),1)),0,1); hm=cv2.applyColorMap((hm*255).astype(np.uint8),cv2.COLORMAP_JET)
                t=np.hstack([fm[a],hm]); t=cv2.resize(t,(400,356)); cv2.putText(t,f"{key[5:]} {a}-{b} p50 {p50:.1f} p10 {p10:.1f} p90 {p90:.1f}",(2,12),cv2.FONT_HERSHEY_SIMPLEX,0.38,(255,255,255),1); sav.append((t,f"{key}-f{a:06d}",f"{key}-f{b:06d}"))
json.dump(res,open('parallax.json','w'),indent=0)
for r in res: print(r['key'],r['a'],r['b'],r['n'],'p10 %.2f p50 %.2f p90 %.2f top %s bot %s'%(r['p10'],r['p50'],r['p90'],None if r['top'] is None else round(r['top'],2),None if r['bot'] is None else round(r['bot'],2)))
while len(sav)%3: sav.append((np.zeros_like(sav[0][0]),'',''))
g=np.vstack([np.hstack([s[0] for s in sav[i:i+3]]) for i in range(0,len(sav),3)]); cv2.imwrite('par_mont.png',g)
open('par_mont.ids','w').write('\n'.join(x for s in sav for x in s[1:] if x))
