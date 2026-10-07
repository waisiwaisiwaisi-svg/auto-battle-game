# 立体（SDF）で 形を 作って 光を 当て、ドットに 落とす 描画エンジン
# - 体は 丸みの ある パーツ（球・楕円体・先細りの 円柱）を なめらかに つなぐ
# - 光は 左上・手前から。素材ごとに 色相を ずらした 4〜5段の ランプで 陰影を つける
# - 3倍で 描いて 縮める（多数決で きれいな かたまりに）、輪郭は 光の 側だけ 体色の 濃い色（セルアウト）
# - 奥行きの 差が 大きい ところに 内側の 線（重なった 足や 首の さかい）
import colorsys, math
import numpy as np

LIGHT = np.array([-0.55, -0.68, 0.48]); LIGHT = LIGHT / np.linalg.norm(LIGHT)
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijmnopqrstuvxyz0123456789'   # 素材×段 に 割り当てる 文字（k l w . は 使わない）

def _rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
def _hex(r, g, b): return '#%02x%02x%02x' % tuple(max(0, min(255, round(c * 255))) for c in (r, g, b))
def _hue_toward(h, target, deg):
    d = (target - h + .5) % 1 - .5; step = deg / 360
    return (h + max(-abs(step), min(abs(step), d))) % 1

def ramp(base, n=4, shadow_hue=.72, light_hue=.14, shift=14):
    """基本色から 暗→明 の n段。影は 青紫へ、明るい 方は 黄へ 色相を ずらす"""
    h, s, v = colorsys.rgb_to_hsv(*_rgb(base))
    out = []
    for i in range(n):
        t = i / (n - 1) * 2 - 1          # -1（いちばん 暗い）〜 +1（いちばん 明るい）
        if t < 0: hh = _hue_toward(h, shadow_hue, shift * -t); vv = v * (1 + .58 * t); ss = min(1, s * (1 - .22 * t))
        else: hh = _hue_toward(h, light_hue, shift * t * .8); vv = min(1, v * (1 + .32 * t)); ss = s * (1 - .38 * t)
        out.append(_hex(*colorsys.hsv_to_rgb(hh, ss, vv)))
    return out

# ---------- 形（SDF：点 p から 表面までの 距離、内側が 負）----------
def sphere(c, r):
    c = np.array(c, float); return lambda p: np.linalg.norm(p - c, axis=-1) - r
def ellipsoid(c, rad):
    c = np.array(c, float); r = np.array(rad, float)
    def f(p):
        q = (p - c) / r; k0 = np.linalg.norm(q, axis=-1); k1 = np.linalg.norm(q / r, axis=-1)
        return k0 * (k0 - 1) / np.maximum(k1, 1e-6)
    return f
def capsule(a, b, ra, rb=None):
    """a→b の 先細り 円柱（両端 丸い）"""
    a = np.array(a, float); b = np.array(b, float); rb = ra if rb is None else rb
    ba = b - a; L2 = ba @ ba
    def f(p):
        h = np.clip(((p - a) @ ba) / L2, 0, 1)
        return np.linalg.norm(p - a - h[..., None] * ba, axis=-1) - (ra + (rb - ra) * h)
    return f
def cone(a, b, ra):
    return capsule(a, b, ra, 0.4)

def smin(a, b, k):
    if k <= 0: return np.minimum(a, b)
    h = np.clip(.5 + .5 * (b - a) / k, 0, 1); return b + (a - b) * h - k * h * (1 - h)

class Model:
    """parts: (名前, 形, 素材, なじませ組)。同じ 組は なめらかに つながり、ちがう 組の さかいには 線が 入る"""
    def __init__(self, yaw=0.0):
        self.parts, self.mats, self.yaw = [], {}, yaw
    def mat(self, name, base=None, n=4, colors=None, glow=False, tex=0.0, **kw):
        self.mats[name] = dict(colors=colors or ramp(base, n, **kw), glow=glow, tex=tex); return name
    def add(self, name, sdf, mat, group=None, k=1.5):
        self.parts.append(dict(name=name, f=sdf, mat=mat, group=group or name, k=k))

    def render(self, W, H, ss=3, thresholds=(.2, .5, .8, .95)):
        """W×H の 文字グリッドと パレットを 返す（足もとは y=H-1 付近、座標は ピクセル単位）"""
        xs = (np.arange(W * ss) + .5) / ss; ys = (np.arange(H * ss) + .5) / ss
        X, Y = np.meshgrid(xs, ys)
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        def world(p):   # 画面の 点 → 模型の 点（たてじくで 回す）
            x, y, z = p[..., 0], p[..., 1], p[..., 2]
            return np.stack([x * cy + z * sy, y, -x * sy + z * cy], -1) if self.yaw else p
        groups = {}
        for i, pt in enumerate(self.parts): groups.setdefault(pt['group'], []).append(i)
        def field(p):
            q = world(p); per = np.stack([pt['f'](q) for pt in self.parts], 0)
            gd = []
            for g, idx in groups.items():
                d = per[idx[0]]
                for j in idx[1:]: d = smin(d, per[j], self.parts[j]['k'])
                gd.append(d)
            return np.min(np.stack(gd, 0), 0), per
        # 手前から 奥へ 光線を 進める
        Z = np.full(X.shape, 40.0); hit = np.zeros(X.shape, bool)
        for _ in range(90):
            p = np.stack([X, Y, Z], -1); d, _ = field(p)
            hit |= d < .02; Z = np.where(hit, Z, Z - np.maximum(d, .05))
        hit &= Z > -40
        p = np.stack([X, Y, Z], -1); d, per = field(p)
        e = .08; n = np.stack([field(p + np.array(v))[0] - field(p - np.array(v))[0] for v in ([e, 0, 0], [0, e, 0], [0, 0, e])], -1)
        n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-6)
        part = np.argmin(per, 0)
        occ = np.clip(field(p + n * 2.2)[0] / 2.2, 0, 1)            # くぼみ（つなぎ目）は 暗く
        lam = np.clip(((n @ LIGHT) * .9 + .1) * (.55 + .45 * occ), 0, 1)
        # 素材ごとの 段
        names = list(self.mats); mat_of_part = np.array([names.index(pt['mat']) for pt in self.parts])
        grp_of_part = np.array([list(groups).index(pt['group']) for pt in self.parts])
        mid = mat_of_part[part]
        tone = np.zeros(X.shape, int)
        for mi, nm in enumerate(names):
            m = self.mats[nm]; nt = len(m['colors']); sel = mid == mi
            v = lam if not m['glow'] else np.clip(.35 + .65 * n[..., 2], 0, 1)
            if m['tex']:   # 毛・うろこの ゆらぎ（3倍の 格子で 2〜3ドット 単位の 斜めの 筋）
                v = v + m['tex'] * (np.sin((X * .9 + Y * 1.6) * 1.1) * np.sin((X * 1.7 - Y * .5) * .7))
            th = np.linspace(0, 1, nt + 1)[1:-1] if nt != 4 else np.array(thresholds[:3]) + .0
            tone[sel] = np.searchsorted(th, v[sel])
        rim = (n @ np.array([.7, .55, .2])) > .62                      # 右下の ふち
        tone = np.where(rim & (tone == 0), 1, tone)
        spec = (n @ (LIGHT + np.array([0, 0, 1])) / np.linalg.norm(LIGHT + np.array([0, 0, 1]))) > .93
        for mi, nm in enumerate(names):
            nt = len(self.mats[nm]['colors']); sel = (mid == mi) & spec & self.mats[nm].get('shiny', True)
            tone[sel] = nt - 1
        code = np.where(hit, mid * 8 + tone, -1); depth = np.where(hit, Z, -99); grp = np.where(hit, grp_of_part[part], -1)
        # 3倍 → 1倍（覆い 5/9 以上で 塗る、色は 多数決）
        out = np.full((H, W), -1, int); dep = np.full((H, W), -99.0); gout = np.full((H, W), -1, int)
        for y in range(H):
            for x in range(W):
                blk = code[y * ss:(y + 1) * ss, x * ss:(x + 1) * ss].ravel()
                cov = blk[blk >= 0]
                if len(cov) * 9 >= 5 * ss * ss:
                    vals, cnt = np.unique(cov, return_counts=True)
                    c = code[y * ss + ss // 2, x * ss + ss // 2]
                    out[y, x] = c if c >= 0 and cnt[list(vals).index(c)] * 3 >= len(cov) else vals[np.argmax(cnt)]
                    dep[y, x] = depth[y * ss:(y + 1) * ss, x * ss:(x + 1) * ss].max()
                    g = grp[y * ss:(y + 1) * ss, x * ss:(x + 1) * ss].ravel(); g = g[g >= 0]
                    gout[y, x] = np.bincount(g).argmax()
        self._names = names
        return self._to_rows(out, dep, gout)

    def _to_rows(self, out, dep, gout):
        H, W = out.shape; names = self._names
        pal = {'k': '#120e18'}; char = {}
        ai = 0
        for mi, nm in enumerate(names):
            for t, col in enumerate(self.mats[nm]['colors']):
                ch = AL[ai]; ai += 1; char[mi * 8 + t] = ch; pal[ch] = col
        g = [['.'] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                if out[y, x] >= 0: g[y][x] = char[out[y, x]]
        # 内側の 線：奥行きが 大きく 下がる（ちがう 組の）さかいの 奥側を その 素材の いちばん 暗い 色に
        line = [[False] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                if out[y, x] < 0: continue
                for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < H and 0 <= xx < W and out[yy, xx] >= 0 and gout[yy, xx] != gout[y, x] and dep[yy, xx] - dep[y, x] > 2.0:
                        line[y][x] = True
        for y in range(H):
            for x in range(W):
                if line[y][x]: g[y][x] = char[(out[y, x] // 8) * 8]   # 段0
        # 外側の 輪郭：光の 側（上・左が 体）は 体の いちばん 暗い 色、それ以外は 黒
        o = [r[:] for r in g]
        for y in range(H):
            for x in range(W):
                if g[y][x] != '.': continue
                nb = [(y + dy, x + dx) for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)) if 0 <= y + dy < H and 0 <= x + dx < W and out[y + dy, x + dx] >= 0]
                if not nb: continue
                below_right = [(yy, xx) for yy, xx in nb if yy > y or xx > x]   # 体が 下か 右 → この 点は 体の 上か 左（光の 側）
                lit = below_right and all(out[yy, xx] % 8 >= 1 for yy, xx in below_right)
                o[y][x] = char[(out[below_right[0]] // 8) * 8] if lit else 'k'
        return [''.join(r) for r in o], pal

def stamp(rows, art, x0, y0):
    """手打ちの 細部（目・牙・模様）を 上に 置く"""
    g = [list(r) for r in rows]
    for j, r in enumerate(art):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c
    return [''.join(r) for r in g]
