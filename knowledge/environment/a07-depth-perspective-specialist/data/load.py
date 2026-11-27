import csv, glob, numpy as np
def load():
    rows=[]
    for f in sorted(glob.glob('regions_*.csv')):
        r=list(csv.reader(open(f)))[1:]
        rows+= [x for x in r if len(x)==9]
    keys=np.array([r[0] for r in rows]); a=np.array([[float(v) for v in r[1:]] for r in rows])
    return keys,a  # frame,gy0,gx0,lapv,lstd,sat,L,chroma
