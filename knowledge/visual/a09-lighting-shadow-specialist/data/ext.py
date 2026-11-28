import subprocess,sys,os
R='/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0'
V='/home/piyush/ricks-clips-private/reference-videos/RC30'
for i in range(1,31):
    n=sum(1 for _ in open(f'{R}/RC30-{i:02d}/frames.csv'))-1
    fr=[int(n*f) for f in (0.06,0.22,0.38,0.54,0.70,0.88)]
    sel='+'.join(f'eq(n\\,{k})' for k in fr)
    out=f'f/{i:02d}_%d.png'
    subprocess.run(['ffmpeg','-nostdin','-v','error','-i',f'{V}/{i}.mp4','-vf',f"select='{sel}'",'-fps_mode','passthrough',f'f/tmp{i:02d}_%d.png'])
    for j,k in enumerate(fr,1): os.rename(f'f/tmp{i:02d}_{j}.png',f'f/{i:02d}_f{k:06d}.png')
    print(i,n,fr,flush=True)
