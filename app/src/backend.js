/* =====================================================================
   アプリ版の オンライン：claude.ai の window.claude.use('db' | 'user' | 'room') と
   おなじ 形を Firebase で つくる。ゲーム本体（index.html）は そのまま うごく。
   - db   … Cloud Firestore（ranks / guilds / gmembers / gchat / profiles / teams）
   - user … 匿名ログイン（id）と profiles/{uid}.name（なまえ）
   - room … Realtime Database（rooms/{へや}/{peer} に presence を おく。きれたら きえる）
   設定は www/firebase-config.js の window.PMA_FIREBASE_CONFIG。なければ オフライン。
   ===================================================================== */
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged, connectAuthEmulator, deleteUser } from 'firebase/auth';
import {
  getFirestore, connectFirestoreEmulator, doc as fsDoc, collection as fsCol, getDoc, getDocs, setDoc, updateDoc,
  deleteDoc, query as fsQuery, where, orderBy, limit as fsLimit, onSnapshot, documentId,
} from 'firebase/firestore';
import {
  getDatabase, connectDatabaseEmulator, ref, set as rtSet, remove as rtRemove, onValue, onDisconnect, serverTimestamp,
} from 'firebase/database';

const cfg = window.PMA_FIREBASE_CONFIG;
const ok = cfg && cfg.apiKey && !/^YOUR_/.test(cfg.apiKey);
window.PMA_APP = { native: true, online: !!ok };

if (ok) {
  const app = initializeApp(cfg);
  const auth = getAuth(app), fs = getFirestore(app), rt = getDatabase(app);
  const emu = window.PMA_FIREBASE_EMULATOR;   // テスト用：{ host: '127.0.0.1' }
  if (emu) {
    connectAuthEmulator(auth, `http://${emu.host}:9099`, { disableWarnings: true });
    connectFirestoreEmulator(fs, emu.host, 8080);
    connectDatabaseEmulator(rt, emu.host, 9000);
  }
  // ---- ログイン（匿名）。はじめての ときだけ アカウントが できる ----
  const login = () => new Promise((res) => {
    let done = false;
    const off = onAuthStateChanged(auth, (u) => { if (u && !done) { done = true; off(); res(u); } });
    (auth.currentUser ? Promise.resolve() : signInAnonymously(auth)).catch((e) => { console.warn('auth', e); if (!done) { done = true; res(null); } });
  });
  let ready = login();

  // ---- db：Firestore を claude の db と おなじ 形で ----
  const snapOf = (s) => ({ id: s.id, exists: s.exists(), data: () => s.data() });
  const qsOf = (q) => { const docs = q.docs.map(snapOf); return { docs, size: docs.length, empty: !docs.length }; };
  const docApi = (path) => {
    const r = fsDoc(fs, path);
    return {
      id: r.id,
      get: async () => snapOf(await getDoc(r)),
      set: (d) => setDoc(r, d),
      update: (d) => updateDoc(r, d),
      delete: () => deleteDoc(r),
      onSnapshot: (next, err) => onSnapshot(r, (s) => next(snapOf(s)), err),
    };
  };
  const queryApi = (path, cons = []) => {
    const build = () => fsQuery(fsCol(fs, path), ...cons);
    return {
      where: (f, op, v) => queryApi(path, cons.concat(where(f === '__name__' ? documentId() : f, op, v))),
      orderBy: (f, dir) => queryApi(path, cons.concat(orderBy(f, dir))),
      limit: (n) => queryApi(path, cons.concat(fsLimit(n))),
      get: async () => qsOf(await getDocs(build())),
      onSnapshot: (next, err) => onSnapshot(build(), (q) => next(qsOf(q)), err),
      doc: (id) => docApi(path + '/' + id),
    };
  };
  const db = { doc: (p) => docApi(p), collection: (p) => queryApi(p) };

  // ---- user：id と なまえ ----
  const NAME_KEY = 'pma_name';
  const user = {
    id: async () => { const u = await ready; return u ? u.uid : null; },
    profiles: async (ids) => {
      const out = {}, list = [...new Set([].concat(ids || []))].filter(Boolean);
      for (let i = 0; i < list.length; i += 30) {   // in は 30こ まで
        const part = list.slice(i, i + 30);
        try { const q = await getDocs(fsQuery(fsCol(fs, 'profiles'), where(documentId(), 'in', part))); q.docs.forEach((d) => { out[d.id] = { name: String(d.data().name || '').slice(0, 12) }; }); } catch (e) { }
      }
      return out;
    },
    canEdit: async () => false,
  };
  // なまえ：ゲームの せってい から かえる
  window.PMA_NAME = {
    get: () => { try { return localStorage.getItem(NAME_KEY) || ''; } catch (e) { return ''; } },
    set: async (name) => {
      name = String(name || '').replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, 12);
      if (!name) return false;
      try { localStorage.setItem(NAME_KEY, name); } catch (e) { }
      const u = await ready; if (!u) return false;
      await setDoc(fsDoc(fs, 'profiles/' + u.uid), { name, t: Date.now() });
      return true;
    },
    // オンラインの データを ぜんぶ けす（ストアの「アカウント削除」）
    wipe: async () => {
      const u = await ready; if (!u) return;
      for (const c of ['ranks', 'gmembers', 'gchat', 'guilds', 'profiles', 'teams']) { try { await deleteDoc(fsDoc(fs, `${c}/${u.uid}`)); } catch (e) { } }
      try { await deleteUser(u); } catch (e) { try { await auth.signOut(); } catch (x) { } }
      try { localStorage.removeItem(NAME_KEY); } catch (e) { }
      lobby = null; ready = login(); ready.then(nameDefault);
    },
  };
  const nameDefault = (u) => {   // なまえが まだ なければ てきとうに つける（あとで かえられる）
    if (!u) return;
    let n = window.PMA_NAME.get();
    if (!n) { n = 'トレーナー' + u.uid.slice(-4).toUpperCase(); }
    window.PMA_NAME.set(n).catch(() => { });
  };
  ready.then(nameDefault);

  let lobby = null;
  // ---- room：Realtime Database で presence を わけあう ----
  const myTab = Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
  const clean = (s) => String(s).replace(/[.#$\[\]\/]/g, '_').slice(0, 60) || 'lobby';
  function makeRoom(name) {
    let me = {}, peersSnap = Object.freeze([]), joinedOnce = false, dead = false;
    const handlers = new Set(), peerObj = new Map(), roomRef = ref(rt, 'rooms/' + clean(name));
    let myRef = null, unsubVal = null, sendT = null, lastSent = 0;
    const start = (async () => {
      const u = await ready; if (!u) throw { code: 'unavailable' };
      myRef = ref(rt, `rooms/${clean(name)}/${myTab}`);
      await onDisconnect(myRef).remove();
      unsubVal = onValue(roomRef, (s) => {
        const v = s.val() || {}, now = Date.now(), prev = peerObj, next = new Map();
        const joined = [], updated = [], left = [];
        for (const [peer, row] of Object.entries(v)) {
          if (!row || typeof row !== 'object') continue;
          const pj = row.p || '{}', old = prev.get(peer);
          if (old && old._pj === pj) { next.set(peer, old); continue; }
          let presence = {}; try { presence = JSON.parse(pj) || {}; } catch (e) { }
          const p = Object.freeze({ peer, by: row.by || null, isMe: row.by === u.uid, sameTab: peer === myTab, kind: 'viewer', guest: false, presence: Object.freeze(presence), updatedAt: now, _pj: pj });
          next.set(peer, p); (old ? updated : joined).push(p);
        }
        for (const [peer, p] of prev) if (!next.has(peer)) left.push(p);
        peerObj.clear(); for (const [k, p] of next) peerObj.set(k, p);
        peersSnap = Object.freeze([...next.values()]);
        if (!joined.length && !updated.length && !left.length && joinedOnce) return;
        joinedOnce = true;
        const ch = { peers: peersSnap, joined, left, updated };
        for (const h of handlers) { try { h.fn(ch); } catch (e) { console.error(e); } }
      }, (e) => { for (const h of handlers) if (h.err) { try { h.err({ code: 'unavailable', message: String(e && e.message || e) }); } catch (x) { } } });
    })();
    start.catch((e) => console.warn('room', name, e && (e.code || e.message) || e));
    const flush = async () => {
      sendT = null; if (dead) return; await start; lastSent = Date.now();
      await rtSet(myRef, { by: (await ready).uid, p: JSON.stringify(me), t: serverTimestamp() });
    };
    return {
      presence: async (patch) => {
        const m = { ...me };
        for (const [k, v] of Object.entries(patch || {})) { if (v === null) delete m[k]; else m[k] = v; }
        if (new Blob([JSON.stringify(m)]).size > 4096) throw { code: 'invalid_argument', message: 'presence は 4KB まで' };
        me = m;
        // 1びょうに 15かい まで まとめて おくる（バトルの スナップショットは ひんぱん）
        if (!sendT) { const wait = Math.max(0, 66 - (Date.now() - lastSent)); sendT = setTimeout(() => flush().catch(() => { }), wait); }
      },
      peers: () => peersSnap,
      onPeers: (fn, err) => {
        const h = { fn, err }; handlers.add(h);
        start.then(() => { if (joinedOnce && handlers.has(h)) setTimeout(() => handlers.has(h) && fn({ peers: peersSnap, joined: peersSnap, left: [], updated: [] }), 0); })
          .catch((e) => err && err({ code: 'unavailable', message: 'offline' }));
        return () => handlers.delete(h);
      },
      emit: async () => { },
      on: () => () => { },
      connected: () => !dead,
      leave: () => { dead = true; handlers.clear(); if (unsubVal) unsubVal(); if (sendT) clearTimeout(sendT); if (myRef) rtRemove(myRef).catch(() => { }); },
    };
  }
  const room = {
    join: async (name) => makeRoom(name),
  };
  // ロビー（だれでも いる へや）は room そのもの でも つかえる
  const lobbyApi = () => (lobby = lobby || makeRoom('lobby'));
  for (const k of ['presence', 'peers', 'onPeers', 'emit', 'on', 'connected']) room[k] = (...a) => lobbyApi()[k](...a);

  window.claude = window.claude || {};
  window.claude.use = async (cap) => {
    const u = await ready; if (!u) return null;
    return cap === 'db' ? db : cap === 'user' ? user : cap === 'room' ? room : null;
  };
}

/* ---- Android の もどるボタン：とじる → もどる → ホームでは アプリを しまう ---- */
import { App as CapApp } from '@capacitor/app';
import { Capacitor } from '@capacitor/core';
if (Capacitor.isNativePlatform()) {
  CapApp.addListener('backButton', () => {
    const vis = (el) => el && !el.hidden && el.offsetParent !== null;
    const modal = [...document.querySelectorAll('.askbg')].pop();
    if (modal) { const no = modal.querySelector('.btn.sub, #oClose, #nClose, #muX, #dClose') || modal.querySelector('button'); if (no) no.click(); else modal.remove(); return; }
    const scr = [...document.querySelectorAll('.screen')].find((s) => !s.hidden);
    if (scr && scr.id === 'scBattle') { const p = document.getElementById('btnPause'); if (vis(p)) p.click(); return; }
    if (scr && scr.id !== 'scHub' && scr.id !== 'scTitle') { const back = scr.querySelector('.sec-title .btn.sub'); if (vis(back)) { back.click(); return; } const home = document.getElementById('tabHome'); if (vis(home)) { home.click(); return; } }
    CapApp.minimizeApp();
  });
}
