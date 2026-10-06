# コオリミミズク（こおり・ひこう(風) × ミミズク）手打ち GBA風
import pix
META = dict(id='koorimimizuku', name='コオリミミズク', types=['ice', 'wind'], base='ミミズク', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2a4c',
    'W': '#f4f8ff', 'I': '#b4e2f8', 'J': '#6aa8d8', 'K': '#3a64a0',
    'N': '#5a6894', 'M': '#343e66',
    'E': '#a6fff2', 'G': '#cdbf9c', 'g': '#7a6a52',
}
LIGHT = set('WIEG')

HEAD = [
    'kk.......................',
    'kWkk.....................',
    'kIWIkk.........kkk.......',
    '.kJIWIkk.....kkIWk.......',
    '..kkJIWIkkkkkJIWk........',
    '...kkkJINNNNNJIk.........',
    '...kNNNNNNNNNNNkk........',
    '..kNNNNNNNNNNNNNNk.......',
    '.kNMMMMMMNNNMMMMMNk......',
    '.kNMkkkkkMMMMkkkMNk......',
    '.kNkEEEEWkMMkEEWkNk......',
    'kNNkEEkEkWkgkEkkNNk......',
    'kNNWkkkkWkgGgkkWNk.......',
    'kMNNWWWWWWgGgWWNNk.......',
    '.kMNNWWWWWWgWWNNk........',
    '..kMMNNWWWWWNMMk.........',
    '...kkMMMMMMMMkk..........',
    '.....kkkkkkkk............',
]
EYEN = ['EEEEW', 'EEkEk']
EYEN_ALT = {'blink': ['kkkkk', 'WWWWW'], 'atk0|atk1|atk2': ['WWWWW', 'EEkEW'], 'hit': ['kEkkk', 'EkEkk'], 'ko': ['EkEkk', 'kEkEk']}
EYEF = ['EW', 'Ek']
EYEF_ALT = {'blink': ['kk', 'WW'], 'atk0|atk1|atk2': ['WW', 'Ek'], 'hit|ko': ['kE', 'Ek']}
BODY = [
    '..............kkkkk.....',
    '...........kkkNNNNIk....',
    '.........kkNNNNNIWWIk...',
    '.......kkNNNNNNIWWWWk...',
    '.....kkNNNNNMNNIWJWWIk..',
    '....kNNNNMNNNNNIWWWJWk..',
    '...kNNNNNNNMNNNIJWWWWIk.',
    '..kNNMNNNNNNNNIWWJWWJIk.',
    '.kNNNNNNMNNNNNIWWWWJWIk.',
    '.kMNNNNNNNNNMNIJWWJWIJk.',
    'kMMNNNNNNNNNNNJIWWWIJk..',
    'kMMMNNNNNNNNNMJIIJIJk...',
    '.kMMMMNNNNNNMMJJJJk.....',
    '..kkMMMMMMMMMkkkkk......',
    '....kkkkkkkkk...........',
]
TALON = [
    '.kIJk..kIJk..',
    '.kJKk..kJKk..',
    'kMMMMk.kMMMMk',
    'kMkMkM.kMkMkM',
    'k.k.k..k.k.k.',
]
WING_UP = [
    '.....k......k......k........',
    '....kWk....kWk....kWk.......',
    '....kIJk..kWIk...kWIJk......',
    '...kWIJk.kWIJk..kWIJk.......',
    '...kWIJkkWIJk..kWIJk..k.....',
    '..kWIJk.kWIJk.kWIJk..kWk....',
    '..kWIJkkWIJkkkWIJkkkWIJk....',
    '.kWIJkkWIJkkWIJkkkWIIJk.....',
    '.kkkkkkkkkkkkkkkkkkkkkk.....',
    '..kNNJNNNJNNNJNNNNJNNMk.....',
    '..kNNNNNNNNNNNNNNNNNMMk.....',
    '...kNJNNNJNNNJNNNJNMMk......',
    '...kNNNNNNNNNNNNNNNMMk......',
    '....kNNJNNNJNNNJNNMMk.......',
    '.....kNNNNNNNNNNNMMMk.......',
    '......kMNNNNNNNNMMMk........',
    '.......kMMNNNNNMMMk.........',
    '........kkMMMMMMMk..........',
    '..........kkkkkk............',
]
def swept(rows):
    keep = [r for y, r in enumerate(rows) if y % 3 != 1]
    H = len(keep); out = []
    for y, r in enumerate(keep):
        sh = (H - 1 - y) * 2 // 3
        out.append(('.' * 12 + r)[sh:])
    w = max(len(r) for r in out); return [r.ljust(w, '.') for r in out]
WING_MID = swept(WING_UP)
WING_DN = pix.flip_v(WING_MID)
def dark(rows): return pix.recolor(rows, {'W': 'I', 'I': 'J', 'J': 'K', 'N': 'M'})

TAIL = [
    '.......kk',
    '.....kkIJk',
    '...kkWIJk.',
    '.kkWIJJk..',
    'kWIJJkk...',
    '.kkkk.....',
]
UP, MID, DN = 'idle0|blink|walk0|atk0', 'idle1|idle3|walk1|walk3|atk2|hit|ko', 'idle2|walk2|atk1'
def layers():
    return [
        dict(n='wingB_up', g='wingB', x=13, y=0, rows=dark(WING_UP), only=UP),
        dict(n='wingB_mid', g='wingB', x=6, y=10, rows=dark(WING_MID), only=MID),
        dict(n='wingB_dn', g='wingB', x=6, y=26, rows=dark(WING_DN), only=DN),
        dict(n='tail', g='body', x=11, y=38, rows=TAIL),
        dict(n='body', g='body', x=20, y=28, rows=BODY),
        dict(n='talon', g='talon', x=33, y=42, rows=TALON),
        dict(n='head', g='head', x=29, y=12, rows=HEAD),
        dict(n='eyeN', g='head', x=33, y=22, rows=EYEN, alt=EYEN_ALT),
        dict(n='eyeF', g='head', x=42, y=22, rows=EYEF, alt=EYEF_ALT),
        dict(n='wingF_up', g='wingF', x=2, y=5, rows=WING_UP, only=UP),
        dict(n='wingF_mid', g='wingF', x=-6, y=13, rows=WING_MID, only=MID),
        dict(n='wingF_dn', g='wingF', x=-6, y=28, rows=WING_DN, only=DN),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, 1)}, 'idle2': {'root': (0, 2)}, 'idle3': {'root': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)}, 'walk1': {}, 'walk2': {'root': (0, 1)}, 'walk3': {},
    'atk0': {'root': (-3, -2)}, 'atk1': {'root': (3, 1)}, 'atk2': {'root': (4, 1)},
    'hit': {'root': (-4, 0)}, 'ko': {'root': (0, 6)},
}
PARENT = {'head': 'body', 'talon': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
