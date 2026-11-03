// 技の あたりやすさ テスト：ほんばんと おなじ うごき（あいては よける）で 撃って、あたった わりあいを はかる
// しくみ：movepower と おなじ 1たい1（オンラインの しくみ＝きまった 乱数）。ためす がわに ためす技＋ふつうの 技、あいては ふつうの 技。
//   あいての はやさを 3しゅるい（おそい・ふつう・はやい）に して、それぞれ n かい たたかわせる。
//   めいちゅう＝撃った 回数の うち、あいてに ダメージが はいった 回数（1回の なかで なんども あたっても 1）
//   訓練あり（ゲームの じどう訓練）で うごかす。ばしょは ランダムな ステージ
//   --stat：じょうたいいじょうの 技（まひの だん など）も はかる（あいてに とどいたら めいちゅう）
// つかいかた：node tools/hitrate/hitrate.js [--n 8] [--moves ice-beam,shadow-pin] [--stat] [--out tools/hitrate/out]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const STAT = process.argv.includes('--stat'), N = +arg('n', 8), OUT = path.resolve(arg('out', path.join(__dirname, 'out'))), ONLY = arg('moves', ''), SRC = arg('src', path.join(ROOT, 'index.html'));
const STEPS = 60 * 90, FIELDS = ['grass', 'fire', 'water', 'elec', 'ground', 'wind'];
const SPEEDS = { slow: .7, mid: 1, fast: 1.3 };
const SIM = `
window.PMA_HITSIM = (job) => {
  if (!S) S = defaultSave(); const mute0 = SND.opt.mute; SND.opt.mute = true;
  try {
    Object.assign(NET, { pending: null, done: { dg: 0, sw: 0, ch: 0 }, lastInp: '', nr: null, host: false, started: true });
    const iv = { hp: 20, atk: 20, def: 20, spa: 20, spd: 20, spe: 20, eva: 20 }, mk = () => ({ sid: job.sid, nat: 'reisei', iv, moves: ['tackle'] });
    startBattle({ kind: 'online', seed: job.seed >>> 0, field: FIELDS.includes(job.field) ? job.field : 'grass', enemies: monsFrom([mk()], job.seed), p0: monsFrom([mk()], job.seed), trainer: { name: '-', spr: trArt('boy') }, title: '-', intro: '-', skill: .5 });
    B.net = 'host'; B.replay = { log: [], i: 0 };
    const me = B.sides[0].fs[0], foe = B.sides[1].fs[0];
    me.moves = job.mine.slice(); foe.moves = job.foe.slice(); me.cd = {}; foe.cd = {};
    me.hp = me.maxHp = me.maxHp * 4; foe.hp = foe.maxHp = foe.maxHp * 4;   // ながく たたかって かずを ふやす
    foe.speStat = Math.round((foe.speStat || 70) * job.spe);
    B.train = true;
    for (const f of [me, foe]) { const e = { moves: f.moves.slice(), nat: f.mon.nat }; autoTrain(e); f.moves = e.moves.slice(); f.mon.tr = e.tr; }
    let uses = 0; const got = new Set();
    window.__use = (f, id) => { if (f === me && id === job.test) uses++; };
    window.__dmg = (att, def, m, d) => { if (att === me && def === foe && m && m.fxid === job.test && d > 0) got.add(uses); };
    window.__hit = (att, def, m) => { if (job.stat && att === me && def === foe && m && m.fxid === job.test) got.add(uses); };
    while (B.stepN < job.steps && B.mode !== 'end') bStep(FIX_DT);
    B = null; window.__hit = null; return { uses, hits: got.size };
  } finally { SND.opt.mute = mute0; window.__dmg = window.__use = null; }
};
`;
const HOOKS = [
  ['def.hp = Math.max(0, def.hp - dmg); def.hurtAt = B.t;', 'def.hp = Math.max(0, def.hp - dmg); def.hurtAt = B.t; if (window.__dmg) window.__dmg(att, def, m, dmg);'],
  ['function beginMove(f, id) {', 'function beginMove(f, id) { if (window.__use) window.__use(f, id);'],
  ['function hit(att, def, m, ang, opt) {', 'function hit(att, def, m, ang, opt) { if (window.__hit) window.__hit(att, def, m);'],
];
(async () => {
  let html = fs.readFileSync(SRC, 'utf8');
  const anchor = 'window.PMA_REPLAY = (job) => {'; if (!html.includes(anchor)) throw new Error('PMA_REPLAY が みつからない');
  html = html.replace(anchor, SIM + anchor);
  for (const [a, b] of HOOKS) { if (html.split(a).length !== 2) throw new Error('フックの ばしょが みつからない: ' + a); html = html.replace(a, b); }
  fs.mkdirSync(OUT, { recursive: true }); const tmp = path.join(ROOT, '.hitrate_tmp_' + process.pid + '.html'); fs.writeFileSync(tmp, html);
  const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  try {
    await p.goto('file://' + tmp); await p.waitForTimeout(1500);
    await p.evaluate((v) => { window.STAT = v; }, STAT);
    const info = await p.evaluate(() => { const M = window.__game.MOVES, X = window.__game.run(o => o);
      return Object.keys(M).filter(id => (M[id].power > 0 || M[id].pow > 0) || (STAT && M[id].cat === 'stat' && ['proj', 'beam', 'cone', 'strike', 'aoe', 'multi', 'swipe', 'dash'].includes(M[id].k))).map(id => ({ id, n: M[id].n, t: M[id].t, k: M[id].k, cat: M[id].cat || '', acc: M[id].acc, aim: M[id].aim || '', power: M[id].power || 0 })); });
    const ids = ONLY ? ONLY.split(',') : info.map(x => x.id).filter(id => !['tackle', 'slap-dash', 'swift', 'echoed-voice'].includes(id));
    const res = []; let i = 0;
    for (const id of ids) {
      const m = info.find(x => x.id === id); if (!m) continue;
      const kit = m.cat === 'spec' ? ['swift', 'echoed-voice'] : ['tackle', 'slap-dash'];
      const o = { ...m };
      let U = 0, H = 0;
      for (const [sk, spe] of Object.entries(SPEEDS)) {
        const r = await p.evaluate(([id, kit, n, spe, fields, steps]) => { let u = 0, h = 0; for (let i = 0; i < n; i++) { const x = window.PMA_HITSIM({ seed: 1000 + i * 7919, field: fields[i % fields.length], sid: 'a_fire5', mine: [id, ...kit], foe: kit, test: id, spe, steps, stat: window.__game.MOVES[id].cat === 'stat' }); u += x.uses; h += x.hits; } return [u, h]; }, [id, kit, N, spe, FIELDS, STEPS]);
        o[sk] = r[0] ? Math.round(r[1] / r[0] * 100) : null; o[sk + 'U'] = r[0]; U += r[0]; H += r[1];
      }
      o.rate = U ? Math.round(H / U * 100) : null; o.uses = U; res.push(o);
      if (++i % 20 === 0) console.log(i + '/' + ids.length);
    }
    res.sort((a, c) => (a.rate ?? 999) - (c.rate ?? 999));
    fs.writeFileSync(path.join(OUT, 'hitrate.json'), JSON.stringify({ meta: { n: N, steps: STEPS, speeds: SPEEDS, date: new Date().toISOString(), errors: errs.slice(0, 20) }, res }, null, 1));
    console.log('done', res.length, errs.length ? 'errors: ' + errs.slice(0, 3).join(' / ') : '');
  } finally { await b.close(); fs.unlinkSync(tmp); }
})();
