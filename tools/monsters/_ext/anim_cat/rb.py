import numpy as np, sys
from PIL import Image
D='/tmp/claude-0/-home-user-auto-battle-game/27abe3ed-76ac-5b94-8383-de41dcf56044/'
SRC=Image.open(D+'images/13.webp').convert('RGBA').crop((1222,253,1525,532))
A=np.asarray(SRC).astype(int)
def rebuild(s,ox,oy):
  H,W,_=A.shape; nx=int((W-ox)/s); ny=int((H-oy)/s); r=max(1,int(s*.3))
  out=np.zeros((ny,nx,4),np.uint8)
  for j in range(ny):
    for i in range(nx):
      cy,cx=int(oy+(j+.5)*s),int(ox+(i+.5)*s)
      b=A[cy-r:cy+r+1,cx-r:cx+r+1].reshape(-1,4)
      if (b[:,3]>128).mean()<.5: continue
      b=b[b[:,3]>128]; med=np.median(b,0); p=b[np.argmin(((b-med)**2).sum(1))]
      out[j,i]=(*p[:3],255)
  return out
def err(s,ox,oy):
  o=rebuild(s,ox,oy); up=np.repeat(np.repeat(o,int(s),0),int(s),1).astype(int)
  sub=A[int(oy):int(oy)+up.shape[0],int(ox):int(ox)+up.shape[1]]
  m=sub[...,3]>128
  return np.abs(up[...,:3][:sub.shape[0],:sub.shape[1]]-sub[...,:3])[m].mean()
if __name__=='__main__':
  for args in [(4,1.5,2.5),(8,1.6,7.7),(8,5.5,2.5),(8,1.5,6.5)]: print(args, round(err(*args),1))
