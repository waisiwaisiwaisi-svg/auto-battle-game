# ユキダル（こおり・ノーマル × 雪だるま）手打ち GBA風：無機物＋かわいい ライン
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, line, stamp
META = dict(id='yukidaru', name='ユキダル', types=['ice', 'normal'], base='雪だるま', size='M')
EYE_BOX = (30, 26, 14, 6)
PAL = {'k': '#141626', 'l': '#46578e',
       'S': '#fbfdff', 'M': '#d2e2f6', 'D': '#94a6d8',          # 雪（影は 青紫へ）
       'A': '#ff9a72', 'B': '#de4c4c', 'C': '#8e2a4e',          # 赤い バケツ
       'T': '#b07a46', 'U': '#64402e',                          # 木の枝
       'O': '#ffa236',                                          # にんじん
       'e': '#56607e', 'w': '#ffffff', 'p': '#ffa6bc',          # 炭の 目の 照り・光・ほっぺ
       'i': '#8ee4ff', 'c': '#1e1e34'}                          # 氷の きらめき・炭
LIGHT = set('SAOwi')
KEEP_BLACK = set('wepc')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch

# ---- 雪玉：左上から 光、右下に 青紫の 三日月影 ----
def ball(rx, ry, cut_top=0):
    W, H = int(rx * 2), int(ry * 2); g = grid(W, H)
    for y in range(H):
        for x in range(W):
            nx, ny = (x + .5 - rx) / rx, (y + .5 - ry) / ry; r2 = nx * nx + ny * ny
            if r2 > 1: continue
            nz = max(0, 1 - r2) ** .5
            I = (-.45 * nx - .55 * ny + .70 * nz)
            g[y][x] = 'S' if I > .86 else 'M' if I > .16 else 'D'
    return g

def body():
    g = ball(15.5, 11.5)
    # 頭の 下の 接地影（頭の 下に かくれる ところ＋少し 右に はみ出す）
    for x in range(8, 27):
        for y in range(0, 4):
            if g[y][x] != '.' and y <= 2 + (x > 20): g[y][x] = 'D'
    put(g, [(4, 6), (5, 5), (6, 4), (7, 4), (3, 7), (3, 8)], 'S')     # 光の 弧
    # 雪の でこぼこ（短い 影の 線）
    put(g, [(20, 13), (21, 13), (22, 12), (12, 18), (13, 18), (25, 16), (25, 17)], 'D')
    return outline(rows_of(g))

def head():
    g = ball(13, 11.5)
    put(g, [(4, 4), (5, 3), (6, 3), (3, 5), (3, 6)], 'S')
    put(g, [(17, 19), (18, 19), (19, 18)], 'M')
    return outline(rows_of(g))

# ---- バケツ（さかさま、少し 左に かたむいた 赤い ブリキ）----
BUCKET = [
    '....kkkkkkkkkkkk.....',
    '...kAAAAABBBBBBCk....',
    '...kAAABBBBBBBBCk....',
    '...kABBBBBBBBBBCk....',
    '..kAABBBBBBBBBBCCk...',
    '..kABBBBBBBBBBBCCk...',
    '..kABBBBBBBBBBBBCk...',
    '.kAABBBBBBBBBBBBCCk..',
    'kkkkkkkkkkkkkkkkkkkk.',
    'kAAAAAAABBBBBBBBBCCk.',
    'kCCCCCCCCCCCCCCCCCCk.',
    '.kkkkkkkkkkkkkkkkkk..',
]
# 取っ手の 付け根は 'U'（こげ茶）で 小さく

# ---- 木の枝の 腕：本線は 2ドット（上 T・下 U）、小枝は 1ドット ----
def branch(main, twigs, W, H):
    g = grid(W, H)
    for (x0, y0, x1, y1) in main:
        line(g, x0, y0 + 1, x1, y1 + 1, 'U')
    for (x0, y0, x1, y1) in main:
        line(g, x0, y0, x1, y1, 'T')
    for (x0, y0, x1, y1) in twigs:
        line(g, x0, y0, x1, y1, 'T')
    return outline(rows_of(g))
ARM_F = branch([(0, 9, 5, 6), (5, 6, 11, 2)], [(8, 4, 8, 0), (11, 2, 13, 2)], 15, 11)          # 手前（右）
ARM_B = branch([(13, 9, 8, 6), (8, 6, 2, 3)], [(5, 4, 4, 1), (2, 3, 0, 3)], 15, 11)              # 奥（左）
ARM_UP = branch([(0, 12, 4, 7), (4, 7, 9, 2)], [(7, 4, 10, 5), (9, 2, 9, 0)], 12, 14)             # ため：うしろへ ふりかぶる
ARM_THROW = branch([(0, 4, 6, 5), (6, 5, 13, 6)], [(10, 5, 12, 2), (13, 6, 15, 7)], 17, 9)       # 投げ：前へ のばす
ARM_FLAIL = branch([(0, 6, 5, 7), (5, 7, 10, 11)], [(8, 9, 11, 8), (10, 11, 10, 13)], 13, 15)    # 被弾：だらり

# ---- にんじんの 鼻（右向き、3/4 なので 右へ つき出る）----
NOSE = ['kkkk.........', 'kOOOkkkk.....', 'kOAAOOOOkkk..', 'kOOBOOOBOOOkk', 'kBBBBBBBBkkk.', '.kkkkkkkk....']
NOSE_KO = ['kkkk.', 'kOOk.', 'kOOBk', '.kOBk', '.kOBk', '..kBk', '..kk.']   # たおれ：下へ たれる

# ---- 顔：炭の 小石の 目（照り＋光）、小石の 口、ほっぺ ----
def face(kind):
    g = grid(18, 14)
    def s(rows, x, y): stamp(g, rows, x, y)
    EN = ['.ccc.', 'cwwcc', 'cwcce', 'cccee', '.ccc.']     # 手前の 目：炭の 小石（左上に 光、右下に 雪の 照り返し）
    EF = ['.cc.', 'cwcc', 'ccce', '.cc.']                   # 奥の 目（小さめ）
    SMILE = ['c....c', '.cccc.']
    cheeks = lambda: (put(g, [(0, 6), (1, 6)], 'p'), None)
    if kind == 'open':
        s(EF, 1, 1); s(EN, 9, 0); s(SMILE, 3, 11); cheeks()
    elif kind == 'blink':
        s(['....', 'c..c', '.cc.'], 1, 1); s(['.....', 'c...c', '.ccc.'], 9, 0); s(SMILE, 3, 11); cheeks()
    elif kind in ('fight', 'shout'):
        s(['cc..', '.ccc', 'cwcc', 'ccce', '.cc.'], 1, 0); s(['...cc', 'cccc.', 'cwwcc', 'cwcce', '.ccc.'], 9, -1)
        s(['.cccc.', 'c....c'] if kind == 'fight' else ['.cccc.', 'cCCCCc', 'cCAACc', '.cccc.'], 3, 10 if kind == 'shout' else 11)
    elif kind == 'pain':
        s(['c...', '.cc.', 'c...'], 1, 1); s(['...c', '.cc.', '...c'], 10, 0); s(['.cc.cc', 'c..c..'], 3, 11)
    elif kind == 'ko':
        s(['c.c', '.c.', 'c.c'], 1, 1); s(['c.c', '.c.', 'c.c'], 10, 0); s(['.cccc'], 3, 11)
    return rows_of(g)
# 怒りの まゆ（小枝）は ため・攻撃で だけ
BROWS = ['UT.......TU', '.UT.....TU.']

# ---- 雪の 結晶（ふわふわ 浮く、はなれているのは 意図的）----
FLAKE = ['.i.', 'iSi', '.i.']
FLAKE2 = ['..i..', '..i..', 'iiSii', '..i..', '..i..']
ICEBTN = ['.kk.', 'kSik', 'kiik', '.kk.']   # 氷の ボタン
SNOWBALL = outline(rows_of(ball(4, 4)))
TRAIL = ['....iiii', 'iiiiii..', '........', '..iiiiii', '.....ii.', 'iiii....']
def splat():
    g = grid(13, 13)
    for y in range(13):
        for x in range(13):
            dx, dy = x - 6, y - 6
            if dx * dx + dy * dy <= 7 or (abs(dx) == abs(dy) and abs(dx) <= 4) or (min(abs(dx), abs(dy)) == 0 and max(abs(dx), abs(dy)) <= 5):
                g[y][x] = 'S' if dx + dy < 0 else 'M' if dx + dy < 4 else 'D'
    put(g, [(6, 0), (0, 6), (12, 6), (6, 12), (2, 2), (10, 2), (2, 10), (10, 10)], 'i')
    return outline(rows_of(g))
BURST = splat()

def ko_pose():
    W, H = 64, 30; g = grid(W, H)
    b = ball(16, 9.5)                                        # とけかけて つぶれた 胴
    put(b, [(4, 4), (5, 3), (6, 3), (7, 2)], 'S')
    stamp(g, outline(rows_of(b)), 18, 10)
    stamp(g, head(), 2, 6)                                   # 頭は 左へ ころげ落ちる
    stamp(g, face('ko'), 6, 11)
    stamp(g, NOSE_KO, 19, 17)
    stamp(g, branch([(0, 4, 6, 4), (6, 4, 12, 3)], [(9, 3, 11, 0)], 14, 7), 46, 22)
    rows = rows_of(g)
    return [r.rstrip('.') for r in rows]
BUCKET_KO = ['..kkkkkkk.', '.kAAAAABk.', 'kAABBBBBCk', 'kABBBBBBCk', 'kABBBBBBCk', 'kABBBBBBCk', 'kAABBBBCCk', 'kkABBBBCkk', '.kkkkkkkk.']

NA = 'ko'
def layers():
    return [
        dict(n='armB', g='armA', x=6, y=39, rows=ARM_B, not_=NA),
        dict(n='body', g='body', x=15, y=36, rows=body(), not_=NA),
        dict(n='btn1', g='body', x=36, y=43, rows=ICEBTN, not_=NA),
        dict(n='btn2', g='body', x=37, y=50, rows=ICEBTN, not_=NA),
        dict(n='armF', g='armB', x=44, y=38, rows=ARM_F, alt={'atk0': ARM_UP, 'atk1|atk2': ARM_THROW, 'hit': ARM_FLAIL}, not_=NA),
        dict(n='head', g='head', x=19, y=16, rows=head(), not_=NA),
        dict(n='face', g='head', x=28, y=24, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        dict(n='brows', g='head', x=29, y=21, rows=BROWS, only='atk0|atk1|atk2'),
        dict(n='nose', g='head', x=35, y=29, rows=NOSE, not_=NA),
        dict(n='hat', g='hat', x=20, y=8, rows=BUCKET, not_=NA),
        dict(n='flake1', g='fx', x=9, y=14, rows=FLAKE, alt={'idle1|idle3|walk1|walk3': FLAKE2}, not_='atk1|atk2|hit|ko'),
        dict(n='flake2', g='fx2', x=51, y=19, rows=FLAKE2, alt={'idle1|idle3|walk1|walk3': FLAKE}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='ballUp', g='armB', x=50, y=33, rows=SNOWBALL, only='atk0'),
        dict(n='ball1', g='root', x=61, y=35, rows=SNOWBALL, only='atk1'),
        dict(n='trail', g='root', x=53, y=36, rows=TRAIL, only='atk1'),
        dict(n='burst', g='root', x=62, y=31, rows=BURST, only='atk2'),
        dict(n='ko', g='root', x=0, y=32, rows=ko_pose(), only='ko'),
        dict(n='koHat', g='root', x=51, y=50, rows=BUCKET_KO, only='ko'),
        dict(n='koFlake', g='root', x=30, y=34, rows=FLAKE2, only='ko'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'fx': (0, -1), 'fx2': (0, 1)}, 'idle2': {'head': (0, 1), 'hat': (0, -1), 'armB': (0, -1)},
    'idle3': {'armA': (0, 1), 'fx': (0, 1), 'fx2': (0, -1)}, 'blink': {},
    'walk0': {'head': (0, 1), 'armB': (0, 1)}, 'walk1': {'root': (1, -2), 'head': (1, -1), 'hat': (0, -1), 'armA': (0, -1)},
    'walk2': {'head': (0, 1), 'armA': (0, 1)}, 'walk3': {'root': (-1, -2), 'head': (-1, -1), 'hat': (0, -1), 'armB': (0, -1)},
    'atk0': {'root': (-2, 1), 'head': (-1, 0), 'armB': (0, -6), 'hat': (-1, 0)},
    'atk1': {'root': (2, 0), 'head': (1, 0), 'armB': (0, 0)}, 'atk2': {'root': (1, 0), 'armB': (0, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, 0), 'hat': (-1, -2), 'armB': (0, 2)}, 'ko': {},
}
PARENT = {'body': 'root', 'armA': 'body', 'armB': 'body', 'head': 'body', 'hat': 'head', 'fx': 'root', 'fx2': 'root'}
