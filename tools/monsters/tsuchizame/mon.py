# ツチザメ（みず・かくとう × シュモクザメ）手打ち GBA風・デフォルメ（2〜3頭身：頭の 左右が 槌の ように はり出す 大きな 頭、胴は 短く 太く、胸びれの こぶしに さらし）
META = dict(id='tsuchizame', name='ツチザメ', types=['water', 'fighting'], base='シュモクザメ', size='L')
PAL = {
    'k': '#101018', 'l': '#1c2436',
    'P': '#a2bcd2', 'Q': '#5c7a9a', 'R': '#34485e',                    # サメの はだ
    'E': '#eaf0f2', 'T': '#aab6c4',                                    # 腹・さらし（明・暗）
    'V': '#a0e8ff', 'W': '#2e8cd8',                                    # 水
    'Y': '#ffd84a', 'O': '#e0661c',                                    # 目
    'r': '#8a1a3a', 'w': '#ffffff',
}
LIGHT = set('PEVYw')
KEEP_BLACK = set('wEYO')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角 / ('t',ch,r,[(x,y),...]) 太い 線。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
        elif s[0] == 't':
            r, pts = s[2], s[3]
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                n = int(max(abs(bx - ax), abs(by - ay)) * 2) + 1
                for i in range(n + 1):
                    t = i / n; pix.ellipse(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, r, s[1]) if False else _disc(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, s[1])
    return g
def _disc(g, cx, cy, r, ch):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if 0 <= y < len(g) and 0 <= x < len(g[0]) and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: g[y][x] = ch
def shade(g, ramps, lw=2, dw=2):
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, c):
        n = 1
        while 0 <= y + dy * n < H and 0 <= x + dx * n < W and src[y + dy * n][x + dx * n] == c: n += 1
        return n
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c not in ramps: continue
            hi, mid, lo = ramps[c]
            if run(y, x, 1, 0, c) <= dw or run(y, x, 0, 1, c) <= dw: g[y][x] = lo
            elif run(y, x, -1, 0, c) <= lw or run(y, x, 0, -1, c) <= 1: g[y][x] = hi
            else: g[y][x] = mid
    return g
def P(g, ramps, over=(), lw=2, dw=2, ol=True):
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭（輪郭の ぶん 左上へ 1 ずれる）"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '........', '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
SKIN = {'1': 'PQR', '2': 'EET'}
DK = {'P': 'Q', 'Q': 'R', 'R': 'l', 'E': 'T', 'T': 'Q', 'w': 'T'}

# ---- 胴＋頭（ひとつの 形で 描く）：短く 太い 胴 → 太い 首 → 頭の 左右が なめらかに はり出した 槌の 頭 ----
# 頭は 3/4 で 少し こちらを 向く：奥の はり出しは 上・後ろ、手前の はり出しは 下・前。はしに 目
def body():
    g = M(52, 46,
          ('e', '1', 21, 25, 18, 10.5),                                  # 胴
          ('p', '1', [(28, 16), (38, 15), (44, 18), (46, 30), (40, 35), (30, 35)]),   # 首（太く なめらかに）
          ('t', '1', 4.6, [(40, 7), (43.5, 23), (47, 39)]),               # 槌の 頭（左右の はり出し）
          ('e', '1', 40, 7, 4.4, 4.2), ('e', '1', 47.5, 39.5, 5, 5))     # 頭の はし（目の ある ふくらみ）
    # 腹がわは 白（カウンターシェーディング）
    for y in range(44):
        for x in range(52):
            if g[y][x] == '1' and (x < 42 and y > 27 + (x - 20) * .05): g[y][x] = '2'
    return P(g, SKIN, [
        (['...PPPP', '.PP', 'P'], 6, 16),
        (['R', 'R', 'R'], 30, 22), (['R', 'R', 'R'], 33, 22), (['R', 'R', 'R'], 36, 22),     # えらの すじ
        (['PP', 'P'], 37, 4),
    ], lw=2, dw=2)
BODY = body()
# 目（K：魚の 目）：槌の 両はしに まぶたの ない 丸い 目。大きく 平たい 黒瞳＋細い 黄〜だいだいの 輪＋白い 光、上に 骨の ふち（明るい はだ色）
# まばたきは 白い 瞬膜（灰）が おおう、被弾は 瞳が 点に ちぢむ、攻撃は 輪が 白く 光る
EYE = ['.PPPP..', '.kkkkk.', 'kwYYYOk', 'kYkkkOk', 'kYkkkOk', '.kOOOk.', '..kkk..']
EYE_ALT = {'blink': ['.PPPP..', '.kkkkk.', 'kETTTTk', 'kETTTTk', 'kTTTTQk', '.kTTQk.', '..kkk..'],
           'hit': ['.PPPP..', '.kkkkk.', 'kwYYYOk', 'kYYkYOk', 'kYOYOOk', '.kOOOk.', '..kkk..'],
           'atk0|atk1|atk2': ['.PPPP..', '.kkkkk.', 'kwwwYYk', 'kwkkkYk', 'kYkkkOk', '.kYYOk.', '..kkk..'],
           'ko': ['.PPPP..', '.kkkkk.', 'kEkTkTk', 'kTEkTTk', 'kEkTkTk', '.kTTQk.', '..kkk..']}
EYE_FAR = ['.kkk.', 'kwkYk', 'kYkOk', '.kkk.']
EYE_FAR_ALT = {'blink': ['.kkk.', 'kETTk', 'kTTQk', '.kkk.'], 'hit': ['.kkk.', 'kwYYk', 'kYkOk', '.kkk.'],
               'ko': ['.kkk.', 'kkTkk', 'kTkTk', '.kkk.']}
# 口：槌の 頭の 下（首の 前の 下）に 三日月に ひらき、するどい 歯が 並ぶ
MOUTH = ['kkkkkkkk.', '.kwkwkwkk', '..kkkkkk.']
MOUTH_OPEN = ['kkkkkkkk..', 'kwrwrwrwk.', '.krrrrrrrk', '.kwrwrwkk.', '..kkkkkk..']

# ---- 背びれ・しっぽ・胸びれ（こぶしの ように にぎった ひれ、さらしを まく）----
DORSAL = P(M(12, 13, ('p', '1', [(0, 13), (5, 4), (9, 0), (9, 4), (12, 13)])), SKIN, [], lw=1, dw=2)
def tail(up=0):
    return P(M(14, 24, ('p', '1', [(14, 10), (14, 14), (8, 13), (2, 22 - up), (4, 13), (0, 1 + up), (7, 8)])), SKIN, [], lw=1, dw=2)
TAIL = tail(); TAIL2 = tail(1)
def fin(punch=False):
    if punch:
        return pix.outline([
            'PPPQQQQQ......',
            'PQQQQQQQQEEE..',
            'QQQQQQQQETEEE.',
            'QQQQQQQQETEEEE',
            '.QQQQQQRETTTTT',
            '..RRRRRRRRRRR.',
        ])
    return pix.outline([
        'PPQQQQ....',
        'PQQQQQQ...',
        '.EEEEEEE..',
        '..TTTTTTT.',
        '..EEEEEEE.',
        '...TTTTTT.',
        '...QQQQQR.',
        '...QQQQRR.',
        '....QQRRR.',
        '....QRRRR.',
        '.....RRR..',
    ])
FIN = fin(); FIN_P = fin(True); FIN_F = dark(fin(), DK)
WAVE = ['....kk......', '..kkVVkk....', '.kVVWWVVk.kk', 'kVWWkkWWVkVk', 'kWkk..kkWWk.', '.k......kk..']
SPLASH = ['..k...k...', '.kVk.kVk.k', 'kVWkkVWkkV', '.kVWVWVWk.', '..kkkkkk..']
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='finF', g='finF', x=38, y=42, rows=FIN_F),
        dict(n='tail', g='tail', x=1, y=21, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='dorsal', g='body', x=19, y=13, rows=DORSAL),
        dict(n='body', g='body', x=11, y=10, rows=BODY),
        dict(n='eyeF', g='body', x=50, y=14, rows=EYE_FAR, alt=EYE_FAR_ALT),
        dict(n='eye', g='body', x=56, y=44, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='body', x=46, y=38, rows=MOUTH, alt={NB: MOUTH_OPEN}),
        dict(n='fin', g='fin', x=29, y=42, rows=FIN, alt={NB: FIN_P}),
        dict(n='splash', g='fin', x=44, y=41, rows=SPLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'fin': (0, 1)}, 'idle2': {'body': (0, 1)}, 'idle3': {'fin': (0, -1)}, 'blink': {},
    'walk0': {'root': (1, -1)}, 'walk1': {'root': (2, -2), 'tail': (0, 1)}, 'walk2': {'root': (1, -1)}, 'walk3': {'tail': (0, -1)},
    'atk0': {'root': (-2, 0), 'fin': (-2, 0)}, 'atk1': {'root': (4, 0), 'fin': (6, -3)}, 'atk2': {'root': (5, 0), 'fin': (3, -3)},
    'hit': {'root': (-3, 0), 'fin': (-1, -1)}, 'ko': {'_flip': True},
}
EYE_BOX = (50, 14, 13, 37)
PARENT = {'head': 'body', 'tail': 'body', 'fin': 'body', 'finF': 'body', 'body': 'root'}
