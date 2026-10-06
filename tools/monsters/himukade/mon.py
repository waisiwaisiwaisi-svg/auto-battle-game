# ヒムカデ（むし・ほのお × ムカデ）手打ち GBA風・デフォルメ（大きな 頭、短い 体を 前で 持ち上げる）
EYE_BOX = (45, 31, 7, 4)
META = dict(id='himukade', name='ヒムカデ', types=['bug', 'fire'], base='ムカデ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1014',
    'A': '#b8484a', 'B': '#74242c', 'D': '#3e121c',
    'E': '#d09450', 'e': '#7e4a28',
    'Y': '#fff27a', 'O': '#ffa424', 'F': '#e0441a',
    'w': '#fff6e4',
}
LIGHT = set('AEYw')
KEEP_BLACK = set('wYO')
from pix import grid, rows_of

# ---- 体：甲の 節を しっぽ → 前へ 重ねる。節の さかい目から 溶けた 火が のぞく ----
SEGS = [(9, 52, 4.6, 4.4), (15, 51, 5.2, 5), (21, 50, 5.6, 5.4), (27, 48, 5.6, 5.4), (32, 44, 5.4, 5.4), (35, 39, 5, 5)]
def segs(idx, hot=False):
    g = grid(64, 64)
    for n, i in enumerate(idx):
        cx, cy, rx, ry = SEGS[i]
        m = [[((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1 for x in range(64)] for y in range(64)]
        prev = [r[:] for r in g]
        for y in range(64):
            for x in range(64):
                if m[y][x]: continue
                if any(0 <= y + dy < 64 and 0 <= x + dx < 64 and m[y + dy][x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                    # 前の 節に かかる さかい目は 溶けた 火（ところどころ）
                    if prev[y][x] not in '.k' and x < cx and (y + (1 if hot else 0)) % 2 == 0 and y < cy + ry * .5: g[y][x] = 'O' if y < cy else 'F'
                    else: g[y][x] = 'k'
        for y in range(64):
            for x in range(64):
                if not m[y][x]: continue
                nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry
                lt = -nx * .6 - ny * .8
                c = 'B'
                if ny > .42: c = 'e' if nx > .25 or ny > .8 else 'E'
                elif lt > .5: c = 'A'
                elif lt < -.25: c = 'D'
                g[y][x] = c
        # 背の 甲の 光るみぞ（1本）
        x = round(cx - 1); 
        for y in range(round(cy - ry) + 1, round(cy + ry * .3)):
            if g[y][x] in 'ABD': g[y][x] = 'F' if y > cy - 2 else 'O'
    return rows_of(g)
REAR = segs([0, 1, 2, 3]); REAR_H = segs([0, 1, 2, 3], True)
FRONT = segs([4, 5]); FRONT_H = segs([4, 5], True)

# 足：短く 太く、先が 熾火（おきび）。付け根は 体の 下へ もぐる
LEG = ['.kk..', '.kDk.', '..kDk', '..kDk', '..kFk', '..kOk', '.kOk.', '.kYk.', '..k..']
LEG2 = ['..kk.', '.kDk.', 'kDk..', 'kDk..', 'kFk..', 'kOk..', '.kOk.', '.kYk.', '..k..']
LEGF = ['kk...', 'kDk..', '.kDk.', '.kFk.', '..kOk', '..kYk', '...k.']
# 頭：大きな 甲の かぶと。重い まゆの 下に 光る つり目
HEAD = [
    '.....kkkkkkkkk......',
    '...kkAAAAAAAAAkkk...',
    '..kAAAAAAABBBBBAAk..',
    '.kAAABBBBBBBBBBBBAk.',
    'kABBBBBBBBBBBBBBBBAk',
    'kABBBBBBkkkkkkkBBBBk',
    'kABBBBBBBkkkkkkkkkBk',
    'kABBBBBBk.......kBBk',
    'kABBDBBBk.......kBDk',
    'kDBBBDBBBk......kBDk',
    'kDBBBBBBBBkkkkkkkDDk',
    'kDDBBBBBBBBBBBBBDDk.',
    '.kDDDBBBBBBBBBBDDk..',
    '..kkDDDDDDDDDDDkk...',
    '....kkkkkkkkkkk.....',
]
assert all(len(r) == 20 for r in HEAD)
# F 黒い 強膜：白目の かわりに 黒に 近い 赤黒（l）、左上に 熾火の 照り返し（D）。中に 細い たての 瞳が だいだい→黄に 光る。
# 下まぶたは 茶（e）の 線で 黒い 目玉の 形を 見せる
EYE = ['DDlOlll', 'DllYlll', '.llOlll', '.eeeee.']
EYE_ALT = {'blink': ['kkkkkkk', 'BBBBBBB', '.BBBBBB', '.eeeee.'], 'atk0|atk1|atk2': ['DlOYOll', 'DlYwYll', '.lOYOll', '.eeeee.'],
           'hit': ['kkkkkkk', 'DlOllll', '.kkkkkk', '.eeeee.'], 'ko': ['DlOlOll', 'lllOlll', '.lOlOll', '.eeeee.']}
# 毒あご（顎肢）：頭の 下から 前へ 大きく 曲がる 二本の 牙（見せ所）。先は 熾火色
FANG = [
    'kkkkk.......',
    'kEEEEkkk....',
    'keEEEEEEkk..',
    '.kkeeeEEEEk.',
    '...kkkeeEEk.',
    '......keEEk.',
    '......keEk..',
    '.....kOFek..',
    '....kYOk....',
    '....kYk.....',
    '.....k......',
]
FANG_OPEN = [
    'kkkkk.........',
    'kEEEEkkkk.....',
    'keEEEEEEEkk...',
    '.kkeeeeEEEEkk.',
    '...kkkkeeeEEk.',
    '.......kkkeEk.',
    '.........kOYk.',
    '.........kYk..',
    '..........k...',
]
DK = {'A': 'B', 'B': 'D', 'E': 'e', 'e': 'D', 'Y': 'O', 'O': 'F'}
FANG_FAR = [''.join(DK.get(c, c) for c in r) for r in FANG]
FANG_FAR_OPEN = [''.join(DK.get(c, c) for c in r) for r in FANG_OPEN]
# 触角：うしろへ のびて 先が 炎
ANT = [
    '.........kk.',
    '.......kkYOk',
    '......kDkkk.',
    '.....kDk....',
    '....kDk.....',
    '...kDk......',
    '..kDk.......',
    '.kDk........',
    'kDk.........',
]
ANT_FAR = [
    '....kk..',
    '...kYOk.',
    '...kFk..',
    '...kDk..',
    '..kDk...',
    '..kDk...',
    '.kDk....',
    '.kDk....',
    'kDk.....',
    'kk......',
]
ANT2 = [
    '........kk..',
    '......kkYOk.',
    '.....kDkkk..',
    '.....kDk....',
    '....kDk.....',
    '...kDk......',
    '..kDk.......',
    '.kDk........',
    'kDk.........',
]
# 尾の 二本の 尾脚（先が 炎）
TAIL = [
    'kk.....',
    'kYkk...',
    '.kOFkk.',
    '..kkFDk',
    '....kDk',
]
# 攻撃：牙から ふき出す 炎
FIRE = [
    '.......kk.....',
    '....kkkOOkk...',
    '..kkFOOYYOOk..',
    'kkFOYYYwwYYOk.',
    'kOYYwwwwwwYYOk',
    'kkFOYYYwwYYOk.',
    '..kkFOOYYOOk..',
    '....kkkOOkk...',
    '.......kk.....',
]
FIRE2 = [
    '....kkk...',
    '..kkOOOk..',
    'kkFOYYYOk.',
    'kOYYwwYYOk',
    'kkFOYYYOk.',
    '..kkOOOk..',
    '....kkk...',
]
EMBER = [['.O...Y', '......', '..Y...'], ['..Y...', '.O..O.', '......']]

# 攻撃：牙から ふき出す 炎
FIRE = [
    '.......kk.....',
    '....kkkOOkk...',
    '..kkFOOYYOOk..',
    'kkFOYYYwwYYOk.',
    'kOYYwwwwwwYYOk',
    'kkFOYYYwwYYOk.',
    '..kkFOOYYOOk..',
    '....kkkOOkk...',
    '.......kk.....',
]
FIRE2 = [
    '....kkk...',
    '..kkOOOk..',
    'kkFOYYYOk.',
    'kOYYwwYYOk',
    'kkFOYYYOk.',
    '..kkOOOk..',
    '....kkk...',
]
EMBER = [['.O...Y', '......', '..Y...'], ['..Y...', '.O..O.', '......']]

HX, HY = 36, 24
def layers():
    L = [
        dict(n='tail', g='body', x=1, y=47, rows=TAIL),
        dict(n='antf', g='head', x=HX + 4, y=HY - 9, rows=ANT_FAR),
        dict(n='fangfar', g='head', x=HX + 10, y=HY + 10, rows=FANG_FAR, alt={'atk0': FANG_FAR_OPEN}),
    ]
    for i, x in enumerate((12, 18, 24)):        # 奥の 足
        L.append(dict(n=f'bl{i}', g='legB' if i % 2 else 'legA', x=x, y=52, rows=LEG2 if i % 2 else LEG))
    L += [
        dict(n='body', g='body', x=0, y=0, rows=REAR, alt={'idle2|idle3|walk2|walk3': REAR_H}),
        dict(n='front', g='front', x=0, y=0, rows=FRONT, alt={'idle2|idle3|walk2|walk3': FRONT_H}),
    ]
    for i, x in enumerate((8, 14, 20, 26)):     # 手前の 足
        L.append(dict(n=f'fl{i}', g='legA' if i % 2 else 'legB', x=x, y=52, rows=LEG if i % 2 else LEG2))
    L += [
        dict(n='ff1', g='front', x=31, y=47, rows=LEGF),
        dict(n='ant', g='head', x=HX + 6, y=HY - 8, rows=ANT, alt={'idle1|idle3|walk1|walk3': ANT2}),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD),
        dict(n='eye', g='head', x=HX + 9, y=HY + 7, rows=EYE, alt=EYE_ALT),
        dict(n='fang', g='head', x=HX + 7, y=HY + 11, rows=FANG, alt={'atk0': FANG_OPEN}),
        dict(n='ember', g='body', x=14, y=38, rows=EMBER[0], alt={'idle2|idle3|walk2|walk3': EMBER[1]}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='fire', g='head', x=HX + 19, y=HY + 13, rows=FIRE, only='atk1'),
        dict(n='fire2', g='head', x=HX + 20, y=HY + 15, rows=FIRE2, only='atk2'),
    ]
    return L
FRAMES = {
    'idle0': {}, 'idle1': {'front': (0, -1)}, 'idle2': {'front': (0, -1), 'body': (0, 0)}, 'idle3': {'front': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'front': (0, -1), 'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'front': (0, -1), 'body': (0, -1)},
    'atk0': {'front': (-1, -2), 'head': (-1, -1), 'body': (0, -1)}, 'atk1': {'root': (4, 0), 'front': (2, 1), 'head': (1, 0)}, 'atk2': {'root': (5, 0), 'front': (1, 1), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'front': (-1, -2), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'front', 'front': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
