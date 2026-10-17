// ../index.html を アプリ用に www/ へ コピーする。
// - Google Fonts → 同梱フォント（オフラインでも おなじ みため）
// - Firebase の つなぎ（backend.js）を バンドルして ゲームより さきに よみこむ
import { build } from 'esbuild';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const www = path.join(root, 'www');
fs.mkdirSync(path.join(www, 'fonts'), { recursive: true });

// フォント
const fdir = path.join(root, 'node_modules/@fontsource/dotgothic16/files');
// fontsource の CSS（unicode-range つき）を そのまま つかう。woff2 だけ コピー
for (const f of fs.readdirSync(fdir).filter((f) => f.endsWith('-400-normal.woff2'))) fs.copyFileSync(path.join(fdir, f), path.join(www, 'fonts', f));
const css = fs.readFileSync(path.join(root, 'node_modules/@fontsource/dotgothic16/400.css'), 'utf8')
  .replace(/url\(\.\/files\/([^)]+\.woff2)\) format\('woff2'\),\s*url\([^)]+\) format\('woff'\)/g, "url($1) format('woff2')");
fs.writeFileSync(path.join(www, 'fonts/fonts.css'), css);

// Firebase の つなぎ
await build({ entryPoints: [path.join(root, 'src/backend.js')], bundle: true, minify: true, format: 'iife', target: ['es2020', 'safari15'], outfile: path.join(www, 'backend.js'), logLevel: 'warning' });
const cfgSrc = path.join(root, 'firebase-config.js');
fs.copyFileSync(fs.existsSync(cfgSrc) ? cfgSrc : path.join(root, 'firebase-config.example.js'), path.join(www, 'firebase-config.js'));

// ステージの きょく（mp3）
fs.mkdirSync(path.join(www, 'music'), { recursive: true });
for (const f of fs.readdirSync(path.join(root, '..', 'music')).filter((f) => f.endsWith('.mp3'))) fs.copyFileSync(path.join(root, '..', 'music', f), path.join(www, 'music', f));
fs.mkdirSync(path.join(www, 'se8bit'), { recursive: true });   // 効果音
for (const f of fs.readdirSync(path.join(root, '..', 'se8bit')).filter((f) => f.endsWith('.wav'))) fs.copyFileSync(path.join(root, '..', 'se8bit', f), path.join(www, 'se8bit', f));

// ゲーム本体
let html = fs.readFileSync(path.join(root, '..', 'index.html'), 'utf8');
html = html.replace(/<link rel="preconnect"[^>]*>(<link rel="preconnect"[^>]*>)?\s*/g, '')
  .replace(/<link href="https:\/\/fonts\.googleapis\.com[^>]*>/, '<link href="fonts/fonts.css" rel="stylesheet">');
const inject = '<script src="firebase-config.js"></script><script src="backend.js"></script>';
if (!html.includes('</title>')) throw new Error('index.html に <title> が ありません');
html = html.replace('</title>', '</title>\n' + inject);
fs.writeFileSync(path.join(www, 'index.html'), html);
console.log('www/ を つくりました', (html.length / 1024 / 1024).toFixed(2) + 'MB');
