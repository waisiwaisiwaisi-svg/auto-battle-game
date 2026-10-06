// ====== ここから AISPR ======
// モンスターの ドット絵（画像生成AI で 下絵を 作り、減色・輪郭・掃除して ドット絵に したもの）。
// 1体 1枚の 絵から、ドット単位の 変形（行の けずり／ふやし・ずらし・ななめ・上下反転）で 14コマの アニメを 作る
const AISpr = (() => {
  const FRAMES = ['idle0', 'idle1', 'idle2', 'idle3', 'blink', 'walk0', 'walk1', 'walk2', 'walk3', 'atk0', 'atk1', 'atk2', 'hit', 'ko'];
  const AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-';
  const PAD = 8; // 動いても はみ出さない 余白
  const DATA = {};
  function decode(s) {
    const g = new Uint8Array(s.w * s.h); let p = 0;
    for (let i = 0; i < s.d.length; i += 3) { const c = AL.indexOf(s.d[i]), n = parseInt(s.d.substr(i + 1, 2), 36); g.fill(c, p, p + n); p += n; }
    const rows = []; for (let y = 0; y < s.h; y++) rows.push(Array.from(g.subarray(y * s.w, (y + 1) * s.w)));
    return rows;
  }
  // ---- 変形（rows は 色番号の 2次元配列、足もとは 下の 行）----
  const W = rows => rows[0].length;
  const blank = w => new Array(w).fill(0);
  const mid = rows => Math.floor(rows.length * .45);
  function squash(rows, n) { const m = mid(rows); return [...Array.from({ length: n }, () => blank(W(rows))), ...rows.slice(0, m), ...rows.slice(m + n)]; }
  function dupMid(rows, m, n) { const top = rows.slice(0, m), bot = rows.slice(m); return [...top, ...Array.from({ length: n }, () => rows[m].slice()), ...bot]; }
  // 上の 行ほど 横に ずらす（k>0 で 前のめり）
  function shear(rows, k) { const h = rows.length; return rows.map((r, y) => shift1(r, Math.round(k * (h - 1 - y) / (h - 1)))); }
  function shift1(r, d) { if (!d) return r.slice(); const o = blank(r.length); for (let x = 0; x < r.length; x++) { const t = x + d; if (t >= 0 && t < r.length) o[t] = r[x]; } return o; }
  function flipV(rows) { return rows.slice().reverse(); }
  // まばたき：目の 四角を まわりの 色で うめて 下に 線
  function blink(rows, eyes) {
    const o = rows.map(r => r.slice());
    for (const [ex, ey, ew, eh, lid, line] of eyes || []) {
      for (let y = ey; y < ey + eh; y++) for (let x = ex; x < ex + ew; x++) if (o[y] && o[y][x] !== undefined) o[y][x] = y === ey + eh - 1 && x > ex && x < ex + ew - 1 ? line : lid;
    }
    return o;
  }
  function framesOf(id) {
    const s = DATA[id], M = 4, base = decode(s).map(r => [...blank(M), ...r, ...blank(M)]), w = s.w + PAD * 2, h = s.h + PAD;
    const put = (rows, dx = 0, dy = 0) => {
      const px = new Uint8ClampedArray(w * h * 4), pal = s.pal.map(c => [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]);
      const oy = h - rows.length + dy, ox = PAD - M + dx;
      rows.forEach((r, y) => r.forEach((c, x) => {
        if (!c) return; const X = ox + x, Y = oy + y; if (X < 0 || Y < 0 || X >= w || Y >= h) return;
        const i = (Y * w + X) * 4, col = pal[c - 1]; px[i] = col[0]; px[i + 1] = col[1]; px[i + 2] = col[2]; px[i + 3] = 255;
      }));
      return px;
    };
    const eye = (s.eyes || []).map(e => [e[0] + M, ...e.slice(1)]);
    const F = {
      idle0: put(base), idle1: put(squash(base, 1)), idle2: put(squash(base, 1)), idle3: put(base),
      blink: put(blink(base, eye)),
      walk0: put(base), walk1: put(shear(dupMid(base, mid(base), 1), 1), 0, -2), walk2: put(squash(base, 1)), walk3: put(shear(dupMid(base, mid(base), 1), -1), 0, -2),
      atk0: put(shear(squash(base, 2), -2), -2), atk1: put(shear(dupMid(base, mid(base), 1), 3), 5), atk2: put(shear(base, 1), 3),
      hit: put(shear(base, -3), -4), ko: put(flipV(base)),
    };
    return F;
  }
  return { DATA, FRAMES, framesOf, PAD };
})();
// ====== ここまで AISPR ======
