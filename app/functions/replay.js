/* サーバーで たたかいを さいげん する：ゲームの ページ（game/index.html）を ヘッドレス Chromium で ひらいて PMA_REPLAY を よぶ
   ページは つかいまわす（ひらくのに すこし かかる）。PMA_REPLAY は どうき なので いっぺんに ひとつずつ うごく */
'use strict';
const path = require('path');
let pageP = null;
async function openPage() {
  const pptr = require('puppeteer-core');
  let exe = process.env.PMA_CHROME, args = ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'];
  if (!exe) { const ch = require('@sparticuz/chromium'); exe = await ch.executablePath(); args = ch.args; }
  const b = await pptr.launch({ executablePath: exe, args, headless: true });
  const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'game', 'index.html'), { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForFunction(() => window.PMA_REPLAY && window.PMA_CHECK, { timeout: 90000 });
  p.on('close', () => { pageP = null; }); b.on('disconnected', () => { pageP = null; });
  return p;
}
const page = () => (pageP = pageP || openPage().catch((e) => { pageP = null; throw e; }));
// job：{ seed, field, h, g, log, steps } → { ver, hOk, gOk, r: { res, n, hp, fa } }
async function replay(job) {
  const p = await page();
  return p.evaluate((j) => ({ ver: window.PMA_VER, hOk: window.PMA_CHECK(j.h), gOk: window.PMA_CHECK(j.g), r: window.PMA_REPLAY(j) }), job);
}
module.exports = { replay };
