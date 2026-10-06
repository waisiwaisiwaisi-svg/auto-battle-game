using System.Collections.Generic;
using UnityEngine;

namespace PixelMonsterArena
{
    /// <summary>
    /// ドット絵の生成。文字マップ → 2倍拡大（EPX）→ 左上ハイライト／右下の影 → 輪郭線 の順に焼き込む。
    /// 1テクセル = 1ワールド単位（pixelsPerUnit = 1）。ピボットは足元（下中央）。
    /// </summary>
    public static class PixelArt
    {
        static readonly Color Outline = Util.Hex("#1a1424");

        public static string[] Scale2x(string[] rows)
        {
            int h = rows.Length, w = 0;
            foreach (var r in rows) w = Mathf.Max(w, r.Length);
            char At(int x, int y) => (y >= 0 && y < h && x >= 0 && x < rows[y].Length) ? rows[y][x] : '.';
            var outRows = new string[h * 2];
            for (int y = 0; y < h; y++)
            {
                var r1 = new System.Text.StringBuilder(); var r2 = new System.Text.StringBuilder();
                for (int x = 0; x < w; x++)
                {
                    char P = At(x, y), A = At(x, y - 1), B = At(x + 1, y), C = At(x - 1, y), D = At(x, y + 1);
                    char p1 = P, p2 = P, p3 = P, p4 = P;
                    if (C == A && C != D && A != B) p1 = A;
                    if (A == B && A != C && B != D) p2 = B;
                    if (D == C && D != B && C != A) p3 = C;
                    if (B == D && B != A && D != C) p4 = D;
                    r1.Append(p1).Append(p2); r2.Append(p3).Append(p4);
                }
                outRows[y * 2] = r1.ToString(); outRows[y * 2 + 1] = r2.ToString();
            }
            return outRows;
        }

        /// <summary>文字マップをテクスチャに焼く。solid を指定すると単色シルエット（被弾フラッシュ用）。</summary>
        public static Texture2D Bake(string[] rows, Dictionary<char, string> pal, Color? solid, bool shade)
        {
            int h = rows.Length, w = 0;
            foreach (var r in rows) w = Mathf.Max(w, r.Length);
            int W = w + 2, H = h + 2;
            var px = new Color32[W * H];
            bool Filled(int x, int y) => y >= 0 && y < h && x >= 0 && x < rows[y].Length && rows[y][x] != '.';
            void Set(int x, int y, Color c) => px[(H - 1 - y) * W + x] = c; // テクスチャは下が y=0
            for (int y = -1; y <= h; y++)
                for (int x = -1; x <= w; x++)
                {
                    if (Filled(x, y)) continue;
                    if (Filled(x - 1, y) || Filled(x + 1, y) || Filled(x, y - 1) || Filled(x, y + 1)) Set(x + 1, y + 1, solid ?? Outline);
                }
            for (int y = 0; y < h; y++)
                for (int x = 0; x < rows[y].Length; x++)
                {
                    char ch = rows[y][x];
                    if (ch == '.') continue;
                    Color col;
                    if (solid.HasValue) col = solid.Value;
                    else
                    {
                        col = pal != null && pal.TryGetValue(ch, out var hx) ? Util.Hex(hx) : Color.magenta;
                        if (shade)
                        {
                            float lum = (col.r * .3f + col.g * .59f + col.b * .11f) * 255f;
                            if (lum > 50 && lum < 245)
                            {
                                if (!Filled(x, y - 1) || !Filled(x - 1, y)) col = Util.Shade(col, .28f);
                                else if (!Filled(x, y + 1) || !Filled(x + 1, y)) col = Util.Shade(col, -.32f);
                                else if (!Filled(x, y + 2) || !Filled(x + 2, y)) col = Util.Shade(col, -.14f);
                            }
                        }
                    }
                    Set(x + 1, y + 1, col);
                }
            return MakeTex(W, H, px);
        }

        public static Texture2D MakeTex(int w, int h, Color32[] px)
        {
            var t = new Texture2D(w, h, TextureFormat.RGBA32, false) { filterMode = FilterMode.Point, wrapMode = TextureWrapMode.Clamp };
            t.SetPixels32(px);
            t.Apply(false, true);
            return t;
        }

        public static Sprite ToSprite(Texture2D t, Vector2 pivot) =>
            Sprite.Create(t, new Rect(0, 0, t.width, t.height), pivot, 1f, 0, SpriteMeshType.FullRect);

        // ---------- モンスター／トレーナー ----------
        /// <summary>アニメのフレーム名（index.html の SpriteGen.FRAMES と同じ）</summary>
        public static readonly string[] Frames = { "idle0", "idle1", "idle2", "idle3", "blink", "walk0", "walk1", "walk2", "walk3", "atk0", "atk1", "atk2", "hit", "ko" };
        /// <summary>フレームごとの 通常／白シルエット。全フレームが 同じ 大きさ（足元が そろう）。</summary>
        public class MonSprites
        {
            public Sprite Normal, White; public int W, H;
            /// <summary>表示倍率。生成AIの 絵（約70px）は 小さめ、手打ち（約48px）は 1.6</summary>
            public float Ms = 1.6f;
            public readonly Dictionary<string, Sprite> N = new Dictionary<string, Sprite>(), Wt = new Dictionary<string, Sprite>();
            public Sprite Frame(string name, bool white) => (white ? Wt : N).TryGetValue(name, out var sp) ? sp : (white ? White : Normal);
        }
        static readonly Dictionary<string, MonSprites> MonCache = new Dictionary<string, MonSprites>();
        /// <summary>
        /// Resources/Sprites の PNG（index.html の SpriteGen から tools/export-sprites.js で書き出したもの）を読む。
        /// .png.bytes にしてあるので 圧縮されず、ドットが そのまま 出る。
        /// </summary>
        static Texture2D LoadPng(string name)
        {
            var ta = Resources.Load<TextAsset>("Sprites/" + name + ".png");
            if (ta == null) return null;
            var t = new Texture2D(2, 2, TextureFormat.RGBA32, false) { filterMode = FilterMode.Point, wrapMode = TextureWrapMode.Clamp };
            t.LoadImage(ta.bytes, false);
            t.filterMode = FilterMode.Point;
            return t;
        }
        static Texture2D WhiteOf(Texture2D src)
        {
            var px = src.GetPixels32();
            for (int i = 0; i < px.Length; i++) if (px[i].a > 0) px[i] = new Color32(255, 255, 255, 255);
            return MakeTex(src.width, src.height, px);
        }

        static MonSprites Load(string name, Texture2D fallback)
        {
            var n = LoadPng(name) ?? fallback;
            var s = new MonSprites { Normal = ToSprite(n, new Vector2(.5f, 0)), White = ToSprite(WhiteOf(n), new Vector2(.5f, 0)), W = n.width, H = n.height, Ms = n.height > 56 ? 1.15f : 1.6f };
            foreach (var f in Frames)
            {
                var t = LoadPng(name + "_" + f);
                if (t == null) continue;
                s.N[f] = ToSprite(t, new Vector2(.5f, 0));
                s.Wt[f] = ToSprite(WhiteOf(t), new Vector2(.5f, 0));
            }
            return s;
        }

        public static MonSprites Mon(string sid)
        {
            if (MonCache.TryGetValue(sid, out var s)) return s;
            Texture2D fb = null;
            if (Resources.Load<TextAsset>("Sprites/" + sid + ".png") == null)
            { // 画像が ないときは 文字マップから 作る（予備）
                var sp = Data.Species[sid];
                fb = Bake(Scale2x(sp.Rows), sp.Pal, null, true);
            }
            return MonCache[sid] = Load(sid, fb);
        }

        static readonly Dictionary<string, MonSprites> TrainerCache = new Dictionary<string, MonSprites>();
        public static MonSprites Trainer(string hat, string coat)
        {
            string key = $"trainer_{hat.Substring(1)}_{coat.Substring(1)}";
            if (TrainerCache.TryGetValue(key, out var spr)) return spr;
            Texture2D fb = null;
            if (Resources.Load<TextAsset>("Sprites/" + key + ".png") == null)
            {
                var pal = new Dictionary<char, string> { { 'h', hat }, { 'H', hat }, { 's', "#f2c79b" }, { 'k', "#1a1626" }, { 'c', coat }, { 'p', "#3a3350" }, { 'b', "#2a1e1e" } };
                fb = Bake(Scale2x(Data.TrainerRows), pal, null, true);
            }
            return TrainerCache[key] = Load(key, fb);
        }

        // ---------- 図形スプライト（白で作り、色は SpriteRenderer.color で付ける） ----------
        static Sprite _px, _pxLeft, _disc, _ring, _star;
        /// <summary>1x1 の白（中心ピボット）</summary>
        public static Sprite Pixel => _px ? _px : (_px = ToSprite(MakeTex(1, 1, new[] { (Color32)Color.white }), new Vector2(.5f, .5f)));
        /// <summary>1x1 の白（左中央ピボット：ビームや線分用）</summary>
        public static Sprite PixelLeft => _pxLeft ? _pxLeft : (_pxLeft = ToSprite(MakeTex(1, 1, new[] { (Color32)Color.white }), new Vector2(0, .5f)));
        /// <summary>直径 128 の塗りつぶし円</summary>
        public static Sprite Disc => _disc ? _disc : (_disc = ToSprite(Circle(128, 0), new Vector2(.5f, .5f)));
        /// <summary>直径 128 のリング（太さ 6）</summary>
        public static Sprite Ring => _ring ? _ring : (_ring = ToSprite(Circle(128, 6), new Vector2(.5f, .5f)));
        public static Sprite Star => _star ? _star : (_star = ToSprite(StarTex(32), new Vector2(.5f, .5f)));

        static Texture2D Circle(int d, float thick)
        {
            var px = new Color32[d * d];
            float r = d / 2f;
            for (int y = 0; y < d; y++)
                for (int x = 0; x < d; x++)
                {
                    float dist = Mathf.Sqrt((x + .5f - r) * (x + .5f - r) + (y + .5f - r) * (y + .5f - r));
                    bool on = thick <= 0 ? dist <= r : dist <= r && dist >= r - thick;
                    px[y * d + x] = on ? new Color32(255, 255, 255, 255) : new Color32(255, 255, 255, 0);
                }
            var t = MakeTex(d, d, px);
            t.filterMode = FilterMode.Bilinear;
            return t;
        }

        static Texture2D StarTex(int d)
        {
            var px = new Color32[d * d];
            var pts = new Vector2[10];
            for (int i = 0; i < 10; i++)
            {
                float a = Mathf.PI / 2 + i * Mathf.PI / 5, rr = i % 2 == 1 ? d * .22f : d * .5f;
                pts[i] = new Vector2(d / 2f + Mathf.Cos(a) * rr, d / 2f + Mathf.Sin(a) * rr);
            }
            for (int y = 0; y < d; y++)
                for (int x = 0; x < d; x++)
                    px[y * d + x] = InPoly(new Vector2(x + .5f, y + .5f), pts) ? new Color32(255, 255, 255, 255) : new Color32(0, 0, 0, 0);
            return MakeTex(d, d, px);
        }

        static bool InPoly(Vector2 p, Vector2[] v)
        {
            bool c = false;
            for (int i = 0, j = v.Length - 1; i < v.Length; j = i++)
                if (((v[i].y > p.y) != (v[j].y > p.y)) && (p.x < (v[j].x - v[i].x) * (p.y - v[i].y) / (v[j].y - v[i].y) + v[i].x)) c = !c;
            return c;
        }
    }

    /// <summary>CPU 上の簡易キャンバス（y は下向き）。ステージ背景の焼き込みに使う。</summary>
    public class PixCanvas
    {
        public readonly int W, H;
        public readonly Color32[] Px;
        public PixCanvas(int w, int h) { W = w; H = h; Px = new Color32[w * h]; }

        public void Blend(int x, int y, Color c)
        {
            if (x < 0 || y < 0 || x >= W || y >= H) return;
            int i = (H - 1 - y) * W + x;
            if (c.a >= .999f) { Px[i] = c; return; }
            Color d = Px[i];
            Px[i] = new Color(d.r + (c.r - d.r) * c.a, d.g + (c.g - d.g) * c.a, d.b + (c.b - d.b) * c.a, 1);
        }
        public void Rect(float x, float y, float w, float h, Color c)
        {
            int x0 = Mathf.RoundToInt(x), y0 = Mathf.RoundToInt(y), x1 = Mathf.RoundToInt(x + w), y1 = Mathf.RoundToInt(y + h);
            for (int yy = Mathf.Max(0, y0); yy < Mathf.Min(H, y1); yy++)
                for (int xx = Mathf.Max(0, x0); xx < Mathf.Min(W, x1); xx++) Blend(xx, yy, c);
        }
        public void Ellipse(float cx, float cy, float rx, float ry, Color c)
        {
            for (int yy = Mathf.FloorToInt(cy - ry); yy <= Mathf.CeilToInt(cy + ry); yy++)
                for (int xx = Mathf.FloorToInt(cx - rx); xx <= Mathf.CeilToInt(cx + rx); xx++)
                {
                    float dx = (xx + .5f - cx) / rx, dy = (yy + .5f - cy) / ry;
                    if (dx * dx + dy * dy <= 1) Blend(xx, yy, c);
                }
        }
        public void RingStroke(float cx, float cy, float r, float thick, Color c)
        {
            for (int yy = Mathf.FloorToInt(cy - r - thick); yy <= Mathf.CeilToInt(cy + r + thick); yy++)
                for (int xx = Mathf.FloorToInt(cx - r - thick); xx <= Mathf.CeilToInt(cx + r + thick); xx++)
                {
                    float d = Mathf.Sqrt((xx + .5f - cx) * (xx + .5f - cx) + (yy + .5f - cy) * (yy + .5f - cy));
                    if (Mathf.Abs(d - r) <= thick / 2) Blend(xx, yy, c);
                }
        }
        public void Line(float x0, float y0, float x1, float y1, Color c)
        {
            int n = Mathf.CeilToInt(Mathf.Max(Mathf.Abs(x1 - x0), Mathf.Abs(y1 - y0)));
            for (int i = 0; i <= n; i++) { float t = n == 0 ? 0 : (float)i / n; Blend(Mathf.RoundToInt(x0 + (x1 - x0) * t), Mathf.RoundToInt(y0 + (y1 - y0) * t), c); }
        }
        public Texture2D ToTexture() => PixelArt.MakeTex(W, H, Px);
    }

    /// <summary>なめらかなノイズ（芝生や土のまだら模様）。index.html と同じ式。</summary>
    public static class Noise
    {
        static float H(float a, float b, float seed) { float t = Mathf.Sin(a * 127.1f + b * 311.7f + seed * 17.31f) * 43758.5453f; return t - Mathf.Floor(t); }
        public static float V(float x, float y, float seed)
        {
            float ix = Mathf.Floor(x), iy = Mathf.Floor(y), fx = x - ix, fy = y - iy;
            float u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy);
            float a = H(ix, iy, seed) + (H(ix + 1, iy, seed) - H(ix, iy, seed)) * u;
            float b = H(ix, iy + 1, seed) + (H(ix + 1, iy + 1, seed) - H(ix, iy + 1, seed)) * u;
            return a + (b - a) * v;
        }
        public static float Fbm(float x, float y, float seed) => V(x / 46f, y / 46f, seed) * .5f + V(x / 17f, y / 17f, seed + 1) * .3f + V(x / 6f, y / 6f, seed + 2) * .2f;

        public static void Paint(PixCanvas g, int x0, int y0, int w, int h, int seed, string[] ramp, float jitter)
        {
            var cols = new Color[ramp.Length];
            for (int i = 0; i < ramp.Length; i++) cols[i] = Util.Hex(ramp[i]);
            var r = new System.Random(seed * 31 + 7);
            for (int y = 0; y < h; y++)
                for (int x = 0; x < w; x++)
                {
                    float v = Fbm(x0 + x, y0 + y, seed);
                    if (r.NextDouble() < jitter) v += ((float)r.NextDouble() - .5f) * .25f;
                    int ci = Mathf.Clamp(Mathf.FloorToInt((v - .2f) / .6f * cols.Length), 0, cols.Length - 1);
                    g.Blend(x0 + x, y0 + y, cols[ci]);
                }
        }
    }
}
