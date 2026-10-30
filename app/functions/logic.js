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
  return { mid, a: host.by, b: guest.by, rk: !!(host.p.rk && guest.p.rk) };
}

module.exports = { elo, decide, weekNo, jstDay, cleanRoom, findMatch, RES };
