// PC版の しるし（ゲームは window.PMA_DESKTOP で PC版 と わかる）＋ Steam の 実績・Steam Cloud の セーブ
const { contextBridge, ipcRenderer } = require('electron');

// ---- Steam Cloud：ゲームが よみこむ まえに、ファイルの ほうが あたらしければ localStorage に もどす ----
const TS_KEY = 'pma__cloud_ts', SKIP = new Set([TS_KEY, 'pma_dev']);   // pma_dev は この 端末の しるし（バックアップ用）：おくらない
const keys = () => { const o = []; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && k.startsWith('pma') && !SKIP.has(k)) o.push(k); } return o; };
try {
  const f = ipcRenderer.sendSync('pma-cloud-read'), mine = +localStorage.getItem(TS_KEY) || 0;
  if (f && f.ts > mine) {   // ほかの PC で あそんだ ぶんが あたらしい
    for (const k of keys()) if (!(k in f.data)) localStorage.removeItem(k);
    for (const k in f.data) if (k.startsWith('pma') && !SKIP.has(k) && typeof f.data[k] === 'string') localStorage.setItem(k, f.data[k]);
    localStorage.setItem(TS_KEY, String(f.ts));
  }
} catch (e) { }
let last = '';
const dump = () => {
  try { const d = {}; for (const k of keys().sort()) d[k] = localStorage.getItem(k); const s = JSON.stringify(d); if (s === last) return; last = s;
    const ts = Math.max(Date.now(), (+localStorage.getItem(TS_KEY) || 0) + 1); /* ほかの PC の とけいが すすんで いても まけない */ localStorage.setItem(TS_KEY, String(ts)); ipcRenderer.send('pma-cloud-write', { ts, data: d }); } catch (e) { }
};
window.addEventListener('DOMContentLoaded', () => { try { const d = {}; for (const k of keys().sort()) d[k] = localStorage.getItem(k); last = JSON.stringify(d); } catch (e) { } setInterval(dump, 5000); });   // いまの なかみを おぼえて、かわったら 5びょうごとに かく
window.addEventListener('pagehide', dump); window.addEventListener('beforeunload', dump);

const steam = (() => { try { return ipcRenderer.sendSync('pma-steam'); } catch (e) { return null; } })();
contextBridge.exposeInMainWorld('PMA_DESKTOP', {
  platform: process.platform,
  steam: !!steam,
  achv: (id) => { if (typeof id === 'string') ipcRenderer.send('pma-achv', id); },
});
