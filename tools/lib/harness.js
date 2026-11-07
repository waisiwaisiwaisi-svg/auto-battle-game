// 計測ツールの きょうつう：index.html に コード（inject）と フック（hooks）を さしこんで ヘッドレス Chromium で ひらく
//   いちじファイルは ブラウザの 起動に しっぱいしても かならず けす
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const ANCHOR = 'window.PMA_REPLAY = (job) => {';
const once = (html, a, b) => { const i = html.indexOf(a); if (i < 0 || html.indexOf(a, i + 1) >= 0) throw new Error('さしこむ ばしょが 1つに きまらない: ' + a); return html.slice(0, i) + b + html.slice(i + a.length); };   // replace の $ を つかわない
async function withGame({ src = path.join(ROOT, 'index.html'), inject = '', hooks = [], tag = 'tool', wait = 1500 }, fn) {
  let html = fs.readFileSync(src, 'utf8');
  html = once(html, ANCHOR, inject + ANCHOR);
  for (const [a, b] of hooks) html = once(html, a, b);
  const tmp = path.join(ROOT, `.${tag}_tmp_${process.pid}.html`); fs.writeFileSync(tmp, html);
  let b = null;
  try {
    b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + tmp); await p.waitForTimeout(wait);
    return await fn(p, errs);
  } finally { if (b) await b.close().catch(() => { }); try { fs.unlinkSync(tmp); } catch (e) { } }
}
module.exports = { withGame, ROOT };
