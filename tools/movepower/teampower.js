// 技の強さを 実戦で はかる（チーム テスト）
//
// しくみ：ゲームに 出てくる ほんものの 相手チーム（クルーの サモナー・ヘッド、ビッグフォー・キング。技も 訓練も ゲームの まま）と 3たい3で たたかう。
//   ためす がわ：その 技を おぼえられる ほんものの モンスター 3たい。ふだんの 技の いちばん よわい 1つを ためす 技に かえる（技あり）。
//   くらべる がわ：おなじ 3たいで ふだんの 技の まま（技なし）。おなじ 相手・おなじ 乱数で たたかわせて さを みる。
//   撃ち方：どちらも ゲームの おまかせ訓練（autoTrain）。
//   つよさ点＝（技ありの「じぶんの のこりHP% − あいての のこりHP%」の へいきん − 技なしの へいきん）× 100
//   かち：技ありの 勝率 と 技なしの 勝率
// つかいかた：node tools/movepower/teampower.js [--n 24] [--seed 0（かえると べつの 乱数・べつの 3たい）] [--moves ember,surf] [--shard 1/3] [--out tools/movepower/out]
//   → out/teampower(_1of3).json
const { withGame } = require('../lib/harness');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const SEED = +arg('seed', 0), N = +arg('n', 24), OUT = path.resolve(arg('out', path.join(__dirname, 'out'))), ONLY = arg('moves', ''), SHARD = arg('shard', ''), SRC = arg('src', path.join(ROOT, 'index.html'));

const SIM = `
window.PMA_TEAM_FOES = (n, seed) => {   // あいての チームを n こ つくる（クルー 4〜10 の サモナー・ヘッド、ビッグフォー・キング）
  if (!S) S = defaultSave(); const p = SIM_RNG; SIM_RNG = mkRng(seed >>> 0); const out = [];
  try { const J = jr(); const keep = JSON.stringify(J);
    const slots = []; for (let gi = 3; gi < GYMS.length; gi++) for (let st = 0; st < 3; st++) slots.push(['g', gi, st]); for (let k = 0; k < LEAGUE.length; k++) slots.push(['l', k]);
    for (let i = 0; i < n; i++) { const s = slots[i % slots.length];
      let T; if (s[0] === 'g') { J.gym = s[1]; J.step = s[2]; T = journeyFoes(s[1], s[2]); } else { J.gym = GYMS.length; J.badges = GYMS.map(g => g.f); J.league = s[1]; T = leagueFoes(s[1]); }
      const t3 = T.slice(0, 3).map(e => JSON.parse(JSON.stringify(e)));
      out.push({ tag: s.join(':'), team: t3, field: s[0] === 'g' ? (GYMS[s[1]].st || GYMS[s[1]].f) : 'grass' }); }
    Object.assign(J, JSON.parse(keep));
  } finally { SIM_RNG = p; } return out; };
window.PMA_TEAM_MINE = (id, seed) => {   // ためす 3たい：その 技を おぼえられる モンスター
  if (!S) S = defaultSave(); const p = SIM_RNG; SIM_RNG = mkRng(seed >>> 0);
  try { const L = poolIds().filter(sid => canLearn(sid, id)); if (!L.length) return null;
    const pick = []; for (let i = 0; i < 3; i++) pick.push(L[Math.floor(i * L.length / 3 + (seed % 7) * L.length / 21) % L.length]);
    const mk = (sid, k) => { const m = fixMon({ uid: 9000 + k, sid, nat: 'reisei', iv: { hp: 20, atk: 20, def: 20, spa: 20, spd: 20, spe: 20, eva: 20 } }); m.fed = 30; m.ev = { hp: 10, atk: 10, def: 0, spa: 10, spd: 0, spe: 0, eva: 0 }; return m; };
    const base = pick.map((sid, k) => { const m = mk(sid, k); if (m.moves.includes(id)) m.moves = m.moves.map(x => x === id ? 'tackle' : x); return m; });
    const test = base.map(m => { const t = JSON.parse(JSON.stringify(m)); const pw = (x) => (MOVES[x] && (MOVES[x].power || MOVES[x].pow * 5)) || 0; let w = 0; t.moves.forEach((x, i) => { if (pw(x) < pw(t.moves[w])) w = i; }); if (t.moves.length < 4) t.moves.push(id); else t.moves[w] = id; return t; });
    for (const m of [...base, ...test]) { const e = { moves: m.moves.slice(), nat: m.nat }; autoTrain(e); m.moves = e.moves.slice(); m.tr = e.tr; }
    return { sids: pick, base, test };
  } finally { SIM_RNG = p; } };
window.PMA_TEAM_FIGHT = (job) => {   // 1しあい（ゲームの シミュレーションと おなじ：ヘッドレス・訓練どおり・たおれたら じどうで つぎ）
  if (!S) S = defaultSave(); const mute0 = SND.opt.mute; SND.opt.mute = true; const train0 = S.train; S.train = true;
  try { startBattle({ kind: 'cup', sim: true, seed: job.seed >>> 0, field: FIELDS.includes(job.field) ? job.field : 'grass', enemies: JSON.parse(JSON.stringify(job.foes)), p0: JSON.parse(JSON.stringify(job.mine)), title: '-' });
    let used = 0; window.__use = (f, id) => { if (f.side === 0 && id === job.test) used++; };
    for (let s = 0; s < 60 * (MATCH_T + 20) && B.mode !== 'end'; s++) bStep(FIX_DT);
    const hp = (sd) => sd.fs.reduce((a, f) => a + (f.fainted ? 0 : Math.max(0, f.hp) / f.maxHp), 0) / sd.fs.length;
    const r = { d: hp(B.sides[0]) - hp(B.sides[1]), win: B.result === 'win' ? 1 : B.result === 'lose' ? 0 : .5, t: Math.round(B.fightT || B.t), used };
    B = null; return r;
  } finally { window.__use = null; SND.opt.mute = mute0; S.train = train0; }
};
`;
const HOOKS = [['function beginMove(f, id) {', 'function beginMove(f, id) { if (window.__use) window.__use(f, id);']];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  await withGame({ src: SRC, inject: SIM, hooks: HOOKS, tag: 'teampower' }, async (p, errs) => {
    const info = await p.evaluate(() => { const M = window.__game.MOVES; return Object.keys(M).map(id => ({ id, n: M[id].n, t: M[id].t, k: M[id].k, cat: M[id].cat || '', power: M[id].power || Math.round((M[id].pow || 0) * 5) })); });
    let ids = ONLY ? ONLY.split(',') : info.filter(m => m.cat !== 'stat' && m.power > 0).map(m => m.id);
    if (SHARD) { const [a, n] = SHARD.split('/').map(Number); ids = ids.filter((_, i) => i % n === a - 1); }
    const foes = await p.evaluate(([n, s]) => window.PMA_TEAM_FOES(n, 4242 + s * 101), [N, SEED]);
    const res = []; let i = 0;
    for (const id of ids) {
      const m = info.find(x => x.id === id); if (!m) continue;
      const r = await p.evaluate(([id, foes, sd]) => { const T = window.PMA_TEAM_MINE(id, 77 + sd); if (!T) return null; const out = { sids: T.sids, a: [], b: [] };
        foes.forEach((F, k) => { const seed = 1000 + k * 7919 + sd * 31337; out.a.push(window.PMA_TEAM_FIGHT({ seed, field: F.field, foes: F.team, mine: T.test, test: id })); out.b.push(window.PMA_TEAM_FIGHT({ seed, field: F.field, foes: F.team, mine: T.base, test: id })); });
        return out; }, [id, foes, SEED]);
      if (!r) { res.push({ ...m, skip: 'おぼえる モンスター なし' }); continue; }
      const avg = (a, f) => a.reduce((s, x) => s + f(x), 0) / a.length, r1 = (v) => Math.round(v * 10) / 10;
      const time = r.a.reduce((s, x) => s + x.t, 0) || 1;
      res.push({ ...m, sids: r.sids, score: r1((avg(r.a, x => x.d) - avg(r.b, x => x.d)) * 100), win: Math.round(avg(r.a, x => x.win) * 100), win0: Math.round(avg(r.b, x => x.win) * 100), uses: r1(r.a.reduce((s, x) => s + x.used, 0) / time * 60 / 3) });
      if (++i % 10 === 0) console.log(i + '/' + ids.length);
    }
    res.sort((a, c) => (c.score ?? -1e9) - (a.score ?? -1e9));
    fs.writeFileSync(path.join(OUT, SHARD ? 'teampower_' + SHARD.replace('/', 'of') + '.json' : 'teampower.json'), JSON.stringify({ meta: { n: N, foes: foes.map(f => f.tag), date: new Date().toISOString(), errors: errs.slice(0, 20) }, res }, null, 1));
    console.log('done', res.length, errs.length ? 'errors: ' + errs.slice(0, 3).join(' / ') : '');
  });
})();
