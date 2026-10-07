# ホムラジシ（立体 → ドット）：ポーズを 変えて 14コマを 描く
import sys, math, json
sys.path.insert(0, '/home/user/auto-battle-game/tools/monsters/_lib')
from sdf import *

def leg(m, nm, hip, foot, mat, grp, r=(3.6, 3.0, 2.8), knee_fwd=1.0):
    kx = (hip[0] + foot[0]) / 2 + knee_fwd; ky = (hip[1] + foot[1]) / 2; kz = (hip[2] + foot[2]) / 2
    m.add(nm + '1', capsule(hip, (kx, ky, kz), r[0], r[1]), mat, grp, 1.5)
    m.add(nm + '2', capsule((kx, ky, kz), foot, r[1], r[2]), mat, grp, 1.5)
    m.add(nm + 'p', ellipsoid((foot[0] + 1.2, foot[1] + 1.1, foot[2]), (3.6, 2.2, 3)), mat, grp, 1.5)

def lion(P):
    """P: ポーズ。bx,by=胴、hx,hy=頭（胴から）、legs={名前:(足先dx,dy)}、jaw=口の 開き、flame=炎の ゆらぎ、ko=たおれ"""
    m = Model(0)
    fur = m.mat('fur', '#d08a34', 4); cream = m.mat('cream', '#e8c48a', 3)
    fire = m.mat('fire', colors=['#8c1c20', '#e0401c', '#ff9a1c', '#ffe066'])
    steel = m.mat('steel', '#9aa4b8', 3)
    bx, by = P.get('bx', 0), P.get('by', 0); hx, hy = P.get('hx', 0), P.get('hy', 0)
    X, Y = 30 + bx, 43 + by
    m.add('torso', ellipsoid((X, Y, 0), (11, 7.5, 7.5)), fur, 'body', 3)
    m.add('chest', sphere((X + 7, Y - 1 + P.get('chest', 0), 0), 7.5), fur, 'body', 3)
    m.add('hip', sphere((X - 8, Y, 0), 7), fur, 'body', 3)
    L = P.get('legs', {}); ground = 57.5
    for nm, hip, fx, z, grp in (('fn', (X + 7, Y + 3), 39, 5.5, 'legFN'), ('ff', (X + 4, Y + 3), 35, -5.5, 'legFF'),
                                ('hn', (X - 8, Y + 3), 21, 5.5, 'legHN'), ('hf', (X - 10, Y + 3), 19, -5.5, 'legHF')):
        dx, dy = L.get(nm, (0, 0))
        foot = (fx + dx + (bx if P.get('ko') else 0), min(ground, ground + dy), z)
        leg(m, nm, (hip[0], hip[1], z * .8), foot, fur, grp, knee_fwd=-1.2 if nm[0] == 'h' else 1.0)
        if nm[0] == 'f':
            kx = (hip[0] + foot[0]) / 2 + 1; ky = (hip[1] + foot[1]) / 2
            m.add('g' + nm, capsule((kx, ky + 1, z), (foot[0] - .3, foot[1] - 2.5, z), 3.9, 3.7), steel, 'g' + nm, 0)
    # しっぽ
    tw = P.get('tail', 0)
    m.add('t1', capsule((X - 14, Y - 2, 0), (X - 21, Y - 6 + tw, -1), 1.8, 1.4), fur, 'tail', 1)
    m.add('t2', capsule((X - 21, Y - 6 + tw, -1), (X - 23 + tw, Y - 13, 0), 1.4, 1.2), fur, 'tail', 1)
    m.add('tt', sphere((X - 23 + tw, Y - 14.5, 0), 3 + .4 * P.get('flame', 0)), fire, 'tail', 1)
    # たてがみ（炎）：ゆらぎで 長さが 変わる
    HX, HY = X + 13 + hx, Y - 14 + hy
    fl = P.get('flame', 0)
    for i in (range(13) if not P.get('vec') else []):
        a = math.radians(50 + 215 * i / 12)
        Lm = (16 + 3.5 * (i % 2)) * P.get('mane', 1) + 1.5 * math.sin(fl * 2.1 + i * 1.7)
        tip = (HX - 3 + math.cos(a) * Lm, HY - math.sin(a) * Lm, -8)
        m.add('mane%d' % i, cone((HX - 3, HY, -5), tip, 7), fire, 'mane', 2)
    for i, (dx, dy, Lr) in enumerate(((.9, .55, 9), (.55, .9, 10), (.15, 1, 9), (-.3, .95, 8)) if not P.get('vec') else []):
        Lr *= P.get('mane', 1)
        m.add('ruff%d' % i, cone((HX + 1, HY + 5, 1), (HX + 1 + dx * Lr, HY + 5 + dy * Lr, 2.5), 4.5), fire, 'mane', 2)
    # 頭
    jaw = P.get('jaw', 0)
    m.add('head', sphere((HX, HY, 2), 10), fur, 'head', 2.5)
    m.add('muzzle', ellipsoid((HX + 8.5, HY + 3.5 - jaw * .3, 3), (5.5, 4.5, 5)), cream, 'head', 2.5)
    m.add('jaw', ellipsoid((HX + 6 + jaw * .4, HY + 8.5 + jaw, 2.5), (5.5, 2.8, 4.5)), cream, 'jaw' if jaw else 'head', 2)
    m.add('brow', ellipsoid((HX + 4, HY - 3.5, 4), (5.5, 2.5, 5)), fur, 'head', 2)
    m.add('ear', sphere((HX - 3, HY - 9.5, 3), 3), fur, 'head', 1.5)
    return m, (HX, HY)

EYES = {
    'open':  ['rr.....', '.kkkkk.', 'kekkwek', '.keeek.', '..kkk..'],
    'angry': ['rrr....', '.rkkkk.', '..kkwek', '.keeek.', '..kkk..'],
    'shut':  ['rr.....', '.......', '.kkkkk.', '..kkk..', '.......'],
    'pain':  ['rr.....', '.k...k.', '..k.k..', '.k...k.', '.......'],
    'x':     ['.......', '.k...k.', '..k.k..', '.k...k.', '.......'],
}
def frame(P, eye='open', fx=None):
    m, (HX, HY) = lion(P)
    rows, pal = m.render(64, 64)
    pal.update({'w': '#ffffff', 'e': '#ffd23a', 'r': '#c0281c', 'n': '#3a1a12', 'f': '#ffe066', 'o': '#ff8a1c', 'd': '#c0281c'})
    ex, ey = int(round(HX + 1)), int(round(HY - 4))
    rows = stamp(rows, EYES[eye], ex, ey)
    rows = stamp(rows, ['kk', 'kn'], int(HX + 13), int(HY + 1))
    if P.get('jaw', 0) > 1:
        rows = stamp(rows, ['kkkkkkk', 'wd.d.w.', 'kdddddk'], int(HX + 6), int(HY + 7))
    else:
        rows = stamp(rows, ['kkkkkkk.', '.w...w..'], int(HX + 6), int(HY + 7))
    if fx: rows = stamp(rows, fx[0], fx[1], fx[2])
    return rows, pal

FIRE = ['...ff...', '..fffo..', '.ffoood.', 'fffooddk', '.foodd..', '..oodk..']
POSES = {
    'idle0': (dict(flame=0), 'open'), 'idle1': (dict(by=1, hy=1, flame=1, tail=1), 'open'),
    'idle2': (dict(by=1, hy=1, flame=2, tail=2), 'open'), 'idle3': (dict(flame=3, tail=1), 'open'),
    'blink': (dict(flame=0), 'shut'),
    'walk0': (dict(by=-1, legs={'fn': (3, -2), 'hf': (3, -2), 'ff': (-2, 0), 'hn': (-2, 0)}, flame=1, tail=1), 'open'),
    'walk1': (dict(by=0, legs={'fn': (1, 0), 'hf': (1, 0), 'ff': (0, -1), 'hn': (0, -1)}, flame=2), 'open'),
    'walk2': (dict(by=-1, legs={'ff': (3, -2), 'hn': (3, -2), 'fn': (-2, 0), 'hf': (-2, 0)}, flame=3, tail=-1), 'open'),
    'walk3': (dict(by=0, legs={'ff': (1, 0), 'hn': (1, 0), 'fn': (0, -1), 'hf': (0, -1)}, flame=0), 'open'),
    'atk0': (dict(bx=-3, by=2, hx=-1, hy=3, legs={'fn': (-3, 0), 'ff': (-3, 0)}, flame=1, mane=1.12, tail=-2), 'angry'),
    'atk1': (dict(bx=4, by=-1, hx=2, hy=-1, jaw=3, legs={'fn': (8, -6), 'ff': (5, -3), 'hn': (-3, 0), 'hf': (-3, 0)}, flame=2, mane=1.2), 'angry'),
    'atk2': (dict(bx=5, by=0, hx=2, jaw=2, legs={'fn': (7, 0), 'ff': (5, 0), 'hn': (-4, 0), 'hf': (-4, 0)}, flame=3, mane=1.1), 'angry'),
    'hit': (dict(bx=-4, by=0, hx=-3, hy=-2, legs={'fn': (-4, 0), 'ff': (-4, 0)}, flame=1, mane=.85, tail=2), 'pain'),
}
if __name__ == '__main__':
    out = {}
    for k, (P, eye) in POSES.items():
        fx = (FIRE, 56, 24) if k == 'atk1' else (FIRE, 58, 25) if k == 'atk2' else None
        rows, pal = frame(P, eye, fx); out[k] = rows; print(k, flush=True)
    # たおれ：立ち絵を 横だおしに（足を 投げだし、体は 低く）
    P = dict(by=6, hy=10, hx=2, legs={'fn': (6, 0), 'ff': (4, 0), 'hn': (-6, 0), 'hf': (-6, 0)}, mane=.7, tail=4)
    rows, pal = frame(P, 'x'); out['ko'] = rows
    json.dump(dict(frames=out, pal=pal), open('lion3d/frames.json', 'w'))
