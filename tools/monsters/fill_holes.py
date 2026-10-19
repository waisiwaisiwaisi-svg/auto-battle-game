# モンスターの ドット絵（M64）の「ぬけ」を うめる
#   ぬけ：体の なかに ぽつんと あいた とうめいの 穴（4つで かこまれた 外と つながらない 穴）
#   ・4ドット いかの 穴は いつも うめる
#   ・5〜40ドットの 穴は、まわりが ふちどり（くらい いろ）で ない とき だけ うめる（パーツの すきまは のこす）
#   うめる いろ：穴の まわりの いろで 外がわから じゅんに ぬる
# usage: python3 tools/monsters/fill_holes.py index.html   （M64 の ぶぶんを かきかえる）
#        python3 tools/monsters/fill_holes.py m64.json       （json を かきかえる）
import sys, json
from collections import Counter
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'


def decode(fr):
    w, h, d = fr['w'], fr['h'], fr['d']; px = []
    for i in range(0, len(d), 3): px += [AL.index(d[i])] * int(d[i + 1:i + 3], 36)
    return w, h, px


def encode(px):
    s = []; i = 0
    while i < len(px):
        j = i
        while j < len(px) and px[j] == px[i] and j - i < 1295: j += 1
        n = j - i; t = ''
        while n: t = '0123456789abcdefghijklmnopqrstuvwxyz'[n % 36] + t; n //= 36
        s.append(AL[px[i]] + t.rjust(2, '0')); i = j
    return ''.join(s)


def lum(c): return .299 * int(c[1:3], 16) + .587 * int(c[3:5], 16) + .114 * int(c[5:7], 16)


def fill(w, h, px, pal):
    dark = [False] + [lum(c) < 70 for c in pal]; seen = [0] * (w * h); n = 0
    N8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for st in range(w * h):
        if px[st] or seen[st]: continue
        stack = [st]; seen[st] = 1; comp = []; edge = False
        while stack:
            p = stack.pop(); comp.append(p); x, y = p % w, p // w
            if x in (0, w - 1) or y in (0, h - 1): edge = True
            for q in ((p - 1) if x > 0 else -1, (p + 1) if x < w - 1 else -1, (p - w) if y > 0 else -1, (p + w) if y < h - 1 else -1):
                if q >= 0 and not px[q] and not seen[q]: seen[q] = 1; stack.append(q)
        if edge or len(comp) > 40: continue
        cs = set(comp); ring = [px[(p // w + dy) * w + p % w + dx] for p in comp for dx, dy in N8 if 0 <= p % w + dx < w and 0 <= p // w + dy < h and (p // w + dy) * w + p % w + dx not in cs]
        ring = [k for k in ring if k]
        if len(comp) > 4 and (not ring or sum(dark[k] for k in ring) / len(ring) >= .35): continue   # ふちどりに かこまれた すきま＝わざと
        todo = set(comp)
        while todo:   # 外がわから じゅんに まわりの いちばん おおい いろで ぬる
            nxt = {}
            for p in todo:
                x, y = p % w, p // w; c = Counter(px[(y + dy) * w + x + dx] for dx, dy in N8 if 0 <= x + dx < w and 0 <= y + dy < h and px[(y + dy) * w + x + dx])
                if c: nxt[p] = c.most_common(1)[0][0]
            if not nxt: break
            for p, k in nxt.items(): px[p] = k
            todo -= set(nxt); n += len(nxt)
    return n


def fix_all(M):
    tot = {}
    for sid, v in M.items():
        n = 0
        for fr in v['f']:
            w, h, px = decode(fr); k = fill(w, h, px, v['pal'])
            if k: fr['d'] = encode(px); n += k
        if n: tot[sid] = n
    return tot


if __name__ == '__main__':
    path = sys.argv[1]; s = open(path).read()
    if path.endswith('.json'):
        M = json.loads(s); tot = fix_all(M); json.dump(M, open(path, 'w'), separators=(',', ':'))
    else:
        key = 'const M64 = '; i = s.index(key) + len(key); M, end = json.JSONDecoder().raw_decode(s[i:])
        tot = fix_all(M); s = s[:i] + json.dumps(M, separators=(',', ':'), ensure_ascii=False) + s[i + end:]; open(path, 'w').write(s)
    print(len(tot), 'たい', sum(tot.values()), 'ドット うめた'); print(sorted(tot.items(), key=lambda x: -x[1])[:20])
