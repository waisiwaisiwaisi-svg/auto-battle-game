const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage(); await p.goto('file:///home/user/auto-battle-game/index.html'); await p.waitForTimeout(1200);
  const out = await p.evaluate(() => { const G = window.__game; return G.run(X => { const ids = X.poolIds(), res = [];
    for (const id of ids) { const sp = X.SPECIES[id], S = X.SPR[id]; if (!S) continue; const im = S.fr.idle0.n;
      const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0); const d = g.getImageData(0, 0, c.width, c.height).data;
      let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1; for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) if (d[(y * c.width + x) * 4 + 3] > 0) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
      const w = x1 - x0 + 1, h = y1 - y0 + 1, cc = document.createElement('canvas'); cc.width = w; cc.height = h; cc.getContext('2d').drawImage(c, x0, y0, w, h, 0, 0, w, h);
      res.push({ id, n: sp.n, t: [sp.type, sp.type2].filter(Boolean), ms: +S.ms.toFixed(4), w, h, img: cc.toDataURL(), cat: sp.sizeCat, dexH: sp.prof && sp.prof.h, rare: sp.rare ? 1 : 0 }); }
    return { mons: res, types: Object.fromEntries(Object.entries(X.TYPES).map(([k, v]) => [k, { n: v.n, c: v.c }])) }; }); });
  fs.writeFileSync(__dirname + '/sizes/mons.json', JSON.stringify(out)); console.log(out.mons.length, Math.round(JSON.stringify(out).length / 1024) + 'KB'); await b.close(); })();
