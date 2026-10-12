# 宣伝動画の つくりかた

1. `node tools/promo/record.js`（Playwright と Chromium が ひつよう）で `tools/promo/frames/` に 30fps の コマを かきだす
2. mp4 に まとめる（BGM は こおりの きょく）

```sh
ffmpeg -framerate 30 -i tools/promo/frames/%05d.png -i music/ice_battle_loop.flac \
  -filter_complex "[1:a]atrim=0:24.7,afade=t=in:d=0.4,afade=t=out:st=22.9:d=1.8,volume=0.8[a]" \
  -map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 20 -preset slow -movflags +faststart \
  -c:a aac -b:a 160k -shortest promo/promo_pixel_monster_arena.mp4
```
