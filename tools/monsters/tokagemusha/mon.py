# トカゲムシャ（ドラゴン・かくとう × リザードマン）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく 描きなおし、胴と 足は 短く。曲刀・角・しっぽは 大きい まま）
META = dict(id='tokagemusha', name='トカゲムシャ', types=['dragon', 'fighting'], base='リザードマン', size='M')
PAL = {
    'k': '#101018', 'l': '#1e3a2c',
    'G': '#9ed67c', 'H': '#4f9a58', 'J': '#2a5e44',
    'B': '#f2e2a6', 'b': '#bc9a5c',
    'A': '#f2b452', 'a': '#a8682c', 'z': '#5a321e',
    'S': '#e2eaf4', 's': '#8a98b6',
    'Y': '#ffe23a', 'R': '#e04040', 'r': '#86203a',
    'w': '#ffffff',
}
LIGHT = set('GBASYRw')
EYE_BOX = (35, 23, 9, 9)   # 目（idle0 の 64x64 座標）

HEAD = [
    '.......kkkkk................',
    '.....kkGGGGGkk..............',
    '....kGGGGGGGGGkkk...........',
    '...kGGGGGGGGGGGGGkkkk.......',
    '..kGGGGGGGGGGGGGGGGGGkkkk...',
    '..kGGGHHHHHHHHGGGGGGGGGGGk..',
    '.kGGHHHHHHHHHHHHHGGGGGGGGGk.',
    '.kGHHHHHHHHHHHHHHHHHHHHHHGk.',
    '.kGHHHHHHHHHHHHHHHHHHHHkHHk.',
    'kHHHHHHHHHHHHHHHHHHHHHHHHJk.',
    'kHHHHHHHHHHHHHHHHHJJJJJJJk..',
    'kHHJJkkkkkkkkkkkkkkkkkkkk...',
    'kHJJkwkkwkkkwkkwkkwkkwkwk...',
    'kJJJkrrrrrrrrrrrrrrrrrrk....',
    'kJJJkwkwkkwkkwkkwkkwkk......',
    'kJJkBBBBbbbbbbbbbbbbbk......',
    '.kJkBBBbbbbbbbbbbbbk........',
    '..kkkbbbbbbbbbbbkk..........',
    '....kkkkkkkkkkkk............',
]
HORN = [
    'kkk..........',
    'kBBkk........',
    '.kbBBBkk.....',
    '..kbbBBBBkk..',
    '...kkbbbBBBk.',
    '.....kkkbbbk.',
    '........kkk..',
]
FIN = [  # 首の うしろの 赤い ひれ
    '...k......',
    '..kRk.k...',
    '..kRkkRk..',
    '.kRrkRrk..',
    '.kRrkRrkk.',
    'kRrkRrkRk.',
    'kRrkRrkrk.',
    'kkkkkkkkk.',
]
TORSO = [
    '..........kkkkk.....',
    '........kkGGGHHk....',
    '......kkGGGGHHBBk...',
    '....kkGGGGGAHHBBk...',
    '...kGGGGGGAaHHBBbk..',
    '..kGGGGHHAaHHHkkkk..',
    '..kGGHHHAaHHHHkBBbk.',
    '.kGGHHHAaHHHHJkkkkk.',
    '.kGHHHAaHHHHJJkBBbk.',
    '.kGHHAaHHHHJJJkkkk..',
    '.kkkkkkkkkkkkkkkkk..',
    '.kAAARRRRAAaaaaazk..',
    '.kaaRRrrRaaazzzzk...',
    '..kkRrrRkkkkkkkk....',
    '...kRrrk............',
    '...kRrk.............',
    '....kk..............',
]
TAIL = [
    '..................kk..',
    '..............k..kRk..',
    '.........k...kRkkRrkk.',
    '.....k..kRk.kRrkkkGGGk',
    '....kRkkRrkkkkkGGGHHHk',
    '...kRrkkkkkGGGGHHJHHJk',
    '...kkkkGGGGHHHHHHHHJk.',
    '...kkGGHHJHHHHJHJJJk..',
    '..kGGHHHHHHJHJJJJkk...',
    '.kGHHJHHJJJJJkkk......',
    '.kGHHHJJJkkk..........',
    'kGHJJkkk..............',
    'kHJkk.................',
    'kkk...................',
]
LEG = [
    '.kkkkkkk..',
    'kGGGGHHJk.',
    'kGHHHHHJJk',
    '.kGHHHHJk.',
    '..kGHHJk..',
    '..kGHHJk..',
    '.kGGHHJJk.',
    'kGGHHHHHJk',
    'kwkGkwkHwk',
    'kwkkkwkkwk',
    '.k...k..k.',
]
DLEG = [r.replace('G', 'H') for r in LEG]
SCIM = [
    'kkk.....................',
    'kSSkkk..................',
    '.kwSSSkkk...............',
    '..kwwSSSSkkk............',
    '...kkwwSSSSsskk.........',
    '.....kkwwwSSSsskk.......',
    '.......kkkwwSSSssk......',
    '..........kkwwSSsk......',
    '............kkwSSkk.....',
    '..............kkkkAk....',
    '...............kAAaAk...',
    '................kRk.....',
    '................kRk.....',
    '................kk......',
]
ARM_B = [
    '.kkkk....',
    'kHHJJk...',
    'kHJJJk...',
    '.kkHJJk..',
    '...kHJJk.',
    '....kHJJk',
    '.....kkk.',
]
ARM_F = [   # 肩当て → 短い うで → こて → 前に 出した こぶし
    '.kkkkkk.........',
    'kAAAAaak.....kk.',
    'kAaaaazk...kkGwk',
    'kaazzzzk..kGGHHw',
    '.kkGHHJk.kAAaazk',
    '...kGHHJkAAazkw.',
    '...kGHHJAaazk...',
    '....kGHJJazk....',
    '.....kkkkkk.....',
]

DORSAL = [
    '..........k...',
    '.........kRk..',
    '.........kRrk.',
    '......k..kRrk.',
    '.....kRk.kkkk.',
    '.....kRrkk....',
    '..k..kRrrk....',
    '.kRk.kkkk.....',
    '.kRrkk........',
    'kRrrk.........',
    'kkkkk.........',
]
# 目（O：傷の 目）：たてに 走る 古い 刀傷（クリーム B＋影 b）が まゆと 上下の まぶたを 切って いる。目は 黄の 虹彩に 丸い 小さな 黒瞳
EYE = [
    '.......B.',
    '......Bb.',
    'kkkkk.Bbk',
    '.kkkkkBkk',
    '.kwYkkYYk',
    '.kYAkkAAk',
    '..kkkkBk.',
    '.....Bb..',
    '.....B...',
]
_T, _B = EYE[:4], EYE[6:]
EYE_ALT = {
    'blink': _T + ['.kHHHHBHk', '.kkkkkBkk'] + ['..HHHHBH.'] + _B[1:],
    'atk0|atk1|atk2': _T + ['.kwwkkYwk', '.kYYkkYAk'] + _B,
    'hit': ['.......B.', '......Bb.', '......Bb.', 'kkkkkkBkk', '.kkk..Bk.', '...kkkB..', '......B..', '.....Bb..', '.....B...'],
    'ko': ['.......B.', '......Bb.', '......Bb.', '.r...rB..', '..r.r.B..', '...r.....', '..r.r.B..', '.r...rBb.', '.....B...'],
}
# 攻撃：曲刀を 前へ ふりぬく
SCIM_F = [
    '.kkkk.....................',
    'kHHJJk....................',
    'kHJJJkk.kk................',
    '.kHJJkAkSSkkkkkkkk........',
    '..kHkkAkwwSSSSSSSSkkkk....',
    '...kRkaksswwwwSSSSSSSSkk..',
    '...kRk.kkkkksssssSSSSSSSk.',
    '....k......kkkkkkksssSSSk.',
    '..................kkkkkk..',
]
SCIM_D = [
    '.kkkk...........',
    'kHHJJk..........',
    'kHJJJkk.........',
    '.kkJJkAk........',
    '...kkkAak.......',
    '....kRkkSkk.....',
    '....kRk.kwSkk...',
    '.....k...kwSSk..',
    '..........kwSsk.',
    '...........kwSsk',
    '............kwsk',
    '.............kSk',
    '..............kk',
]
ARC = [  # 竜の 気を まとった 横なぎの 斬撃（金）
    '......kkkkkkk.........',
    '...kkkYYYYYYYkkk......',
    '.kkYYwwwwwwwwYYYkk....',
    'kAAwwkkkkkkkkwwwYYkk..',
    'kakkk........kkkwwYYk.',
    '.k..............kkwYAk',
    '..................kwAk',
    '..................kwAk',
    '.................kwAak',
    '...............kkYAak.',
    '.............kkYAakk..',
    '...........kkAAakk....',
    '............kkkk......',
]
# ダウン：うつぶせに たおれ、曲刀を 手放す
KO_BODY = [
    '..k....k....k.......',
    '.kRk..kRk..kRk......',
    '.kRrkkkRrkkkRrkkk...',
    '..kkGGGGGGGGGGGGGkk.',
    '.kGGGHHHHHHHHHHHHHGk',
    '.kGHHHHJHHHHHHHJHHHk',
    'kGHHAAARRRRAAaaaHHJk',
    'kHHHaaaRrrRaaazzHJk.',
    'kHHHHJJJJJJJJJJJJJk.',
    'kkkkkkkkkkkkkkkkkk..',
]
KO_LEG = ['..kkkk..', '.kGHHJk.', 'kGHHJJk.', 'kHHJJk..', 'kwkwkk..']
KO_SCIM = [
    '.kkkkkkkkkkkkkkk....',
    'kwwwwwSSSSSSSSSSkkk.',
    '.kkssssssSSSSSSSSSkAk',
    '...kkkkkkkkkkkkkkkkRRk',
]
def layers():
    N = 'atk1|atk2|ko'
    return [
        dict(n='scim', g='armB', x=9, y=22, rows=SCIM, not_=N),
        dict(n='armB', g='armB', x=25, y=33, rows=ARM_B, not_=N),
        dict(n='dorsal', g='body', x=17, y=33, rows=DORSAL, not_='ko'),
        dict(n='tail', g='tail', x=4, y=40, rows=TAIL, not_='ko'),
        dict(n='legB', g='legB', x=25, y=50, rows=DLEG, not_='ko'),
        dict(n='torso', g='body', x=21, y=37, rows=TORSO, not_='ko'),
        dict(n='legA', g='legA', x=33, y=50, rows=LEG, not_='ko'),
        dict(n='fin', g='head', x=26, y=25, rows=FIN, not_='ko'),
        dict(n='horn', g='head', x=24, y=18, rows=HORN, not_='ko'),
        dict(n='head', g='head', x=30, y=21, rows=HEAD, not_='ko'),
        dict(n='eye', g='head', x=35, y=23, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='armF', g='armF', x=34, y=40, rows=ARM_F, not_='ko'),
        dict(n='koTail', g='ko', x=0, y=47, rows=TAIL, only='ko'),
        dict(n='koLeg', g='ko', x=12, y=47, rows=KO_LEG, only='ko'),
        dict(n='koBody', g='ko', x=12, y=51, rows=KO_BODY, only='ko'),
        dict(n='koFin', g='ko', x=24, y=44, rows=FIN, only='ko'),
        dict(n='koHorn', g='ko', x=25, y=39, rows=HORN, only='ko'),
        dict(n='koHead', g='ko', x=30, y=42, rows=HEAD, only='ko'),
        dict(n='koEye', g='ko', x=35, y=44, rows=EYE, alt=EYE_ALT, only='ko'),
        dict(n='koScim', g='ko', x=40, y=57, rows=KO_SCIM, only='ko'),
        dict(n='scimF', g='armF', x=37, y=41, rows=SCIM_F, only='atk1'),
        dict(n='scimD', g='armF', x=39, y=42, rows=SCIM_D, only='atk2'),
        dict(n='arc', g='fx', x=54, y=36, rows=ARC, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'armF': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'tail': (0, -1)},
    'idle3': {'body': (0, 0), 'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'tail': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'tail': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 1), 'armB': (-2, -1), 'armF': (-1, 0), 'tail': (1, 0)},
    'atk1': {'root': (5, 0), 'body': (1, 1), 'legA': (2, 0), 'tail': (0, -1)},
    'atk2': {'root': (7, 0), 'body': (1, 2), 'legA': (2, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, 0), 'head': (-2, -1), 'armF': (-2, 1), 'tail': (0, 1)},
    'ko': {},
}
PARENT = {'fx': 'root', 'ko': 'root', 'head': 'body', 'armF': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
