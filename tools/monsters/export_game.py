# 採用された 手打ちモンスターを ゲーム（index.html）に 入れる
# 使い方: python3 tools/monsters/export_game.py
#   ADOPTED.json（図鑑の 採用 一覧）の モンスターを、
#   index.html の「HANDMON」区間に 絵（14コマ）・SPECIES（種族値・タイプ・説明）・LEARN（おぼえる わざ）として 書きこむ
import json, os, re, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, '..', '..', 'index.html')
BEGIN, END = '// ====== HANDMON（tools/monsters/export_game.py が 自動生成）======', '// ====== ここまで HANDMON ======'

src = open(GAME).read()
# ---- わざ 一覧（元の MOVES と MOVES100）----
i = src.index('const MOVES100 = '); j = src.index('\n};', i)
M100 = {}
for line in src[i:j].splitlines()[1:]:
    m = re.match(r'\s*"([\w-]+)": (\{.*\}),?$', line)
    if m: M100[m.group(1)] = json.loads(m.group(2))
BASIC = {'fire': ['ember', 'flame', 'blaze'], 'water': ['bubble', 'tide', 'icicle'], 'grass': ['leaf', 'vine', 'spore'], 'elec': ['spark', 'thunder'],
         'rock': ['rockfall', 'quake'], 'wind': ['gust', 'tornado'], 'normal': ['tackle']}

roster = {}
for n, i_, nm, t, base, body, size, note in re.findall(r'^\| (\d+) \| (\w+) \| (\S+) \| (\S+) \| (.+?) \| (\w) \| (\w) \| (.+?) \|$', open(os.path.join(HERE, 'ROSTER.md')).read(), re.M):
    roster[i_] = dict(no=int(n), name=nm, types=t.split('/'), base=base, body=body, size=size, note=note.replace('（完成）', '').strip())
def _ids(): return sorted(json.load(open(os.path.join(HERE, 'ADOPTED.json'))), key=lambda k: roster[k]['no'])


def h(s, k):  # 決まった ゆらぎ（-1〜1）
    return (int(hashlib.md5((s + k).encode()).hexdigest()[:6], 16) / 0xffffff) * 2 - 1

BODY = {'Q': (1, 1.15, 1, .95), 'B': (1, 1.1, .95, 1), 'F': (.9, 1, .85, 1.25), 'W': (1.05, .95, 1, 1), 'S': (1, 1.05, .9, 1.05),
        'M': (.95, 1, 1.2, .85), 'P': (1.1, .95, 1.1, .75)}
TYPEB = {'steel': (0, 0, .15, -.05), 'rock': (0, 0, .15, -.05), 'elec': (0, 0, 0, .12), 'wind': (0, 0, 0, .12), 'fighting': (0, .12, 0, 0),
         'dragon': (.05, .08, 0, 0), 'fairy': (.05, -.05, .05, 0), 'ghost': (-.05, 0, 0, .08), 'ice': (0, .05, 0, 0), 'normal': (.1, 0, 0, 0)}
TOTAL = {'S': 205, 'M': 235, 'L': 265}

def stats(i_, r):
    w = list(BODY[r['body']])
    for t in r['types']:
        for k, d in enumerate(TYPEB.get(t, (0, 0, 0, 0))): w[k] += d
    w = [max(.6, x + .08 * h(i_, 'hads'[k])) for k, x in enumerate(w)]
    tot = TOTAL[r['size']]; s = sum(w)
    return dict(zip(('hp', 'atk', 'def', 'spd'), (round(tot * x / s) for x in w)))

def style(r):
    t = set(r['types'])
    if t & {'psychic', 'fairy', 'ghost', 'elec', 'ice'} and not t & {'fighting'}: return 'ranged'
    if t & {'fighting', 'bug', 'ground', 'rock', 'dragon', 'steel', 'dark'} and r['body'] in 'QBM': return 'melee'
    return 'mid'

def learnset(i_, r):
    types = r['types']
    pool = []
    for t in types:
        pool += [(m, M100[m]) for m in M100 if M100[m]['t'] == t]
    pool = sorted(pool, key=lambda x: (x[1]['power'] or 70) + 30 * h(i_, x[0]))
    basic = [b for t in types for b in BASIC.get(t, [])][:2]
    out, lv = [], 1
    first = basic[:]
    if len(first) < 2: first += ['tackle'] if 'tackle' not in first else []
    for b in first[:2]: out.append([1, b])
    seen = set(first)
    for m, _ in pool:
        if m in seen: continue
        seen.add(m)
        lv = 1 if len(out) < 3 else lv + 3
        out.append([lv, m])
        if len(out) >= 12: break
    if len(out) < 6:   # 少ない タイプは ノーマルの わざで おぎなう
        for m in sorted((m for m in M100 if M100[m]['t'] == 'normal'), key=lambda m: h(i_, m)):
            if m in seen: continue
            seen.add(m); lv += 3; out.append([lv, m])
            if len(out) >= 8: break
    return out

def main():
    global src
    ids = _ids()
    data, species, learn = {}, {}, {}
    for i_ in ids:
        r = roster[i_]; sp = json.load(open(os.path.join(HERE, i_, 'sprite.json')))
        data[i_] = {'w': sp['w'], 'h': sp['h'], 'pal': sp['pal'], 'f': sp['f']}
        L = learnset(i_, r)
        species[i_] = {'n': r['name'], 'type': r['types'][0], **({'type2': r['types'][1]} if len(r['types']) > 1 else {}),
                       'base': stats(i_, r), 'moves': [m for _, m in L[:2]], 'style': style(r),
                       'catch': {'S': .5, 'M': .4, 'L': .3}[r['size']], 'rare': 1 if r['size'] == 'L' else 0,
                       'desc': r['note'] + '。（もと：' + r['base'] + '）', 'hand': 1}
        learn[i_] = L

    js = BEGIN + '\n' + '''// 図鑑で 採用された 手打ちモンスター（%d体）。絵は 14コマ（パレット＋ランレングス）
    const HandMon = (() => {
      const AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-';
      const DATA = %s;
      function frames(id) {
        const m = DATA[id], pal = m.pal.map(c => [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]), F = {};
        for (const k in m.f) {
          const s = m.f[k], px = new Uint8ClampedArray(m.w * m.h * 4); let p = 0, i = 0;
          while (i < s.length) {
            const c = AL.indexOf(s[i]); let n;
            if (s[i + 1] === '~') { n = parseInt(s.substr(i + 2, 3), 16); i += 5 } else { n = parseInt(s.substr(i + 1, 2), 16); i += 3 }
            if (c > 0) { const col = pal[c - 1]; for (let q = p; q < p + n; q++) { px[q * 4] = col[0]; px[q * 4 + 1] = col[1]; px[q * 4 + 2] = col[2]; px[q * 4 + 3] = 255 } }
            p += n;
          }
          F[k] = px;
        }
        return F;
      }
      return { DATA, frames };
    })();
    Object.assign(SPECIES, %s);
    Object.assign(LEARN, %s);
    ''' % (len(ids), json.dumps(data, ensure_ascii=False, separators=(',', ':')), json.dumps(species, ensure_ascii=False, separators=(',', ':')),
           json.dumps(learn, ensure_ascii=False, separators=(',', ':'))) + END

    if BEGIN in src:
        a = src.index(BEGIN); b = src.index(END) + len(END); src = src[:a] + js + src[b:]
    else:
        anchor = '// ====== ここまで AISPR ======'
        k = src.index(anchor) + len(anchor); src = src[:k] + '\n' + js + src[k:]
    open(GAME, 'w').write(src)
    print('handmon', len(ids), 'species written,', len(js) // 1024, 'KB')

if __name__ == '__main__':
    main()
