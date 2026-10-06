// index.html の SpriteGen（図形→陰影つきドット絵）で モンスターとトレーナーの PNG を書き出す（Unity 版用）。
// 使い方: node tools/export-sprites.js index.html unity/PixelMonsterArena/Assets/Resources/Sprites
const fs = require('fs'), path = require('path'), png = require('./png.js');
const src = fs.readFileSync(process.argv[2], 'utf8');
const a = src.indexOf('// ====== ここから SPRITEGEN'), b = src.indexOf('// ====== ここまで SPRITEGEN');
const SpriteGen = new Function(src.slice(a, b) + ';return SpriteGen;')();
const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
function crop(px, W, H) {
  let x0 = W, y0 = H, x1 = -1, y1 = -1;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (px[(y * W + x) * 4 + 3]) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  const w = x1 - x0 + 1, h = y1 - y0 + 1, o = new Uint8ClampedArray(w * h * 4);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) for (let k = 0; k < 4; k++) o[(y * w + x) * 4 + k] = px[((y + y0) * W + x + x0) * 4 + k];
  return { w, h, o };
}
// .bytes にしておくと Unity が 画像を 圧縮せず そのまま 読める（ドットが にじまない）
const write = (name, px, W, H) => { const c = crop(px, W, H); fs.writeFileSync(path.join(out, name + '.png.bytes'), png(c.w, c.h, c.o)); };
for (const id in SpriteGen.MON) write(id, SpriteGen.render(SpriteGen.MON[id](), SpriteGen.W, SpriteGen.H), SpriteGen.W, SpriteGen.H);
const i = src.indexOf('const ROUNDS = ['), j = src.indexOf('];', i), ROUNDS = eval(src.slice(i + 15, j + 1));
const combos = [['#e84a5f', '#3a6ee8'], ...ROUNDS.map(r => [r.hat, r.coat])];
for (const [hat, coat] of combos) write(`trainer_${hat.slice(1)}_${coat.slice(1)}`, SpriteGen.render(SpriteGen.TRAINER(hat, coat), SpriteGen.TW, SpriteGen.TH), SpriteGen.TW, SpriteGen.TH);
console.log('exported', fs.readdirSync(out).length, 'files');
