// ====== I18N（tools/i18n/build_i18n.py が 自動生成：ことば＝日本語・English・简体中文）======
// ひょうじの ときに 日本語を おきかえる（DOMの 文字・title など・キャンバスの 文字）。マギア名・技名は ローマ字。
const LANG = (() => { try { const v = localStorage.getItem('pma_lang'); return v === 'en' || v === 'zh' ? v : 'ja'; } catch (e) { return 'ja'; } })();
const I18N_DICT = __I18N_DICT__;
const ROMA_K = { 'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo', 'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho', 'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho', 'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo', 'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo', 'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo', 'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo', 'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo', 'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo', 'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo', 'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo', 'てぃ': 'ti', 'でぃ': 'di', 'ふぁ': 'fa', 'ふぃ': 'fi', 'ふぇ': 'fe', 'ふぉ': 'fo', 'うぃ': 'wi', 'うぇ': 'we', 'うぉ': 'wo', 'ゔぁ': 'va', 'ゔぃ': 'vi', 'ゔぇ': 've', 'ゔぉ': 'vo', 'しぇ': 'she', 'じぇ': 'je', 'ちぇ': 'che', 'つぁ': 'tsa', 'とぅ': 'tu', 'どぅ': 'du' };
const ROMA_1 = (() => { const o = {}, a = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉゃゅょゔ', r = 'a i u e o ka ki ku ke ko sa shi su se so ta chi tsu te to na ni nu ne no ha hi fu he ho ma mi mu me mo ya yu yo ra ri ru re ro wa o n ga gi gu ge go za ji zu ze zo da ji zu de do ba bi bu be bo pa pi pu pe po a i u e o ya yu yo vu'.split(' '); for (let i = 0; i < a.length; i++) o[a[i]] = r[i]; return o; })();
function romaji(w) {
  const h = [...w].map(c => { const x = c.charCodeAt(0); return x >= 0x30a1 && x <= 0x30f4 ? String.fromCharCode(x - 0x60) : c; }).join('');
  let o = '', dbl = false;
  for (let i = 0; i < h.length; i++) {
    const c = h[i], two = h.slice(i, i + 2);
    if (c === 'っ') { dbl = true; continue; }
    if (c === 'ー' || c === '・') continue;
    let r = ROMA_K[two]; if (r) i++; else r = ROMA_1[c] != null ? ROMA_1[c] : c;
    if (dbl) { r = (r.startsWith('ch') ? 't' : r[0]) + r; dbl = false; }
    o += r;
  }
  return o ? o[0].toUpperCase() + o.slice(1) : o;
}
const tr = (() => {
  if (LANG === 'ja') return (s) => s;
  const LI = LANG === 'en' ? 0 : 1, EX = new Map(), TPL = [], SUB = [], JPRE = /[぀-ヿ一-鿿]/, cache = new Map(), DONE = new Set();
  const esc = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  for (const k in I18N_DICT) {
    const v = I18N_DICT[k][LI]; if (!v) continue;
    if (k.includes('⟦')) { if (/⟧⟦/.test(k) || (k.replace(/⟦\d+⟧/g, '').trim().length < 3 && !/[\u4e00-\u9fff]/.test(k))) continue;   // ならんだ ⟦⟧（どこで わけるか きまらない）・きまった 文字が すくない ものは つかわない
      const ps = k.split(/⟦(\d+)⟧/); let re = '^'; const ord = []; ps.forEach((p, i) => { if (i % 2) { re += '(.+?)'; ord.push(+p); } else re += esc(p); }); TPL.push({ re: new RegExp(re + '$', 's'), ord, out: v, dot: k.includes('・'), fx: k.replace(/⟦\d+⟧/g, '').length }); }
    else { EX.set(k, v); if (k.length >= 2) SUB.push([k, v]); }
  }
  TPL.sort((a, b) => b.fx - a.fx); SUB.sort((a, b) => b[0].length - a[0].length);
  const MISS = new Set(); window.__trMiss = MISS;
  let NS = null; const NSET = () => NS || (NS = new Set(names().map(x => x[0])));
  let NAMES = null;   // マギア名・技名 → ローマ字（ながい じゅん）
  const names = () => { if (NAMES) return NAMES; const s = new Set(); try { for (const k in SPECIES) s.add(SPECIES[k].n); for (const k in MOVES) s.add(MOVES[k].n); } catch (e) { return []; } NAMES = [...s].filter(n => n && JPRE.test(n) && !EX.has(n)).sort((a, b) => b.length - a.length).map(n => [n, romaji(n)]); return NAMES; };
  function core(c) {
    let r = EX.get(c); if (r !== undefined) return r;
    { const m = c.match(/^(相手の|野生の)?(.+?)の(.+?)([！!]?)$/); if (m && NSET().has(m[2]) && NSET().has(m[3])) { const pre = m[1] ? (m[1][0] === '相' ? (LI ? '对手的' : 'Foe ') : (LI ? '野生的' : 'Wild ')) : ''; return pre + (LI ? romaji(m[2]) + '的' + romaji(m[3]) : romaji(m[2]) + "'s " + romaji(m[3])) + m[4]; } }   // 「マギアの わざ」
    const dot = c.includes('・');
    for (const t of TPL) { if (dot && !t.dot) continue; const m = t.re.exec(c); if (m) return t.out.replace(/⟦(\d+)⟧/g, (_, n) => { const j = t.ord.indexOf(+n); return j >= 0 ? tr1(m[j + 1]) : ''; }); }
    { const m = c.match(/^([^：]{1,8})：(.+)$/); if (m && EX.has(m[1] + '：')) return EX.get(m[1] + '：') + core(m[2].trim()); if (m && EX.has(m[1])) return EX.get(m[1]) + (LI ? '：' : ': ') + core(m[2].trim()); }   // 「みだし：なかみ」
    if (c.includes('・')) return c.split('・').map(x => core(x.trim())).filter(x => x !== '').join(LI ? '、' : ', ');   // 「・」で ならべた ものは ひとつずつ
    if (MISS.size < 3000) MISS.add(c);   // 訳が ない 文（しらべる ため）
    r = c; for (const [n, ro] of names()) if (r.includes(n)) r = r.split(n).join(ro);
    if (!JPRE.test(r)) return r;
    for (const [k, v] of SUB) if (r.includes(k)) r = r.split(k).join(v);
    return r.replace(/[぀-ヿ]+/g, (w) => romaji(w));
  }
  function tr1(s) {
    if (!s || typeof s !== 'string' || !JPRE.test(s) || DONE.has(s)) return s;   // DONE：おきかえた あとの 文字（中国語の 漢字を もう いちど おきかえない）
    { const U = window.__noTr, k = s.trim(); if (U && U.size && U.has(k) && !EX.has(k) && !NSET().has(k)) return s; }   // 人が 書いた なまえ・チャットは そのまま（ゲームの ことば・マギア名・技名と おなじ ときは ふつうに 訳す）
    const hit = cache.get(s); if (hit !== undefined) return hit;
    const lead = s.match(/^\s*/)[0], tail = s.match(/\s*$/)[0], c = s.trim().replace(/[ \t　]+/g, ' ');
    const r = lead + c.split('\n').map(x => core(x.trim())).join('\n') + tail;
    if (cache.size > 8000) { cache.clear(); DONE.clear(); } cache.set(s, r); DONE.add(r); return r;
  }
  return tr1;
})();
if (LANG !== 'ja') {
  const JPRE = /[぀-ヿ一-鿿]/, ATTR = ['title', 'placeholder', 'aria-label', 'alt'];
  const doAttr = (n) => { for (const a of ATTR) { const v = n.getAttribute(a); if (v && JPRE.test(v)) { const t = tr(v); if (t !== v) n.setAttribute(a, t); } } if (n.tagName === 'INPUT' && (n.type === 'button' || n.type === 'submit') && JPRE.test(n.value)) { const t = tr(n.value); if (t !== n.value) n.value = t; } };   // かわる ときだけ かく（かかないと 変化の つうちが とまらない）
  const doNode = (n) => {
    if (n.nodeType === 3) { const v = n.nodeValue; if (v && JPRE.test(v)) { const p = n.parentNode; if (p && ((p.closest && p.closest('[data-notr]')) || p.tagName === 'SCRIPT' || p.tagName === 'STYLE' || p.tagName === 'TEXTAREA' || p.isContentEditable)) return; const t = tr(v); if (t !== v) n.nodeValue = t; } return; }
    if (n.nodeType !== 1 || (n.dataset && n.dataset.notr != null) || n.tagName === 'SCRIPT' || n.tagName === 'STYLE' || n.tagName === 'TEXTAREA' || n.isContentEditable) return;
    doAttr(n); for (const c of n.childNodes) doNode(c);
  };
  new MutationObserver((ms) => { for (const m of ms) { if (m.type === 'characterData') doNode(m.target); else if (m.type === 'attributes') { if (m.target.nodeType === 1) doAttr(m.target); } else for (const a of m.addedNodes) doNode(a); } })
    .observe(document.documentElement, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTR });
  doNode(document.documentElement); document.title = tr(document.title);
  const P = CanvasRenderingContext2D.prototype;
  for (const f of ['fillText', 'strokeText', 'measureText']) { const o = P[f]; P[f] = function (t, ...a) { return o.call(this, typeof t === 'string' ? tr(t) : t, ...a); }; }
  document.documentElement.lang = LANG === 'en' ? 'en' : 'zh-CN';
}
const setLang = (v) => { try { localStorage.setItem('pma_lang', v); } catch (e) { } location.reload(); };
// ====== ここまで I18N ======
