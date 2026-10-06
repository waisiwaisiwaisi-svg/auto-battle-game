# GBA風 仕上げ：16色パレットに まとめ、光の 当たる ふちの 輪郭を 黒から 濃い色に（セルアウト）
import dragon as D
PAL16 = {
    'k': '#101018',            # 輪郭（黒）
    'l': '#1e4a2e',            # 輪郭（光側／内側の 線：濃い緑）
    '1': '#b4ec68', '2': '#5cb84a', '3': '#2f7a44',      # 体 3色
    '4': '#fff6cc', '5': '#f6d27e', '6': '#c8904e',      # おなか 3色
    '7': '#ff9c74', '8': '#e0505a', '9': '#8a2a52',      # 翼膜 3色
    'h': '#fff2d8', 'j': '#b89c78',                      # 角・つめ 2色
    'y': '#ffd23f', 'o': '#ff7a1f',                      # 目・ほのお 2色
}
MAP = {'A': '1', 'B': '1', 'C': '2', 'D': '3', 'E': 'l', 'a': '4', 'b': '5', 'd': '6', 'r': '7', 's': '8', 't': '9', 'u': '9',
       'H': 'h', 'I': 'h', 'J': 'j', 'w': 'h', 'y': 'y', 'Y': 'o', 'p': 'k', 'm': '9', 'n': '8', 'F': 'h', 'G': 'y', 'K': 'o', 'L': '8', 'k': 'k'}
LIGHT = set('147h')
def convert(rows):
    return [''.join(MAP.get(ch, ch) for ch in r) for r in rows]
def selout(img_rows):
    """合成後の 絵で：明るい色に 上か 左で 接する 黒輪郭 → 濃い緑（光が 当たる 側の 輪郭）"""
    H = len(img_rows); out = [list(r) for r in img_rows]
    for y in range(H):
        for x in range(len(img_rows[y])):
            if img_rows[y][x] != 'k': continue
            below = img_rows[y + 1][x] if y + 1 < H else '.'
            right = img_rows[y][x + 1] if x + 1 < len(img_rows[y]) else '.'
            above = img_rows[y - 1][x] if y > 0 else '.'
            left = img_rows[y][x - 1] if x > 0 else '.'
            # 外側（空気）に 面していて、内側が 明るい色 → 光の 当たる 輪郭
            if (below in LIGHT or right in LIGHT) and (above == '.' or left == '.'): out[y][x] = 'l'
    return [''.join(r) for r in out]

def finish(raw):
    """生の 文字（A〜E など）で 合成した 絵 → GBA風に 仕上げ"""
    H = len(raw); W = len(raw[0]); g = [list(r) for r in raw]
    def at(y, x): return raw[y][x] if 0 <= y < H and 0 <= x < W else '.'
    out = [[MAP.get(ch, ch) for ch in r] for r in g]
    for y in range(H):
        for x in range(W):
            ch = raw[y][x]
            # 明るい色は 上か 左の ふち（2ドット以内に 空気か 輪郭）だけに のこす＝三日月の ハイライト
            if ch == 'B':
                edge = any(at(y - d, x) in '.k' or at(y, x - d) in '.k' for d in (1, 2))
                out[y][x] = '1' if edge else '2'
            # 内側の 線（まわりに 空気が ない 黒）は 濃い緑に。目の まわりは 黒の まま
            if ch == 'k':
                nb = [at(y + dy, x + dx) for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))]
                if '.' not in nb and not any(c in 'wyYp' for c in nb): out[y][x] = 'l'
    return selout([''.join(r) for r in out])
