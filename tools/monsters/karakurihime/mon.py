# カラクリヒメ（フェアリー・はがね × からくり人形）手打ち GBA風
META = dict(id='karakurihime', name='カラクリヒメ', types=['fairy', 'steel'], base='からくり人形', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1634',
    'P': '#fcf4ee', 'Q': '#dcc2c6', 'V': '#987a8e',
    'i': '#7a6aa2', 'h': '#3a3054',
    'M': '#f47cb6', 'N': '#b83e86', 'O': '#661c50',
    'Y': '#f8cc58', 'y': '#a87428',
    'S': '#e6eef8', 's': '#8a96b8',
    'w': '#ffffff',
}
LIGHT = set('PMYSwi')

# 頭：黒うるしの 髪（姫カット）＋ 金の かんざし、白い 面の 顔
HEAD = [
    '......kkkkkk........',
    '....kkhiiiihkk......',
    '...khiiihhhhhhk.kk..',
    '..khiihhhhhhhhhkkYYk',
    '..khhhhhhhhhhhhhkYyk',
    '.khhhhhhhhhhhhhhhkk.',
    'khiihhhhhhkkkkkkkhk.',
    'khhhhhhhkkPPPPPPPkhk',
    'khhhhhhkPPPPPPPPPPkk',
    'khhhhhhkPPPPPPPPPPPk',
    'khhhhhhkPPPPPPPPPPPk',
    'khhhhhhkQPPPPPPPPPPk',
    'khhhhhhkQPPPPPPPPPkk',
    'khhhhhhkQQPPPPPPPPk.',
    'khhhhhhkVkQPPkkkkkk.',
    'khhhhhhkVkQPkNwkwNk.',
    'khhhhhhhkVkQkkkkkk..',
    'khhhhhhhkkVQPPPk....',
    'khhhhhhk.kkkkkk.....',
    'khhhhhk.............',
]
EYE = ['NPPPPPPPPNN', 'kkPPPPPPkkN', 'MwkPPPkMwMk', 'NPPPPPPNNPP']
EYE_ALT = {
    'blink': ['PPPPPPPPPNN', 'PPPPPPPPPPN', 'kkkPPPkkkkk', 'NPPPPPPNNPP'],
    'atk0|atk1|atk2': ['NPPPPPPPPNN', 'kkkPPPPkkkN', 'MwkPPPkwwMk', 'NNPPPPPNNNP'],
    'hit|ko': ['PPPPPPPPPNN', 'kPkPPPkPkPN', 'PkPPPPPkPPP', 'kPkPPPkPkPP'],
}
BUN = ['..kkkk..', '.khiihk.', 'khiihhhk', 'khhhhhhk', '.kkkkkk.']
HAIR = [
    '.khhk',
    'khihk',
    'khhhk',
    'khihk',
    'khhhk',
    'khhhk',
    'khhhk',
    'khhk.',
    'khhk.',
    '.kk..',
]
# 胴（えり・帯）と すそ広がりの 着物
KIMONO = [
    '......kkkkkkk.........',
    '.....kYyYkkPPk........',
    '....kMkkkPkPNNk.......',
    '...kMMMMkPkNNNOk......',
    '...kMMMNNkNNNNOk......',
    '...kMMMNNNNNNNOk......',
    '...kkkkkkkkkkkkk......',
    '...kYYYYYYyyyyyk......',
    '...kYyYkYYYyykyk......',
    '...kYYYYYYyyyyyk......',
    '...kkkkkkkkkkkkk......',
    '...kMMMNNNNNNNOOk.....',
    '...kMMMNNNNNNkNOOk....',
    '...kMMNNNNNNNkNOOk....',
    '..kMMNNNPNNNNkNNOOk...',
    '..kMMNNPMPNNNNkNOOk...',
    '..kMMNNNPNNNNNkNOOk...',
    '..kMMNNNNNNNNNkNNOOk..',
    '.kMMNNNNNNNNNNNkNOOk..',
    '.kMMNNNNNNNNNNNkNOOk..',
    '.kMMNNNNNNNNPNNkNNOOk.',
    '.kMMNNNNNNNPMPNNkNOOk.',
    '.kMNNNNNNNNNPNNNkNOOk.',
    'kMMNNNNNNNNNNNNNkNNOOk',
    'kMMNNNNNNNNNNNNNNkNOOk',
    'kMNNNPNNNNNNNNNNNkNOOk',
    'kMNNPMPNNNNNNNNNNkNOOk',
    'kMNNNPNNNNNNNNNNNkNOOk',
    'kMNNNNNNNNNNNNNNNNkOOk',
    'kPPPPPPPQQQQQQQQQVkVVk',
    'kMMMMMMNNNNNNNNNNOkOOk',
    '.kkkkkkkkkkkkkkkkkkkk.',
]
# 奥の うで：ふり上げて 扇を 頭の 後ろに
ARM_B = [
    'kYk.......',
    'kQVk......',
    '.kQVk.....',
    '..kYyk....',
    '..kyYk....',
    '...kQVk...',
    '....kQVk..',
    '.....kQVk.',
    '......kQVk',
    '.......kkk',
]
# 手前の うで：袖を まくって からくりの 腕（歯車の ひじ・手首）、刃の 扇を 前へ
SLEEVE_F = [
    '.kkkkkkk..',
    'kMMMMNNNk.',
    'kMMMNNNNOk',
    'kMMNNNNNOk',
    'kMNNNNNOOk',
    'kMNNPNNOOk',
    'kNNPMPNOOk',
    'kNNNPNOOOk',
    'kNNNNNOOOk',
    'kNNNNOOOk.',
    'kOOOOOOOk.',
    'kQQQQVVk..',
    '.kkkkkk...',
]
ARM_F = [
    '......kkk....',
    '.....kYyYk...',
    'kkkkkYkkYkkkk',
    'kPPQQkYyYkQVk',
    'kQQVVVkkkQQVk',
    '.kkkkkk.kkkk.',
]
HAND = ['.kkk.', 'kPQk.', 'kQVk.', 'kPkPk', '.k.k.']
import math
def fan(R, a0, a1, dark=False):
    """開いた 鉄扇：要（かなめ）＝ (R+1, R+1)。a0〜a1 度（0＝右、反時計回り）の 扇形。
    骨ごとに 明暗の ひだ、外の ふちは 刃（光る）、要の まわりは 金"""
    N = 2 * R + 3; c = R + 1; g = [['.'] * N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            dx, dy = x - c, c - y; d = math.hypot(dx, dy)
            if d > R + .4: continue
            rel = (math.degrees(math.atan2(dy, dx)) - a0) % 360
            if rel > a1 - a0: continue
            band = min(6, int(rel / ((a1 - a0) / 7)))
            if d < 2.2: ch = 'Y' if d < 1.2 else 'y'
            elif d > R - .8: ch = 'w' if band < 4 else 'S'
            elif d < 4: ch = 'M' if band % 2 == 0 else 'N'
            else: ch = 'S' if band % 2 == 0 else 's'
            if dark: ch = {'S': 's', 's': 'V', 'w': 'S', 'M': 'N', 'N': 'O', 'Y': 'y'}.get(ch, ch)
            g[y][x] = ch
    return pix.outline([''.join(r) for r in g])
import pix
FAN = fan(9, -40, 80)
FAN_B = fan(9, 95, 215, dark=True)
GETA = ['kPQk', 'kkkkk', 'kyyyk', '.k.k.']

PETAL = ['kk.', 'kMk', '.kPk', '..k']
PETAL2 = ['.kk', 'kMk', 'kPk.', 'k..']
def arc():
    """攻撃：鉄扇の 刃風（三日月）＋ 桜の はなびらを 手で 散らす"""
    g = pix.grid(22, 30)
    pix.ellipse(g, 3, 15, 16, 14, 'S'); pix.ellipse(g, 3, 15, 15, 13, 'w'); pix.ellipse(g, 3, 15, 13.5, 12, 'M')
    pix.ellipse(g, -1, 15, 14, 12.5, '.')
    r = pix.outline(pix.rows_of(g)); g = pix.grid_of(r)
    for (x, y, p) in ((3, 4, PETAL), (8, 12, PETAL2), (5, 20, PETAL), (2, 13, PETAL2), (10, 25, PETAL)):
        pix.stamp(g, p, x, y)
    return pix.rows_of(g)
# ダウン：糸が 切れた ように くずれる（着物が 床に ひろがり、面が あおむけに ころがる）
KO_POOL = [
    '........kkkkkkkkkkkkkkk.......',
    '.....kkkMMMNNNNNNNNNNNOkkk....',
    '...kkMMMNNNNNPNNNNNNNNOOOOkk..',
    '..kMMMNNNNNNPMPNNNNNNNNNOOOOk.',
    '.kMMNNNNNNNNNPNNNNNNNNNNNOOOk.',
    'kMMNNNNNNNNNNNNNNNNNNNNNNNOOOk',
    'kPPPPPPPQQQQQQQQQQQQQVVVVVVVVk',
    '.kkkkkkkkkkkkkkkkkkkkkkkkkkkk.',
]
def ko_head():
    g = pix.grid_of(HEAD)
    pix.stamp(g, EYE_ALT['hit|ko'], 8, 7)
    r = pix.rows_of(g)
    for _ in range(3): r = pix.rot90(r)
    return r
KO_FAN = fan(7, 0, 110)

# 背中の ぜんまい（ねじ）：待機中に 回る
KEY0 = ['.kk.....', 'kYyk....', 'kykkkkkk', 'kYyYYYyk', 'kykkkkkk', 'kYyk....', '.kk.....']
KEY1 = ['.k......', 'kYk.....', 'kYkkkkkk', 'kYyYYYyk', 'kykkkkkk', 'kyk.....', '.k......']

def layers():
    N = 'ko'
    return [
        dict(n='fanB', g='armB', x=17, y=2, rows=FAN_B, not_=N),
        dict(n='bun', g='head', x=28, y=6, rows=BUN, not_=N),
        dict(n='hair', g='head', x=28, y=26, rows=HAIR, not_=N),
        dict(n='getaB', g='legB', x=27, y=56, rows=GETA, not_=N),
        dict(n='getaA', g='legA', x=37, y=56, rows=GETA, not_=N),
        dict(n='key', g='body', x=17, y=32, rows=KEY0, alt={'idle1|idle3|walk1|walk3|atk0': KEY1}, not_=N),
        dict(n='kimono', g='body', x=24, y=25, rows=KIMONO, not_=N),
        dict(n='head', g='head', x=28, y=9, rows=HEAD, not_=N),
        dict(n='eye', g='head', x=36, y=16, rows=EYE, alt=EYE_ALT, not_=N),
        dict(n='sleeveF', g='body', x=33, y=30, rows=SLEEVE_F, not_=N),
        dict(n='armF', g='armF', x=40, y=32, rows=ARM_F, not_=N),
        dict(n='hand', g='armF', x=52, y=33, rows=HAND, not_=N),
        dict(n='fan', g='armF', x=42, y=23, rows=FAN, not_=N),
        # 桜の はなびら（ゆらゆら）
        dict(n='p1', g='petal', x=14, y=30, rows=PETAL, only='idle0|idle1|blink|walk0|walk1|hit'),
        dict(n='p1b', g='petal', x=15, y=27, rows=PETAL2, only='idle2|idle3|walk2|walk3'),
        dict(n='p2', g='petal', x=56, y=46, rows=PETAL2, only='idle0|idle1|blink|walk0|walk1|atk0'),
        dict(n='p2b', g='petal', x=57, y=49, rows=PETAL, only='idle2|idle3|walk2|walk3'),
        dict(n='p3', g='petal', x=46, y=10, rows=PETAL, only='idle1|idle2|walk1|walk2|atk0'),
        dict(n='arc', g='fx', x=55, y=16, rows=arc(), only='atk1'),
        dict(n='koFan', g='ko', x=4, y=46, rows=KO_FAN, only=N),
        dict(n='koPool', g='ko', x=14, y=52, rows=KO_POOL, only=N),
        dict(n='koHead', g='ko', x=30, y=43, rows=ko_head(), only=N),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'armB': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'armF': (0, 0)},
    'idle3': {'body': (0, 0), 'armB': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'body': (0, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'armF': (-3, -3), 'armB': (1, -1), 'head': (0, 1)},
    'atk1': {'root': (5, 0), 'armF': (3, 3), 'body': (1, 0)},
    'atk2': {'root': (6, 0), 'armF': (2, 6), 'armB': (2, 3)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 2), 'armB': (-1, 2)},
    'ko': {},
}
PARENT = {'fx': 'root', 'ko': 'root', 'petal': 'root', 'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
