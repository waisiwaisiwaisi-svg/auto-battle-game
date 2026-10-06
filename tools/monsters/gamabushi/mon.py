# ガマブシ（みず・かくとう × ガマガエル）手打ち GBA風
from pix import outline
META = dict(id='gamabushi', name='ガマブシ', types=['water', 'fighting'], base='ガマガエル', size='M')
PAL = {
    'k': '#101018', 'l': '#1c3040',
    'A': '#86c8b0', 'B': '#3f8a84', 'C': '#22505a',      # 皮（青みどり）
    'E': '#f2e2b0', 'F': '#c4a070',                      # はら
    'R': '#e85a44', 'S': '#a82e36', 'T': '#5a1a2e',      # 朱ぬりの よろい
    'w': '#ffffff', 'W': '#8ee4ff', 'V': '#3a8ee0',      # 水の 刀
    'Y': '#ffd23a', 'O': '#c8781e', 'n': '#f07a98',
}
LIGHT = set('AERwWY')
KEEP_BLACK = set('wY')
DK = {'A': 'B', 'B': 'C', 'C': 'C', 'E': 'F', 'R': 'S', 'S': 'T'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]

BODY0 = [
    ".....AAAAAAAAAAAA.......",
    "...AABBBBBBBBBBBBBA.....",
    "..ABBBBBBBBBBBBBBBBBA...",
    ".ABBBBBBBBBBBBBEEEEBBC..",
    ".ABBABBBBBBBBEEEEEEEEBC.",
    "ABBBCBBBBBBEEEEEEEEEEEC.",
    "ABBBBBBBBBEEEEEEEEEEEEFC",
    "ABBBBBBBBBEEFFFFFFFEEEFC",
    "ABBBBBABBEEEEEEEEEEEEEFC",
    "ABBBBBCBBEEEEEEEEEEEEEFC",
    "ABBBBBBBBEEFFFFFFFFEEFFC",
    "ABBABBBBBEEEEEEEEEEEEFFC",
    "ABBCBBBBBFEEEEEEEEEEEFFC",
    "ABBBBBBBBFEEFFFFFFFEFFCC",
    "BBBBBBBBCFFEEEEEEEEFFFC.",
    "BBBBBBBCCFFFFFFFFFFFFCC.",
    ".BBBBCCCCCFFFFFFFFFCCC..",
    "..CCCCCCCCCCCCCCCCCC....",
]
SKIRT0 = [
    "RRRRRRRRRRRRRRRRRRRRRRRRRS",
    "RSSSSSkRSSSSSkRSSSSSkSSSST",
    "TTTTTTkTTTTTTkTTTTTTkTTTTT",
    "RSSSSSkRSSSSSkRSSSSSkSSSST",
    "TTTTTTkTTTTTTkTTTTTTkTTTTT",
    "RSSSSSkRSSSSSkSSSSSTkSSSTT",
    "STTTTTkSTTTTTkSTTTTTkTTTT.",
]
# デフォルメ：胴を 3行・草ずりを 2行・うでを 2行 みじかく（頭は そのまま）
BODY = [r for i, r in enumerate(BODY0) if i not in (8, 9, 11)]
SKIRT = [r for i, r in enumerate(SKIRT0) if i not in (3, 4)]
LEG = [
    "..AAABBBBC...",
    ".ABBBBBBBBC..",
    "ABBBBABBBBBC.",
    "ABBBBBBBBBBC.",
    ".ABBBBBBBBC..",
    "..ABBBBBBC...",
    "..ABBBBBC....",
    ".AABBBBBBC...",
    "ABBBBBBBBBBC.",
    "ABBCBBBCBBBBw",
    ".CC.CCC.CCCCw",
]
HEAD = [
    ".................AAAAA..........",
    "...............AABBBBBA.........",
    "........AAAAAAABBBBBBBBA........",
    "......AABBBBBBBBBBBBBBBBBAAA....",
    ".....ABBBBBBBBBBBBBBBBBBBBBBAA..",
    "....ABBBBBBBBBBBBBBBBBBBBBBBBBA.",
    "....ABBBAABBBBBBBBBBBBBBBBBBBBBA",
    "...ABBBACCBBBBABBBBBBBBBBBBBBBBB",
    "...ABBBBCBBBBBCBBBBBBBBBBBBBBBBC",
    "...ABBABBBBBBBBBBBBBBBBBBBBBBBCC",
    "...ABBCBBBkkkkkkkkkkkkkkkkkkkkkk",
    "...ABBBBkkCCCCCCCCCCCCCCCCCCCCC.",
    "...ABBBBkBEEEEEEEEEEEEEEEEEEEC..",
    "....ABBBCEEEEEEEEEEEEEEEEEEEFC..",
    ".....ABBCFEEEEEEEEEEEEEEEEFFC...",
    "......BCCCFFFFFFFFFFFFFFFFCC....",
    ".......CCCCCCCCCCCCCCCCCCCC.....",
]
HELM = [
    ".....RRRRRR......",
    "...RRRRSRRRRS....",
    "..RRRRSRRRRRSS...",
    ".RRRRSRRRRRRSSS..",
    ".RRRSRRRRRRRSSSRR",
    "SSSSSSSSSSSSSSTRS",
    "TTTTTTTTTTTTTTTTT",
    "SSSSSST..........",
    "SkkkkT...........",
    "STTTT............",
]
CREST = ['w....w', 'Wk..kW', 'VWkkWV', '.VWWV.', '..YY..']
# 目：金の 虹彩（明 Y・暗 O）＋白い 光＋横長の ひとみ。黒い まぶたが 前へ つり下がる
EYE = ['.kkk.....', 'kYYYkkk..', 'kYwYYYYkk', 'kYOkkkOYk', '.kOOOOOk.', '..kkkkk..']
EYE_ALT = {'blink': ['.kkk.....', 'kBBBkkk..', 'kBBBBBBkk', 'kkkkkkkkk', '.CBBBBBC.', '..CCCCC..'],
           'hit': ['..kk.....', '.kYYkk...', 'kYkwYOkk.', 'kkOOOkkk.', '.kkkkkk..', '.........'],
           'atk0|atk1|atk2': ['.kkk.....', 'kwwYkkk..', 'kYwwYYYkk', 'kYYkkkwYk', '.kOYYYOk.', '..kkkkk..'],
           'ko': ['.........', '.k...k...', '..k.k....', '...k.....', '..k.k....', '.k...k...']}
# 刀は 舌で にぎる。刀の 絵は 40x34 の 板に 手描きの 部品を 置く（原点 x=44, y=6）
def place(parts, W=50, H=34):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]
SWORD = [
    "......kk........",
    "..nn..kWkkkkkk..",
    "kkTTnkYwwwwwwwkk",
    "kTYTYkYWWWWWWVVk",
    "kkTTnkYVVVVVkkk.",
    "..nn..kVkkkkk...",
    "......kk........",
]
DROP1 = ['.k.', 'kWk', 'kVk', '.k.']
DROP2 = ['.k.', 'kwk', 'WVk', 'kk.']
# ため：刀を 上へ 立てる（ななめ 45度、刃の 断面 kwWVk を 1行ずつ ずらして 手で 打つ）
SWORD_UP = [
    "..............kk",
    ".............kwVk",
    "............kwWVk",
    "...........kwWVk.",
    "..........kwWVk..",
    ".........kwWVk...",
    "........kwWVk....",
    ".......kwWVk.....",
    "......kwWVk......",
    "....kkYWVk.......",
    "...kYYYYk........",
    "..nTTkYk.........",
    ".nTYTk.k.........",
    "nTTkn............",
    "nnnn.............",
]
# 決め：舌が のびて 刀を 前へ つきだす
SWORD_THRUST = [
    "...........kk...............",
    "...........kWkkkkkkkkkkkk...",
    "kkkkkkkkkkkYwwwwwwwwwwwwwkk.",
    "nnnnnnnnTTYYWWWWWWWWWWWWWVVk",
    "knnnnnnnTYTYVVVVVVVVVVVVkkk.",
    ".kkkkkkkkkkYkkkkkkkkkkkk....",
    "...........kk...............",
]
SPLASH = ['..k.......k.', '.kWk.k...kwk', '..k.kwk...k.', '......k.....']
# ふりぬき：刀を 前下へ ふりおろし、水の 三日月を のこす
SWORD_DOWN = [
    "nnnnnkk.......",
    "knnTTYk.......",
    ".kTYYYYk......",
    "..kkYkwWk.....",
    "....kkwWVk....",
    ".....kwWVk....",
    "......kwWVk...",
    ".......kwWVk..",
    "........kwWVk.",
    ".........kwVk.",
    "..........kk..",
]
ARC = [
    "....kkkkk.......",
    "...kwwwwwkk.....",
    ".....kkwwWWk....",
    ".......kkWWWk...",
    ".........kWWVk..",
    "..........kWVVk.",
    "..........kWWVk.",
    "..........kWVVk.",
    ".........kWVVk..",
    "........kVVVk...",
    "......kkVVk.....",
    "....kkkkk.......",
]
SW = {
    'idle0|idle3|blink|walk0|walk1|walk2|walk3|hit': place([(SWORD, 4, 13)]),
    'idle1': place([(SWORD, 4, 13), (DROP1, 16, 19)]),
    'idle2': place([(SWORD, 4, 13), (DROP2, 15, 21)]),
    'atk0': place([(SWORD_UP, 6, 2)]),
    'atk1': place([(SWORD_THRUST, 2, 13), (DROP1, 30, 18), (DROP2, 25, 20)]),
    'atk2': place([(ARC, 13, 5), (SWORD_DOWN, 8, 14), (SPLASH, 16, 24)]),
}
ARM0 = [
    ".RRRRRRRR......",
    "RRSSSSSSSR.....",
    "RkkkkkkkkS.....",
    "SSSSSSSSST.....",
    "SkkkkkkkkT.....",
    "STTTTTTTTT.....",
    ".ABBBBBC.......",
    ".ABBABBBC......",
    "..ABBBBBBC.....",
    "..ABBBBBBBC....",
    "...ABBBBBBBAA..",
    "...ABBBBBAABBA.",
    "....ABBBABBBBBC",
    "....ABBBABkBkBC",
    "....CBBBBBkBkBC",
    ".....CCCBBBBBC.",
    "........CCCCC..",
]

ARM = [r for i, r in enumerate(ARM0) if i not in (7, 9)]
ARM_PUNCH = [
    ".RRRRRRRR...........",
    "RRSSSSSSSR..........",
    "RkkkkkkkkS..........",
    "SSSSSSSSST..........",
    "SkkkkkkkkTAAAAA.....",
    "STTTTTTTTBBBBBBAAA..",
    ".ABBBBBBBBBBBBABBBA.",
    ".ABBBBBBBBBBBABBBBBC",
    "..ABBBBBBBBBBABkBkBC",
    "...CCCCCCCCCCCBkBkBC",
    "..............CCCCC.",
]

def base():
    return [
        dict(n='legB', g='legB', x=9, y=48, rows=outline(dk(LEG))),
        dict(n='armB', g='armB', x=8, y=31, rows=outline(dk(ARM))),
        dict(n='body', g='body', x=12, y=30, rows=outline(BODY)),
        dict(n='skirt', g='body', x=11, y=43, rows=outline(SKIRT)),
        dict(n='legA', g='legA', x=27, y=48, rows=outline(LEG)),
        dict(n='head', g='head', x=22, y=14, rows=outline(HEAD)),
        dict(n='helm', g='head', x=20, y=10, rows=outline(HELM)),
        dict(n='crest', g='head', x=28, y=8, rows=outline(CREST)),
        dict(n='eye', g='head', x=39, y=15, rows=EYE, alt=EYE_ALT),
        dict(n='sword', g='head', x=44, y=9, rows=SW['idle0|idle3|blink|walk0|walk1|walk2|walk3|hit'], alt=SW),
        dict(n='armF', g='armF', x=30, y=31, rows=outline(ARM), alt={'atk1': outline(ARM_PUNCH)}),
    ]
# ダウン：たっている 絵を 90度 たおして（あおむけ・頭が 後ろ）、目は ×
def knocked():
    g = [['.'] * 80 for _ in range(70)]
    for l in base():
        if l['n'] in ('sword', 'armB'): continue
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if 'ko' in k.split('|'): rows = v
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[l['y'] + j][l['x'] + i] = c
    ys = [y for y in range(70) if any(c != '.' for c in g[y])]; xs = [x for x in range(80) if any(g[y][x] != '.' for y in range(70))]
    g = [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
    h, w = len(g), len(g[0])
    return [''.join(g[y][w - 1 - x] for y in range(h)) for x in range(w)]   # 反時計回りに 90度
def layers():
    L = [dict(l, not_='ko') for l in base()]
    ko = knocked()
    return L + [dict(n='ko', g='root', x=2, y=61 - len(ko), rows=ko, only='ko'),
                dict(n='kosword', g='root', x=2 + len(ko[0]) - 6, y=55, rows=SWORD, only='ko')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1)}, 'idle3': {},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 0), 'armF': (-1, 1), 'legA': (1, 0)},
    'atk1': {'root': (5, 0), 'head': (1, 0), 'legB': (-2, 0)}, 'atk2': {'root': (6, 0), 'body': (0, 1), 'legB': (-2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1)},
    'ko': {},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
