using System.Collections.Generic;
using UnityEngine;

namespace PixelMonsterArena
{
    /// <summary>
    /// Battle の中身を Painter で描く（index.html の render() の移植）。
    /// 文字（ダメージ数値など）は WorldTexts に積んで、Game の OnGUI で描く。
    /// </summary>
    public class BattleRenderer
    {
        const float BODY = Data.Body;
        public readonly Painter P;
        public readonly List<(Vector2 pos, string txt, Color col, int size)> WorldTexts = new List<(Vector2, string, Color, int)>();
        public float ViewCx, ViewCy, ViewZ;

        // 描画順
        const int O_BG = -30000, O_CROWD_BACK = -29500, O_DECAL = -29000, O_HAZ = -28500, O_TELE = -28000, O_GHOST = -27000;
        const int O_PROJ = 20000, O_CAP = 20500, O_FX = 21000, O_PART = 22000, O_CROWD_FRONT = 23000;
        static int Ord(float y) => Mathf.RoundToInt(y) * 10;

        public BattleRenderer(Transform root) { P = new Painter(root); }

        static Color C(string h) => Util.Hex(h);
        static Color A(Color c, float a) => new Color(c.r, c.g, c.b, c.a * a);

        public void Render(Battle B, Camera cam)
        {
            WorldTexts.Clear();
            P.Begin();
            var st = B.St;
            // カメラ（ワールドの外が見えないよう制限）
            float z = B.Cam.z, aspect = cam.aspect;
            float hh = 120f / z, hw = hh * aspect;
            float cx = st.W > hw * 2 ? Mathf.Clamp(B.Cam.x, hw, st.W - hw) : st.W / 2f;
            float cy = st.H > hh * 2 ? Mathf.Clamp(B.Cam.y, hh, st.H - hh) : st.H / 2f;
            if (B.Shake > 0) { cx += Util.Rand(-B.Shake, B.Shake) / z; cy += Util.Rand(-B.Shake, B.Shake) / z; }
            cam.orthographicSize = hh;
            cam.transform.position = new Vector3(cx, -cy, -10);
            ViewCx = cx; ViewCy = cy; ViewZ = z;

            P.Sprite(st.Bg, 0, 0, 1, 1, Color.white, O_BG);
            if (st.Crowd != null)
            {
                int frame = B.Cheer < .3f ? 0 : 1 + Mathf.FloorToInt(B.T * (4 + B.Cheer * 6)) % 2;
                P.Sprite(st.Crowd[0][frame], 0, st.CrowdY[0], 1, 1, Color.white, O_CROWD_BACK);
                P.Sprite(st.Crowd[1][frame], 0, st.CrowdY[1], 1, 1, Color.white, O_CROWD_FRONT);
            }
            foreach (var p in st.Pools)
                if (Mathf.FloorToInt(B.T * 3 + p.X) % 2 == 1) { P.Rect(p.X - p.Rx * .4f, p.Y - 3, 6, 1, A(Color.white, .5f), O_DECAL); P.Rect(p.X + p.Rx * .2f, p.Y + 4, 4, 1, A(Color.white, .5f), O_DECAL); }
            foreach (var d in B.Decals) DrawDecal(B, d);
            DrawHazards(B);

            Fighter a = B.Active(0), e = B.Active(1);
            foreach (var f in new[] { a, e }) if (f != null && f.State == "wind" && f.Cur != null) DrawTele(B, f);
            foreach (var fx in B.Fxs) if (fx.Type == "ghost" && fx.Sid != null) { var ms = PixelArt.Mon(fx.Sid); P.Sprite(ms.White, fx.X, fx.Y + 3, 2 * fx.Face, 2, A(Color.white, .3f * fx.Life / fx.Max), O_GHOST); }

            foreach (var sd in B.Sides) if (sd.Trainer != null) DrawTrainer(B, sd);
            foreach (var f in new[] { a, e }) if (f != null) DrawFighter(B, f);
            foreach (var p in B.Projs) DrawProj(B, p);
            if (B.Catch != null) DrawCapsule(B);
            foreach (var fx in B.Fxs) DrawFx(B, fx);
            foreach (var q in B.Parts) P.Rect(q.X, q.Y, q.Size, q.Size, A(q.Col, Mathf.Clamp01(q.Life / q.Max * 1.5f)), O_PART);
            foreach (var t in B.Texts)
            {
                float pop = t.Big == 2 ? 1 + Mathf.Max(0, (t.Life - t.Max + .15f) / .15f) * .6f : 1;
                WorldTexts.Add((new Vector2(t.X, t.Y), t.Txt, A(t.Col, Mathf.Clamp01(t.Life / t.Max * 2)), Mathf.RoundToInt((t.Big == 2 ? 20 : t.Big == 1 ? 15 : 12) * pop)));
            }
            P.End();
        }

        void DrawDecal(Battle B, Decal d)
        {
            if (d.Kind == "crater")
            {
                P.Ellipse(d.X, d.Y, d.R, d.R * .55f, new Color(40 / 255f, 28 / 255f, 20 / 255f, .45f), O_DECAL);
                P.Ellipse(d.X, d.Y + 1, d.R * .6f, d.R * .3f, new Color(20 / 255f, 14 / 255f, 10 / 255f, .4f), O_DECAL + 1);
            }
            else P.Ellipse(d.X, d.Y, d.R * 1.1f, d.R * .6f, new Color(30 / 255f, 20 / 255f, 20 / 255f, .35f), O_DECAL);
        }

        void DrawHazards(Battle B)
        {
            var st = B.St; float cy = (st.Fy0 + st.Fy1) / 2;
            for (int side = 0; side < 2; side++)
            {
                var hz = B.Sides[side].Hz; float x0 = side == 1 ? st.Fx1 - 150 : st.Fx0 + 40;
                var r = new System.Random(77 + side); float R() => (float)r.NextDouble();
                if (hz.Rocks > 0) for (int i = 0; i < 6; i++) { float x = x0 + R() * 110, y = cy - 120 + R() * 240 + Mathf.Sin(B.T * 2 + i) * 4; P.Rect(x - 6, y - 6, 12, 12, C("#120e1c"), O_HAZ); P.Rect(x - 5, y - 5, 10, 10, C("#c49a6c"), O_HAZ + 1); }
                for (int i = 0; i < hz.Spikes * 5; i++) { float x = x0 + R() * 110, y = cy - 140 + R() * 280; P.Rect(x - 3, y - 4, 6, 8, C("#5a4a3a"), O_HAZ); }
                for (int i = 0; i < hz.TSpikes * 5; i++) { float x = x0 + R() * 110, y = cy - 140 + R() * 280; P.Rect(x - 3, y - 4, 6, 8, C("#b86ad8"), O_HAZ); }
            }
        }

        // 扇形：放射状の線で塗る
        void Sector(float ox, float oy, float ang, float rad, float half, Color col, int order, float thick = 6)
        {
            int n = Mathf.Max(6, Mathf.RoundToInt(half * 2 * rad / 8));
            for (int i = 0; i <= n; i++) { float a2 = ang - half + half * 2 * i / n; P.Sprite(PixelArt.PixelLeft, ox, oy, rad, thick, col, order, a2); }
        }
        void ArcDots(float ox, float oy, float ang, float rad, float half, Color col, int order, float size = 3)
        {
            int n = Mathf.Max(6, Mathf.RoundToInt(half * 2 * rad / 6));
            for (int i = 0; i <= n; i++) { float a2 = ang - half + half * 2 * i / n; P.Rect(ox + Mathf.Cos(a2) * rad - size / 2, oy + Mathf.Sin(a2) * rad - size / 2, size, size, col, order); }
        }
        void BeamRect(float x, float y, float ang, float len, float wid, Color col, int order) => P.Sprite(PixelArt.PixelLeft, x, y, len, wid, col, order, ang);

        void DrawTele(Battle B, Fighter f)
        {
            var cur = f.Cur; var m = cur.M;
            if (m.K == "melee" && cur.Id == "tackle") return;
            float prog = Mathf.Clamp01(cur.T / cur.Wind);
            var baseC = f.Side == 1 ? new Color(1, 60 / 255f, 70 / 255f) : new Color(90 / 255f, 190 / 255f, 1);
            bool blink = prog > .7f && Mathf.FloorToInt(B.T * 18) % 2 == 0;
            var outline = blink ? A(Color.white, .95f) : A(baseC, .9f);
            var fill = A(baseC, .14f); var inner = A(baseC, .2f + prog * .25f);
            switch (m.K)
            {
                case "proj":
                    {
                        float c = Mathf.Cos(cur.Ang), s = Mathf.Sin(cur.Ang), L = m.Aim == "dir" ? 300 : 110;
                        for (float i = 24; i < L * prog + 24; i += 12) P.Rect(f.X + c * i - 2, f.Y - BODY + s * i - 2, 4, 4, A(baseC, .8f), O_TELE);
                        return;
                    }
                case "aoe": Circle(f.X, f.Y, m.Rad, prog, fill, inner, outline); return;
                case "strike": Circle(cur.Tx, cur.Ty, m.Rad, prog, fill, inner, outline); return;
                case "multi": foreach (var p in cur.Pts) Circle(p.x, p.y, m.Rad, prog, fill, inner, outline); return;
                case "cone": Sector(f.X, f.Y, cur.Ang, m.Rad, m.Half, fill, O_TELE); Sector(f.X, f.Y, cur.Ang, m.Rad * prog, m.Half, inner, O_TELE + 1); ArcDots(f.X, f.Y, cur.Ang, m.Rad, m.Half, outline, O_TELE + 2); return;
                case "swipe":
                case "melee":
                    { float rr = (m.Rad > 0 ? m.Rad : 40) + f.R; Sector(f.X, f.Y, cur.Ang, rr, .95f, fill, O_TELE); Sector(f.X, f.Y, cur.Ang, rr * prog, .95f, inner, O_TELE + 1); ArcDots(f.X, f.Y, cur.Ang, rr, .95f, outline, O_TELE + 2); return; }
                case "beam":
                case "dash":
                    {
                        float w = m.K == "dash" ? f.R * 2 + 8 : m.Wid;
                        BeamRect(f.X, f.Y, cur.Ang, m.Len, w, fill, O_TELE); BeamRect(f.X, f.Y, cur.Ang, m.Len * prog, w, inner, O_TELE + 1);
                        float c = Mathf.Cos(cur.Ang), s = Mathf.Sin(cur.Ang);
                        BeamRect(f.X - s * w / 2, f.Y + c * w / 2, cur.Ang, m.Len, 2, outline, O_TELE + 2); BeamRect(f.X + s * w / 2, f.Y - c * w / 2, cur.Ang, m.Len, 2, outline, O_TELE + 2);
                        return;
                    }
                default: // 補助わざ：じぶんの まわりに ひかる輪
                    P.RingE(f.X, f.Y, 26 + prog * 10, 12 + prog * 4, A(C("#ffd166"), .4f + prog * .5f), O_TELE); return;
            }
        }
        void Circle(float x, float y, float r, float prog, Color fill, Color inner, Color outline)
        {
            P.Ellipse(x, y, r, r, fill, O_TELE); P.Ellipse(x, y, r * prog, r * prog, inner, O_TELE + 1); P.RingE(x, y, r, r, outline, O_TELE + 2);
        }

        void DrawTrainer(Battle B, Side sd)
        {
            var t = sd.Trainer;
            float jump = t.Shout > 0 ? Mathf.Round(Mathf.Abs(Mathf.Sin(t.Shout * 12)) * 5) : 0;
            int o = Ord(t.Y);
            P.Ellipse(t.X, t.Y, 14, 5.6f, new Color(10 / 255f, 8 / 255f, 18 / 255f, .35f), o - 5);
            P.Sprite(t.Spr, t.X, t.Y - jump, sd == B.Sides[0] ? 2 : -2, 2, Color.white, o);
            if (t.Shout > .2f) WorldTexts.Add((new Vector2(t.X + (sd == B.Sides[0] ? 22 : -22), t.Y - 56), "!", Color.white, 16));
        }

        static readonly Dictionary<string, string> StCol = new Dictionary<string, string> { { "brn", "#ff8a3d" }, { "par", "#ffd84a" }, { "psn", "#b86ad8" }, { "tox", "#8a3ab0" }, { "slp", "#9fb0ff" }, { "frz", "#9fe8ff" } };

        void DrawFighter(Battle B, Fighter f)
        {
            if (f.State == "bench" || f.State == "capt") return;
            float alpha = 1, sy = 1, sx = 1, oy = 0;
            if (f.State == "faint") { alpha = Mathf.Clamp01(f.StT / 1.2f); sy = .4f + .6f * alpha; }
            if (f.State == "enter" || f.State == "return") sx = sy = Mathf.Max(.05f, f.Scale);
            if (f.State == "wind" && f.Cur != null && f.Cur.M.K != "melee") sy = 1 - .1f * Mathf.Clamp01(f.Cur.T / f.Cur.Wind);
            if (f.State == "stun") { sx = 1.08f; sy = .92f; }
            if (f.State == "lag") { sy = 1 + Mathf.Sin(B.T * 14) * .04f; sx = 2 - sy; }
            if (f.State == "dodge") alpha = .75f;
            float bob = f.Moving ? (Mathf.FloorToInt(f.Walk * 9) % 2) * 2 : 0;
            if (f.Sp.Flying) oy = -8 - Mathf.Round(Mathf.Sin(B.T * 4 + f.Side) * 3);
            var ms = PixelArt.Mon(f.Mon.sid);
            int o = Ord(f.Y);
            P.Ellipse(f.X, f.Y, ms.W * .62f, ms.W * .25f, new Color(10 / 255f, 8 / 255f, 18 / 255f, .35f), o - 5);
            var spr = (f.Flash > 0 || f.State == "enter" || f.State == "return") ? ms.White : ms.Normal;
            P.Sprite(spr, f.X, f.Y + 3 + oy - bob, 2 * sx * f.Face, 2 * sy, A(Color.white, alpha), o);
            float top = Mathf.Round(f.Y + oy - ms.H * 2 - 6);
            if (f.State != "faint" && f.State != "enter" && f.State != "return")
            {
                // 頭上のHPバー
                float w = 46, x = Mathf.Round(f.X - w / 2), k = f.Hp / f.MaxHp;
                P.Rect(x - 1, top - 1, w + 2, 7, C("#120e1c"), o + 3);
                P.Rect(x, top, w, 5, C("#3a3350"), o + 4);
                P.Rect(x, top, Mathf.Round(w * k), 5, k > .5f ? (f.Side == 1 ? C("#ff7a6a") : C("#5ab8ff")) : k > .2f ? C("#ffd166") : C("#ff4a4a"), o + 5);
                if (f.Side == 0) { P.Rect(f.X - 4, top - 7, 9, 2, C("#5ab8ff"), o + 5); P.Rect(f.X - 2, top - 5, 5, 2, C("#5ab8ff"), o + 5); }
                DrawConditions(B, f, top, oy, ms, o);
            }
            if (f.Dizzy > 0 && f.State != "faint")
                for (int i = 0; i < 4; i++) { float an = B.T * 5 + i * Mathf.PI / 2; P.Star(f.X + Mathf.Cos(an) * 24, top - 4 + Mathf.Sin(an) * 7, 5, C("#ffd84a"), o + 7); }
        }

        void DrawConditions(Battle B, Fighter f, float top, float oy, PixelArt.MonSprites ms, int o)
        {
            float h = ms.H * 2, cx = f.X, cy = f.Y - h / 2 + oy;
            if (f.State == "lag")
            { // 交代直後の スキ：のこり時間バー
                float w = 46, x = Mathf.Round(cx - w / 2), k = Mathf.Clamp01(f.StT / (f.LagMax > 0 ? f.LagMax : Battle.SwapLag));
                P.Rect(x - 1, top + 6, w + 2, 5, C("#120e1c"), o + 3);
                P.Rect(x, top + 7, Mathf.Round(w * k), 3, Mathf.FloorToInt(B.T * 8) % 2 == 1 ? C("#ff9a8a") : C("#ff6b5b"), o + 4);
                WorldTexts.Add((new Vector2(cx, top - 10), "スキ", C("#ff9a8a"), 11));
            }
            if (f.Status != "")
            {
                WorldTexts.Add((new Vector2(cx, top - 10), Battle.StatusNames[f.Status], C(StCol[f.Status]), 10));
                if (f.Status == "frz") P.Rect(cx - ms.W, cy - h / 2, ms.W * 2, h, new Color(160 / 255f, 230 / 255f, 1, .45f), o + 2);
                if (f.Status == "slp" && Mathf.FloorToInt(B.T * 2) % 2 == 1) WorldTexts.Add((new Vector2(cx + 22, top - 18 - (B.T * 10 % 10)), "Z", Color.white, 14));
            }
            if (f.V.Protect > 0) { P.Ellipse(cx, cy, ms.W * 1.25f, h * .7f, new Color(160 / 255f, 240 / 255f, 1, .18f), o + 2); P.RingE(cx, cy, ms.W * 1.25f, h * .7f, new Color(160 / 255f, 240 / 255f, 1, .7f), o + 2); }
            if (f.V.Sub > 0) P.Sprite(ms.White, f.X - f.Face * 26, f.Y + 4, 1.2f * f.Face, 1.2f, A(Color.white, .55f), o - 1);
            if (f.V.CounterT > 0) P.RingE(cx, cy, ms.W * 1.1f, h * .62f, A(Color.white, .8f), o + 2);
            if (f.V.DBond > 0) P.Ellipse(cx, cy, ms.W * 1.1f, h * .62f, new Color(60 / 255f, 20 / 255f, 80 / 255f, .35f), o + 2);
            if (f.V.Confuse > 0) for (int i = 0; i < 3; i++) { float an = -B.T * 6 + i * 2.1f; P.Rect(cx + Mathf.Cos(an) * 18 - 2, top - 14 + Mathf.Sin(an) * 5 - 2, 4, 4, Color.white, o + 6); }
        }

        void DrawProj(Battle B, Proj p)
        {
            float R = p.R; var t = p.M.T;
            P.Ellipse(p.X, p.Y + BODY, R, R * .4f, new Color(10 / 255f, 8 / 255f, 18 / 255f, .25f), O_PROJ - 1);
            if (t == "fire") { P.Ellipse(p.X, p.Y, R + 2, R + 2, C("#c0281e"), O_PROJ); P.Ellipse(p.X, p.Y, R, R, C("#ff7a2a"), O_PROJ + 1); P.Ellipse(p.X - 1, p.Y - 1, R * .5f, R * .5f, C("#fff2a0"), O_PROJ + 2); }
            else if (t == "water") { P.Ellipse(p.X, p.Y, R + 1.5f, R + 1.5f, C("#1d3d7a"), O_PROJ); P.Ellipse(p.X, p.Y, R, R, C("#7ac8ff"), O_PROJ + 1); P.Rect(p.X - R * .5f, p.Y - R * .5f, 2, 2, Color.white, O_PROJ + 2); }
            else if (t == "grass") { P.Sprite(PixelArt.Pixel, p.X, p.Y, R * 2 + 4, 6, C("#1e5a26"), O_PROJ, p.Rot); P.Sprite(PixelArt.Pixel, p.X, p.Y, R * 2, 3, C("#7be07b"), O_PROJ + 1, p.Rot); }
            else if (t == "wind") { P.RingE(p.X, p.Y, R, R, C("#e8ffff"), O_PROJ); P.RingE(p.X, p.Y, R * .55f, R * .55f, C("#7fd8d0"), O_PROJ + 1); }
            else { P.Ellipse(p.X, p.Y, R + 1, R + 1, C("#120e1c"), O_PROJ); P.Ellipse(p.X, p.Y, R, R, Battle.TC(t), O_PROJ + 1); P.Ellipse(p.X - R * .3f, p.Y - R * .3f, R * .35f, R * .35f, A(Color.white, .7f), O_PROJ + 2); }
        }

        void DrawCapsule(Battle B)
        {
            var c = B.Catch; float ox = 0;
            if (c.Phase == "shake" && c.T < .35f) ox = Mathf.Round(Mathf.Sin(c.T / .6f * Mathf.PI * 2) * 2);
            float x = Mathf.Round(c.X) + ox, y = Mathf.Round(c.Y);
            P.Rect(x - 9, y - 8, 18, 17, C("#120e1c"), O_CAP);
            P.Rect(x - 8, y - 7, 16, 15, C("#3ad0c8"), O_CAP + 1);
            P.Rect(x - 8, y + 4, 16, 4, C("#1e8a84"), O_CAP + 2);
            P.Rect(x - 8, y, 16, 2, C("#ffd166"), O_CAP + 2);
            P.Rect(x - 6, y - 5, 4, 2, C("#e8ffff"), O_CAP + 2);
            if (c.Phase == "shake") for (int i = 0; i < c.Shakes; i++) P.Star(x - 12 + i * 12, y - 18, 4, C("#ffd84a"), O_CAP + 3);
        }

        void DrawFx(Battle B, Fx fx)
        {
            float k = fx.Life / fx.Max, al = Mathf.Clamp01(k * 1.4f);
            switch (fx.Type)
            {
                case "swipe": ArcDots(fx.X, fx.Y, fx.Ang, 28, 1, A(fx.Col, al), O_FX, 4); break;
                case "sector": Sector(fx.X, fx.Y, fx.Ang, fx.Rad * (1.05f - k * .3f), fx.Half, A(fx.Col, al * .4f), O_FX); ArcDots(fx.X, fx.Y - BODY, fx.Ang, fx.Rad * (1.05f - k * .3f), fx.Half, A(Color.white, al), O_FX + 1, 4); break;
                case "impact":
                    {
                        float rr = fx.Rad * (1.2f - k * .8f);
                        P.RingE(fx.X, fx.Y, rr, rr, A(C("#e8c04a"), al), O_FX);
                        for (int i = 0; i < 8; i++) { float an = i * Mathf.PI / 4 + fx.Rot; P.Rect(fx.X + Mathf.Cos(an) * rr * 1.25f - 1, fx.Y + Mathf.Sin(an) * rr * 1.25f - 1, 3, 3, A(C("#fff6c0"), al), O_FX + 1); }
                        break;
                    }
                case "beam":
                    if (fx.Look == "spikes" || fx.Look == "crack")
                    {
                        float c = Mathf.Cos(fx.Ang), s = Mathf.Sin(fx.Ang);
                        for (float d = 10; d < fx.Len; d += 22)
                        {
                            float hgt = (fx.Look == "spikes" ? 26 : 10) * k, bx = fx.X + c * d, by = fx.Y + BODY + s * d;
                            P.Rect(bx - 7, by - hgt - 1, 14, hgt + 2, A(C("#120e1c"), al), O_FX); P.Rect(bx - 6, by - hgt, 12, hgt, A(fx.Col, al), O_FX + 1);
                        }
                    }
                    else { BeamRect(fx.X, fx.Y, fx.Ang, fx.Len, fx.Wid * k, A(fx.Col, al), O_FX); BeamRect(fx.X, fx.Y, fx.Ang, fx.Len, fx.Wid / 2.5f * k, A(Color.white, al), O_FX + 1); }
                    break;
                case "ring":
                case "pop": { float rr = fx.Rad * (1.1f - k * .6f); P.RingE(fx.X, fx.Y, rr, rr * .6f, A(fx.Col, al), O_FX); break; }
                case "bolt":
                    {
                        float x = fx.X, y = fx.Y - 240;
                        while (y < fx.Y) { float nx = fx.X + Util.Rand(-12, 12), ny = Mathf.Min(y + 20, fx.Y); P.Line(x, y, nx, ny, 3, A(C("#fff8c0"), al), O_FX); x = nx; y = ny; }
                        float rr = fx.Rad * (1.1f - k * .5f); P.RingE(fx.X, fx.Y, rr, rr * .55f, A(fx.Col, al), O_FX);
                        break;
                    }
                case "rocks":
                    for (int i = 0; i < 4; i++) { float ry = fx.Y - k * 100 - i * 10, rx = fx.X + (i - 1.5f) * 14; P.Rect(rx - 9, ry - 9, 18, 18, A(C("#120e1c"), al), O_FX); P.Rect(rx - 8, ry - 8, 16, 16, A(C("#a88a6c"), al), O_FX + 1); P.Rect(rx - 6, ry - 6, 6, 4, A(C("#d8c0a0"), al), O_FX + 2); }
                    { float rr = fx.Rad * (1.1f - k * .5f); P.RingE(fx.X, fx.Y, rr, rr * .55f, A(fx.Col, al), O_FX); }
                    break;
                case "beamIn": P.Line(fx.X0, fx.Y0, fx.X1, fx.Y1, 4, A(Color.white, al), O_FX); P.Line(fx.X0, fx.Y0, fx.X1, fx.Y1, 2, A(C("#9ff0ff"), al), O_FX + 1); break;
                case "ray": P.Line(fx.X0, fx.Y0, fx.X1, fx.Y1, 4, A(fx.Col, al), O_FX); break;
                case "toss":
                    {
                        float t = 1 - k, x = fx.X0 + (fx.X1 - fx.X0) * t, y = fx.Y0 + (fx.Y1 - fx.Y0) * t - Mathf.Sin(t * Mathf.PI) * 90;
                        for (int i = 0; i < 3; i++) { P.Rect(x - 5 + i * 9, y - 5 + (i % 2) * 6, 9, 9, C("#120e1c"), O_FX); P.Rect(x - 4 + i * 9, y - 4 + (i % 2) * 6, 7, 7, fx.Col, O_FX + 1); }
                        break;
                    }
            }
        }
    }
}
