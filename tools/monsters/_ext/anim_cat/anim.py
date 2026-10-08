# ゴースト5番（黒猫）の アニメ試作
# 体を パーツ（しっぽ・前足・後ろ足・のこり）に 分けて、行き先の マスから 元の マスを 逆に たどって 描く（ドット抜けが 出ない）
import numpy as np, math
from PIL import Image
from collections import deque
C = np.asarray(Image.open('cat.png')).astype(int); H, W, _ = C.shape
on = C[..., 3] > 0
# つながり（8近傍）で 本体と 浮いてる 火の玉を 分ける
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
eye = body & (C[..., 0] > 170) & (C[..., 1] > 100) & (C[..., 2] < 120)
eys, exs = np.nonzero(eye)
Y, X = np.mgrid[0:H, 0:W]
TAILY, TAILX = 37, 37
tail = body & (Y <= TAILY) & (X >= TAILX)
front = body & (Y >= 53) & (X <= 30)          # 前足
back = body & (Y >= 53) & (X >= 33)           # 後ろ足
rest = body & ~tail & ~front & ~back
FP, BP = (22, 51), (42, 51)                    # 前足・後ろ足の つけね（x, y）
BREATH_Y = 50                                  # これより 上が 呼吸で 上下する
OUT = (16, 10, 28)
PAD_L, PAD_R, PAD_T, PAD_B = 16, 6, 8, 4
FW, FH = W + PAD_L + PAD_R, H + PAD_T + PAD_B

def src(mask, sy, sx):
    if 0 <= sy < H and 0 <= sx < W and mask[sy, sx]: return C[sy, sx]
    return None

def rot(y, x, piv, deg):
    """行き先 (y,x) を つけね まわりに -deg 回して 元の 位置へ"""
    a = math.radians(-deg); px, py = piv; dx, dy = x - px, y - py
    return round(py + dx * math.sin(a) + dy * math.cos(a)), round(px + dx * math.cos(a) - dy * math.sin(a))

def frame(t, blink=False, dx=0, dy=0, b=None, fsh=0, bsh=0, arm=None, flash=0, wobble=0, smear=None):
    """t: 時間（しっぽ・火の玉）  b: 体の 沈み（呼吸）  fsh/bsh: 前足・後ろ足の ななめ（+で 足先が 後ろへ）
       arm: ひっかく 前足の 先の 位置 (x, y)  smear: つめの 軌跡 [(x, y), ...]"""
    if b is None: b = 1 if math.sin(t) > 0.3 else 0
    F = np.zeros((FH, FW, 4), int)
    for fy in range(FH):
        for fx in range(FW):
            y, x = fy - PAD_T - dy, fx - PAD_L - dx
            if wobble: x -= round(wobble * math.sin(y * .5))
            c = None
            # 後ろ足（いちばん 下）
            sx = x - round(bsh * max(0, y - BP[1])); c = src(back, y, sx)   # 足先ほど ずらす（つけねは 動かない）
            # 体の のこり：上の ほうだけ b マス 沈む（元の 行を 1つ 飛ばすので 穴は あかない）
            sy = y - b if y - b < BREATH_Y else (y if y >= BREATH_Y + b else BREATH_Y - 1)
            r = src(rest, sy, x)
            if r is not None:
                r = r.copy()
                if blink and eye[sy, x]: r[:3] = (58, 30, 96)
                c = r
            # しっぽ：根元は 動かず 先ほど 大きく ゆれる
            k = max(0., (TAILY - (y - b)) / TAILY) ** 1.3
            sy = y - b - round(k * math.cos(t + y * .3)); sx = x - round(3 * k * math.sin(t + y * .22))
            r = src(tail, sy, sx)
            if r is None: r = src(tail, y - b, x) if k < .15 else None   # 根元の すきま 埋め
            if r is not None: c = r
            # 前足（いちばん 上）
            sx = x - round(fsh * max(0, y - FP[1])); r = src(front, y, sx)
            if r is not None: c = r
            if c is not None: F[fy, fx] = c
    if blink:   # 目を 閉じた 線
        ey = (eys.min() + eys.max()) // 2 + b
        for x in range(exs.min(), exs.max() + 1):
            if eye[:, x].any(): F[ey + PAD_T + dy, x + PAD_L + dx] = (*OUT, 255)
    for i, k in enumerate(wisps):
        ph = t + i * 1.7; oy = round(2 * math.sin(ph)); ox = round(math.cos(ph * .7))
        if math.sin(ph * 1.3) < -0.85: continue
        wy, wx = np.nonzero(lab == k)
        for y, x in zip(wy, wx):
            cc = C[y, x].copy()
            if math.sin(ph * 1.3) > 0.6: cc[:3] = np.minimum(255, cc[:3] + 50)
            yy, xx = y + oy + PAD_T + dy, x + ox + PAD_L + dx
            if 0 <= yy < FH and 0 <= xx < FW and not F[yy, xx, 3]: F[yy, xx] = cc
    if arm is not None:   # 腕は 頭や 体の 後ろから 出す（顔に かぶらない）
        A = np.zeros_like(F); draw_arm(A, (SHOULDER[0] + PAD_L + dx, SHOULDER[1] + b + PAD_T + dy), (arm[0] + PAD_L + dx, arm[1] + PAD_T + dy))
        m = (F[..., 3] == 0) & (A[..., 3] > 0); F[m] = A[m]
    if smear:   # つめの 軌跡：まんなか 白、ふちは うす紫
        pts = [(px + PAD_L + dx, py + PAD_T + dy) for px, py in smear]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            for u in np.linspace(0, 1, 12):
                xx, yy = round(x0 + (x1 - x0) * u), round(y0 + (y1 - y0) * u)
                for ox, col in ((-2, (150, 90, 240)), (2, (150, 90, 240)), (-1, (200, 165, 255)), (1, (200, 165, 255)), (0, (255, 245, 255))):
                    if 0 <= yy < FH and 0 <= xx + ox < FW: F[yy, xx + ox] = (*col, 255)
    if flash:
        m = F[..., 3] > 0; F[m, :3] = (F[m, :3] * (1 - flash) + 255 * flash).astype(int)
    return Image.fromarray(F.astype(np.uint8), 'RGBA')

SHOULDER = (14, 46)
BASE, LIGHT, DARK, LINE = (78, 30, 129), (100, 45, 165), (52, 18, 92), (1, 1, 3)
def draw_arm(F, sh, paw, r0=2.2, r1=3.4, pr=3.8):
    """肩から 足先まで 太い 線（ふちどり つき）＋丸い 足先＋つめ"""
    (x0, y0), (x1, y1) = sh, paw; vx, vy = x1 - x0, y1 - y0; L2 = vx * vx + vy * vy or 1
    inside = np.zeros(F.shape[:2], bool); shade = np.zeros(F.shape[:2])
    for y in range(F.shape[0]):
        for x in range(F.shape[1]):
            u = max(0, min(1, ((x - x0) * vx + (y - y0) * vy) / L2)); cx, cy = x0 + vx * u, y0 + vy * u
            d = math.hypot(x - cx, y - cy); dp = math.hypot(x - x1, y - y1)
            if d <= r0 + (r1 - r0) * u or dp <= pr:
                inside[y, x] = True; shade[y, x] = (y - cy) * .8 + (x - cx) * .4   # 下・右が かげ
    ring = np.zeros_like(inside)
    ring[1:] |= inside[:-1]; ring[:-1] |= inside[1:]; ring[:, 1:] |= inside[:, :-1]; ring[:, :-1] |= inside[:, 1:]
    ring &= ~inside
    for y, x in zip(*np.nonzero(ring)): F[y, x] = (*LINE, 255)
    for y, x in zip(*np.nonzero(inside)):
        F[y, x] = (*(DARK if shade[y, x] > 1.2 else LIGHT if shade[y, x] < -1.5 else BASE), 255)
    # つめ：足先の 進む 向きに 3本
    n = math.hypot(vx, vy) or 1; ux, uy = vx / n, vy / n
    for k in (-1, 0, 1):
        cx, cy = x1 + ux * (pr + 1) - uy * k * 1.6, y1 + uy * (pr + 1) + ux * k * 1.6
        for j in (0, 1):
            xx, yy = round(cx + ux * j), round(cy + uy * j)
            if 0 <= yy < F.shape[0] and 0 <= xx < F.shape[1]: F[yy, xx] = (240, 236, 255, 255)

def rot_fwd(piv, deg, r):
    a = math.radians(deg); px, py = piv
    return round(py + r * math.cos(a)), round(px - r * math.sin(a))

def gif(frames, durs, name, z=5, bg=(34, 38, 58)):
    out = []
    for f in frames:
        g = Image.new('RGBA', f.size, bg + (255,)); g.alpha_composite(f); out.append(g.convert('RGB').resize((f.width * z, f.height * z), Image.NEAREST))
    out[0].save(name, save_all=True, append_images=out[1:], duration=durs, loop=0)

if __name__ == '__main__':
    N = 16
    idle = [frame(2 * math.pi * i / N, blink=(i in (10, 11))) for i in range(N)]
    gif(idle, [90] * N, 'cat_idle.gif')
    # こうげき：しゃがんで ためる → 後ろ足で けって とびだす → 前足を ふりあげて ひっかく → もどる
    atk = [
        frame(0.0, b=1, dx=1, fsh=.25, bsh=-.2),                                 # ため：前足を ひっこめる
        frame(0.3, b=2, dx=3, fsh=.35, bsh=-.3),                                 # 深く ため
        frame(0.6, b=0, dx=-4, dy=-2, fsh=.3, bsh=.7, arm=(-4, 44)),             # 後ろ足で けって 前足 ふりあげ
        frame(0.9, b=0, dx=-8, dy=-3, fsh=.3, bsh=.9, arm=(-8, 36)),             # いちばん 上
        frame(1.2, b=1, dx=-10, dy=-1, fsh=.2, bsh=.6, arm=(-9, 58),
              smear=[(-14, 34), (-17, 42), (-17, 50), (-15, 58), (-11, 64)]),       # ひっかき！
        frame(1.5, b=1, dx=-9, dy=0, fsh=.1, bsh=.3, arm=(-4, 62), smear=[(-15, 56), (-11, 64), (-5, 68)]),   # ふりぬき
        frame(1.8, b=1, dx=-6, bsh=.1, arm=(4, 60)),
        frame(2.1, b=0, dx=-3),
        frame(2.4, b=0, dx=-1),
    ]
    adur = [120, 140, 70, 80, 90, 90, 90, 90, 90]
    hit = [frame(3, flash=.85, dx=3, fsh=.3, bsh=-.2), frame(3.3, dx=-2, wobble=1, fsh=.15), frame(3.6, flash=.5, dx=2, fsh=.1), frame(3.9, dx=-1), frame(4.2)]
    gif(atk + idle[:4], adur + [90] * 4, 'cat_attack.gif')
    gif(idle + atk + idle[:8] + hit + idle, [90] * N + adur + [90] * 8 + [60, 70, 60, 70, 90] + [90] * N, 'cat_all.gif')
    fr = [idle[0], idle[4]] + atk[:7] + hit[:1]; z = 4
    sheet = Image.new('RGB', (FW * z * 5, FH * z * 2), (34, 38, 58))
    for i, f in enumerate(fr):
        g = Image.new('RGBA', f.size, (34, 38, 58, 255)); g.alpha_composite(f); sheet.paste(g.convert('RGB').resize((f.width * z, f.height * z), Image.NEAREST), ((i % 5) * FW * z, (i // 5) * FH * z))
    sheet.save('cat_frames.png')
