const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, 'frames');   // つかいかた：node tools/promo/record.js → ffmpeg で mp4 に（README 参照） fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT, { recursive: true });
const FPS = 30; let fno = 0;
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(__dirname, '../../index.html') + ''); await p.waitForTimeout(1500);
  await p.addStyleTag({ content: `
    #tutBox{display:none!important}
    #pc{position:fixed;left:0;right:0;top:9%;z-index:9999;text-align:center;pointer-events:none;font-family:"DotGothic16",monospace}
    #pc .t{display:inline-block;padding:10px 18px;background:linear-gradient(180deg,rgba(20,16,34,.92),rgba(42,32,80,.92));border:3px solid #ffd166;border-radius:6px;color:#fff;font-size:24px;line-height:1.35;letter-spacing:.04em;text-shadow:2px 2px 0 #000;box-shadow:0 6px 0 rgba(0,0,0,.35)}
    #pc .t b{color:#ffd166}
    #pe{position:fixed;inset:0;z-index:9998;display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;background:radial-gradient(circle at 50% 38%,#3a2a78,#120e22 70%);font-family:"DotGothic16",monospace;color:#fff;text-align:center}
    #pe .l1{font-size:40px;color:#ffd166;text-shadow:3px 3px 0 #000;line-height:1.1}
    #pe .l2{font-size:20px;letter-spacing:.3em;text-shadow:2px 2px 0 #000}
    #pe .l3{font-size:18px;line-height:1.7;color:#cfe;text-shadow:2px 2px 0 #000}
    #pe .l4{margin-top:10px;font-size:30px;color:#fff;background:#e84a5f;padding:8px 22px;border-radius:6px;box-shadow:0 5px 0 #8a1a2a}
    #pe .mons{display:flex;gap:6px}` });
  await p.evaluate(() => { const c = document.createElement('div'); c.id = 'pc'; document.body.appendChild(c); const e = document.createElement('div'); e.id = 'pe'; document.body.appendChild(e); window.requestAnimationFrame = () => 0; });
  const cap = (html, k) => p.evaluate(([h, k]) => { const c = document.getElementById('pc'); c.innerHTML = h ? `<span class="t" style="transform:scale(${k});opacity:${Math.min(1, k)}">${h}</span>` : ''; }, [html, k == null ? 1 : k]);
  const snap = async () => { await p.screenshot({ path: path.join(OUT, String(fno++).padStart(5, '0') + '.png') }); };
  const pop = (i) => Math.min(1, .6 + i / 8 * .4);   // テロップが ぽんっと でる

  // 1) タイトル
  await p.evaluate(() => { window.__game.run(o => o).show('scTitle'); });
  for (let i = 0; i < FPS * 3; i++) { await cap(i > 8 ? 'ドット絵モンスターが<br><b>リアルタイム</b>で ぶつかりあう！' : '', pop(i - 8)); await snap(); }

  // 2) バトルの みどころ
  const clips = [
    { field: 'ice', sid: 'a_dragon5', move: 'draco-meteor', far: 210, cap: 'わざは <b>140しゅるい</b> いじょう！' },
    { field: 'grass', sid: 'yorukoumo', move: 'double-team', far: 200, react: 'ember', cap: '<b>かげぶんしん</b>で まどわせ！' },
    { field: 'water', sid: 'mizupuku', move: 'surf', far: 210, cap: '<b>おおなみ</b>で おしながせ！' },
    { field: 'fire', sid: 'gouen', move: 'close-combat', far: 170, cap: 'つかんで <b>5れんだ</b>！' },
    { field: 'elec', sid: 'happamogu', move: 'leaf-storm', far: 70, cap: '<b>このは</b>を まとって こうげき' },
    { field: 'ice', sid: 'a_dragon5', move: 'garyou', far: 240, charge: 1, cap: 'ためて はなつ <b>ひっさつビーム</b>' },
  ];
  for (const c of clips) {
    await p.evaluate((c) => {
      const G = window.__game, X = G.run(o => o); let sid = null; for (const k in G.LEARN) if (G.LEARN[k].some(x => x[1] === c.move) && (!sid || G.SPECIES[k].type === G.MOVES[c.move].t)) sid = k; G.newGame(sid || 'hinokon'); G.S.auto = true; G.S.round = 2; G.startCup(c.field);
      const B = G.B; let i = 0; while (B.mode !== 'fight' && i++ < 900) G.step(1 / 60);
      const f = B.sides[0].fs[B.sides[0].act], o = B.sides[1].fs[B.sides[1].act]; for (const x of [f, o]) { x.hp = x.maxHp = 9999; x.cur = null; x.state = 'free'; x.v = {}; }
      const cx = (B.st.fx0 + B.st.fx1) / 2, cy = (B.st.fy0 + B.st.fy1) / 2;
      for (let k = 0; k < 60; k++) { f.aiT = o.aiT = 999; f.x = cx - c.far / 2; o.x = cx + c.far / 2; f.y = o.y = cy; G.step(1 / 60); }
      for (const x of [f, o]) { x.hp = x.maxHp = 9999; for (const k in x.cd) x.cd[k] = 0; x.uses = {}; } f.moves[0] = c.move; f.cur = null; f.state = 'free';
      if (c.charge) f.v.charged = 1;
      X.beginMove(f, c.move); window.__clip = { f, o, c, n: 0 }; B.cam.x = (f.x + o.x) / 2; B.cam.y = (f.y + o.y) / 2 - 20;
    }, c);
    const N = Math.round(FPS * 2.6);
    for (let i = 0; i < N; i++) {
      await p.evaluate(() => { const G = window.__game, X = G.run(o => o), { f, o, c } = window.__clip; window.__clip.n++;
        for (let s = 0; s < 2; s++) { o.aiT = 999; o.dodgeCd = 99; f.aiT = 999; if (!f.cur) f.queued = null; G.step(1 / 60); }
        if (c.react && (window.__clip.n === 14 || window.__clip.n === 40) && o.state === 'free') { if (!o.moves.includes(c.react)) o.moves[0] = c.react; for (const k in o.cd) o.cd[k] = 0; X.beginMove(o, c.react); }
        const B = G.B; if (!window.__clip.z0) window.__clip.z0 = B.cam.z; B.cam.z = window.__clip.z0 * 1.9; B.cam.x += ((f.x + o.x) / 2 - B.cam.x) * .25; B.cam.y += ((f.y + o.y) / 2 - 20 - B.cam.y) * .25; X.render(); X.updHUD(); });
      await cap(c.cap, pop(i)); await snap();
    }
  }

  // 3) ずかん
  await p.evaluate(() => { const G = window.__game, X = G.run(o => o); G.S.dex = {}; for (const id in G.SPECIES) G.S.dex[id] = 2; X.renderDex(); X.show('scDex'); });
  const sc = await p.evaluate(() => { const el = document.querySelector('#dexGrid'); let e = el; while (e && e.scrollHeight <= e.clientHeight + 5) e = e.parentElement; return e ? (e.id || e.className || e.tagName) : null; });
  for (let i = 0; i < FPS * 2.6; i++) { await p.evaluate((i) => { let e = document.querySelector('#dexGrid'); while (e && e.scrollHeight <= e.clientHeight + 5) e = e.parentElement; if (e) e.scrollTop = i * 9; }, i); await cap('モンスターは <b>173しゅるい</b>！', pop(i)); await snap(); }

  // 4) さいごの カード
  await cap('');
  await p.evaluate(() => { const G = window.__game; G.run(o => o).show('scTitle'); const e = document.getElementById('pe'); e.style.display = 'flex';
    const ids = ['hinokon', 'mizupuku', 'happamogu', 'birikurage', 'gouen'].filter(id => G.SPECIES[id]);
    e.innerHTML = `<div class="l1">PIXEL MONSTER<br>ARENA</div><div class="l2">ピクセルモンスターアリーナ</div><div class="mons" id="pmons"></div><div class="l3">ランク対戦 ・ ギルド ・ ジムめぐり<br>オフラインでも あそべる！</div><div class="l4">近日 とうじょう！</div>`;
    const sc = G.run(o => o); const M = document.getElementById('pmons'); for (const id of ids) { const cv = document.querySelector('.dexc canvas'); void cv; }
    document.querySelectorAll('#dexGrid .dexc canvas').forEach((cv, i) => { if (i < 5) { const c2 = document.createElement('canvas'); c2.width = cv.width; c2.height = cv.height; c2.getContext('2d').drawImage(cv, 0, 0); c2.style.width = '64px'; c2.style.height = '64px'; c2.style.imageRendering = 'pixelated'; M.appendChild(c2); } }); });
  for (let i = 0; i < FPS * 3.5; i++) { await p.evaluate((i) => { const e = document.getElementById('pe'); e.style.opacity = Math.min(1, i / 10); const m = document.getElementById('pmons'); if (m) [...m.children].forEach((c, j) => c.style.transform = `translateY(${Math.round(Math.sin(i / 5 + j) * 4)}px)`); }, i); await snap(); }
  console.log('frames', fno, 'scroll', sc, errs.slice(0, 5)); await b.close();
})();
