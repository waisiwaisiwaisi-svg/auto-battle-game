// 技の強さを数値にする（わざの つよさ テスト）
//
// しくみ：おなじ モンスター どうしを 1たい1で なんども たたかわせる（ゲームの 中の たたかいと おなじ しくみ）。
//   2つの「型」で はかる：
//     物理型：こうげき 高め・とくこう 低め。もち技 [たいあたり, つきとばし]（あいても 物理型）
//     属性型：とくこう 高め・こうげき 低め。もち技 [スピードスター, エコーボイス]（あいても 属性型）
//   ためす がわ だけ、もち技に ためす技を 1つ たす。
//   つよさ点＝（たした ときの「じぶんの のこりHP% − あいての のこりHP%」の へいきん − たさない ときの へいきん）× 100
//   → のうりょくアップ・ダウンの ねうちは 型で かわる（こうげきアップは 物理型で、あいての とくこうダウンは 属性型で 点が でる）
// あわせて はかる もの：
//   1回あたりの ダメージ（実際に あたった ぶん。はずれ・よけ・れんぞくヒット・うちつづけ も こみ）
//   実威力：1回あたりの ダメージを「威力100・はずれない 1ぱつ」と くらべた 数（ふつうの 威力と おなじ ものさし）
//   足きり：その ダメージで、全モンスターの なんわりを 1回・2回で たおせるか、まんなかの モンスターを なん回で たおせるか（確定数）
// こうへいに する ため：ためす がわの タイプは ためす技と おなじ（タイプ一致は いつも 1.5ばい）、あいては どの タイプにも ふつう。
//
// 訓練：--train both（きほん）で「訓練なし」と「訓練あり」を りょうほう はかる。訓練ありは、りょうほうに ゲームの じどう訓練（トレーナーの あいてと おなじ：
//   近接・突進・前方を きる 技は 近づいてから、まっすぐ 飛ぶ 技は 離れてから、じゅんび技は 出場時、かいふくは HPが へってから など）を つける。
//   点・実威力などは 訓練なしが score / real …、訓練ありが scoreT / realT …。gain＝訓練で のびた 点。
// つかいかた：node tools/movepower/movepower.js [--n 24] [--train both|none|on] [--moves ember,surf] [--out tools/movepower/out]
//   → out/movepower.json と out/movepower.html（表）
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const N = +arg('n', 24), OUT = path.resolve(arg('out', path.join(__dirname, 'out'))), ONLY = arg('moves', '');
const TRAIN = arg('train', 'both');   // none：訓練なし だけ・on：訓練あり だけ・both：りょうほう
const MODES = TRAIN === 'none' ? [[false, '']] : TRAIN === 'on' ? [[true, 'T']] : [[false, ''], [true, 'T']];
const SID = arg('sid', 'a_fire5'), NAT = 'reisei', FIELDS = ['grass', 'fire', 'water', 'elec'], STEPS = 60 * 120;
const STYLES = {
  phys: { n: '物理型', kit: ['tackle', 'slap-dash'], atk: 1.25, spa: .75 },
  spec: { n: '属性型', kit: ['swift', 'echoed-voice'], atk: .75, spa: 1.25 },
};

// ゲームの ページに ためしの たたかいを たす（ゲームの ファイルは かえない。コピーに いれる）
const SIM = `
window.PMA_MOVESIM = (job) => {
  if (!S) S = defaultSave(); const mute0 = SND.opt.mute; SND.opt.mute = true;
  try {
    Object.assign(NET, { pending: null, done: { dg: 0, sw: 0, ch: 0 }, lastInp: '', nr: null, host: false, started: true });
    const iv = { hp: 20, atk: 20, def: 20, spa: 20, spd: 20, spe: 20, eva: 20 }, mk = () => ({ sid: job.sid, nat: job.nat, iv, moves: ['tackle'] });
    startBattle({ kind: 'online', seed: job.seed >>> 0, field: job.field, enemies: monsFrom([mk()], job.seed), p0: monsFrom([mk()], job.seed), trainer: { name: '-', spr: trArt('boy') }, title: '-', intro: '-', skill: .5 });
    B.net = 'host'; B.replay = { log: [], i: 0 };
    const set = (f, moves, type, st) => { f.moves = moves.slice(); f.cd = {}; f.sp = Object.assign({}, f.sp, { type, type2: null });
      const a = (f.atk + f.spa) / 2, d = Math.round((f.def + f.sdef) / 2); f.atk = Math.round(a * st.atk); f.spa = Math.round(a * st.spa); f.def = f.sdef = d; };
    const me = B.sides[0].fs[0], foe = B.sides[1].fs[0];
    set(me, job.mine, job.type, job.st); set(foe, job.foe, 'zz_none', job.st);
    B.train = !!job.train;
    if (job.train) for (const f of [me, foe]) { const e = { moves: f.moves.slice(), nat: f.mon.nat }; autoTrain(e); f.moves = e.moves.slice(); f.mon.tr = e.tr; }   // 訓練あり：ゲームの じどう訓練（トレーナーと おなじ）
    const tm = MOVES[job.test]; let unit = 0;
    if (tm) { const ref = { pow: 20, power: 100, k: 'dash', cat: tm.cat === 'spec' ? 'spec' : 'phys', t: job.type, e: {} }; unit = estDmg(me, foe, ref) / 100; }   // 威力1ぶんの ダメージ（はずれない 1ぱつ）
    let dmg = 0, uses = 0; const hpF0 = foe.maxHp, D0 = tm && tm.cat === 'spec' ? foe.sdef : foe.def;
    window.__dmg = (att, def, m, d) => { if (att === me && def === foe && m && m.fxid === job.test) dmg += d; };
    window.__use = (f, id) => { if (f === me && id === job.test) uses++; };
    while (B.stepN < job.steps && B.mode !== 'end') bStep(FIX_DT);
    window.__dmg = window.__use = null;
    const hp = (f) => f.fainted ? 0 : Math.max(0, f.hp) / f.maxHp;
    const r = { d: hp(me) - hp(foe), win: B.mode === 'end' ? (B.result === 'win' ? 1 : B.result === 'lose' ? 0 : .5) : (hp(me) > hp(foe) ? 1 : hp(me) < hp(foe) ? 0 : .5), t: B.stepN / 60, dmg, uses, unit, hp0: hpF0, D0 };
    B = null; return r;
  } finally { SND.opt.mute = mute0; window.__dmg = window.__use = null; }
};
// 全モンスターの HP・ぼうぎょ・とくぼう（足きりの けいさん）
window.PMA_MONSTATS = () => Object.keys(SPECIES).map(sid => { const f = mkFighter(fixMon({ uid: 0, sid, nat: 'reisei', iv: { hp: 20, atk: 20, def: 20, spa: 20, spd: 20, spe: 20, eva: 20 }, moves: ['tackle'] }), 1); return { sid, hp: f.maxHp, def: f.def, sdef: f.sdef }; });
`;
const HOOKS = [
  ['def.hp = Math.max(0, def.hp - dmg); def.hurtAt = B.t;', 'def.hp = Math.max(0, def.hp - dmg); def.hurtAt = B.t; if (window.__dmg) window.__dmg(att, def, m, dmg);'],
  ['function beginMove(f, id) {', 'function beginMove(f, id) { if (window.__use) window.__use(f, id);'],
];

(async () => {
  let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const anchor = 'window.PMA_REPLAY = (job) => {'; if (!html.includes(anchor)) throw new Error('PMA_REPLAY が みつからない');
  html = html.replace(anchor, SIM + anchor);
  for (const [a, b] of HOOKS) { if (html.split(a).length !== 2) throw new Error('フックの ばしょが みつからない: ' + a); html = html.replace(a, b); }
  fs.mkdirSync(OUT, { recursive: true }); const tmp = path.join(ROOT, '.movepower_tmp.html'); fs.writeFileSync(tmp, html);
  const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  try {
    await p.goto('file://' + tmp); await p.waitForTimeout(1500);
    const info = await p.evaluate(() => { const G = window.__game, M = G.MOVES, X = G.run(o => o);
      return Object.keys(M).map(id => ({ id, n: M[id].n, t: M[id].t, k: M[id].k, cat: M[id].cat || '', power: M[id].power || Math.round((M[id].pow || 0) * 5), desc: X.moveDesc(M[id]) })); });
    const mons = await p.evaluate(() => window.PMA_MONSTATS());
    const kits = Object.values(STYLES).flatMap(s => s.kit);
    const ids = ONLY ? ONLY.split(',') : info.map(x => x.id).filter(id => !kits.includes(id));
    const run = (st, mine, type, test, train) => p.evaluate(([st, mine, type, test, n, sid, nat, fields, steps, train]) => {
      const out = []; for (let i = 0; i < n; i++) out.push(window.PMA_MOVESIM({ seed: 1000 + i * 7919, field: fields[i % fields.length], sid, nat, mine, foe: st.kit, type, steps, st, test, train })); return out;
    }, [st, mine, type, test, N, SID, NAT, FIELDS, STEPS, train]);
    const avg = (a, f) => a.reduce((s, x) => s + f(x), 0) / a.length, r1 = (v) => Math.round(v * 10) / 10;
    const baseBy = {}; const base = async (k, type, tr) => baseBy[k + type + tr] || (baseBy[k + type + tr] = await run(STYLES[k], STYLES[k].kit, type, '', tr));
    const res = []; let i = 0;
    for (const id of ids) {
      const m = info.find(x => x.id === id); if (!m) continue;
      const o = { ...m };
      for (const [tr, sfx] of MODES) for (const k0 of Object.keys(STYLES)) {
        const k = k0 + sfx, r = await run(STYLES[k0], [id, ...STYLES[k0].kit], m.t, id, tr), b0 = await base(k0, m.t, tr);
        o[k] = r1((avg(r, x => x.d) - avg(b0, x => x.d)) * 100); o[k + 'Win'] = Math.round(avg(r, x => x.win) * 100);
        const uses = r.reduce((s, x) => s + x.uses, 0), dmg = r.reduce((s, x) => s + x.dmg, 0), time = r.reduce((s, x) => s + x.t, 0);
        o[k + 'Uses'] = r1(uses / time * 60);   // 1分あたり なんかい つかったか
        if (m.cat !== 'stat' && uses) {
          const per = dmg / uses, unit = r[0].unit, hp0 = r[0].hp0, D0 = r[0].D0;
          o[k + 'Per'] = r1(per / hp0 * 100);   // 1回で あいての HPの なん%
          o[k + 'Real'] = unit ? Math.round(per / unit) : 0;   // 実威力
          const key = m.cat === 'spec' ? 'sdef' : 'def', ko = (n) => Math.round(mons.filter(x => per * n * (D0 / x[key]) >= x.hp).length / mons.length * 100);
          o[k + 'KO1'] = ko(1); o[k + 'KO2'] = ko(2);   // 足きり：1回・2回で たおせる モンスターの わりあい
          const hits = mons.map(x => Math.ceil(x.hp / Math.max(.01, per * (D0 / x[key])))).sort((p, q) => p - q); o[k + 'Hits'] = per / hp0 < .01 ? 0 : hits[hits.length >> 1];   // 確定数（まんなかの モンスターを なん回で たおせるか）
        }
      }
      // 総合：その技に むいた 型の 点（物理技は 物理型、属性技は 属性型、ほじょ技は よい ほう）
      for (const [, sfx] of MODES) {
        const fit = m.cat === 'phys' ? 'phys' : m.cat === 'spec' ? 'spec' : (o['phys' + sfx] >= o['spec' + sfx] ? 'phys' : 'spec'), F = fit + sfx;
        Object.assign(o, { ['fit' + sfx]: fit, ['score' + sfx]: o[F], ['real' + sfx]: o[F + 'Real'] || 0, ['per' + sfx]: o[F + 'Per'] || 0, ['ko1' + sfx]: o[F + 'KO1'] || 0, ['ko2' + sfx]: o[F + 'KO2'] || 0, ['hits' + sfx]: o[F + 'Hits'] || 0, ['uses' + sfx]: o[F + 'Uses'] });
      }
      if (o.scoreT != null) o.gain = r1(o.scoreT - o.score);   // 訓練で どれだけ のびるか
      res.push(o);
      if (++i % 20 === 0) console.log(i + '/' + ids.length);
    }
    res.sort((a, c) => c.score - a.score);
    const meta = { train: TRAIN, n: N, sid: SID, nat: NAT, fields: FIELDS, steps: STEPS, styles: STYLES, mons: mons.length, date: new Date().toISOString(), errors: errs.slice(0, 20) };
    fs.writeFileSync(path.join(OUT, 'movepower.json'), JSON.stringify({ meta, res }, null, 1));
    console.log('done', res.length, 'moves', errs.length ? 'errors: ' + errs.slice(0, 3).join(' / ') : '');
  } finally { await b.close(); fs.unlinkSync(tmp); }
})();
