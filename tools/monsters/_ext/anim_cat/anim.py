import numpy as np, math
from PIL import Image
from collections import deque
C=np.asarray(Image.open('cat.png')).astype(int); H,W,_=C.shape
on=C[...,3]>0
# つながり（8近傍）で 本体と 浮いてる 火の玉を 分ける
lab=np.zeros((H,W),int); n=0; sizes={}
for y in range(H):
  for x in range(W):
    if on[y,x] and not lab[y,x]:
      n+=1; q=deque([(y,x)]); lab[y,x]=n; c=0
      while q:
        cy,cx=q.popleft(); c+=1
        for dy in(-1,0,1):
          for dx in(-1,0,1):
            ny,nx=cy+dy,cx+dx
            if 0<=ny<H and 0<=nx<W and on[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; q.append((ny,nx))
      sizes[n]=c
main=max(sizes,key=sizes.get); body=lab==main
wisps=[k for k in sizes if k!=main]
print('wisps',[(k,sizes[k]) for k in wisps])
eye=body&(C[...,0]>170)&(C[...,1]>100)&(C[...,2]<120)
ys,xs=np.nonzero(eye); print('eye',ys.min(),ys.max(),xs.min(),xs.max())
TAILY=37; TAILX=37
tail=body&(np.arange(H)[:,None]<=TAILY)&(np.arange(W)[None,:]>=TAILX)
OUT=(16,10,28)
def frame(t, blink=False, dx=0, dy=0, squash=0, flash=0, wobble=0):
  F=np.zeros((H+8,W+8,4),int); oX,oY=4,4
  def put(y,x,c):
    if 0<=y<H+8 and 0<=x<W+8: F[y,x]=c
  breathe=1 if math.sin(t)>0.3 else 0
  for y in range(H):
    for x in range(W):
      if not body[y,x]: continue
      c=C[y,x].copy()
      if blink and eye[y,x]: c[:3]=(58,30,96)
      yy,xx=y,x
      if tail[y,x]:
        k=((TAILY-y)/TAILY)**1.3; xx=x+round(3*k*math.sin(t*1+y*.22)); yy=y+round(1*k*math.cos(t*1+y*.3))
      elif y<50: yy=y+breathe
      if wobble: xx+=round(wobble*math.sin(y*.5))
      if y>=50 and squash: pass
      put(yy+oY+dy, xx+oX+dx, c)
  if blink:
    ey=(ys.min()+ys.max())//2+(1 if math.sin(t)>0.3 else 0)
    for x in xs:
      put(ey+oY+dy, x+oX+dx, (*OUT,255))
  for i,k in enumerate(wisps):
    ph=t+i*1.7; fy=round(2*math.sin(ph)); fx=round(math.cos(ph*.7))
    vis=math.sin(ph*1.3)>-0.85
    if not vis: continue
    wy,wx=np.nonzero(lab==k)
    for y,x in zip(wy,wx):
      c=C[y,x].copy()
      if math.sin(ph*1.3)>0.6: c[:3]=np.minimum(255,c[:3]+50)
      put(y+fy+oY+dy, x+fx+oX+dx, c)
  if flash:
    m=F[...,3]>0; F[m,:3]=(F[m,:3]*(1-flash)+255*flash).astype(int)
  return Image.fromarray(F.astype(np.uint8),'RGBA')
def gif(frames, durs, name, z=5, bg=(34,38,58)):
  out=[]
  for f in frames:
    b=Image.new('RGBA',f.size,bg+(255,)); b.alpha_composite(f); out.append(b.convert('RGB').resize((f.width*z,f.height*z),Image.NEAREST))
  out[0].save(name,save_all=True,append_images=out[1:],duration=durs,loop=0)
  return out
N=16
idle=[frame(2*math.pi*i/N, blink=(i in (10,11))) for i in range(N)]
gif(idle,[90]*N,'cat_idle.gif')
# こうげき：ためて → とびかかる → もどる
atk=[frame(0,dx=2,dy=1),frame(.4,dx=3,dy=1),frame(.8,dx=-6,dy=-2),frame(1.2,dx=-9,dy=0),frame(1.6,dx=-5,dy=0),frame(2.0,dx=-2),frame(2.4)]
hit=[frame(3,flash=.85,dx=3),frame(3.3,dx=-2,wobble=1),frame(3.6,flash=.5,dx=2),frame(3.9,dx=-1),frame(4.2)]
seq=idle+atk+idle[:8]+hit+idle
gif(seq,[90]*N+[110,110,60,90,90,90,90]+[90]*8+[60,70,60,70,90]+[90]*N,'cat_all.gif')
# 並べた 静止画（コマ 一覧）
fr=idle[::2]+atk[1:5]+hit[:3]; z=4
S=Image.new('RGB',(len(fr)*(W+8)*z//2+8, (H+8)*z),(34,38,58))
sheet=Image.new('RGB',((W+8)*z*8,(H+8)*z*2),(34,38,58))
for i,f in enumerate(fr[:16]):
  b=Image.new('RGBA',f.size,(34,38,58,255)); b.alpha_composite(f); sheet.paste(b.convert('RGB').resize((f.width*z,f.height*z),Image.NEAREST),((i%8)*(W+8)*z,(i//8)*(H+8)*z))
sheet.save('cat_frames.png')
