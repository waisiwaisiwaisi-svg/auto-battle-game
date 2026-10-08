# ゴースト5番（黒猫）の アニメ 第2版
# ChatGPT 版から 学んだこと：
#   ・体ぜんたいで ポーズを 作る（頭が 下がる・背骨が 曲がる・重心が 移る）
#   ・足は ちゃんとした 猫の 足（太もも→すね→肉球）、地面に ついた 足は 動かさない
#   ・ため → のび → ふりぬき → もどり
# 自分の 強み：
#   ・頭・胴・しっぽ・目・火の玉は 元の ドットを そのまま 使う（デザインが ブレない）
#   ・しっぽは 波で つながった 動き、色は 元の パレットだけ、つめの 軌跡
import numpy as np, math
from PIL import Image
from collections import deque

C = np.asarray(Image.open('cat.png')).astype(int); H, W, _ = C.shape
on = C[..., 3] > 0
lab = np.zeros((H, W), int); n = 0; sizes = {}
for y in range(H):
    for x in range(W):
        if on[y, x] and not lab[y, x]:
            n += 1; q = deque([(y, x)]); lab[y, x] = n; c = 0
            while q:
                cy, cx = q.popleft(); c += 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and on[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; q.append((ny, nx))
            sizes[n] = c
main = max(sizes, key=sizes.get); body = lab == main
wisps = [k for k in sizes if k != main]
Y, X = np.mgrid[0:H, 0:W]
eye = body & (C[..., 0] > 170) & (C[..., 1] > 100) & (C[..., 2] < 120)
eys, exs = np.nonzero(eye)
TAILY = 37
tail = body & (Y <= 34) & (X >= 37)
trunk = body & ~tail & (Y <= 53)          # 頭と 胴（足は 描きなおすので 捨てる）
LINE = np.array((1, 1, 3)); BASE = np.array((78, 30, 129)); LIGHT = np.array((100, 45, 165)); DARK = np.array((52, 18, 92))
FAR, FARD = np.array((50, 18, 88)), np.array((34, 10, 62))
CLAW = np.array((236, 230, 255))
NECK = (30.0, 46.0)
GROUND = 68
# 足の つけね（元の 絵の 座標）と 長さ
LEGS = {  # name: (つけね, 上の長さ, 下の長さ, 上の太さ, 下の太さ, 手前か)
    'ff': ((35, 50), 9.5, 8.5, 2.9, 2.0, False),
    'hf': ((55, 47), 9.5, 9.5, 4.0, 1.9, False),
    'hn': ((49, 48), 9.5, 9.5, 4.6, 2.1, True),
    'fn': ((25, 49), 9.5, 9.0, 3.4, 2.3, True),
}
IDLE_PAWS = {'fn': (19, 67), 'ff': (33, 67), 'hn': (51, 67), 'hf': (59, 66)}
PAD_L, PAD_R, PAD_T, PAD_B = 26, 8, 8, 3
FW, FH = W + PAD_L + PAD_R, H + PAD_T + PAD_B

def headw(x, y):
    if y < 37: return 1.0
    return float(np.clip((34 - x) / 7, 0, 1))

def xf_trunk(x, y, P):
    """頭と 胴：肩（S）と 腰（P）の ずれを 背骨に そって まぜる＋背中の 曲がり＋頭の 回転"""
    u = np.clip((x - 30) / 26, 0, 1)
    sx, sy = P['S']; px, py = P['P']
    tx = (1 - u) * sx + u * px; ty = (1 - u) * sy + u * py + P['arch'] * math.sin(math.pi * u)
    # 頭：首を 中心に まわして 肩と いっしょに 動く
    a = math.radians(P['rot']); hx, hy = P['head']
    rx = NECK[0] + (x - NECK[0]) * math.cos(a) - (y - NECK[1]) * math.sin(a)
    ry = NECK[1] + (x - NECK[0]) * math.sin(a) + (y - NECK[1]) * math.cos(a)
    hX, hY = rx + sx + hx, ry + sy + hy
    w = headw(x, y)
    return w * hX + (1 - w) * (x + tx), w * hY + (1 - w) * (y + ty), w

def xf_tail(x, y, P, t):
    k = max(0., (TAILY - y) / TAILY) ** 1.3; amp = P.get('tail', 1.0)
    px, py = P['P']
    return x + px + amp * 3 * k * math.sin(t + y * .22), y + py + k * math.cos(t + y * .3) * amp

def splat(layer, mask, fn):
    """元の ドットを 3×3 に 細かく して 行き先へ 置く（穴が あかない）"""
    for y, x in zip(*np.nonzero(mask)):
        for oy in (-1 / 3, 0, 1 / 3):
            for ox in (-1 / 3, 0, 1 / 3):
                r = fn(x + ox, y + oy)
                dx, dy = int(round(r[0])) + PAD_L, int(round(r[1])) + PAD_T
                if 0 <= dy < FH and 0 <= dx < FW: layer[dy, dx] = (*C[y, x, :3], 255)

def ik(A, B, l1, l2):
    """2本の 骨で つけね A から 足先 B へ。ひざ（関節）は 後ろ（+x）に まがる"""
    ax, ay = A; bx, by = B; dx, dy = bx - ax, by - ay; d = math.hypot(dx, dy) or 1e-6
    if d > l1 + l2 - .01:   # とどかない ときは 骨を のばす
        s = d / (l1 + l2 - .01); l1, l2 = l1 * s, l2 * s
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d); c = max(-1, min(1, c)); a = math.acos(c)
    base = math.atan2(dy, dx)
    k1 = (ax + l1 * math.cos(base + a), ay + l1 * math.sin(base + a))
    k2 = (ax + l1 * math.cos(base - a), ay + l1 * math.sin(base - a))
    return k1 if k1[0] >= k2[0] else k2

def seg_d(px, py, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy or 1e-6
    u = max(0, min(1, ((px - a[0]) * vx + (py - a[1]) * vy) / L2))
    cx, cy = a[0] + vx * u, a[1] + vy * u
    return math.hypot(px - cx, py - cy), u, (px - cx, py - cy)

def draw_leg(F, name, A, B, raised=False):
    (_, l1, l2, r1, r2, near) = LEGS[name]
    K = ik(A, B, l1, l2)
    base, light, dark = (BASE, LIGHT, DARK) if near else (FAR, BASE * .78, FARD)
    ins = {}
    x0, x1 = int(min(A[0], B[0], K[0]) - 7), int(max(A[0], B[0], K[0]) + 7)
    y0, y1 = int(min(A[1], B[1], K[1]) - 7), int(max(A[1], B[1], K[1]) + 7)
    # 足先の 向き（すねの 向き）
    vx, vy = B[0] - K[0], B[1] - K[1]; vn = math.hypot(vx, vy) or 1; ux, uy = vx / vn, vy / vn
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px, py = x + .5 - .5, y
            d1, u1, n1 = seg_d(px, py, A, K); d2, u2, n2 = seg_d(px, py, K, B)
            rr1 = r1 + (r2 + .4 - r1) * u1; rr2 = r2 + .4 - .4 * u2
            hit = None
            if d1 <= rr1: hit = (n1, d1, rr1)
            if d2 <= rr2 and (hit is None or d2 / rr2 < hit[1] / hit[2]): hit = (n2, d2, rr2)
            if raised:   # 上げた 足：丸い 手
                dp = math.hypot(px - B[0], py - B[1])
                if dp <= 2.9: hit = ((px - B[0], py - B[1]), dp, 2.9)
            else:        # 地面の 足：前に のびた 肉球
                ex, ey = (px - (B[0] - 1.2)) / 3.3, (py - (B[1] - .6)) / 1.9
                if ex * ex + ey * ey <= 1: hit = ((px - B[0] + 1.2, (py - B[1] + .6) * 1.7), 1, 1)
            if hit:
                nx_, ny_ = hit[0]; nn = math.hypot(nx_, ny_) or 1
                lit = (-.7 * nx_ - .7 * ny_) / nn * min(1, hit[1] / max(hit[2], .1) * 1.6)
                ins[(y, x)] = light if lit > .45 else dark if lit < -.35 else base
    # ふちどり
    ring = set()
    for (y, x) in ins:
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (y + dy, x + dx) not in ins: ring.add((y + dy, x + dx))
    put = lambda y, x, c: (0 <= y + PAD_T < FH and 0 <= x + PAD_L < FW) and F.__setitem__((y + PAD_T, x + PAD_L), (*np.asarray(c, int), 255))
    for (y, x) in ring: put(y, x, LINE)
    for (y, x), c in ins.items(): put(y, x, c)
    if not raised:   # 指の すじ
        for k in (0, 1):
            put(int(round(B[1] - 1)), int(round(B[0] - 3 + k * 2)), LINE if near else FARD * .6)
    else:            # つめ 3本
        for k in (-1, 0, 1):
            cx, cy = B[0] + ux * 3.4 - uy * k * 1.7, B[1] + uy * 3.4 + ux * k * 1.7
            for j in (0, 1):
                put(int(round(cy + uy * j)), int(round(cx + ux * j)), CLAW)

def outline_rim(F, mask_layer, keep):
    """胴の 切り口などに 1ドットの ふちを つける"""
    m = mask_layer[..., 3] > 0; k = keep
    rim = m & ~(np.roll(k, 1, 0) & np.roll(k, -1, 0) & np.roll(k, 1, 1) & np.roll(k, -1, 1))
    out = mask_layer.copy(); out[rim, :3] = LINE; return out

def comp(dst, src):
    m = src[..., 3] > 0; dst[m] = src[m]

def frame(P, t=0.0, blink=False, flash=0.0, smear=None, spark=None):
    P = {**dict(S=(0, 0), P=(0, 0), arch=0, rot=0, head=(0, 0), paws=IDLE_PAWS, raise_=None), **P}
    paws = {**IDLE_PAWS, **P['paws']}
    F = np.zeros((FH, FW, 4), int)
    def anchor(name):
        (ax, ay) = LEGS[name][0]; u = np.clip((ax - 30) / 26, 0, 1)
        sx, sy = P['S']; px, py = P['P']
        return (ax + (1 - u) * sx + u * px, ay + (1 - u) * sy + u * py + P['arch'] * math.sin(math.pi * u))
    # 奥の 足
    for nm in ('hf', 'ff'): draw_leg(F, nm, anchor(nm), paws[nm], raised=(P['raise_'] == nm))
    # しっぽ
    L = np.zeros_like(F); splat(L, tail, lambda x, y: xf_tail(x, y, P, t)); comp(F, L)
    # 胴（頭以外）と 頭を 分けて 置く
    Tl = np.zeros_like(F); Hl = np.zeros_like(F)
    tm = trunk & np.array([[headw(x, y) < .5 for x in range(W)] for y in range(H)])
    hm = trunk & ~tm
    splat(Tl, tm, lambda x, y: xf_trunk(x, y, P)[:2]); splat(Hl, hm, lambda x, y: xf_trunk(x, y, P)[:2])
    if blink:
        Bl = np.zeros_like(F)
        splat(Bl, eye & hm, lambda x, y: xf_trunk(x, y, P)[:2]); Hl[Bl[..., 3] > 0, :3] = (58, 30, 96)
    keep = (Tl[..., 3] > 0) | (Hl[..., 3] > 0) | (L[..., 3] > 0)
    Tl = outline_rim(F, Tl, keep)
    comp(F, Tl)
    draw_leg(F, 'hn', anchor('hn'), paws['hn'], raised=(P['raise_'] == 'hn'))
    up = P['raise_'] == 'fn'
    if not up: draw_leg(F, 'fn', anchor('fn'), paws['fn'])
    comp(F, Hl)
    if blink:   # 閉じた 目の 線
        for x in range(exs.min(), exs.max() + 1):
            if eye[:, x].any():
                ys = np.nonzero(eye[:, x])[0]; yy = (eys.min() + eys.max()) / 2
                r = xf_trunk(x, yy, P); F[int(round(r[1])) + PAD_T, int(round(r[0])) + PAD_L] = (*LINE, 255)
    if up: draw_leg(F, 'fn', anchor('fn'), paws['fn'], raised=True)
    # 火の玉
    for i, k in enumerate(wisps):
        ph = t + i * 1.7; oy = round(2 * math.sin(ph)); ox = round(math.cos(ph * .7))
        if math.sin(ph * 1.3) < -0.85: continue
        sx, sy = P['S'] if np.nonzero(lab == k)[1].mean() < 30 else P['P']
        for y, x in zip(*np.nonzero(lab == k)):
            cc = C[y, x].copy()
            if math.sin(ph * 1.3) > 0.6: cc[:3] = np.minimum(255, cc[:3] + 50)
            yy, xx = y + oy + PAD_T + round(sy * .5), x + ox + PAD_L + round(sx * .5)
            if 0 <= yy < FH and 0 <= xx < FW and not F[yy, xx, 3]: F[yy, xx] = cc
    if smear:   # つめの 軌跡（太さが 変わる 三日月）
        pts, wmax = smear
        N = len(pts)
        for i in range(N - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            wv = wmax * math.sin(math.pi * (i + .5) / (N - 1))
            for u in np.linspace(0, 1, 10):
                cx, cy = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                for o in np.arange(-wv, wv + .01, .5):
                    xx = int(round(cx + o)) + PAD_L; yy = int(round(cy)) + PAD_T
                    col = (255, 248, 255) if abs(o) < wv * .35 else (205, 170, 255) if abs(o) < wv * .75 else (140, 80, 235)
                    if 0 <= yy < FH and 0 <= xx < FW: F[yy, xx] = (*col, 255)
    if spark:   # 当たった ところの ひかり
        sx, sy, r = spark
        for a in range(0, 360, 45):
            for d in range(1 if a % 90 else 0, r + (0 if a % 90 else 2)):
                xx = int(round(sx + d * math.cos(math.radians(a)))) + PAD_L; yy = int(round(sy + d * math.sin(math.radians(a)))) + PAD_T
                if 0 <= yy < FH and 0 <= xx < FW: F[yy, xx] = (255, 250, 220, 255) if d < r * .6 else (255, 210, 90, 255)
    if flash:
        m = F[..., 3] > 0; F[m, :3] = (F[m, :3] * (1 - flash) + 255 * flash).astype(int)
    return Image.fromarray(F.clip(0, 255).astype(np.uint8), 'RGBA')

def gif(frames, durs, name, z=5, bg=(34, 38, 58)):
    out = []
    for f in frames:
        g = Image.new('RGBA', f.size, bg + (255,)); g.alpha_composite(f); out.append(g.convert('RGB').resize((f.width * z, f.height * z), Image.NEAREST))
    out[0].save(name, save_all=True, append_images=out[1:], duration=durs, loop=0)

def sheet(frames, name, cols=5, z=4, bg=(34, 38, 58)):
    rows = (len(frames) + cols - 1) // cols; S = Image.new('RGB', (FW * z * cols, FH * z * rows), bg)
    for i, f in enumerate(frames):
        g = Image.new('RGBA', f.size, bg + (255,)); g.alpha_composite(f)
        S.paste(g.convert('RGB').resize((FW * z, FH * z), Image.NEAREST), ((i % cols) * FW * z, (i // cols) * FH * z))
    S.save(name)

# ---- ポーズ（x は 左が 前。y は 下が ＋）----
POSE = {
    'idle':  dict(),
    'ready': dict(S=(2, 3), P=(1, -1), arch=1, rot=-4, head=(1, 1), tail=.5),                       # しゃがむ・おしりが 上がる
    'deep':  dict(S=(3, 5), P=(2, -2), arch=2, rot=-7, head=(1, 2), tail=.3),                       # もっと 低く ためる
    'leap':  dict(S=(-8, -3), P=(-4, -2), arch=-2, rot=6, head=(-1, -1), tail=1.4,
                  paws={'fn': (-2, 50), 'ff': (19, 65), 'hn': (55, 67), 'hf': (61, 66)}, raise_='fn'),   # けりだし・前足 ふりあげ
    'slash': dict(S=(-12, 0), P=(-6, -1), arch=-1, rot=2, head=(-1, 0), tail=1.2,
                  paws={'fn': (-5, 61), 'ff': (15, 67), 'hn': (55, 67), 'hf': (61, 66)}, raise_='fn'),  # ひっかき
    'follow': dict(S=(-11, 3), P=(-5, 1), arch=2, rot=-3, head=(0, 1), tail=1.0,
                   paws={'fn': (-6, 67), 'ff': (13, 67), 'hn': (55, 67), 'hf': (62, 66)}),               # ふりぬいて 着地
    'back1': dict(S=(-6, 1), P=(-3, 0), arch=1, rot=-1, tail=1.0,
                  paws={'fn': (4, 67), 'ff': (22, 67), 'hn': (53, 67), 'hf': (61, 66)}),
    'back2': dict(S=(-2, 0), P=(-1, 0), paws={'fn': (14, 67), 'ff': (29, 67), 'hn': (52, 67), 'hf': (60, 66)}),
    'hit1':  dict(S=(5, 1), P=(3, 0), arch=-1, rot=10, head=(2, -1), tail=1.6,
                  paws={'fn': (22, 67), 'ff': (36, 67)}),
    'hit2':  dict(S=(3, 1), P=(2, 0), rot=5, head=(1, 0), tail=1.2),
}

if __name__ == '__main__':
    N = 16
    idle = []
    for i in range(N):
        t = 2 * math.pi * i / N; b = 1 if math.sin(t) > .3 else 0
        idle.append(frame(dict(S=(0, b), P=(0, b * .5), head=(0, 0)), t=t, blink=i in (10, 11)))
    gif(idle, [90] * N, 'cat2_idle.gif')
    atk = [
        (frame(POSE['ready'], t=0.0), 120),
        (frame(POSE['deep'], t=0.3), 160),
        (frame(POSE['leap'], t=0.6), 70),
        (frame(POSE['slash'], t=0.9, smear=([(-6, 42), (-12, 46), (-15, 53), (-14, 60), (-9, 67)], 3.2), spark=(-14, 56, 6)), 100),
        (frame(POSE['follow'], t=1.2, smear=([(-14, 58), (-11, 64), (-5, 69)], 2.0)), 110),
        (frame(POSE['back1'], t=1.5), 100),
        (frame(POSE['back2'], t=1.8), 100),
    ]
    hit = [(frame(POSE['hit1'], t=3, flash=.85), 60), (frame(POSE['hit1'], t=3.2), 80), (frame(POSE['hit2'], t=3.4, flash=.4), 70), (frame(POSE['hit2'], t=3.6), 90)]
    gif([f for f, _ in atk] + idle[:4], [d for _, d in atk] + [90] * 4, 'cat2_attack.gif')
    seq = idle + atk + [(f, 90) for f in idle[:8]] + hit + [(f, 90) for f in idle]
    seq = [(f, 90) if not isinstance(f, tuple) else f for f in seq]
    gif([f for f, _ in seq], [d for _, d in seq], 'cat2_all.gif')
    sheet([idle[0]] + [f for f, _ in atk] + [hit[0][0], hit[1][0]], 'cat2_frames.png')
