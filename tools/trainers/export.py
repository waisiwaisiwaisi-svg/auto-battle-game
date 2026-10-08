# trainers.json → index.html の「TRAINERART」区間（パレット＋ランレングス）
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); GAME = os.path.join(HERE, '..', '..', 'index.html')
BEGIN, END = '// ====== TRAINERART（tools/trainers/export.py が 自動生成）======', '// ====== ここまで TRAINERART ======'
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
def rle(a):
    flat = np.array(a).ravel(); s = ''; i = 0
    while i < len(flat):
        j = i
        while j < len(flat) and flat[j] == flat[i] and j - i < 1295: j += 1
        s += AL[flat[i]] + np.base_repr(j - i, 36).lower().rjust(2, '0'); i = j
    return s
T = json.load(open(os.path.join(HERE, 'trainers.json')))
data = {k: {'w': v['w'], 'h': v['h'], 'pal': v['pal'], 'f': [rle(f) for f in v['f']]} for k, v in T.items()}
js = BEGIN + '''
// トレーナーの 絵（4ポーズ：0 たち・1 ゆびさし・2 てのひら・3 ガッツポーズ）
const TRAINER_ART = %s;
function trainerArt(key) {
  const a = TRAINER_ART[key], pal = a.pal.map(c => [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]);
  const AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-';
  const pose = a.f.map(s => { const px = new Uint8ClampedArray(a.w * a.h * 4); let p = 0;
    for (let i = 0; i < s.length; i += 3) { const c = AL.indexOf(s[i]), n = parseInt(s.substr(i + 1, 2), 36);
      if (c) for (let q = p; q < p + n; q++) { const col = pal[c - 1]; px[q * 4] = col[0]; px[q * 4 + 1] = col[1]; px[q * 4 + 2] = col[2]; px[q * 4 + 3] = 255; }
      p += n; }
    return px; });
  const fr = { idle0: pose[0], idle1: pose[0], idle2: pose[0], idle3: pose[0], atk1: pose[1], atk2: pose[2], win: pose[3], ko: pose[0] };
  const o = bakeFrames(fr, a.w, a.h); o.art = true; return o;
}
''' % json.dumps(data, separators=(',', ':')) + END
src = open(GAME).read()
if BEGIN in src: i = src.index(BEGIN); j = src.index(END) + len(END); src = src[:i] + js + src[j:]
else: k = src.index('const trainerSpr = '); src = src[:k] + js + '\n' + src[k:]
open(GAME, 'w').write(src); print('trainer art', len(js) // 1024, 'KB')
