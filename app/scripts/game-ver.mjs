// ゲームの バージョン：index.html の なかみの ハッシュ。アプリと サーバー（さいげん）で おなじ ものを つかう
import crypto from 'node:crypto';
export const PLACE = "const GAME_VER = 'dev';";
export function stampVer(html) {
  if (!html.includes(PLACE)) throw new Error('index.html に GAME_VER が ありません');
  const ver = crypto.createHash('sha256').update(html).digest('hex').slice(0, 12);
  return { ver, html: html.replace(PLACE, `const GAME_VER = '${ver}';`) };
}
