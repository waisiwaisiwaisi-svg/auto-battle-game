// node prev.js data.json out.png  … 14コマを 並べた 一覧（4倍）
const fs = require('fs'), png = require('../png.js');
const AISpr = new Function(fs.readFileSync(__dirname + '/aispr.js', 'utf8') + ';return AISpr;')();
const data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ids = Object.keys(data); for (const k of ids) AISpr.DATA[k] = data[k];
const S = 4; const fr0 = ids.map(id => AISpr.framesOf(id));
const cw = Math.max(...ids.map(id => data[id].w + AISpr.PAD * 2)), ch = Math.max(...ids.map(id => data[id].h + AISpr.PAD));
const OW = cw * S * 14, OH = ch * S * ids.length, out = new Uint8ClampedArray(OW * OH * 4);
for (let i = 0; i < OW * OH; i++) { const x = i % OW, y = i / OW | 0, c = ((x >> 4) + (y >> 4)) & 1; out[i * 4] = c ? 74 : 66; out[i * 4 + 1] = c ? 128 : 118; out[i * 4 + 2] = c ? 74 : 66; out[i * 4 + 3] = 255; }
ids.forEach((id, r) => {
  const w = data[id].w + AISpr.PAD * 2, h = data[id].h + AISpr.PAD;
  AISpr.FRAMES.forEach((f, c) => {
    const px = fr0[r][f];
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const si = (y * w + x) * 4; if (!px[si + 3]) continue;
      for (let dy = 0; dy < S; dy++) for (let dx = 0; dx < S; dx++) { const di = ((r * ch * S + (ch - h + y) * S + dy) * OW + c * cw * S + x * S + dx) * 4; out[di] = px[si]; out[di + 1] = px[si + 1]; out[di + 2] = px[si + 2]; } }
  });
});
fs.writeFileSync(process.argv[3], png(OW, OH, out));
