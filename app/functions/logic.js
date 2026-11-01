/* サーバーで きめる ことの けいさん（Firestore に さわらない ので テストしやすい） */
'use strict';

const K = 32;
// レート：ゲームと おなじ しきで うごかす（s：1 かち・0 まけ）
function elo(r, opp, s) {
  const exp = 1 / (1 + Math.pow(10, (opp - r) / 400));
  return Math.max(0, r + Math.round(K * (s - exp)));
}

// ふたりの もうしでから けっかを きめる。a＝ホスト・b＝ゲスト（どちらも じぶんから 見た けっか）
// かえす もの：'a'（ホストの かち）・'b'（ゲストの かち）・'draw'・'dispute'（くいちがい）・null（まだ）
const RES = ['win', 'lose', 'draw', 'dispute'];
function decide(rep, final) {
  const ra = rep && rep.a, rb = rep && rep.b;
  if (ra && rb) {
    if (ra === 'win' && rb === 'lose') return 'a';
    if (ra === 'lose' && rb === 'win') return 'b';
    if (ra === 'draw' && rb === 'draw') return 'draw';
    return 'dispute';
  }
  if (!final) return null;
  // じかんぎれ：かたほうしか もうして いない（あいては とちゅうで いなくなった）。その もうしでを つかう
  const one = ra ? ['a', ra] : rb ? ['b', rb] : null;
  if (!one) return 'none';
  const [side, r] = one, other = side === 'a' ? 'b' : 'a';
  return r === 'win' ? side : r === 'lose' ? other : r === 'draw' ? 'draw' : 'dispute';
}

// しゅうの ばんごう（ゲームと おなじ：げつようび はじまり）
const weekNo = (now) => Math.floor((now + 3 * 864e5) / 6048e5);
// 日本の 日づけ（日替わりの くぎり）
const jstDay = (now) => { const d = new Date(now + 9 * 36e5); return d.getUTCFullYear() * 10000 + (d.getUTCMonth() + 1) * 100 + d.getUTCDate(); };

// へやの 名前（クライアントの clean と おなじ）
const cleanRoom = (s) => String(s).replace(/[.#$\[\]\/]/g, '_').slice(0, 60) || 'lobby';

// へやの presence から この 試合を しらべる：ホストが start を だし、その gp の ゲストが いる
function findMatch(rows, code) {
  const list = Object.entries(rows || {}).map(([key, row]) => { let p = null; try { p = JSON.parse(row && row.p); } catch (e) { } return { key, by: row && row.by, p }; }).filter((x) => x.by && x.p && typeof x.p === 'object');
  // inb：ホストが いま たいせん して いる ゲストの キー（start は はじまると すぐ けす ので inb を つかう）
  const gpOf = (x) => (x.p.start && typeof x.p.start.gp === 'string' ? x.p.start.gp : typeof x.p.inb === 'string' ? x.p.inb : null);
  const host = list.find((x) => x.p.role === 'host' && gpOf(x));
  if (!host) return null;
  const guest = list.find((x) => x.key === gpOf(host) && x.p.role === 'guest');
  if (!guest || guest.by === host.by) return null;
  const mid = (cleanRoom('pma-' + code) + '_' + guest.key).replace(/[^A-Za-z0-9_-]/g, '_').slice(0, 120);
  return { mid, a: host.by, b: guest.by, rk: !!(host.p.rk && guest.p.rk), gk: guest.key };
}

// たたかいの シード（クライアントの seedOf と おなじ）：へや＋ゲストの キー から きまる
const seedOf = (str) => { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; };

// ホストの きろく を しらべる（さいげん の まえ）。だめなら 'tamper'
const monKey = (o) => o && JSON.stringify([o.sid, o.nat || null, ['hp', 'atk', 'def', 'spa', 'spd', 'spe', 'eva'].map((k) => (o.iv && o.iv[k]) | 0), [...(o.moves || [])].sort(), o.fed | 0, o.ev ? ['hp', 'atk', 'def', 'spa', 'spd', 'spe', 'eva'].map((k) => o.ev[k] | 0) : null]);
function checkRec(v, rec, gInp) {
  if (!rec || typeof rec !== 'object' || !Array.isArray(rec.h) || !Array.isArray(rec.g) || !Array.isArray(rec.log)) return 'shape';
  if ((rec.seed >>> 0) !== seedOf(v.code + '|' + v.gk)) return 'seed';   // シードは ホストが えらべない
  if (Array.isArray(v.gt) && v.gt.length && (rec.g.length !== v.gt.length || rec.g.some((o, i) => monKey(o) !== monKey(v.gt[i])))) return 'gteam';   // ゲストの チームを かえた
  if (Array.isArray(gInp)) { const sent = new Set(gInp); for (const e of rec.log) if (e && e[1] === 'g') { const j = JSON.stringify(e[2]); if (!sent.has(j)) return 'ginp'; } }   // ゲストが おくって いない そうさ
  return '';
}

// けっかを きめる：v（試合）・final（じかんぎれ）。かえす もの：{ out, cheat: { a, b } } か null（まつ）
//  - さいげん で ふつうに おわった（たおれた・タイムアップ）：それが ただしい。ちがう ことを いった ほうに cheat
//  - きろくを いじった：ホストに cheat・この 試合は なし
//  - さいげん で おわらなかった（とちゅうで ぬけた など）・きろく なし：ふたりの もうしで（きろく なしで ホスト だけ の ときは つけない）
function judge(v, final) {
  const rep = v.rep || {}, rp = v.rp;
  if (rp && rp.tamper) return { out: 'void', cheat: rp.tamper === 'gown' ? { b: true } : { a: true } };   // gown：ゲストが もって いない モンスター
  if (rp && rp.end === 'ko') {
    const out = rp.res === 'win' ? 'a' : rp.res === 'lose' ? 'b' : 'draw';
    const want = (side) => (out === 'draw' ? 'draw' : out === side ? 'win' : 'lose');
    return { out, cheat: { a: rep.a === 'win' && want('a') !== 'win', b: rep.b === 'win' && want('b') !== 'win' } };   // してない かちを いった ほう（あいてに だまされて まけと いった ほうは ちがう）
  }
  if (!rp && !final) return null;   // ホストの きろくを まつ
  const d = decide(rep, final); if (!d) return null;
  if (!rp && final && rep.a && !rep.b && d === 'a') return { out: 'unverified', cheat: {} };   // きろく なしで ホストが かちと いう だけ：つけない
  return { out: d, cheat: {} };
}

// チームの モンスターが その 人の サーバーの セーブに いるか（しゅるい・個体値・せいかく・きょうか が おなじ 子。1たい 1かい）
const ownKey = (o) => JSON.stringify([o.sid, o.nat || null, ['hp', 'atk', 'def', 'spa', 'spd', 'spe', 'eva'].map((k) => (o.iv && o.iv[k]) | 0), o.fed | 0, ['hp', 'atk', 'def', 'spa', 'spd', 'spe', 'eva'].map((k) => (o.ev && o.ev[k]) | 0)]);
function ownOk(team, save) {
  if (!save) return true;   // サーバーの セーブが まだ ない 人（ふるい アプリ）は みない
  const pool = new Map(); for (const m of [...(save.party || []), ...(save.box || [])]) { const k = ownKey(m); pool.set(k, (pool.get(k) || 0) + 1); }
  for (const o of team || []) { const k = ownKey(o), n = pool.get(k) || 0; if (!n) return false; pool.set(k, n - 1); }
  return true;
}

module.exports = { elo, decide, weekNo, jstDay, cleanRoom, findMatch, RES, seedOf, checkRec, judge, monKey, ownOk };
