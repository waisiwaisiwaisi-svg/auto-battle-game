import numpy as np, subprocess, sys, json
SR=22050
def load(fn):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',fn,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
out={}
for k in sys.argv[1:]:
    x=load(k+'.src.mp3'); hop=256; n=1024; win=np.hanning(n)
    M=np.array([np.abs(np.fft.rfft(x[i:i+n]*win)) for i in range(0,len(x)-n,hop)])
    L=np.log1p(M); on=np.maximum(0,np.diff(L,axis=0)).sum(1); on-=on.mean()
    fr=SR/hop; ac=np.correlate(on,on,'full')[len(on)-1:]
    lo,hi=int(fr*60/200),int(fr*60/70); lag=lo+np.argmax(ac[lo:hi]); bpm=60*fr/lag
    # なめらかに：となりの ピークで 補間
    y0,y1,y2=ac[lag-1],ac[lag],ac[lag+1]; d=.5*(y0-y2)/(y0-2*y1+y2); lagf=lag+d; bpm=60*fr/lagf
    out[k]=round(bpm,3); print(k,'bpm',round(bpm,2))
json.dump(out,open('bpm.json','w'))
