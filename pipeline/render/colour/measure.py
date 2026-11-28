"""A26 colour-patch measurement. Usage: python measure.py file.mp4 [frame]. Decodes with explicit matrix, compares patch centres to source sRGB.
Patch list mirrors colour/index.tsx PATCHES (cols=2, rows=7, 360x640). Centre window = central 40% of each cell."""
import subprocess, sys, json
import numpy as np
W, H, COLS, ROWS = 360, 640, 2, 7
P = [(0,0,0),(255,255,255),(128,128,128),(255,0,0),(0,255,0),(0,0,255),(224,172,138),(141,85,36),(135,206,235),(70,130,180),(32,32,32),(200,200,200),(224,172,138),(224,172,138)]
f = sys.argv[1]; fr = int(sys.argv[2]) if len(sys.argv) > 2 else 3
def dec(vf, pix):
    r = subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'select=eq(n\\,{fr}),{vf}','-frames:v','1','-f','rawvideo','-pix_fmt',pix,'-'], capture_output=True, check=True).stdout
    return r
cw, ch = W//COLS, H//ROWS
def centres(a):
    out = []
    for i in range(len(P)):
        x0, y0 = (i%COLS)*cw, (i//COLS)*ch
        c = a[y0+int(ch*.3):y0+int(ch*.7), x0+int(cw*.3):x0+int(cw*.7)].reshape(-1, a.shape[2]).astype(float)
        out.append(c.mean(0))
    return np.array(out)
res = {}
for name, m in [('bt709','bt709'),('bt601','smpte170m')]:
    a = np.frombuffer(dec(f'scale=in_color_matrix={m}:in_range=tv:out_color_matrix=bt709:out_range=pc,format=rgb24','rgb24'), np.uint8).reshape(H, W, 3)
    c = centres(a); err = np.abs(c - np.array(P))
    res[name] = {'max_abs_err_per_channel': err.max(0).round(2).tolist(), 'per_patch_max': err.max(1).round(2).tolist(), 'centres': c.round(1).tolist()}
y = np.frombuffer(dec('null','yuv420p'), np.uint8)[:W*H].reshape(H, W)  # raw Y' plane, no conversion
yc = centres(y[:, :, None])[:, 0]
res['Y_black_patch0'] = round(float(yc[0]),2); res['Y_white_patch1'] = round(float(yc[1]),2); res['Y_grey128_patch2'] = round(float(yc[2]),2)
print(json.dumps(res, indent=1))
