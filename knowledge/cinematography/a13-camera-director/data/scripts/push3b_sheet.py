"""Start/end native frame pair montages (3 images x 8 moves) for visual check. Private output."""
import json,subprocess,numpy as np,cv2
OUT='/home/piyush/ricks-clips-private/analysis-data/rc30/agents/a13-camera-director/push3b'
V='/home/piyush/ricks-clips-private/reference-videos/RC30/%d.mp4'
rows=json.load(open(OUT+'/push3b_an.json'))
def get(vid,n):
    d=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',V%vid,'-vf',f"select='eq(n\\,{n})',scale=150:267",'-frames:v','1','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
    return np.frombuffer(d,np.uint8).reshape(267,150,3).copy()
cells=[]
for r in rows:
    a=get(int(r['key'][-2:]),r['start']-1); b=get(int(r['key'][-2:]),r['end'])
    for im,n in ((a,r['start']-1),(b,r['end'])): cv2.putText(im,f"{r['key'][-2:]}-f{n}",(2,12),cv2.FONT_HERSHEY_SIMPLEX,0.38,(0,255,255),1)
    cells.append(np.hstack([a,b]))
for i in range(3):
    c=cells[i*8:(i+1)*8]
    while len(c)<8: c.append(np.zeros_like(cells[0]))
    img=np.vstack([np.hstack(c[:4]),np.hstack(c[4:])]); cv2.imwrite(f'{OUT}/pairs_{i}.png',img); print(img.shape)
