/* =====================================================================
   サーバーで きめる もの（クライアントの もうしでを そのまま 信じない）
   - matchStart  … へやの presence を サーバーが よんで「ほんとうに はじまった 試合」を きろく
   - matchReport … ふたりの けっかが あったら レート・せんせき・ギルドポイントを かきこむ
                   くいちがい は どちらにも つけない（flags に かぞえる）
   - matchLog / matchVerify … ホストの きろく（シード・チーム・そうさ）を うけとり、ゲームを サーバーで さいげん して ほんとうの かちまけを きめる
                   （どの 端末でも おなじ けいさんに なる ように ゲームを つくって ある）。ちがう ことを いった ほうは flags.cheat
   - matchSweep  … 10ぷん たっても きまらない：きろくが あれば それで、なければ のこった ほうの もうしでで きめる
   - guildWin1   … ふつうの バトルの かち（+1）。かいすう に せいげん
   - claimDaily  … 日替わりの むりょう（サーバーの 日づけで 1日 1かい）
   ranks の r・w・l・h、gmembers の pts・tot・wk は ここ（管理者）だけが かける（firestore.rules）
   ===================================================================== */
'use strict';
const { onCall, HttpsError } = require('firebase-functions/v2/https');
const { onSchedule } = require('firebase-functions/v2/scheduler');
const { onDocumentCreated } = require('firebase-functions/v2/firestore');
const { setGlobalOptions } = require('firebase-functions/v2');
const admin = require('firebase-admin');
const { FieldValue } = require('firebase-admin/firestore');
const L = require('./logic');

admin.initializeApp();
setGlobalOptions({ region: 'asia-northeast1', maxInstances: 10 });
const fs = admin.firestore();
const STALE = 10 * 60 * 1000;   // この あいだに もうしでが そろわなければ かたほう だけで きめる
const GUILD_ONLINE = 3, GUILD_OFFLINE = 1, OFF_GAP = 30 * 1000, OFF_DAY = 60;

const uidOf = (req) => { const u = req.auth && req.auth.uid; if (!u) throw new HttpsError('unauthenticated', 'login'); return u; };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

exports.matchStart = onCall(async (req) => {
  const uid = uidOf(req), code = req.data && req.data.code, team = req.data && req.data.team;
  if (typeof code !== 'string' || !/^[A-Za-z0-9_-]{1,40}$/.test(code)) throw new HttpsError('invalid-argument', 'code');
  let m = null;
  for (let i = 0; i < 4 && !m; i++) {   // ホストの start が まだ とどいて いない ことが ある
    const snap = await admin.database().ref('rooms/' + L.cleanRoom('pma-' + code)).get();
    m = L.findMatch(snap.val(), code);
    if (!m) await sleep(800);
  }
  if (!m || (uid !== m.a && uid !== m.b)) throw new HttpsError('failed-precondition', 'no-match');
  const gt = uid === m.b && Array.isArray(team) && team.length <= 3 && JSON.stringify(team).length < 20000 ? team : null;   // ゲストが うけとった じぶんの チーム（ホストの きろくと くらべる）
  const ref = fs.doc('matches/' + m.mid);
  await fs.runTransaction(async (tx) => {
    const d = await tx.get(ref);
    if (d.exists) { const v = d.data(); if (v.a !== m.a || v.b !== m.b) throw new HttpsError('failed-precondition', 'mismatch'); if (gt && !v.gt) tx.update(ref, { gt }); return; }
    tx.set(ref, { a: m.a, b: m.b, rk: m.rk, code, gk: m.gk, t0: Date.now(), rep: {}, open: true, ...(gt ? { gt } : {}) });
  });
  return { mid: m.mid, rk: m.rk };
});

// けっかを かきこむ（トランザクションの なか）。j：L.judge の かえり
async function settle(tx, ref, v, j, extra = {}) {
  const out = j.out, now = Date.now(), win = out === 'a' ? v.a : out === 'b' ? v.b : null, lose = out === 'a' ? v.b : out === 'b' ? v.a : null;
  const rA = fs.doc('ranks/' + v.a), rB = fs.doc('ranks/' + v.b), gW = win ? fs.doc('gmembers/' + win) : null;
  const fA = fs.doc('flags/' + v.a), fB = fs.doc('flags/' + v.b);
  const pair = fs.doc('pairs/' + [v.a, v.b].sort().join('_') + '_' + L.jstDay(now));   // おなじ ふたりの 試合（なれあい）：1日 3かい まで レートを うごかす
  const [da, db, dg, fa, fb, dp] = await Promise.all([tx.get(rA), tx.get(rB), gW ? tx.get(gW) : null, tx.get(fA), tx.get(fB), tx.get(pair)]);
  const banned = (fa.exists && fa.data().hide) || (fb.exists && fb.data().hide);   // ずるの うたがいが おおい 人との 試合は レート・ギルドに いれない
  const pn = dp.exists ? dp.data().n || 0 : 0, rated = v.rk && win && pn < PAIR_DAY && !banned;
  if (v.rk && win) tx.set(pair, { n: pn + 1, t: now }, { merge: true });
  if (rated) {
    const ka = da.exists ? da.data() : {}, kb = db.exists ? db.data() : {};
    const ra = typeof ka.r === 'number' ? ka.r : 1000, rb = typeof kb.r === 'number' ? kb.r : 1000;
    const na = L.elo(ra, rb, win === v.a ? 1 : 0), nb = L.elo(rb, ra, win === v.b ? 1 : 0);
    const put = (ref_, k, r0, r1, won) => tx.set(ref_, { r: r1, w: (k.w || 0) + (won ? 1 : 0), l: (k.l || 0) + (won ? 0 : 1), h: (Array.isArray(k.h) ? k.h : [r0]).concat(r1).slice(-30), t: now }, { merge: true });
    put(rA, ka, ra, na, win === v.a); put(rB, kb, rb, nb, win === v.b);
  }
  if (gW && dg && dg.exists && dg.data().gid && pn < PAIR_DAY && !banned) {
    const g = dg.data(), wk = L.weekNo(now);
    tx.set(gW, { wk, pts: (g.wk === wk ? g.pts || 0 : 0) + GUILD_ONLINE, tot: (g.tot || 0) + GUILD_ONLINE }, { merge: true });
  }
  // くいちがい・ずる の かず。おおい 人は ランキングに ださない（hide）
  for (const [side, f, d, rk] of [['a', fA, fa, rA], ['b', fB, fb, rB]]) {
    const o = d.exists ? d.data() : {}, n = (o.n || 0) + 1, disp = (o.disp || 0) + (out === 'dispute' ? 1 : 0), cheat = (o.cheat || 0) + (j.cheat && j.cheat[side] ? 1 : 0);
    const div = (o.div || 0) + (side === 'a' && v.rp && v.rp.div > 0 ? 1 : 0);   // ホストの がめんが サーバーの さいげんと ちがった（ゲームを いじった うたがい）
    const hide = cheat >= CHEAT_HIDE || div >= DIV_HIDE || (disp >= DISP_MIN && disp / n > DISP_RATE);
    tx.set(f, { n, disp, cheat, div, hide, t: now }, { merge: true });
    if (hide !== !!o.hide) tx.set(rk, { hide }, { merge: true });
  }
  tx.update(ref, { open: false, out, win: win || null, lose: lose || null, rated: !!rated, cheat: j.cheat || {}, t1: now, ...extra });
}
const PAIR_DAY = 3, CHEAT_HIDE = 2, DIV_HIDE = 3, DISP_MIN = 5, DISP_RATE = 0.3;

exports.matchReport = onCall(async (req) => {
  const uid = uidOf(req), mid = req.data && req.data.mid, res = req.data && req.data.res, inp = req.data && req.data.inp;
  if (typeof mid !== 'string' || !/^[A-Za-z0-9_-]{1,120}$/.test(mid) || !L.RES.includes(res)) throw new HttpsError('invalid-argument', 'arg');
  const gin = Array.isArray(inp) && inp.length <= 400 && inp.every((x) => typeof x === 'string' && x.length < 400) ? inp : null;   // ゲストが おくった そうさ
  const ref = fs.doc('matches/' + mid);
  return fs.runTransaction(async (tx) => {
    const d = await tx.get(ref); if (!d.exists) throw new HttpsError('not-found', 'match');
    const v = d.data(), side = uid === v.a ? 'a' : uid === v.b ? 'b' : null;
    if (!side) throw new HttpsError('permission-denied', 'member');
    if (!v.open) return { done: true, out: v.out, me: side };
    if (v.rep && v.rep[side]) return { done: false, me: side };   // 1かい だけ
    const rep = { ...(v.rep || {}), [side]: res }, extra = { ['rep.' + side]: res, ...(side === 'b' && gin ? { gin } : {}) };
    let rp = v.rp;
    if (side === 'b' && gin && rp && !rp.tamper) {   // さいげんの あとに ゲストの そうさが とどいた：ホストの きろくと くらべなおす
      const lg = await tx.get(fs.doc('matchlogs/' + mid)); let rec = null; try { rec = lg.exists ? JSON.parse(lg.data().js) : null; } catch (e) { rec = null; }
      const bad = rec && L.checkRec(v, rec, gin); if (bad) { rp = { tamper: bad }; extra.rp = rp; }
    }
    const j = L.judge({ ...v, rep, rp }, false);
    if (!j) { tx.update(ref, extra); return { done: false, me: side }; }
    await settle(tx, ref, { ...v, rep, rp }, j, extra);
    return { done: true, out: j.out, me: side };
  });
});

// ホスト：たたかいの きろく（シード・ばしょ・チーム・そうさ）。うけとったら matchlogs の トリガーで さいげん する
exports.matchLog = onCall(async (req) => {
  const uid = uidOf(req), mid = req.data && req.data.mid, rec = req.data && req.data.rec;
  if (typeof mid !== 'string' || !/^[A-Za-z0-9_-]{1,120}$/.test(mid) || !rec || typeof rec !== 'object') throw new HttpsError('invalid-argument', 'arg');
  const js = JSON.stringify(rec); if (js.length > 800000) throw new HttpsError('invalid-argument', 'size');
  const m = await fs.doc('matches/' + mid).get(); if (!m.exists) throw new HttpsError('not-found', 'match');
  if (m.data().a !== uid) throw new HttpsError('permission-denied', 'host');
  const ref = fs.doc('matchlogs/' + mid);
  await fs.runTransaction(async (tx) => { const d = await tx.get(ref); if (!d.exists) tx.set(ref, { js, t: Date.now() }); });
  return { ok: true };
});

// さいげん：ゲームを サーバーで うごかして ほんとうの けっかを だす
exports.matchVerify = onDocumentCreated({ document: 'matchlogs/{mid}', memory: '2GiB', timeoutSeconds: 180 }, async (ev) => {
  const mid = ev.params.mid, ref = fs.doc('matches/' + mid), d0 = await ref.get(); if (!d0.exists) return;
  const v0 = d0.data(); let rec = null; try { rec = JSON.parse(ev.data.data().js); } catch (e) { rec = null; }
  let rp;
  const bad = L.checkRec(v0, rec, v0.gin || null);
  if (bad) rp = { tamper: bad };
  else {
    try {
      const out = await require('./replay').replay({ seed: rec.seed, field: rec.field, h: rec.h, g: rec.g, log: rec.log, steps: rec.steps, glk: rec.glk, gnm: rec.gnm, tr: Array.isArray(rec.tr) ? rec.tr : null });
      if (out.ver !== rec.ver) rp = { end: 'ver', ver: out.ver, cver: rec.ver };   // ちがう バージョン：さいげん できない（ふたりの もうしで）
      else if (!out.hOk || !out.gOk) rp = { tamper: 'team' };
      else { const lx = rec.log.length && rec.log[rec.log.length - 1]; rp = { end: out.r.res ? (lx && lx[1] === 'x' && lx[0] >= out.r.n ? 'x' : 'ko') : 'none', res: out.r.res, n: out.r.n, hp: JSON.stringify(out.r.hp), div: out.r.div || 0 }; }
    } catch (e) { console.warn('replay', mid, e && e.message); rp = { end: 'err', err: String(e && e.message || e).slice(0, 200) }; }
  }
  await fs.runTransaction(async (tx) => {
    const d = await tx.get(ref); if (!d.exists) return; const v = { ...d.data(), rp };
    if (!v.open) { tx.update(ref, { rp }); return; }
    const j = L.judge(v, false); if (!j) { tx.update(ref, { rp }); return; }
    await settle(tx, ref, v, j, { rp });
  });
});

exports.matchSweep = onSchedule('every 5 minutes', async () => {
  const q = await fs.collection('matches').where('open', '==', true).where('t0', '<', Date.now() - STALE).limit(200).get();
  for (const doc of q.docs) await sweepOne(doc.ref).catch((e) => console.warn('sweep', doc.id, e && e.message));
});
async function sweepOne(ref) {
  return fs.runTransaction(async (tx) => {
    const d = await tx.get(ref); if (!d.exists || !d.data().open) return;
    const v = d.data(), j = L.judge(v, true);
    if (!j || j.out === 'none' || j.out === 'unverified') { tx.update(ref, { open: false, out: j ? j.out : 'none', t1: Date.now() }); return; }
    await settle(tx, ref, v, j);
  });
}

/* ---- セーブ：サーバーが もつ（saves/{uid}.js）。クライアントは よむ だけ ----
   saveGet：サーバーの セーブ（なければ クライアントの データを ありえる はんいに なおして つくる）
   act：クライアントで かえた ところ（わざ・訓練・ならび）を かさね、しごと（ショップ・ボックス・たたかいの けっか…）を
        ゲームの コードで うごかして ほぞん。おなじ シード・じこく を かえすので クライアントも おなじ けっかに なる */
const SAVE_MAX = 900000;
const loadSave = async (tx, ref) => { const d = await tx.get(ref); if (!d.exists) return null; try { return { s: JSON.parse(d.data().js), v: d.data().v || 0 }; } catch (e) { return null; } };
exports.saveGet = onCall({ memory: '2GiB', timeoutSeconds: 60 }, async (req) => {
  const uid = uidOf(req), ref = fs.doc('saves/' + uid), loc = req.data && req.data.loc;
  const d = await ref.get();
  if (d.exists) { try { return { s: JSON.parse(d.data().js), v: d.data().v || 0, now: Date.now() }; } catch (e) { /* こわれた：つくりなおす */ } }
  const s = await require('./replay').call('PMA_IMPORT', loc && typeof loc === 'object' ? loc : null);
  const js = JSON.stringify(s); if (js.length > SAVE_MAX) throw new HttpsError('resource-exhausted', 'size');
  await fs.runTransaction(async (tx) => { const x = await tx.get(ref); if (!x.exists) tx.set(ref, { js, v: 1, t: Date.now(), imp: 1 }); });
  const x = await ref.get(); return { s: JSON.parse(x.data().js), v: x.data().v || 1, now: Date.now() };
});
const ACT_NAMES = new Set(['sync', 'shopBuyDeal', 'shopBuyChest', 'shopBuySpecial', 'openChest', 'payOpen']);
exports.act = onCall({ memory: '2GiB', timeoutSeconds: 60 }, async (req) => {
  const uid = uidOf(req), name = req.data && req.data.name, args = (req.data && req.data.args) || [], loc = req.data && req.data.loc;
  if (!ACT_NAMES.has(name) || !Array.isArray(args) || JSON.stringify(args).length > 200000) throw new HttpsError('invalid-argument', 'act');
  const ref = fs.doc('saves/' + uid), P = require('./replay');
  for (let i = 0; i < 3; i++) {   // ほかの しごとと かさなったら やりなおす
    const d = await ref.get(); if (!d.exists) throw new HttpsError('failed-precondition', 'nosave');
    const v = d.data().v || 0, srv = JSON.parse(d.data().js);
    const pre = await P.call('PMA_MERGE', srv, loc && typeof loc === 'object' ? loc : null);
    const seed = (Math.random() * 4294967296) >>> 0, now = Date.now();
    const r = await P.call('PMA_ACT', pre, name, args, seed, now);
    if (r.err) return { err: r.err };
    const js = JSON.stringify(r.post); if (js.length > SAVE_MAX) throw new HttpsError('resource-exhausted', 'size');
    const ok = await fs.runTransaction(async (tx) => { const x = await tx.get(ref); if ((x.data().v || 0) !== v) return false; tx.set(ref, { js, v: v + 1, t: now }); return true; });
    if (ok) return { pre, seed, now, h: r.h, v: v + 1, out: r.out };
  }
  throw new HttpsError('aborted', 'busy');
});

exports.guildWin1 = onCall(async (req) => {
  const uid = uidOf(req), now = Date.now(), day = L.jstDay(now);
  const lim = fs.doc('limits/' + uid), gm = fs.doc('gmembers/' + uid);
  return fs.runTransaction(async (tx) => {
    const [dl, dg] = await Promise.all([tx.get(lim), tx.get(gm)]);
    if (!dg.exists || !dg.data().gid) return { ok: false, why: 'noguild' };
    const l = dl.exists ? dl.data() : {}, n = l.day === day ? l.n || 0 : 0;
    if (now - (l.last || 0) < OFF_GAP || n >= OFF_DAY) return { ok: false, why: 'limit' };
    const g = dg.data(), wk = L.weekNo(now), pts = (g.wk === wk ? g.pts || 0 : 0) + GUILD_OFFLINE;
    tx.set(gm, { wk, pts, tot: (g.tot || 0) + GUILD_OFFLINE }, { merge: true });
    tx.set(lim, { day, n: n + 1, last: now }, { merge: true });
    return { ok: true, pts };
  });
});

exports.claimDaily = onCall(async (req) => {
  const uid = uidOf(req), k = req.data && req.data.k;
  if (k !== 'free') throw new HttpsError('invalid-argument', 'k');
  const day = L.jstDay(Date.now()), ref = fs.doc('claims/' + uid);
  return fs.runTransaction(async (tx) => {
    const d = await tx.get(ref), v = d.exists ? d.data() : {};
    const got = v.day === day && Array.isArray(v.k) ? v.k : [];
    if (got.includes(k)) return { ok: false, day };
    tx.set(ref, { day, k: got.concat(k) });
    return { ok: true, day };
  });
});
