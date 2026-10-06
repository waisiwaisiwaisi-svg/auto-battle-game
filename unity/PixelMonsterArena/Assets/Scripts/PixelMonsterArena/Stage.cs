using System.Collections.Generic;
using UnityEngine;

namespace PixelMonsterArena
{
    public class Pool { public float X, Y, Rx, Ry; }

    /// <summary>ステージ（スタジアム／くさむら）。座標は y 下向き、左上が原点。</summary>
    public class Stage
    {
        public int W, H;
        public float Fx0, Fy0, Fx1, Fy1;
        public string Kind, Field;
        public List<Pool> Pools = new List<Pool>();
        public Vector2[] Trainers;
        public bool HasTrainer2;
        public Sprite Bg;
        /// <summary>観客：[0]=上段, [1]=下段（手前）。各3フレーム（0=静止, 1,2=ジャンプ）</summary>
        public Sprite[][] Crowd;
        public float[] CrowdY;

        static readonly string[] GrassRamp = { "#24561f", "#2c6326", "#35722e", "#3f8236", "#4a9140", "#58a04b" };

        public bool InField(float x, float y, float r) => x >= Fx0 + r && x <= Fx1 - r && y >= Fy0 + r && y <= Fy1 - r;
        public bool InPool(float x, float y)
        {
            foreach (var p in Pools) { float dx = (x - p.X) / p.Rx, dy = (y - p.Y) / p.Ry; if (dx * dx + dy * dy < 1) return true; }
            return false;
        }

        public static Stage Stadium(string fieldType)
        {
            var st = new Stage { W = 1000, H = 690, Fx0 = 190, Fy0 = 200, Fx1 = 810, Fy1 = 560, Kind = "stadium", Field = fieldType, HasTrainer2 = true };
            st.Trainers = new[] { new Vector2(132, 392), new Vector2(868, 392) };
            var g = new PixCanvas(st.W, st.H);
            var r = new System.Random(fieldType.Length * 977 + 13);
            float R() => (float)r.NextDouble();
            Color C(string h) => Util.Hex(h);

            g.Rect(0, 0, st.W, st.H, C("#1e1832"));
            for (int y = 18, i = 0; y < 154; y += 12, i++) { g.Rect(0, y, st.W, 12, C(i % 2 == 1 ? "#352c50" : "#2e2647")); g.Rect(0, y, st.W, 1, C("#41375f")); }
            g.Rect(0, 0, st.W, 18, C("#120e1c"));
            foreach (var lx in new[] { 60, 340, 660, 940 }) { g.Rect(lx - 2, 0, 4, 16, C("#5a5070")); g.Rect(lx - 12, 3, 25, 9, C("#fff6c8")); g.Rect(lx - 9, 5, 19, 3, Color.white); }
            g.Rect(0, 154, st.W, 18, C("#5b4f80")); g.Rect(0, 154, st.W, 3, C("#7a6ca8"));
            string[] bannerCols = { "#ff6b5b", "#ffd166", "#4fd1a5", "#4aa8ff", "#c08aff" };
            for (int x = 24, i = 0; x < st.W - 60; x += 100, i++)
            {
                g.Rect(x, 158, 72, 11, C(bannerCols[i % 5]));
                for (int k = 0; k < 8; k++) g.Rect(x + 5 + k * 8, 162, 5, 3, new Color(1, 1, 1, .6f));
            }
            Noise.Paint(g, 14, 172, st.W - 28, 440, 91, new[] { "#4a4458", "#544d62", "#5e566c", "#686076" }, .2f);
            var grout = new Color(30 / 255f, 26 / 255f, 40 / 255f, .45f);
            for (int y = 172; y < 612; y += 16) { g.Rect(14, y, st.W - 28, 1, grout); for (int x = 14 + ((y / 16) % 2) * 16; x < st.W - 14; x += 32) g.Rect(x, y, 1, 16, grout); }

            int fx0 = (int)st.Fx0, fy0 = (int)st.Fy0, fx1 = (int)st.Fx1, fy1 = (int)st.Fy1, fw = fx1 - fx0, fh = fy1 - fy0;
            float cx = (fx0 + fx1) / 2f, cy = (fy0 + fy1) / 2f;
            var lineCol = new Color(1, 1, 1, .78f);
            if (fieldType == "grass")
            {
                Noise.Paint(g, fx0, fy0, fw, fh, 5, GrassRamp, .25f);
                for (int x = fx0, i = 0; x < fx1; x += 62, i++) if (i % 2 == 1) g.Rect(x, fy0, 62, fh, new Color(1, 1, 1, .035f));
            }
            else if (fieldType == "dirt")
            {
                Noise.Paint(g, fx0, fy0, fw, fh, 8, new[] { "#6e5032", "#7d5c3a", "#8c6a44", "#9a774e", "#a8855a" }, .3f);
                string[] peb = { "#5e4428", "#b8966a", "#6a5a50" };
                for (int i = 0; i < 260; i++) { int s = R() < .3f ? 3 : 2; g.Rect(fx0 + (int)(R() * fw), fy0 + (int)(R() * fh), s, s - 1, C(peb[r.Next(3)])); }
            }
            else if (fieldType == "concrete")
            {
                // 自陣は紺、あいて陣はえんじ色のタイル
                Noise.Paint(g, fx0, fy0, fw / 2, fh, 11, new[] { "#22244a", "#282a54", "#2e305e", "#343768" }, .2f);
                Noise.Paint(g, (int)cx, fy0, fw / 2, fh, 12, new[] { "#47223a", "#522843", "#5d2e4c", "#683456" }, .2f);
                for (int x = fx0; x <= fx1; x += 62) g.Rect(x - 2, fy0, 4, fh, C("#14121e"));
                for (int y = fy0; y <= fy1; y += 60) g.Rect(fx0, y - 2, fw, 4, C("#14121e"));
                var crack = new Color(10 / 255f, 8 / 255f, 16 / 255f, .55f);
                for (int i = 0; i < 14; i++)
                {
                    float x = fx0 + R() * fw, y = fy0 + R() * fh;
                    for (int k = 0; k < 5; k++) { float nx = x + (R() - .5f) * 30, ny = y + (R() - .5f) * 24; g.Line(x, y, nx, ny, crack); x = nx; y = ny; }
                }
                lineCol = new Color(214 / 255f, 170 / 255f, 80 / 255f, .85f);
            }
            else
            {
                Noise.Paint(g, fx0, fy0, fw, fh, 21, new[] { GrassRamp[2], GrassRamp[3], GrassRamp[4], GrassRamp[5] }, .25f);
                st.Pools.Add(new Pool { X = cx, Y = cy, Rx = 100, Ry = 56 });
                st.Pools.Add(new Pool { X = fx0 + fw * .18f, Y = fy0 + fh * .2f, Rx = 64, Ry = 34 });
                st.Pools.Add(new Pool { X = fx0 + fw * .82f, Y = fy0 + fh * .8f, Rx = 64, Ry = 34 });
                st.Pools.Add(new Pool { X = fx0 + fw * .8f, Y = fy0 + fh * .17f, Rx = 48, Ry = 26 });
                st.Pools.Add(new Pool { X = fx0 + fw * .2f, Y = fy0 + fh * .83f, Rx = 48, Ry = 26 });
                foreach (var p in st.Pools)
                {
                    g.Ellipse(p.X, p.Y + 3, p.Rx + 6, p.Ry + 6, C("#c8b47a"));
                    g.Ellipse(p.X, p.Y, p.Rx, p.Ry, C("#2a6ab8"));
                    g.Ellipse(p.X, p.Y - 3, p.Rx - 8, p.Ry - 8, C("#3a8ad8"));
                    g.Ellipse(p.X - p.Rx * .15f, p.Y - p.Ry * .3f, p.Rx * .5f, p.Ry * .35f, C("#5aa8f0"));
                }
            }
            g.Rect(fx0, fy0, fw, 3, lineCol); g.Rect(fx0, fy1 - 3, fw, 3, lineCol); g.Rect(fx0, fy0, 3, fh, lineCol); g.Rect(fx1 - 3, fy0, 3, fh, lineCol);
            g.Rect(cx - 1, fy0, 3, fh, lineCol);
            g.RingStroke(cx, cy, 110, 3, lineCol);
            g.Ellipse(cx, cy, 6, 6, lineCol);
            foreach (var side in new[] { 0, 1 })
            {
                float x = side == 1 ? fx1 - 70 : fx0;
                g.Rect(x + 1, cy - 90, 68, 3, lineCol); g.Rect(x + 1, cy + 88, 68, 3, lineCol);
                g.Rect(side == 1 ? x : x + 67, cy - 90, 3, 180, lineCol);
            }
            for (int i = 0; i < 2; i++)
            {
                var t = st.Trainers[i];
                g.Rect(t.x - 30, t.y - 62, 60, 80, C("#2a2340"));
                g.Rect(t.x - 28, t.y - 60, 56, 76, C(i == 1 ? "#ff6b5b" : "#4aa8ff"));
                g.Rect(t.x - 24, t.y - 56, 48, 68, C("#2a2340"));
                g.Rect(t.x - 24, t.y - 56, 48, 68, i == 1 ? new Color(1, 107 / 255f, 91 / 255f, .3f) : new Color(74 / 255f, 168 / 255f, 1, .3f));
            }
            g.Rect(0, 612, st.W, 14, C("#5b4f80")); g.Rect(0, 612, st.W, 3, C("#7a6ca8"));
            for (int y = 626, i = 0; y < st.H; y += 12, i++) g.Rect(0, y, st.W, 12, C(i % 2 == 1 ? "#352c50" : "#2e2647"));
            st.Bg = PixelArt.ToSprite(g.ToTexture(), new Vector2(0, 1));
            st.BakeCrowd();
            return st;
        }

        public static Stage Wild()
        {
            var st = new Stage { W = 820, H = 570, Fx0 = 140, Fy0 = 96, Fx1 = 750, Fy1 = 506, Kind = "wild", Field = "grass" };
            st.Trainers = new[] { new Vector2(84, 318), Vector2.zero };
            var g = new PixCanvas(st.W, st.H);
            var r = new System.Random(777);
            float R() => (float)r.NextDouble();
            Color C(string h) => Util.Hex(h);
            Noise.Paint(g, 0, 0, st.W, st.H, 33, GrassRamp, .25f);
            g.Rect(0, 282, 140, 70, C("#b4966a"));
            Noise.Paint(g, 0, 286, 140, 62, 44, new[] { "#a88a5e", "#b4966a", "#c2a476", "#ccb084" }, .3f);
            string[] flowers = { "#ffffff", "#ffd166", "#ff9ad0" };
            for (int i = 0; i < 70; i++) { int x = 150 + (int)(R() * 590), y = 104 + (int)(R() * 390); g.Rect(x, y, 3, 3, C(flowers[r.Next(3)])); g.Rect(x + 1, y + 1, 1, 1, C("#ffe066")); }
            for (int i = 0; i < 140; i++)
            {
                int x = 150 + (int)(R() * 590), y = 104 + (int)(R() * 390);
                g.Rect(x, y, 2, 7, C("#1f4a1c")); g.Rect(x + 3, y - 2, 2, 9, C("#1f4a1c")); g.Rect(x + 6, y, 2, 7, C("#1f4a1c")); g.Rect(x + 3, y - 2, 1, 3, C("#5aa84a"));
            }
            void Tree(float x, float y, float s)
            {
                g.Ellipse(x, y + 8, s, s * .4f, new Color(10 / 255f, 20 / 255f, 10 / 255f, .35f));
                g.Rect(x - 3, y - 2, 6, 10, C("#5a3d2b"));
                g.Ellipse(x, y - 10, s, s, C("#1d4a22"));
                g.Ellipse(x - 3, y - 13, s - 5, s - 5, C("#2a6630"));
                g.Ellipse(x - 6, y - 17, s * .45f, s * .45f, C("#3e8a40"));
            }
            for (int x = 10; x < st.W; x += 34) { Tree(x + r.Next(8), 40 + r.Next(14), 22); Tree(x + r.Next(8), st.H - 18 - r.Next(10), 22); }
            for (int y = 70; y < st.H - 30; y += 34) { if (y < 250 || y > 360) Tree(30 + r.Next(14), y, 20); Tree(st.W - 30 - r.Next(12), y, 22); }
            st.Bg = PixelArt.ToSprite(g.ToTexture(), new Vector2(0, 1));
            return st;
        }

        /// <summary>観客を3フレーム分テクスチャに焼く（1枚ずつ描くと重いため）</summary>
        void BakeCrowd()
        {
            string[] shirt = { "#ff6b5b", "#ffd166", "#4fd1a5", "#4aa8ff", "#c08aff", "#f4ecd8", "#ff9ad0", "#7bd88f" };
            string[] skin = { "#f2c79b", "#d8a070", "#a87048", "#ffe0c0" };
            Crowd = new Sprite[2][];
            CrowdY = new float[] { 18, 626 };
            int[] y0s = { 26, 636 }, y1s = { 150, H - 4 };
            for (int band = 0; band < 2; band++)
            {
                int top = (int)CrowdY[band], hgt = band == 0 ? 140 : H - top;
                Crowd[band] = new Sprite[3];
                for (int frame = 0; frame < 3; frame++)
                {
                    var g = new PixCanvas(W, hgt);
                    var r = new System.Random(4242 + band);
                    for (int y = y0s[band]; y < y1s[band]; y += 12)
                        for (int x = 4; x < W - 6; x += 9)
                        {
                            if (r.NextDouble() >= .86) continue;
                            int px = x + r.Next(3);
                            var sc = Util.Hex(shirt[r.Next(8)]); var sk = Util.Hex(skin[r.Next(4)]);
                            int grp = r.Next(2);
                            bool jump = frame != 0 && grp == frame - 1;
                            int py = y - top - (jump ? 3 : 0);
                            g.Rect(px, py + 3, 6, 6, sc); g.Rect(px + 1, py, 4, 3, sk);
                            if (jump) { g.Rect(px - 2, py - 2, 2, 3, sk); g.Rect(px + 6, py - 2, 2, 3, sk); }
                        }
                    // 透明背景にするため、未描画ピクセルは alpha=0 のまま
                    Crowd[band][frame] = PixelArt.ToSprite(g.ToTexture(), new Vector2(0, 1));
                }
            }
        }
    }
}
