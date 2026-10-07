# ホムラジシ：ベクターで 描いて → VectorCraft で 4倍に 描き出し → ドットに 落とす
import math, subprocess, sys
sys.path.insert(0, '/home/user/auto-battle-game/tools/monsters/_lib')
S = 4  # 4倍で 描く（64ドット → 256）

def ramp_grad(id_, cols, cx=.32, cy=.28, r=.95, stops=(.38, .62, .84)):
    """段が はっきり 切れる 放射グラデ（左上が 明るい）：cols = [明, 中, 暗, いちばん暗い]"""
    s = '<radialGradient id="%s" cx="%s" cy="%s" r="%s" fx="%s" fy="%s">' % (id_, cx, cy, r, cx, cy)
    edges = [0, *stops, 1]
    for i, c in enumerate(cols):
        s += '<stop offset="%s" stop-color="%s"/><stop offset="%s" stop-color="%s"/>' % (edges[i], c, edges[i + 1] - .001 if i + 1 < len(edges) - 1 else 1, c)
    return s + '</radialGradient>'

FUR = ['#f4c77a', '#d8913a', '#a45a26', '#6a2e1e']
FURF = ['#d8913a', '#a45a26', '#6a2e1e', '#4a1e18']   # 奥の 足（暗め）
CREAM = ['#fff0c8', '#f0c88a', '#c08a52', '#8a5a36']
FIRE = ['#fff3a0', '#ffc22a', '#f0641c', '#a0201c']
STEEL = ['#eef2fa', '#aab4c8', '#6c7690', '#3e4458']
OUT = '#140e18'

def path(d, fill, extra=''):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' % (d, fill, OUT, S * 1.0, extra)

def g(content, tx=0, ty=0, rot=0, cx=0, cy=0):
    return '<g transform="translate(%s %s) rotate(%s %s %s)">%s</g>' % (tx * S, ty * S, rot, cx * S, cy * S, content)

def P(*pts):   # 64座標の 点列 → 4倍
    return ' '.join(('%s' % (p * S) if isinstance(p, (int, float)) else p) for p in pts)

def flame(cx, cy, ang, L, w, bend=.25):
    """しずく形の 炎の 舌（ベジェ）：根元 (cx,cy) から 角度 ang に 長さ L"""
    a = math.radians(ang); ux, uy = math.cos(a), -math.sin(a); nx, ny = -uy, ux
    tx, ty = cx + ux * L, cy + uy * L
    b1 = (cx + nx * w + ux * L * .35, cy + ny * w + uy * L * .35)
    b2 = (cx - nx * w + ux * L * .35, cy - ny * w + uy * L * .35)
    c1 = (tx - nx * w * bend * 2 - ux * L * .25, ty - ny * w * bend * 2 - uy * L * .25)
    return 'M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (
        P(cx + nx * w * .6), P(cy + ny * w * .6), P(b1[0]), P(b1[1]), P(c1[0] + nx * w * .5), P(c1[1] + ny * w * .5), P(tx), P(ty),
        P(c1[0] - nx * w * .3), P(c1[1] - ny * w * .3), P(b2[0]), P(b2[1]), P(cx - nx * w * .6), P(cy - ny * w * .6))

def leg(x, y, ang_upper, ang_lower, fill, gaunt=False):
    """関節つきの 足：(x,y) が 付け根。角度は 下向き 0 度、前が +"""
    a1 = math.radians(ang_upper); kx, ky = x + math.sin(a1) * 8, y + math.cos(a1) * 8
    a2 = math.radians(ang_lower); fx, fy = kx + math.sin(a2) * 7, ky + math.cos(a2) * 7
    up = 'M %s %s C %s %s %s %s %s %s L %s %s C %s %s %s %s %s %s Z' % (P(x - 4.2), P(y - 2), P(x - 4.5), P(y + 4), P(kx - 3.6), P(ky - 2), P(kx - 3.2), P(ky + 1),
                                                                       P(kx + 3.2), P(ky + 1), P(kx + 3.6), P(ky - 3), P(x + 4.8), P(y + 2), P(x + 4.2), P(y - 2))
    low = 'M %s %s L %s %s C %s %s %s %s %s %s L %s %s Z' % (P(kx - 3.2), P(ky), P(fx - 2.8), P(fy - 1), P(fx - 3.4), P(fy + 2.6), P(fx + 5.2), P(fy + 3), P(fx + 4.6), P(fy - .4), P(kx + 3.2), P(ky))
    s = path(up, fill) + path(low, fill)
    s += '<path d="M %s %s l %s 0 M %s %s l %s 0" stroke="%s" stroke-width="%s"/>' % (P(fx + 1.2), P(fy + 1.2), P(0) if False else 0, P(fx + 3), P(fy + 1.2), 0, OUT, S * .8)
    if gaunt:
        s += path('M %s %s L %s %s L %s %s L %s %s Z' % (P(kx - 4.2), P(ky + 1), P(kx + 4.2), P(ky + 1), P(fx + 4), P(fy - 1.5), P(fx - 3.8), P(fy - 1.5)), 'url(#steel)')
    return s, (fx, fy)

def lion(pose):
    bx, by = pose.get('bx', 0), pose.get('by', 0); hx, hy = pose.get('hx', 0), pose.get('hy', 0)
    fl = pose.get('flame', 0); jaw = pose.get('jaw', 0); mane = pose.get('mane', 1)
    defs = ramp_grad('fur', FUR) + ramp_grad('furf', FURF) + ramp_grad('cream', CREAM) + ramp_grad('fire', FIRE, .5, .7, .9, (.3, .55, .8)) + ramp_grad('steel', STEEL, .3, .2, .9)
    L = pose.get('legs', {})
    X, Y = 30 + bx, 44 + by
    body = []
    # 奥の 足
    for nm, x, a, b in (('ff', X + 6, 8, -4), ('hf', X - 9, -8, 10)):
        da, db = L.get(nm, (0, 0)); body.append(leg(x, Y + 2, a + da, b + db, 'url(#furf)', nm == 'ff')[0])
    # しっぽ
    tw = pose.get('tail', 0)
    body.append('<path d="M %s %s C %s %s %s %s %s %s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        P(X - 11), P(Y - 3), P(X - 18), P(Y - 4), P(X - 22 + tw), P(Y - 8), P(X - 21 + tw), P(Y - 15), OUT, S * 4.2))
    body.append('<path d="M %s %s C %s %s %s %s %s %s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        P(X - 11), P(Y - 3), P(X - 18), P(Y - 4), P(X - 22 + tw), P(Y - 8), P(X - 21 + tw), P(Y - 15), '#a45a26', S * 2.2))
    for i in range(3):
        body.append(path(flame(X - 21 + tw, Y - 15, 80 + 35 * (i - 1) + 6 * math.sin(fl + i), 6 + (i == 1) * 2, 2.6), 'url(#fire)'))
    # 胴（胸が 高く、腰が 低い）
    body.append(path('M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (
        P(X - 14), P(Y), P(X - 15), P(Y - 7), P(X - 6), P(Y - 9), P(X + 4), P(Y - 9.5),
        P(X + 12), P(Y - 11), P(X + 15), P(Y - 4), P(X + 13), P(Y + 3),
        P(X + 11), P(Y + 8), P(X - 2), P(Y + 7), P(X - 8), P(Y + 7),
        P(X - 13), P(Y + 7), P(X - 14), P(Y + 4), P(X - 14), P(Y)), 'url(#fur)'))
    # 手前の 足
    for nm, x, a, b in (('hn', X - 8, -10, 12), ('fn', X + 8, 6, -2)):
        da, db = L.get(nm, (0, 0)); body.append(leg(x, Y + 3, a + da, b + db, 'url(#fur)', nm == 'fn')[0])
    # たてがみ（炎の 輪）：頭の うしろ
    HX, HY = X + 13 + hx, Y - 15 + hy
    mane_s = []
    for i in range(12):
        ang = 60 + 200 * i / 11 + 4 * math.sin(fl * 1.7 + i)
        Lm = (14 + 4 * (i % 2) + 1.2 * math.sin(fl * 2.3 + i * 2.1)) * mane
        mane_s.append(path(flame(HX - 2, HY + 1, ang, Lm, 6.2), 'url(#fire)'))
    # 頭
    head = path('M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (
        P(HX - 8), P(HY + 2), P(HX - 9), P(HY - 8), P(HX - 1), P(HY - 11), P(HX + 5), P(HY - 9),
        P(HX + 9), P(HY - 8), P(HX + 11), P(HY - 5), P(HX + 12), P(HY - 2),
        P(HX + 12), P(HY + 4), P(HX + 6), P(HY + 9), P(HX), P(HY + 9),
        P(HX - 5), P(HY + 9), P(HX - 8), P(HY + 7), P(HX - 8), P(HY + 2)), 'url(#fur)')
    ear = path('M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (P(HX - 5), P(HY - 8), P(HX - 7), P(HY - 13), P(HX - 3), P(HY - 15), P(HX - 1), P(HY - 13),
                                                                      P(HX + 1), P(HY - 11), P(HX), P(HY - 9), P(HX - 5), P(HY - 8)), 'url(#fur)')
    muzzle = path('M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (
        P(HX + 4), P(HY - 1), P(HX + 9), P(HY - 4), P(HX + 15), P(HY - 3), P(HX + 16), P(HY + 1),
        P(HX + 17), P(HY + 4), P(HX + 13), P(HY + 6), P(HX + 9), P(HY + 6),
        P(HX + 5), P(HY + 6), P(HX + 3), P(HY + 2), P(HX + 4), P(HY - 1)), 'url(#cream)')
    jawp = path('M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (
        P(HX + 3), P(HY + 5 + jaw * .5), P(HX + 6), P(HY + 10 + jaw), P(HX + 12), P(HY + 10 + jaw), P(HX + 14), P(HY + 6 + jaw),
        P(HX + 10), P(HY + 7 + jaw * .5), P(HX + 6), P(HY + 7), P(HX + 3), P(HY + 5 + jaw * .5)), 'url(#cream)')
    mouth = '<path d="M %s %s Q %s %s %s %s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        P(HX + 6), P(HY + 5.5), P(HX + 10), P(HY + 6.5 + jaw * .6), P(HX + 15), P(HY + 4.5), OUT, S * 1)
    if jaw > 1:
        mouth = path('M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (P(HX + 5), P(HY + 5), P(HX + 9), P(HY + 5), P(HX + 13), P(HY + 4), P(HX + 15), P(HY + 4),
                                                                            P(HX + 13), P(HY + 7 + jaw), P(HX + 9), P(HY + 8 + jaw), P(HX + 5), P(HY + 5)), '#8a1c28')
    fang = path('M %s %s l %s %s l %s %s Z M %s %s l %s %s l %s %s Z' % (P(HX + 13), P(HY + 4.5), S * 1.2, S * 2.4, S * 1.2, -S * 2.4,
                                                                          P(HX + 8.5), P(HY + 5.5), S * 1, S * 2, S * 1, -S * 2), '#ffffff')
    nose = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (P(HX + 15.6), P(HY - 1.2), S * 1.6, S * 1.2, OUT)
    # 目（つり目・琥珀・炎の 隈）
    eye_kind = pose.get('eye', 'open')
    ex, ey = HX + 5, HY - 4
    if eye_kind in ('open', 'angry'):
        eye = '<path d="M %s %s Q %s %s %s %s Q %s %s %s %s Z" fill="#ffd23a" stroke="%s" stroke-width="%s"/>' % (
            P(ex - 2.5), P(ey), P(ex + 1), P(ey - 2.4), P(ex + 4.5), P(ey - 1.2), P(ex + 1.5), P(ey + 2), P(ex - 2.5), P(ey), OUT, S * .9)
        eye += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (P(ex + 1.6), P(ey - .3), S * .7, S * 1.3, OUT)
        eye += '<circle cx="%s" cy="%s" r="%s" fill="#fff"/>' % (P(ex + .2), P(ey - .9), S * .5)
        brow = '<path d="M %s %s L %s %s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (P(ex - 3), P(ey - 2.6 - (eye_kind == 'angry')), P(ex + 5), P(ey - 1.2 + (eye_kind == 'angry')), OUT, S * 1.3)
        eye += brow
    elif eye_kind == 'shut':
        eye = '<path d="M %s %s Q %s %s %s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (P(ex - 2.5), P(ey), P(ex + 1), P(ey + 1.5), P(ex + 4.5), P(ey - .5), OUT, S * 1)
    else:  # pain / x
        eye = '<path d="M %s %s l %s %s M %s %s l %s %s" stroke="%s" stroke-width="%s"/>' % (P(ex - 1), P(ey - 2), S * 4, S * 4, P(ex + 3), P(ey - 2), -S * 4, S * 4, OUT, S * 1)
    mark = '<path d="M %s %s q %s %s %s %s" fill="none" stroke="#c0281c" stroke-width="%s" stroke-linecap="round"/>' % (P(ex + 3), P(ey + 2), S * -1, S * 3, S * -4, S * 4, S * .9)
    ruff = ''.join(path(flame(HX + 1, HY + 6, a, 7 * mane, 3.2), 'url(#fire)') for a in (-20, -50, -80, -110))
    headg = ''.join(mane_s) + ear + head + muzzle + jawp + mouth + fang + nose + eye + mark + ruff
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs>%s</defs>%s%s</svg>' % (64 * S, 64 * S, 64 * S, 64 * S, defs, ''.join(body), headg)
    return svg

if __name__ == '__main__':
    open('lion.svg', 'w').write(lion({}))
    subprocess.run([sys.argv[1] if len(sys.argv) > 1 else '/root/tools/vectorcraft-0.3.1-linux-x86_64/bin/vectorcraft-cli', 'convert', 'lion.svg', 'lion_hi.png'], check=True, capture_output=True)
