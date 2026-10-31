// 技の強さを数値にする（わざの つよさ テスト）
//
// しくみ：おなじ モンスター どうしを 1たい1で なんども たたかわせる。
//   ためす がわ：[ためす技, たいあたり, スピードスター]   あいて：[たいあたり, スピードスター]
//   くらべる もと：ためす がわも [たいあたり, スピードスター]（あいてと おなじ）
//   1しあいの けっか＝（じぶんの のこりHP% − あいての のこりHP%）。−1〜+1
//   つよさ点＝（ためす技を もった ときの へいきん − くらべる もとの へいきん）× 100
//   ＝ その技を 1つ たすと、1たい1の しあいが どれだけ ゆうりに なるか（0＝たしても かわらない）。
//   ほじょ技（のうりょくアップ・まもる など）も、ほかの 2つの こうげきを たすける ぶんが 点に なる。
// こうへいに する ため：
//   - ためす がわの タイプは ためす技と おなじ（タイプ一致は いつも 1.5ばい）
//   - あいての タイプは どの タイプにも ふつう（こうかばつぐん・いまひとつ なし）
//   - こうげき と とくこう、ぼうぎょ と とくぼう を おなじ 数に（物理・属性で ふこうへいに ならない）
//   - 戦いの みためは うごかさない（ゲームの 中の たたかいと おなじ しくみを そのまま つかう）
//
// つかいかた：node tools/movepower/movepower.js [--n 12] [--moves ember,surf] [--out tools/movepower/out]
//   → out/movepower.json と out/movepower.html（表）
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const N = +arg('n', 12), OUT = path.resolve(arg('out', path.join(__dirname, 'out'))), ONLY = arg('moves', '');
const SID = arg('sid', 'a_fire5'), NAT = 'reisei', FIELDS = ['grass', 'fire', 'water', 'elec'], STEPS = 60 * 120;
const KIT = ['tackle', 'swift'], BASE_MINE = KIT, FOE = KIT;

// ゲームの ページに ためしの たたかいを 1つ たす（ゲームの ファイルは かえない。コピーに いれる）
const SIM = `
window.PMA_MOVESIM = (job) => {
  if (!S) S = defaultSave(); const mute0 = SND.opt.mute; SND.opt.mute = true;
  try {
    Object.assign(NET, { pending: null, done: { dg: 0, sw: 0, ch: 0 }, lastInp: '', nr: null, host: false, started: true });
    const iv = { hp: 20, atk: 20, def: 20, spa: 20, spd: 20, spe: 20, eva: 20 }, mk = () => ({ sid: job.sid, nat: job.nat, iv, moves: ['tackle'] });
    startBattle({ kind: 'online', seed: job.seed >>> 0, field: job.field, enemies: monsFrom([mk()], job.seed), p0: monsFrom([mk()], job.seed), trainer: { name: '-', spr: trArt('boy') }, title: '-', intro: '-', skill: .5 });
    B.net = 'host'; B.replay = { log: [], i: 0 };
    const set = (f, moves, type) => { f.moves = moves.slice(); f.cd = {}; f.sp = Object.assign({}, f.sp, { type, type2: null });
      const a = Math.round((f.atk + f.spa) / 2), d = Math.round((f.def + f.sdef) / 2); f.atk = f.spa = a; f.def = f.sdef = d; };
    for (const f of B.sides[0].fs) set(f, job.mine, job.type);
    for (const f of B.sides[1].fs) set(f, job.foe, 'zz_none');   // どの タイプにも ふつう
    while (B.stepN < job.steps && B.mode !== 'end') bStep(FIX_DT);
    const a = B.sides[0].fs[0], b = B.sides[1].fs[0], hp = (f) => f.fainted ? 0 : Math.max(0, f.hp) / f.maxHp;
    const r = { d: hp(a) - hp(b), win: B.mode === 'end' ? (B.result === 'win' ? 1 : B.result === 'lose' ? 0 : .5) : (hp(a) > hp(b) ? 1 : hp(a) < hp(b) ? 0 : .5), t: B.stepN / 60 };
    B = null; return r;
  } finally { SND.opt.mute = mute0; }
};
`;

(async () => {
  let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const anchor = 'window.PMA_REPLAY = (job) => {'; if (!html.includes(anchor)) throw new Error('PMA_REPLAY が みつからない');
  html = html.replace(anchor, SIM + anchor);
  fs.mkdirSync(OUT, { recursive: true }); const tmp = path.join(ROOT, '.movepower_tmp.html'); fs.writeFileSync(tmp, html);
  const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  try {
    await p.goto('file://' + tmp); await p.waitForTimeout(1500);
    const info = await p.evaluate(() => { const G = window.__game, M = G.MOVES, X = G.run(o => o);
      return Object.keys(M).map(id => ({ id, n: M[id].n, t: M[id].t, k: M[id].k, cat: M[id].cat || '', desc: X.moveDesc(M[id]) })); });
    const ids = ONLY ? ONLY.split(',') : info.map(x => x.id).filter(id => !KIT.includes(id));
    const run = (mine, type) => p.evaluate(([mine, type, n, sid, nat, fields, steps, foe]) => {
      const out = []; for (let i = 0; i < n; i++) out.push(window.PMA_MOVESIM({ seed: 1000 + i * 7919, field: fields[i % fields.length], sid, nat, mine, foe, type, steps })); return out;
    }, [mine, type, N, SID, NAT, FIELDS, STEPS, FOE]);
    const avg = (a, k) => a.reduce((s, x) => s + x[k], 0) / a.length;
    // くらべる もと（たいあたり・スピードスター）は タイプ ごとに（タイプ一致が かわるので）
    const baseBy = {};
    const base = async (type) => baseBy[type] || (baseBy[type] = await run(BASE_MINE, type));
    const res = []; let i = 0;
    for (const id of ids) {
      const m = info.find(x => x.id === id); if (!m) continue;
      const r = await run([id, ...KIT], m.t), b0 = await base(m.t);
      res.push({ ...m, score: Math.round((avg(r, 'd') - avg(b0, 'd')) * 1000) / 10, win: Math.round(avg(r, 'win') * 100), t: Math.round(avg(r, 't')) });
      if (++i % 20 === 0) console.log(i + '/' + ids.length);
    }
    res.sort((a, c) => c.score - a.score);
    const meta = { n: N, sid: SID, nat: NAT, fields: FIELDS, steps: STEPS, foe: FOE, date: new Date().toISOString(), errors: errs.slice(0, 20) };
    fs.writeFileSync(path.join(OUT, 'movepower.json'), JSON.stringify({ meta, res }, null, 1));
    fs.writeFileSync(path.join(OUT, 'movepower.html'), page(meta, res));
    console.log('done', res.length, 'moves', errs.length ? 'errors: ' + errs.slice(0, 3).join(' / ') : '');
  } finally { await b.close(); fs.unlinkSync(tmp); }
})();

function page(meta, res) {
  const T = { fire: '火', water: '水', grass: '草', wind: '風', ground: '土', elec: '雷', normal: '無', machine: '機械', bug: '虫', ghost: '霊', demi: '亜人', fairy: '妖精', dragon: '竜', beast: '獣' };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const rows = res.map((r, i) => `<tr><td>${i + 1}</td><td><b>${esc(r.n)}</b></td><td>${T[r.t] || r.t}</td><td>${esc(r.k)}</td><td class="n ${r.score >= 0 ? 'p' : 'm'}">${r.score > 0 ? '+' : ''}${r.score}</td><td class="n">${r.win}%</td><td class="n">${r.t}秒</td><td class="d">${esc(r.desc)}</td></tr>`).join('');
  return `<!doctype html><meta charset="utf-8"><title>技の強さ</title><style>body{font:14px system-ui,sans-serif;margin:16px}table{border-collapse:collapse}td,th{border-bottom:1px solid #ddd;padding:3px 8px;text-align:left}.n{text-align:right;font-variant-numeric:tabular-nums}.p{color:#0a7}.m{color:#c33}.d{color:#666;font-size:12px}</style>
<h1>技の強さ</h1><p>1たい1で ${meta.n}しあいずつ。つよさ点＝その技を たいあたり・スピードスターに たすと、たさない ときより どれだけ ゆうりか（のこりHPの さ ×100）。</p>
<table><tr><th>#</th><th>技</th><th>タイプ</th><th>かたち</th><th>つよさ点</th><th>勝率</th><th>しあい時間</th><th>効果</th></tr>${rows}</table>`;
}
