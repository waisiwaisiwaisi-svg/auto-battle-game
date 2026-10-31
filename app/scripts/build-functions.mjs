// サーバーで たたかいを さいげん する ための ゲームの ページを functions/game/ へ コピーする（firebase deploy の まえに じどうで うごく）
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { stampVer } from './game-ver.mjs';
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const { ver, html } = stampVer(fs.readFileSync(path.join(root, '..', 'index.html'), 'utf8'));
fs.mkdirSync(path.join(root, 'functions', 'game'), { recursive: true });
fs.writeFileSync(path.join(root, 'functions', 'game', 'index.html'), html);
console.log('functions/game/index.html を つくりました（GAME_VER ' + ver + '）');
