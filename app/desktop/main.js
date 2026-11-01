/* PC版（Steam）：ゲーム（app/www）を Electron の まどで うごかす
   - app:// で だす（ファイルの ばしょが かわっても セーブ・ログインが きえない おなじ オリジン）
   - F11：ぜんがめん、Alt+Enter でも。ゲームの そとの サイトは ふつうの ブラウザで ひらく
   - Steam には このまま の 実行ファイルを のせる（dist/ の なか） */
'use strict';
const { app, BrowserWindow, protocol, net, shell, Menu } = require('electron');
const path = require('path');
const url = require('url');

protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true, corsEnabled: true, stream: true } }]);
const WWW = app.isPackaged ? path.join(process.resourcesPath, 'www') : path.join(__dirname, '..', 'www');
const single = app.requestSingleInstanceLock();   // 2つ ひらくと セーブが まざる：1つだけ
if (!single) app.quit();

function createWindow() {
  const win = new BrowserWindow({
    width: 1280, height: 760, minWidth: 800, minHeight: 480, backgroundColor: '#141022', title: 'Pixel Monster Arena', autoHideMenuBar: true,
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false, sandbox: true, backgroundThrottling: false },
  });
  win.loadURL('app://game/index.html');
  win.webContents.setWindowOpenHandler(({ url: u }) => { if (/^https?:/.test(u)) shell.openExternal(u); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, u) => { if (!u.startsWith('app://')) { e.preventDefault(); if (/^https?:/.test(u)) shell.openExternal(u); } });
  win.webContents.on('before-input-event', (e, inp) => {
    if (inp.type === 'keyDown' && (inp.key === 'F11' || (inp.alt && inp.key === 'Enter'))) { win.setFullScreen(!win.isFullScreen()); e.preventDefault(); }
  });
  return win;
}

app.whenReady().then(() => {
  protocol.handle('app', (req) => {
    const p = decodeURIComponent(new URL(req.url).pathname).replace(/^\/+/, '');
    const file = path.normalize(path.join(WWW, p || 'index.html'));
    if (!file.startsWith(WWW)) return new Response('forbidden', { status: 403 });   // www の そとは よまない
    return net.fetch(url.pathToFileURL(file).toString());
  });
  Menu.setApplicationMenu(null);
  createWindow();
  app.on('second-instance', () => { const w = BrowserWindow.getAllWindows()[0]; if (w) { if (w.isMinimized()) w.restore(); w.focus(); } });
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});
app.on('window-all-closed', () => app.quit());
