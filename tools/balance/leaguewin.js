// キングバトル・クルーの ヘッドの 勝ちやすさを 統計で はかる
//
// しくみ：ランダムに つくった プレイヤーの 手もち（6たい・強化ポイント FED・おまかせ訓練）を T くみ つくり、
//   ビッグフォー・キング・クルー6〜10の ヘッドと 1かいずつ たたかわせて 勝率と 95%信頼区間（ウィルソン）を だす。
//   --pick：ランダムな 18たいから ゲームの「へんせい」（sortPartyFor）で あいてに むいた 6たいを えらぶ（えらばない ときは ランダムの 6たい）
// つかいかた：node tools/balance/leaguewin.js [--t 200] [--fed 40] [--pick] [--out tools/balance/out]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const T = +arg('t', 200), FED = +arg('fed', 40), PICK = process.argv.includes('--pick'), OUT = path.resolve(arg('out', path.join(__dirname, 'out'))), SRC = arg('src', path.join(ROOT, 'index.html'));
const SIM = `
window.PMA_LW = (job) => {
  if (!S) S = defaultSave(); const mute0 = SND.opt.mute; SND.opt.mute = true; const keep = JSON.stringify(S); const p = SIM_RNG; SIM_RNG = mkRng(job.seed >>> 0);
  try {
    const J = jr(); J.rival = 1; J.badges = GYMS.map(g => g.f); J.gym = GYMS.length; J.champ = 0;
    const ids = poolIds(), mk = (sid, k) => { const m = fixMon({ uid: 7000 + k, sid }); m.fed = job.fed; const b = SPECIES[sid].base, main = (b.spa || 0) > b.atk ? 'spa' : 'atk'; m.ev = { [main]: Math.min(EV_STAT_MAX, Math.ceil(job.fed * .5)), hp: Math.floor(job.fed * .3), spe: Math.floor(job.fed * .2) }; const e = { moves: m.moves.slice(), nat: m.nat }; autoTrain(e); m.moves = e.moves.slice(); m.tr = e.tr; return m; };
    const cand = []; for (let i = 0; i < (job.pick ? 18 : 6); i++) cand.push(mk(ids[Math.floor(rnd() * ids.length)], i));
    const res = [];
    for (const o of job.opp) {
      let foes, type, field = 'grass';
      if (o[0] === 'l') { J.league = o[1]; foes = leagueFoes(o[1]); type = LEAGUE[o[1]][3]; field = leagueStage(o[1]); }
      else { J.gym = o[1]; J.step = 2; foes = journeyFoes(o[1], 2); type = GYMS[o[1]].t; field = GYMS[o[1]].st || GYMS[o[1]].f; J.gym = GYMS.length; }
      let team = cand.slice(0, 6);
      if (job.pick && type) { S.party = cand.slice(0, 6).map(m => JSON.parse(JSON.stringify(m))); S.box = cand.slice(6).map(m => JSON.parse(JSON.stringify(m))); sortPartyFor(type); team = S.party.slice(0, 6); }
      startBattle({ kind: 'cup', sim: true, seed: (job.seed * 31 + res.length) >>> 0, field: FIELDS.includes(field) ? field : 'grass', enemies: JSON.parse(JSON.stringify(foes)), p0: JSON.parse(JSON.stringify(team)), title: '-' });
      for (let s = 0; s < 60 * (MATCH_T + 20) && B.mode !== 'end'; s++) bStep(FIX_DT);
      res.push({ win: B.result === 'win' ? 1 : 0, left: B.sides[1].fs.filter(f => !f.fainted && f.hp > 0).length, n: B.sides[1].fs.length }); B = null;
    }
    return res;
  } finally { SIM_RNG = p; S = Object.assign(defaultSave(), JSON.parse(keep)); SND.opt.mute = mute0; }
};
`;
(async () => {
  let html = fs.readFileSync(SRC, 'utf8'); const anchor = 'window.PMA_REPLAY = (job) => {'; if (!html.includes(anchor)) throw new Error('PMA_REPLAY が みつからない');
  html = html.replace(anchor, SIM + anchor);
  fs.mkdirSync(OUT, { recursive: true }); const tmp = path.join(ROOT, '.movepower_tmp_' + process.pid + '.html'); fs.writeFileSync(tmp, html);
  const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  try {
    await p.goto('file://' + tmp); await p.waitForTimeout(1500);
    const opp = [['g', 5], ['g', 6], ['g', 7], ['g', 8], ['g', 9], ['l', 0], ['l', 1], ['l', 2], ['l', 3], ['l', 4]];
    const acc = opp.map(() => ({ w: 0, n: 0, left: 0 }));
    for (let t = 0; t < T; t++) { const r = await p.evaluate((job) => window.PMA_LW(job), { seed: 9001 + t * 101, fed: FED, pick: PICK, opp });
      r.forEach((x, i) => { acc[i].w += x.win; acc[i].n++; acc[i].left += x.left / x.n; }); if ((t + 1) % 20 === 0) console.log((t + 1) + '/' + T); }
    const wil = (w, n) => { const z = 1.96, ph = w / n, d = 1 + z * z / n, c = ph + z * z / (2 * n), s = z * Math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)); return [(c - s) / d, (c + s) / d]; };
    const label = (o) => o[0] === 'l' ? ['サトリ', 'ヨミ', 'ガイ', 'ツバキ', 'キング'][o[1]] : `クルー${o[1] + 1}ヘッド`;
    const res = opp.map((o, i) => { const a = acc[i], [lo, hi] = wil(a.w, a.n); return { who: label(o), win: Math.round(a.w / a.n * 1000) / 10, lo: Math.round(lo * 1000) / 10, hi: Math.round(hi * 1000) / 10, n: a.n, leftFoe: Math.round(a.left / a.n * 100) }; });
    fs.writeFileSync(path.join(OUT, `leaguewin_${PICK ? 'pick' : 'rand'}_fed${FED}.json`), JSON.stringify({ meta: { T, FED, PICK, errors: errs.slice(0, 10) }, res }, null, 1));
    for (const r of res) console.log(`${r.who}\t勝率 ${r.win}%（95%: ${r.lo}〜${r.hi}%）\tのこった あいて ${r.leftFoe}%`);
  } finally { await b.close(); fs.unlinkSync(tmp); }
})();
