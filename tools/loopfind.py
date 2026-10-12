import numpy as np, subprocess, sys, json
SR=44100
def load(fn):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',fn,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2)
def feats(mono,hop):
    n=2048; win=np.hanning(n); F=[]
    edges=np.geomspace(60,11000,33); freqs=np.fft.rfftfreq(n,1/SR)
    idx=[(freqs>=edges[i])&(freqs<edges[i+1]) for i in range(32)]
    for i in range(0,len(mono)-n,hop):
        sp=np.abs(np.fft.rfft(mono[i:i+n]*win))
        F.append([np.log1p(sp[m].sum()) for m in idx])
    F=np.array(F); F-=F.mean(1,keepdims=True); F/=np.linalg.norm(F,axis=1,keepdims=True)+1e-9
    return F
import os
res=json.load(open('loops.json')) if os.path.exists('loops.json') else {}
for k in sys.argv[1:]:
    a=load(k+'.src.mp3'); mono=a.mean(1); D=len(a)/SR
    hop=int(SR*.1); F=feats(mono,hop); T=len(F)
    rms=np.array([np.sqrt((mono[i*hop:(i+1)*hop]**2).mean()) for i in range(T)])
    med=np.median(rms); good=np.where(rms>.55*med)[0]; endOK=good[-1]*.1-2.0   # フェードの まえ
    S=F@F.T; W=30  # ±3s
    cands=[]
    for L in range(int(40/.1), int(min(105, endOK)/.1)):
        d=np.diagonal(S,L)
        if len(d)<2*W+1: continue
        c=np.convolve(d,np.ones(2*W+1)/(2*W+1),'valid')   # c[i] -> s=i+W
        for i in range(len(c)):
            s=i+W; e=s+L
            if s*.1<1.5 or s*.1>35 or e*.1>endOK: continue
            sc=c[i]-0.0006*L*.1   # ながすぎない ほうが すこし いい
            cands.append((sc,s,e))
    cands.sort(reverse=True); picked=[]
    for c in cands:
        if all(abs(c[1]-p[1])>15 or abs(c[2]-p[2])>15 for p in picked): picked.append(c)
        if len(picked)>=25: break
    bpm=round(json.load(open('bpm.json'))[k]); bar=4*60/bpm*SR; N=int(.25*SR); top=None
    for sc,s,e in picked:
        s0=int(s*.1*SR); nb=round((e*.1*SR-s0)/bar); e0=int(s0+nb*bar)
        if e0/SR>endOK: continue
        ref=mono[s0:s0+N]; bo=0; bv=-9
        for o in range(-int(.04*SR),int(.04*SR),2):
            seg=mono[e0+o:e0+o+N]; v=float(ref@seg/(np.linalg.norm(ref)*np.linalg.norm(seg)+1e-9))
            if v>bv: bv=v; bo=o
        tot=sc+.5*bv
        if top is None or tot>top[0]: top=(tot,sc,s0,e0+bo,bv,nb)
    _,sc,s0,e1,bv,nb=top
    res[k]=dict(bars=nb,dur=round(D,2),endOK=round(endOK,2),ls=round(s0/SR,4),le=round(e1/SR,4),loop=round((e1-s0)/SR,2),featSim=round(float(sc),3),waveCorr=round(bv,3),s0=s0,e1=e1)
    print(k,res[k],flush=True)
json.dump(res,open('loops.json','w'))
