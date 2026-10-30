/* =====================================================================
   サーバーで きめる もの（クライアントの もうしでを そのまま 信じない）
   - matchStart  … へやの presence を サーバーが よんで「ほんとうに はじまった 試合」を きろく
   - matchReport … ふたりの けっかが あったら レート・せんせき・ギルドポイントを かきこむ
                   くいちがい は どちらにも つけない（flags に かぞえる）
   - matchSweep  … 10ぷん たっても かたほう だけ（とちゅうで ぬけた）：のこった ほうの もうしでで きめる
   - guildWin1   … ふつうの バトルの かち（+1）。かいすう に せいげん
   - claimDaily  … 日替わりの むりょう（サーバーの 日づけで 1日 1かい）
   ranks の r・w・l・h、gmembers の pts・tot・wk は ここ（管理者）だけが かける（firestore.rules）
   ===================================================================== */
'use strict';
const { onCall, HttpsError } = require('firebase-functions/v2/https');
const { onSchedule } = require('firebase-functions/v2/scheduler');
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
  const uid = uidOf(req), code = req.data && req.data.code;
  if (typeof code !== 'string' || !/^[A-Za-z0-9_-]{1,40}$/.test(code)) throw new HttpsError('invalid-argument', 'code');
  let m = null;
  for (let i = 0; i < 4 && !m; i++) {   // ホストの start が まだ とどいて いない ことが ある
    const snap = await admin.database().ref('rooms/' + L.cleanRoom('pma-' + code)).get();
    m = L.findMatch(snap.val(), code);
    if (!m) await sleep(800);
  }
  if (!m || (uid !== m.a && uid !== m.b)) throw new HttpsError('failed-precondition', 'no-match');
  const ref = fs.doc('matches/' + m.mid);
  await fs.runTransaction(async (tx) => {
    const d = await tx.get(ref);
    if (d.exists) { const v = d.data(); if (v.a !== m.a || v.b !== m.b) throw new HttpsError('failed-precondition', 'mismatch'); return; }
    tx.set(ref, { a: m.a, b: m.b, rk: m.rk, t0: Date.now(), rep: {}, open: true });
  });
  return { mid: m.mid, rk: m.rk };
});

// けっかを かきこむ（トランザクションの なか）
async function settle(tx, ref, v, out, extra = {}) {
  const now = Date.now(), win = out === 'a' ? v.a : out === 'b' ? v.b : null, lose = out === 'a' ? v.b : out === 'b' ? v.a : null;
  const rA = fs.doc('ranks/' + v.a), rB = fs.doc('ranks/' + v.b), gW = win ? fs.doc('gmembers/' + win) : null;
  const fA = fs.doc('flags/' + v.a), fB = fs.doc('flags/' + v.b);
  const [da, db, dg] = await Promise.all([tx.get(rA), tx.get(rB), gW ? tx.get(gW) : null]);
  if (v.rk && win) {
    const ka = da.exists ? da.data() : {}, kb = db.exists ? db.data() : {};
    const ra = typeof ka.r === 'number' ? ka.r : 1000, rb = typeof kb.r === 'number' ? kb.r : 1000;
    const na = L.elo(ra, rb, win === v.a ? 1 : 0), nb = L.elo(rb, ra, win === v.b ? 1 : 0);
    const put = (ref_, k, r0, r1, won) => tx.set(ref_, { r: r1, w: (k.w || 0) + (won ? 1 : 0), l: (k.l || 0) + (won ? 0 : 1), h: (Array.isArray(k.h) ? k.h : [r0]).concat(r1).slice(-30), t: now }, { merge: true });
    put(rA, ka, ra, na, win === v.a); put(rB, kb, rb, nb, win === v.b);
  }
  if (gW && dg && dg.exists && dg.data().gid) {
    const g = dg.data(), wk = L.weekNo(now);
    tx.set(gW, { wk, pts: (g.wk === wk ? g.pts || 0 : 0) + GUILD_ONLINE, tot: (g.tot || 0) + GUILD_ONLINE }, { merge: true });
  }
  if (out === 'dispute') for (const f of [fA, fB]) tx.set(f, { disp: FieldValue.increment(1), t: now }, { merge: true });
  tx.update(ref, { open: false, out, win: win || null, lose: lose || null, t1: now, ...extra });
}

exports.matchReport = onCall(async (req) => {
  const uid = uidOf(req), mid = req.data && req.data.mid, res = req.data && req.data.res;
  if (typeof mid !== 'string' || !/^[A-Za-z0-9_-]{1,120}$/.test(mid) || !L.RES.includes(res)) throw new HttpsError('invalid-argument', 'arg');
  const ref = fs.doc('matches/' + mid);
  return fs.runTransaction(async (tx) => {
    const d = await tx.get(ref); if (!d.exists) throw new HttpsError('not-found', 'match');
    const v = d.data(), side = uid === v.a ? 'a' : uid === v.b ? 'b' : null;
    if (!side) throw new HttpsError('permission-denied', 'member');
    if (!v.open) return { done: true, out: v.out, me: side };
    if (v.rep && v.rep[side]) return { done: false, me: side };   // 1かい だけ
    const rep = { ...(v.rep || {}), [side]: res }, out = L.decide(rep, false);
    if (!out) { tx.update(ref, { ['rep.' + side]: res }); return { done: false, me: side }; }
    await settle(tx, ref, { ...v, rep }, out, { ['rep.' + side]: res });
    return { done: true, out, me: side };
  });
});

exports.matchSweep = onSchedule('every 5 minutes', async () => {
  const q = await fs.collection('matches').where('open', '==', true).where('t0', '<', Date.now() - STALE).limit(200).get();
  for (const doc of q.docs) {
    await fs.runTransaction(async (tx) => {
      const d = await tx.get(doc.ref); if (!d.exists || !d.data().open) return;
      const v = d.data(), out = L.decide(v.rep, true);
      if (out === 'none') { tx.update(doc.ref, { open: false, out, t1: Date.now() }); return; }
      await settle(tx, doc.ref, v, out);
    }).catch((e) => console.warn('sweep', doc.id, e && e.message));
  }
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
