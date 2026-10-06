// index.html の ドット絵を PNG に 書き出す（Unity 版用）。モンスターは 手打ちの HandPix、トレーナーは SpriteGen。
// 使い方: node tools/export-sprites.js index.html unity/PixelMonsterArena/Assets/Resources/Sprites
const fs = require('fs'), path = require('path'), png = require('./png.js');
const src = fs.readFileSync(process.argv[2], 'utf8');
const a = src.indexOf('// ====== ここから SPRITEGEN'), b = src.indexOf('// ====== ここまで SPRITEGEN');
const SpriteGen = new Function(src.slice(a, b) + ';return SpriteGen;')();
// モンスターは 手打ちドット絵（HandPix）を つかう
const c = src.indexOf('// ====== ここから HANDPIX'), d = src.indexOf('// ====== ここまで HANDPIX');
const HandPix = new Function(src.slice(c, d) + ';return HandPix;')();
const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
// 全フレームを 同じ 枠で 切り抜く（フレームを 切り替えても 足元が ずれない）
function frameBox(frames, W, H) {
  let x0 = W, y0 = H, x1 = -1, y1 = -1;
  for (const px of Object.values(frames)) for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (px[(y * W + x) * 4 + 3]) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  return [x0, y0, x1, y1];
}
function crop(px, W, box) {
  const [x0, y0, x1, y1] = box, w = x1 - x0 + 1, h = y1 - y0 + 1, o = new Uint8ClampedArray(w * h * 4);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) for (let k = 0; k < 4; k++) o[(y * w + x) * 4 + k] = px[((y + y0) * W + x + x0) * 4 + k];
  return { w, h, o };
}
// .bytes にしておくと Unity が 画像を 圧縮せず そのまま 読める（ドットが にじまない）
// {name}_{frame}.png.bytes（アニメ用）と {name}.png.bytes（= idle0、一覧の サムネ用）を 書く
function writeAll(name, fr, W, H) {
  const box = frameBox(fr, W, H);
  const put = (n, px) => { const c = crop(px, W, box); fs.writeFileSync(path.join(out, n + '.png.bytes'), png(c.w, c.h, c.o)); };
  put(name, fr.idle0);
  for (const k of SpriteGen.FRAMES) put(name + '_' + k, fr[k]);
}
for (const id in SpriteGen.MON) {
  if (HandPix.MON[id]) writeAll(id, HandPix.frames(HandPix.MON[id]()), HandPix.W, HandPix.H);
  else writeAll(id, SpriteGen.frames(SpriteGen.MON[id](), SpriteGen.W, SpriteGen.H), SpriteGen.W, SpriteGen.H);
}
const i = src.indexOf('const ROUNDS = ['), j = src.indexOf('];', i), ROUNDS = eval(src.slice(i + 15, j + 1));
const combos = [['#e84a5f', '#3a6ee8'], ...ROUNDS.map(r => [r.hat, r.coat])];
for (const [hat, coat] of combos) writeAll(`trainer_${hat.slice(1)}_${coat.slice(1)}`, SpriteGen.frames(SpriteGen.TRAINER(hat, coat), SpriteGen.TW, SpriteGen.TH), SpriteGen.TW, SpriteGen.TH);
console.log('exported', fs.readdirSync(out).length, 'files');
