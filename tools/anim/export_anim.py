# out/*.npz（走り4・ため・攻撃）→ ゲーム用 AISpr.ANIM の JSON
import json, glob, os, base64, io, numpy as np
from PIL import Image
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
d = json.load(open('../sizes/mons.json')); d = d if isinstance(d, list) else d.get('mons', d); d = d if isinstance(d, list) else list(d.values())
M = {m['id']: m for m in d}
def cxu(a):   # 上 6わりの 重心（からだの 中心）
    al = a[..., 3] > 0; h = al.shape[0]; yy, xx = np.where(al[:max(1, int(h * .6))]); return xx.mean()
def rle(idx):
    f = idx.ravel(); s = []; i = 0
    while i < len(f):
        j = i
        while j < len(f) and f[j] == f[i] and j - i < 1295: j += 1
        s.append(AL[f[i]] + np.base_repr(j - i, 36).lower().rjust(2, '0')); i = j
    return ''.join(s)
out = {}
for p in sorted(glob.glob('out/*.npz')):
    sid = os.path.basename(p)[:-4]; z = np.load(p); fr = [z[f'arr_{i}'] for i in range(6)]
    o = np.array(Image.open(io.BytesIO(base64.b64decode(M[sid]['img'].split(',')[1]))).convert('RGBA'))
    cb = cxu(o)
    cols = {}; pal = []
    F = []
    for k, a in enumerate(fr):
        yy, xx = np.where(a[..., 3] > 0); a = a[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
        idx = np.zeros(a.shape[:2], int)
        for y, x in zip(*np.where(a[..., 3] > 0)):
            c = '#%02x%02x%02x' % tuple(a[y, x, :3])
            if c not in cols: pal.append(c); cols[c] = len(pal)
            idx[y, x] = cols[c]
        F.append(dict(w=int(a.shape[1]), h=int(a.shape[0]), x=int(round(cb - cxu(a))), d=rle(idx)))
    F[5]['x'] = F[4]['x']   # 攻撃は ため と うしろ はし を そろえる（前へ ふみこむ）
    assert len(pal) < 64, (sid, len(pal))
    out[sid] = dict(pal=pal, f=F)
json.dump(out, open('anim_export.json', 'w'), separators=(',', ':'))
print(len(out), os.path.getsize('anim_export.json') // 1024, 'KB', max(len(v['pal']) for v in out.values()))
