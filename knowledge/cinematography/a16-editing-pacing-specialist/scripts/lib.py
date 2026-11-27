import csv,numpy as np
P="/home/piyush/ricks-clips-private/analysis-data/rc30/v0.2.0/"
def col(k,f,c):
    with open(P+f"{k}/{f}") as fh:
        r=csv.DictReader(fh);return np.array([float(x[c]) if x[c] not in("","nan") else np.nan for x in r])
