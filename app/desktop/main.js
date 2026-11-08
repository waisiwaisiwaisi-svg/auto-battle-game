/* PC版（Steam）：ゲーム（app/www）を Electron の まどで うごかす
   - app:// で だす（ファイルの ばしょが かわっても セーブ・ログインが きえない おなじ オリジン）
   - F11：ぜんがめん、Alt+Enter でも。ゲームの そとの サイトは ふつうの ブラウザで ひらく
   - Steam には このまま の 実行ファイルを のせる（dist/ の なか）
   - Steam：steam.json の appId で つなぐ（Steam が うごいて いない ときは つながず ふつうに あそべる）。オーバーレイ（Shift+Tab）・実績
   - Steam Cloud：セーブ（localStorage の pma_*）を ファイル（appData/PixelMonsterArena/cloud/save.json）にも かく。Steam の Auto-Cloud で この ファイルを おくる */
'use strict';
const { app, BrowserWindow, protocol, net, shell, Menu, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');
const url = require('url');

protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true, corsEnabled: true, stream: true } }]);
const WWW = app.isPackaged ? path.join(process.resourcesPath, 'www') : path.join(__dirname, '..', 'www');
const single = app.requestSingleInstanceLock();   // 2つ ひらくと セーブが まざる：1つだけ
if (!single) app.quit();

// ---- Steam ----
const STEAM_ID = (() => { const e = +process.env.STEAM_APP_ID; if (e > 0) return e; try { return +JSON.parse(fs.readFileSync(path.join(__dirname, 'steam.json'), 'utf8')).appId || 0; } catch (e2) { return 0; } })();
let steam = null, steamLib = null;
try { steamLib = require('steamworks.js'); } catch (e) { steamLib = null; }
if (single && steamLib && STEAM_ID && app.isPackaged && STEAM_ID !== 480) { try { if (steamLib.restartAppIfNecessary(STEAM_ID)) app.exit(0); } catch (e) { } }   // Steam の そとから ひらいた：Steam から ひらきなおす
if (single && steamLib && STEAM_ID) { try { steam = steamLib.init(STEAM_ID); } catch (e) { steam = null; console.log('steam: not connected', e && e.message); } }
if (steam) try { steamLib.electronEnableSteamOverlay(); } catch (e) { }
ipcMain.on('pma-achv', (_, id) => { if (!steam || typeof id !== 'string' || !/^[A-Z0-9_]{1,40}$/.test(id)) return; try { if (!steam.achievement.isActivated(id)) steam.achievement.activate(id); } catch (e) { } });
ipcMain.on('pma-steam', (e) => { let v = null; try { if (steam) v = { appId: STEAM_ID, name: steam.localplayer.getName(), lang: steam.apps.currentGameLanguage() }; } catch (x) { } e.returnValue = v; });

// ---- Steam Cloud（セーブの ファイル）----
const CLOUD_DIR = path.join(app.getPath('appData'), 'PixelMonsterArena', 'cloud'), CLOUD_FILE = path.join(CLOUD_DIR, 'save.json');
ipcMain.on('pma-cloud-read', (e) => { try { const j = JSON.parse(fs.readFileSync(CLOUD_FILE, 'utf8')); e.returnValue = j && typeof j.ts === 'number' && j.data && typeof j.data === 'object' ? j : null; } catch (x) { e.returnValue = null; } });
ipcMain.on('pma-cloud-write', (_, j) => {
  if (!j || typeof j.ts !== 'number' || !j.data || typeof j.data !== 'object') return;
  try { fs.mkdirSync(CLOUD_DIR, { recursive: true }); const tmp = CLOUD_FILE + '.tmp'; fs.writeFileSync(tmp, JSON.stringify(j)); fs.renameSync(tmp, CLOUD_FILE); } catch (e) { }   // とちゅうで おちても こわれない：べつの ファイルに かいてから いれかえ
});

function createWindow() {
  const win = new BrowserWindow({
    width: 1280, height: 760, minWidth: 800, minHeight: 480, backgroundColor: '#141022', title: 'Magic Gear Arena', autoHideMenuBar: true,
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
