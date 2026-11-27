import numpy as np,json,os
def events(a,thr=200):
    d=a[:,2];n=len(d);ev=[]
    for i in range(1,n):
        if d[i]>=thr and d[i]==d[max(0,i-3):i+4].max():
            ev.append(i)
    out=[]
    for i in ev:
        if not out or i-out[-1]>=3: out.append(i)
    return out
if __name__=="__main__":
    res={}
    for n in range(1,31):
        if not os.path.exists(f"capser_{n}.npy"):continue
        a=np.load(f"capser_{n}.npy");e=events(a);res[n]=e
        print(n,len(e),round(len(e)/(len(a)/30),2),e[:14])
    json.dump(res,open("capev.json","w"))
