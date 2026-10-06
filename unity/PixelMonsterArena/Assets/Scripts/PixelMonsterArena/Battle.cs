using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace PixelMonsterArena
{
    public class MoveExec
    {
        public string Id; public Move M; public float T, Wind, Ang, Tx, Ty, D; public int Uid; public bool Hit;
    }

    public class Plan { public bool Will; public float At; }

    public class Fighter
    {
        public MonData Mon; public Species Sp; public int Side, Lvl;
        public float Hp, MaxHp, Atk, Def, Speed;
        public float X, Y, R = 19; public int Face;
        public string State = "bench"; public float StT;
        public Dictionary<string, float> Cd = new Dictionary<string, float>();
        public string Queued; public MoveExec Cur;
        public float Inv, Flash, Kx, Ky, DodgeCd, AiT = 1, Dizzy, Scale = 1, Walk, GhostT, SplashT, StratT, Dvx, Dvy;
        public Plan Plan; public int PlanFor; public int Strafe = 1;
        public bool Fainted, Moving;
        public float CdOf(string id) => Cd.TryGetValue(id, out var v) ? v : 0;
    }

    public class Proj { public Fighter F; public int Side; public Move M; public float X, Y, Vx, Vy, R, Life, Rot; public bool Rolled, Will; }
    public class Fx { public string Type; public float X, Y, Ang, Len, Wid, Rad, Life, Max, Rot, X0, Y0, X1, Y1; public Color Col; public string Sid; public int Face; }
    public class Part { public float X, Y, Vx, Vy, Life, Max, G; public Color Col; public int Size; }
    /// <summary>Big: 0=ふつう 1=大きい 2=マンガ文字（BONK! など）</summary>
    public class FText { public float X, Y, Life, Max; public string Txt; public Color Col; public int Big; }
    public class Decal { public float X, Y, R; public string Kind; public int Seed; }
    public class TrainerInfo { public string Name; public Sprite Spr; public float X, Y, Shout; }
    public class Side { public List<Fighter> Fs; public int Act; public TrainerInfo Trainer; }
    public class CatchO { public string Phase; public float T, Sx, Sy, Tx, Ty, X, Y, P; public int Shakes; }

    public class BattleConfig
    {
        public string Kind, Field, Title, Intro;
        public List<MonData> Enemies;
        public float Skill;
        public TrainerInfo Trainer;
    }

    /// <summary>リアルタイムバトルの中身（描画は BattleRenderer が担当）。index.html の処理をそのまま移植。</summary>
    public class Battle
    {
        const float K = Data.K, BODY = Data.Body;

        public readonly SaveData S;
        public readonly string Kind;
        public readonly Stage St;
        public readonly Side[] Sides;
        public readonly List<Proj> Projs = new List<Proj>();
        public readonly List<Part> Parts = new List<Part>();
        public readonly List<FText> Texts = new List<FText>();
        public readonly List<Fx> Fxs = new List<Fx>();
        public readonly List<Decal> Decals = new List<Decal>();
        public float T, ModeT, Cheer = .3f, Shake, Hitstop, EndT;
        public string Mode = "intro";
        public bool Paused;
        public CatchO Catch;
        public string Result;
        public readonly List<string> ResLines = new List<string>();
        public Vector3 Cam; // x, y, zoom
        public readonly float Skill;
        public Vector2 InputVec; public bool InputActive;
        public event Action<string> OnSay;

        int _uidc, _sent, _swapTo;
        readonly Dictionary<int, int> _exp = new Dictionary<int, int>();
        (int side, int idx, float t)? _pendingSend;

        public Battle(SaveData save, BattleConfig cfg)
        {
            S = save; Kind = cfg.Kind; Skill = cfg.Skill;
            St = cfg.Kind == "wild" ? Stage.Wild() : Stage.Stadium(cfg.Field);
            var pf = S.party.Take(3).Select(m => MkFighter(m, 0)).ToList();
            var ef = cfg.Enemies.Select(m => MkFighter(m, 1)).ToList();
            var trP = new TrainerInfo { Name = "あなた", Spr = PixelArt.Trainer("#e84a5f", "#3a6ee8"), X = St.Trainers[0].x, Y = St.Trainers[0].y };
            TrainerInfo trE = null;
            if (cfg.Trainer != null) { trE = cfg.Trainer; trE.X = St.Trainers[1].x; trE.Y = St.Trainers[1].y; }
            Sides = new[] { new Side { Fs = pf, Trainer = trP }, new Side { Fs = ef, Trainer = trE } };
            Cam = new Vector3(St.W / 2f, St.H / 2f, 320f / St.W);
        }

        public void Start(string intro) => Say(intro);

        static Fighter MkFighter(MonData mon, int side)
        {
            var st = Data.CalcStats(mon);
            return new Fighter
            {
                Mon = mon, Sp = Data.Species[mon.sid], Side = side, Lvl = mon.lvl, Hp = st.Hp, MaxHp = st.Hp, Atk = st.Atk, Def = st.Def,
                Speed = (46 + st.Spd * .5f) * K, Face = side == 1 ? -1 : 1,
            };
        }

        public Fighter Active(int side) { var sd = Sides[side]; return sd.Fs.Count > sd.Act ? sd.Fs[sd.Act] : null; }
        Fighter Opp(Fighter f) => Active(1 - f.Side);
        static bool Targetable(Fighter f) => f != null && (f.State == "free" || f.State == "wind" || f.State == "dash" || f.State == "act" || f.State == "stun" || f.State == "dodge");
        static float Dist(Fighter a, Fighter b) => Mathf.Sqrt((a.X - b.X) * (a.X - b.X) + (a.Y - b.Y) * (a.Y - b.Y));

        // ---------- 演出 ----------
        public void Say(string t) => OnSay?.Invoke(t);
        void Burst(float x, float y, Color col, int n, float spd, float life)
        {
            for (int i = 0; i < n; i++)
            {
                float a = Util.Value * Mathf.PI * 2, s = Util.Rand(spd * .3f, spd);
                Parts.Add(new Part { X = x, Y = y, Vx = Mathf.Cos(a) * s * K, Vy = (Mathf.Sin(a) * s - 20) * K, Life = Util.Rand(life * .5f, life), Max = life, Col = col, Size = Util.Value < .3f ? 3 : 2, G = 160 });
            }
        }
        void PopText(float x, float y, string txt, Color col, int big = 0) => Texts.Add(new FText { X = x, Y = y, Txt = txt, Col = col, Life = .9f, Max = .9f, Big = big });
        void AddDecal(float x, float y, float r, string kind)
        {
            if (x < St.Fx0 || x > St.Fx1 || y < St.Fy0 || y > St.Fy1) return;
            Decals.Add(new Decal { X = x, Y = y, R = r, Kind = kind, Seed = Util.RandI(0, 999) });
            if (Decals.Count > 40) Decals.RemoveAt(0);
        }
        static Color TC(string t) => Data.Types[t].C;

        void SendOut(int side, int idx)
        {
            var sd = Sides[side]; sd.Act = idx;
            var f = sd.Fs[idx];
            f.X = side == 1 ? St.Fx1 - 120 : St.Fx0 + 120; f.Y = (St.Fy0 + St.Fy1) / 2 + Util.Rand(-20, 20);
            f.State = "enter"; f.StT = .5f; f.Inv = .6f; f.Cur = null; f.Queued = null; f.Kx = f.Ky = 0; f.Face = side == 1 ? -1 : 1; f.AiT = Util.Rand(.6f, 1.2f); f.Scale = 0;
            var tr = sd.Trainer;
            if (tr != null) { Fxs.Add(new Fx { Type = "beamIn", X0 = tr.X, Y0 = tr.Y - 30, X1 = f.X, Y1 = f.Y - 20, Life = .45f, Max = .45f }); tr.Shout = .7f; }
            else Burst(f.X, f.Y - 4, Util.Hex("#3f9040"), 16, 90, .5f);
            Burst(f.X, f.Y - 10, Color.white, 12, 80, .45f);
            Cheer = Mathf.Max(Cheer, .7f);
            if (side == 0) Say($"いけっ！ {f.Sp.N}！");
            else if (tr != null) Say($"{tr.Name}は {f.Sp.N}を くりだした！");
            else Say($"あっ！ やせいの {f.Sp.N}（Lv{f.Lvl}）が とびだしてきた！");
        }

        // ---------- 当たり判定 ----------
        bool InZone(MoveExec cur, Fighter owner, float x, float y, float r)
        {
            var m = cur.M;
            if (m.K == "aoe") return Hyp(x - owner.X, y - owner.Y) <= m.Rad + r;
            if (m.K == "strike") return Hyp(x - cur.Tx, y - cur.Ty) <= m.Rad + r;
            if (m.K == "beam" || m.K == "dash")
            {
                float wid = m.K == "dash" ? owner.R * 2 + 8 : m.Wid;
                float c = Mathf.Cos(cur.Ang), s = Mathf.Sin(cur.Ang), dx = x - owner.X, dy = y - owner.Y;
                float along = dx * c + dy * s, perp = -dx * s + dy * c;
                return along >= -10 && along <= m.Len + 10 && Mathf.Abs(perp) <= wid / 2 + r;
            }
            return false;
        }
        static float Hyp(float a, float b) => Mathf.Sqrt(a * a + b * b);
        void ClampF(Fighter f) { f.X = Util.Clamp(f.X, St.Fx0 + f.R, St.Fx1 - f.R); f.Y = Util.Clamp(f.Y, St.Fy0 + f.R, St.Fy1 - f.R); }

        // ---------- わざ ----------
        void BeginMove(Fighter f, string id)
        {
            var o = Opp(f); if (o == null) return;
            var m = Data.Moves[id];
            f.Cur = new MoveExec { Id = id, M = m, Wind = m.Wind, Ang = Mathf.Atan2(o.Y - f.Y, o.X - f.X), Uid = ++_uidc, Tx = o.X, Ty = o.Y };
            f.Cd[id] = m.Cd;
            f.State = "wind";
            if (m.K != "melee")
            {
                Say($"{(f.Side == 0 ? "" : (Kind == "wild" ? "やせいの " : "あいての "))}{f.Sp.N}の {m.N}！");
                if (Sides[f.Side].Trainer != null) Sides[f.Side].Trainer.Shout = .6f;
            }
        }

        void FireMove(Fighter f)
        {
            var cur = f.Cur; var m = cur.M; var o = Opp(f);
            var col = TC(m.T);
            if (o != null && (m.K == "proj" || m.K == "melee")) cur.Ang = Mathf.Atan2(o.Y - f.Y, o.X - f.X);
            switch (m.K)
            {
                case "melee":
                    Fxs.Add(new Fx { Type = "swipe", X = f.X, Y = f.Y - BODY, Ang = cur.Ang, Life = .14f, Max = .14f, Col = Color.white });
                    if (Targetable(o) && Dist(f, o) <= f.R + o.R + 20) Hit(f, o, m, cur.Ang);
                    f.State = "act"; f.StT = .22f; break;
                case "proj":
                    {
                        int n = m.Cnt;
                        for (int i = 0; i < n; i++)
                        {
                            float a = cur.Ang + (n > 1 ? (i - (n - 1) / 2f) * m.Spread : 0);
                            Projs.Add(new Proj { F = f, Side = f.Side, M = m, X = f.X + Mathf.Cos(a) * 20, Y = f.Y - BODY + Mathf.Sin(a) * 20, Vx = Mathf.Cos(a) * m.Spd, Vy = Mathf.Sin(a) * m.Spd, R = m.R, Life = m.Life > 0 ? m.Life : 1.8f });
                        }
                        f.State = "act"; f.StT = .25f; break;
                    }
                case "beam":
                    Fxs.Add(new Fx { Type = "beam", X = f.X, Y = f.Y - BODY, Ang = cur.Ang, Len = m.Len, Wid = m.Wid, Col = col, Life = .3f, Max = .3f });
                    Shake = Mathf.Max(Shake, 3);
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, cur.Ang);
                    f.State = "act"; f.StT = .35f; break;
                case "aoe":
                    Fxs.Add(new Fx { Type = "ring", X = f.X, Y = f.Y, Rad = m.Rad, Col = col, Life = .35f, Max = .35f });
                    Shake = Mathf.Max(Shake, 6);
                    Burst(f.X, f.Y, col, 24, 160, .55f);
                    AddDecal(f.X, f.Y, m.Rad * .45f, m.T == "fire" ? "scorch" : "crater");
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, Mathf.Atan2(o.Y - f.Y, o.X - f.X));
                    f.State = "act"; f.StT = .4f; break;
                case "strike":
                    Fxs.Add(new Fx { Type = m.T == "elec" ? "bolt" : m.T == "rock" ? "rocks" : "pop", X = cur.Tx, Y = cur.Ty, Rad = m.Rad, Col = col, Life = .35f, Max = .35f });
                    Shake = Mathf.Max(Shake, 5);
                    Burst(cur.Tx, cur.Ty, col, 18, 130, .5f);
                    AddDecal(cur.Tx, cur.Ty, m.Rad * .5f, m.T == "elec" ? "scorch" : "crater");
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, Mathf.Atan2(o.Y - cur.Ty, o.X - cur.Tx));
                    f.State = "act"; f.StT = .3f; break;
                case "dash":
                    cur.D = 0; cur.Hit = false; f.State = "dash"; break;
            }
        }

        static readonly string[] Comic = { "BONK!", "POW!", "WHAM!", "SMASH!" };
        bool Hit(Fighter att, Fighter def, Move m, float ang)
        {
            if (def.Inv > 0) { PopText(def.X, def.Y - 66, "かわした！", Util.Hex("#7fd8ff")); Burst(def.X, def.Y - BODY, Util.Hex("#7fd8ff"), 6, 50, .3f); return false; }
            float eff = m.T == "normal" ? 1 : Data.Eff(m.T, def.Sp.Type);
            float stab = m.T == att.Sp.Type ? 1.25f : 1;
            int dmg = Mathf.Max(1, Mathf.RoundToInt(m.Pow * att.Atk / def.Def * stab * eff * Util.Rand(.88f, 1.12f)));
            def.Hp = Mathf.Max(0, def.Hp - dmg); def.Flash = .12f;
            bool heavy = m.Pow >= 19;
            def.Cur = null; def.Queued = null; def.State = "stun"; def.StT = heavy ? .45f : .25f;
            def.Kx = Mathf.Cos(ang) * (heavy ? 230 : 140) * K; def.Ky = Mathf.Sin(ang) * (heavy ? 230 : 140) * K;
            Hitstop = Mathf.Max(Hitstop, heavy ? .08f : .04f);
            Shake = Mathf.Max(Shake, heavy ? 5 : 2);
            Cheer = Mathf.Min(1, Cheer + (heavy ? .7f : .3f));
            PopText(def.X + Util.Rand(-6, 6), def.Y - 66, dmg.ToString(), eff > 1 ? Util.Hex("#ffd166") : eff < 1 ? Util.Hex("#a49ac0") : Color.white, eff > 1 || heavy ? 1 : 0);
            Burst(def.X, def.Y - BODY, TC(m.T), heavy ? 16 : 8, 110, .4f);
            Fxs.Add(new Fx { Type = "impact", X = def.X, Y = def.Y - BODY, Rad = heavy ? 34 : 22, Rot = Util.Value, Life = .28f, Max = .28f });
            if (heavy || eff > 1) { PopText(def.X + Util.Rand(-10, 10), def.Y - 92, Util.Choice(Comic), Util.Hex("#ffd84a"), 2); def.Dizzy = 1; }
            if (eff > 1) Say("ばつぐんの いりょくだ！");
            else if (eff < 1) Say("あまり きいていない ようだ…");
            if (def.Hp <= 0) Faint(def);
            return true;
        }

        void Faint(Fighter f)
        {
            f.State = "faint"; f.StT = 1.2f; f.Cur = null; f.Queued = null;
            Cheer = 1; Shake = Mathf.Max(Shake, 6);
            Say($"{(f.Side == 0 ? "" : Kind == "wild" ? "やせいの " : "あいての ")}{f.Sp.N}は たおれた！");
            Burst(f.X, f.Y - BODY, Color.white, 24, 140, .7f);
            if (f.Side == 1)
            {
                var me = Active(0);
                if (me != null)
                {
                    _exp.TryGetValue(me.Mon.uid, out var e0);
                    _exp[me.Mon.uid] = e0 + Mathf.RoundToInt((f.Lvl * 6 + 4) * (Kind == "cup" ? 1.5f : 1));
                }
            }
        }

        void AfterFaint(Fighter f)
        {
            f.Fainted = true; f.State = "bench";
            var sd = Sides[f.Side];
            int next = sd.Fs.FindIndex(x => !x.Fainted && x.Hp > 0);
            if (next < 0) { EndBattle(f.Side == 0 ? "lose" : "win"); return; }
            _pendingSend = (f.Side, next, .5f);
        }

        // ---------- 回避 ----------
        (float, Func<float, float, bool>) ThreatDir(Fighter f, Fighter o)
        {
            if (o != null && o.Cur != null && o.State == "wind" && o.Cur.M.K != "proj" && o.Cur.M.K != "melee")
            {
                var cur = o.Cur; var m = cur.M; float b;
                if (m.K == "beam" || m.K == "dash")
                {
                    float s = Mathf.Sign(-(f.X - o.X) * Mathf.Sin(cur.Ang) + (f.Y - o.Y) * Mathf.Cos(cur.Ang)); if (s == 0) s = 1;
                    b = cur.Ang + s * Mathf.PI / 2;
                }
                else if (m.K == "aoe") b = Mathf.Atan2(f.Y - o.Y, f.X - o.X);
                else b = Mathf.Atan2(f.Y - cur.Ty, f.X - cur.Tx);
                return (b, (x, y) => InZone(cur, o, x, y, f.R));
            }
            Proj best = null; float bd = 1e9f;
            foreach (var p in Projs) if (p.Side != f.Side) { float d = Hyp(p.X - f.X, p.Y + 8 - f.Y); if (d < bd) { bd = d; best = p; } }
            if (best != null && bd < 140)
            {
                float a = Mathf.Atan2(best.Vy, best.Vx);
                float s = Mathf.Sign(-(f.X - best.X) * Mathf.Sin(a) + (f.Y - best.Y) * Mathf.Cos(a)); if (s == 0) s = 1;
                return (a + s * Mathf.PI / 2, (x, y) => false);
            }
            return (o != null ? Mathf.Atan2(f.Y - o.Y, f.X - o.X) + (Util.Value < .5f ? 1 : -1) * 1.2f : 0, (x, y) => false);
        }

        void StartDodge(Fighter f, float? dirOverride)
        {
            var o = Opp(f);
            float reach = 250 * K * .22f;
            float dir;
            if (dirOverride.HasValue) dir = dirOverride.Value;
            else
            {
                var (b, test) = ThreatDir(f, o);
                float[] cands = { b, b + .7f, b - .7f, b + 1.4f, b - 1.4f, b + Mathf.PI };
                float? pick = null;
                foreach (var c in cands)
                {
                    float ex = f.X + Mathf.Cos(c) * reach, ey = f.Y + Mathf.Sin(c) * reach;
                    if (!St.InField(ex, ey, f.R)) continue;
                    if (!test(ex, ey)) { pick = c; break; }
                    if (pick == null) pick = c;
                }
                dir = pick ?? b;
            }
            f.Cur = null; f.Queued = null;
            f.State = "dodge"; f.StT = .22f; f.Dvx = Mathf.Cos(dir) * 250 * K; f.Dvy = Mathf.Sin(dir) * 250 * K;
            f.Inv = .3f; f.DodgeCd = f.Side == 0 ? .9f : 1.4f; f.GhostT = 0;
        }

        // ---------- AI ----------
        void AiDodgeCheck(Fighter f, Fighter o)
        {
            bool isP = f.Side == 0;
            float skill = isP ? (S.auto ? .5f : 0) : Skill;
            if (skill <= 0 || f.DodgeCd > 0 || !(f.State == "free" || f.State == "act")) return;
            if (o != null && o.State == "wind" && o.Cur != null && o.Cur.M.K != "melee" && o.Cur.M.K != "proj")
            {
                if (f.PlanFor != o.Cur.Uid) { f.PlanFor = o.Cur.Uid; f.Plan = new Plan { Will = Util.Value < skill, At = Util.Rand(.12f, .4f) * o.Cur.Wind / .8f }; }
                if (f.Plan.Will && o.Cur.T >= f.Plan.At && InZone(o.Cur, o, f.X, f.Y, f.R)) { StartDodge(f, null); return; }
            }
            foreach (var p in Projs)
            {
                if (p.Side == f.Side) continue;
                float dx = f.X - p.X, dy = f.Y - BODY - p.Y, d = Hyp(dx, dy);
                if (d > 110) continue;
                if (!p.Rolled) { p.Rolled = true; p.Will = Util.Value < skill * .8f; }
                if (p.Will && (dx * p.Vx + dy * p.Vy) > 0) { StartDodge(f, null); return; }
            }
        }

        void AiMove(Fighter f, Fighter o, float dt, bool autoSpecial)
        {
            float d = Dist(f, o), ang = Mathf.Atan2(o.Y - f.Y, o.X - f.X);
            if (autoSpecial && f.Queued == null)
            {
                f.AiT -= dt;
                if (f.AiT <= 0)
                {
                    f.AiT = Util.Rand(.5f, 1.3f) * (f.Side == 1 ? (1.2f - Skill * .5f) : 1);
                    var ready = f.Sp.Moves.Where(id => f.CdOf(id) <= 0).ToList();
                    if (ready.Count > 0 && Util.Value < .75f) f.Queued = Util.Choice(ready);
                }
            }
            if (f.Queued != null)
            {
                var m = Data.Moves[f.Queued];
                float need = m.K == "dash" ? m.Len * .8f : m.K == "aoe" ? m.Rad * .75f : m.K == "beam" ? m.Len * .8f : 999;
                if (d <= need) { var q = f.Queued; f.Queued = null; BeginMove(f, q); return; }
                MoveDir(f, Mathf.Cos(ang), Mathf.Sin(ang), dt); return;
            }
            float reach = f.R + o.R + 14;
            if (d < reach && f.CdOf("tackle") <= 0) { BeginMove(f, "tackle"); return; }
            f.StratT -= dt;
            if (f.StratT <= 0) { f.StratT = Util.Rand(.4f, .9f); if (Util.Value < .3f) f.Strafe *= -1; }
            bool allCd = f.Sp.Moves.All(id => f.CdOf(id) > 1.2f);
            float pref = f.Sp.Style == "melee" ? 0 : f.Sp.Style == "mid" ? 96 : 160;
            if (allCd || !autoSpecial) pref = f.Sp.Style == "ranged" && autoSpecial ? 96 : 0;
            float k = Util.Clamp((d - pref) / 48, -1, 1), tang = ang + f.Strafe * Mathf.PI / 2;
            float mx = Mathf.Cos(ang) * k + Mathf.Cos(tang) * .6f, my = Mathf.Sin(ang) * k + Mathf.Sin(tang) * .6f;
            const float mg = 40;
            if (f.X < St.Fx0 + mg) mx += 1; if (f.X > St.Fx1 - mg) mx -= 1; if (f.Y < St.Fy0 + mg) my += 1; if (f.Y > St.Fy1 - mg) my -= 1;
            float L = Hyp(mx, my); if (L > 1) { mx /= L; my /= L; }
            MoveDir(f, mx, my, dt);
        }

        void MoveDir(Fighter f, float mx, float my, float dt)
        {
            float sp = f.Speed;
            if (St.Pools.Count > 0 && St.InPool(f.X, f.Y))
            {
                sp *= f.Sp.Type == "water" ? 1.2f : .6f;
                f.SplashT -= dt;
                if (f.SplashT <= 0 && (mx != 0 || my != 0)) { f.SplashT = .12f; Parts.Add(new Part { X = f.X + Util.Rand(-5, 5), Y = f.Y, Vx = Util.Rand(-20, 20), Vy = -40, Life = .3f, Max = .3f, Col = Util.Hex("#bfe4ff"), Size = 2, G = 200 }); }
            }
            f.X += mx * sp * dt; f.Y += my * sp * dt;
            f.Moving = Hyp(mx, my) > .15f; if (f.Moving) f.Walk += dt;
        }

        // ---------- 1体ぶんの更新 ----------
        void UpdateFighter(Fighter f, float dt)
        {
            if (f == null) return;
            foreach (var key in f.Cd.Keys.ToList()) f.Cd[key] = Mathf.Max(0, f.Cd[key] - dt);
            f.DodgeCd = Mathf.Max(0, f.DodgeCd - dt); f.Inv = Mathf.Max(0, f.Inv - dt); f.Flash -= dt; f.Dizzy = Mathf.Max(0, f.Dizzy - dt);
            f.Moving = false;
            var o = Opp(f); bool oT = Targetable(o);
            if (oT && f.State != "dodge" && f.State != "dash") f.Face = o.X >= f.X ? 1 : -1;
            switch (f.State)
            {
                case "bench": case "capt": return;
                case "enter":
                    f.StT -= dt; f.Scale = Util.Clamp(1 - f.StT / .5f, 0, 1); if (f.StT <= 0) { f.State = "free"; f.Scale = 1; }
                    break;
                case "return":
                    f.StT -= dt; f.Scale = Util.Clamp(f.StT / .3f, 0, 1);
                    if (f.StT <= 0) { f.State = "bench"; f.Scale = 1; _pendingSend = (f.Side, _swapTo, .2f); }
                    return;
                case "faint":
                    f.StT -= dt; if (f.StT <= 0) AfterFaint(f); return;
                case "free":
                    {
                        if (!oT) { if (f.Side == 0 && InputActive) MoveDir(f, InputVec.x, InputVec.y, dt); break; }
                        AiDodgeCheck(f, o);
                        if (f.State != "free") break;
                        if (f.Side == 0 && !S.auto)
                        {
                            if (f.Queued != null)
                            {
                                var m = Data.Moves[f.Queued]; float d = Dist(f, o);
                                float need = m.K == "dash" ? m.Len * .85f : m.K == "aoe" ? m.Rad * .8f : m.K == "melee" ? f.R + o.R + 18 : 999;
                                if (d <= need) { var q = f.Queued; f.Queued = null; BeginMove(f, q); }
                                else if (InputActive) MoveDir(f, InputVec.x, InputVec.y, dt);
                                else { float a = Mathf.Atan2(o.Y - f.Y, o.X - f.X); MoveDir(f, Mathf.Cos(a), Mathf.Sin(a), dt); }
                            }
                            else if (InputActive) MoveDir(f, InputVec.x, InputVec.y, dt);
                        }
                        else if (f.Side == 0)
                        {
                            if (InputActive && f.Queued == null) MoveDir(f, InputVec.x, InputVec.y, dt); else AiMove(f, o, dt, true);
                        }
                        else AiMove(f, o, dt, true);
                        break;
                    }
                case "wind":
                    {
                        var cur = f.Cur; cur.T += dt;
                        if (oT && (cur.M.K == "beam" || cur.M.K == "dash") && cur.T < cur.Wind * .5f)
                        {
                            float want = Mathf.Atan2(o.Y - f.Y, o.X - f.X);
                            cur.Ang += Util.Clamp(Util.WrapAng(want - cur.Ang), -2.5f * dt, 2.5f * dt);
                        }
                        if (cur.M.K == "melee" && oT && Dist(f, o) > f.R + o.R + 6) { float a = Mathf.Atan2(o.Y - f.Y, o.X - f.X); f.X += Mathf.Cos(a) * 120 * dt; f.Y += Mathf.Sin(a) * 120 * dt; }
                        if (cur.T >= cur.Wind) FireMove(f);
                        if (f.Side != 0) AiDodgeCheck(f, o);
                        break;
                    }
                case "dash":
                    {
                        var cur = f.Cur; float sp = 300 * K;
                        float px = f.X + Mathf.Cos(cur.Ang) * sp * dt, py = f.Y + Mathf.Sin(cur.Ang) * sp * dt;
                        f.X = px; f.Y = py; cur.D += sp * dt; f.Moving = true; f.Walk += dt * 3;
                        if (Util.Value < .6f) Parts.Add(new Part { X = f.X + Util.Rand(-6, 6), Y = f.Y + 2, Vy = -10, Life = .3f, Max = .3f, Col = TC(cur.M.T), Size = 3 });
                        if (!cur.Hit && oT && Dist(f, o) < f.R + o.R + 4) { cur.Hit = true; Hit(f, o, cur.M, cur.Ang); }
                        ClampF(f);
                        bool wall = Mathf.Abs(f.X - px) > .5f || Mathf.Abs(f.Y - py) > .5f;
                        if (cur.D >= cur.M.Len || wall)
                        {
                            if (wall) { Shake = Mathf.Max(Shake, 4); AddDecal(f.X, f.Y, 14, "crater"); Burst(f.X, f.Y, Util.Hex("#c9b8ff"), 8, 70, .35f); }
                            if (f.State == "dash") { f.State = "act"; f.StT = wall ? .6f : .35f; }
                        }
                        break;
                    }
                case "act":
                case "stun":
                    f.StT -= dt; if (f.StT <= 0) f.State = "free";
                    if (f.State == "act") AiDodgeCheck(f, o);
                    break;
                case "dodge":
                    f.StT -= dt; f.GhostT -= dt;
                    f.X += f.Dvx * dt; f.Y += f.Dvy * dt;
                    if (Mathf.Abs(f.Dvx) > 1) f.Face = f.Dvx > 0 ? 1 : -1;
                    if (f.GhostT <= 0) { Fxs.Add(new Fx { Type = "ghost", Sid = f.Mon.sid, X = f.X, Y = f.Y, Face = f.Face, Life = .2f, Max = .2f }); f.GhostT = .04f; }
                    if (f.StT <= 0) f.State = "free";
                    break;
            }
            f.X += f.Kx * dt; f.Y += f.Ky * dt; float decay = Mathf.Pow(.002f, dt); f.Kx *= decay; f.Ky *= decay;
            ClampF(f);
        }

        // ---------- 捕獲 ----------
        float CatchProb(Fighter e) => Util.Clamp(e.Sp.Catch * (1.6f - 1.3f * e.Hp / e.MaxHp) * (e.State == "stun" ? 1.15f : 1), .04f, .95f);
        public void CmdCapsule()
        {
            if (Kind != "wild" || Mode != "fight" || Catch != null || Paused) return;
            if (S.capsules <= 0) { Say("カプセルが もう ない！"); return; }
            var e = Active(1); if (!Targetable(e)) return;
            S.capsules--; S.Save();
            var tr = Sides[0].Trainer; tr.Shout = .6f;
            Mode = "catch";
            Catch = new CatchO { Phase = "throw", Sx = tr.X, Sy = tr.Y - 30, Tx = e.X, Ty = e.Y - 12, P = CatchProb(e), X = tr.X, Y = tr.Y };
            Say("いけっ！ キャプチャーカプセル！");
        }
        static readonly string[] FailLines = { "ああっ！ カプセルから でてしまった！", "おしい！ もうすこしだったのに！", "だめだ！ にげだした！" };
        void UpdateCatch(float dt)
        {
            var c = Catch; var e = Active(1); c.T += dt;
            if (c.Phase == "throw")
            {
                float k = Mathf.Min(1, c.T / .55f);
                c.X = c.Sx + (c.Tx - c.Sx) * k; c.Y = c.Sy + (c.Ty - c.Sy) * k - Mathf.Sin(k * Mathf.PI) * 80;
                if (k >= 1) { c.Phase = "suck"; c.T = 0; e.State = "capt"; Burst(c.Tx, c.Ty, Util.Hex("#9ff0ff"), 20, 100, .5f); Fxs.Add(new Fx { Type = "ring", X = c.Tx, Y = c.Ty, Rad = 20, Col = Util.Hex("#9ff0ff"), Life = .3f, Max = .3f }); }
            }
            else if (c.Phase == "suck")
            {
                c.Y = c.Ty + Mathf.Min(1, c.T / .3f) * 6;
                if (c.T > .45f) { c.Phase = "shake"; c.T = 0; }
            }
            else if (c.Phase == "shake" && c.T >= .6f)
            {
                c.T = 0;
                if (Util.Value < Mathf.Pow(c.P, 1f / 3))
                {
                    c.Shakes++;
                    if (c.Shakes >= 3)
                    {
                        c.Phase = "done";
                        Burst(c.X, c.Y, Util.Hex("#ffd166"), 24, 90, .8f);
                        Say($"やった！ {e.Sp.N}を つかまえた！");
                        Cheer = 1;
                        EndBattle("caught");
                    }
                }
                else
                {
                    c.Phase = "fail";
                    e.State = "stun"; e.StT = .4f; e.Inv = .4f;
                    Burst(c.X, c.Y, Color.white, 20, 120, .5f);
                    Say(Util.Choice(FailLines));
                    Catch = null; Mode = "fight";
                }
            }
        }

        // ---------- コマンド ----------
        bool CanCommand => Mode == "fight" && !Paused;
        public void CmdMove(int i)
        {
            if (!CanCommand) return;
            var f = Active(0); if (f == null) return;
            var id = f.Sp.Moves[i];
            if (!(f.State == "free" || f.State == "act")) { f.Queued = id; return; }
            if (f.CdOf(id) > 0) return;
            f.Queued = id;
        }
        public void CmdAttack()
        {
            if (!CanCommand) return;
            var f = Active(0); if (f == null || f.CdOf("tackle") > 0) return;
            f.Queued = "tackle";
        }
        public void CmdDodge()
        {
            if (!CanCommand) return;
            var f = Active(0); if (f == null || f.DodgeCd > 0 || !(f.State == "free" || f.State == "act" || f.State == "wind")) return;
            StartDodge(f, InputActive ? Mathf.Atan2(InputVec.y, InputVec.x) : (float?)null);
        }
        public bool CanSwap(out List<int> bench)
        {
            bench = new List<int>();
            if (!CanCommand || Kind == "wild") return false;
            var f = Active(0); if (f == null || !(f.State == "free" || f.State == "act")) return false;
            for (int i = 0; i < Sides[0].Fs.Count; i++) { var x = Sides[0].Fs[i]; if (i != Sides[0].Act && !x.Fainted && x.Hp > 0) bench.Add(i); }
            return bench.Count > 0;
        }
        public void DoSwap(int idx)
        {
            var f = Active(0);
            f.State = "return"; f.StT = .3f; f.Cur = null; f.Queued = null; _swapTo = idx;
            Say($"もどれ、{f.Sp.N}！");
        }
        public void CmdRun() { if (!CanCommand || Kind != "wild") return; Say("うまく にげきれた！"); EndBattle("run"); }

        // ---------- メインループ ----------
        public void Step(float dt)
        {
            if (Paused) return;
            foreach (var sd in Sides) if (sd.Trainer != null) sd.Trainer.Shout = Mathf.Max(0, sd.Trainer.Shout - dt);
            if (Hitstop > 0) { Hitstop -= dt; return; }
            T += dt; ModeT += dt;
            Cheer = Mathf.Max(.15f, Cheer - dt * .4f);
            Shake = Mathf.Max(0, Shake - dt * 20);

            if (Mode == "intro")
            {
                if (_sent == 0 && ModeT > .8f) { _sent = 1; SendOut(1, 0); }
                if (_sent == 1 && ModeT > 1.7f) { _sent = 2; SendOut(0, 0); }
                if (ModeT > 2.3f) { Mode = "fight"; ModeT = 0; Say("バトル スタート！"); }
            }
            if (_pendingSend.HasValue)
            {
                var p = _pendingSend.Value; p.t -= dt;
                if (p.t <= 0) { _pendingSend = null; SendOut(p.side, p.idx); } else _pendingSend = p;
            }

            if (Mode == "catch") UpdateCatch(dt);
            else if (Mode == "fight" || Mode == "intro")
            {
                Fighter a = Active(0), e = Active(1);
                UpdateFighter(a, dt);
                if (Mode == "fight" || Mode == "intro") UpdateFighter(e, dt);
                if (Targetable(a) && Targetable(e))
                {
                    float d = Dist(a, e), min = a.R + e.R - 2;
                    if (d < min && d > .001f)
                    {
                        float p = min - d, nx = (a.X - e.X) / d, ny = (a.Y - e.Y) / d;
                        a.X += nx * p * .5f; a.Y += ny * p * .5f; e.X -= nx * p * .5f; e.Y -= ny * p * .5f; ClampF(a); ClampF(e);
                    }
                }
                foreach (var p in Projs)
                {
                    var tgt = Active(1 - p.Side);
                    if (p.M.Homing > 0 && Targetable(tgt))
                    {
                        float want = Mathf.Atan2(tgt.Y - BODY - p.Y, tgt.X - p.X), cur = Mathf.Atan2(p.Vy, p.Vx), sp = Hyp(p.Vx, p.Vy);
                        float na = cur + Util.Clamp(Util.WrapAng(want - cur), -p.M.Homing * dt, p.M.Homing * dt);
                        p.Vx = Mathf.Cos(na) * sp; p.Vy = Mathf.Sin(na) * sp;
                    }
                    p.X += p.Vx * dt; p.Y += p.Vy * dt; p.Life -= dt; p.Rot += dt * 12;
                    if (Targetable(tgt) && Hyp(tgt.X - p.X, tgt.Y - BODY - p.Y) < tgt.R + p.R) { p.Life = 0; Hit(p.F, tgt, p.M, Mathf.Atan2(p.Vy, p.Vx)); }
                    if (p.X < St.Fx0 - 10 || p.X > St.Fx1 + 10 || p.Y < St.Fy0 - 40 || p.Y > St.Fy1 + 4) { p.Life = 0; Burst(p.X, p.Y, TC(p.M.T), 4, 40, .25f); }
                }
                Projs.RemoveAll(p => p.Life <= 0);
            }
            if (Mode == "end") EndT -= dt;

            foreach (var q in Parts) { q.X += q.Vx * dt; q.Y += q.Vy * dt; q.Vy += q.G * dt; q.Vx *= .96f; q.Life -= dt; }
            Parts.RemoveAll(q => q.Life <= 0);
            foreach (var t in Texts) { t.Y -= 22 * dt; t.Life -= dt; }
            Texts.RemoveAll(t => t.Life <= 0);
            foreach (var f in Fxs) f.Life -= dt;
            Fxs.RemoveAll(f => f.Life <= 0);

            // カメラ：ふたりの中間を追い、距離に合わせてズーム
            Fighter A = Active(0), E = Active(1);
            float tx = St.W / 2f, ty = St.H / 2f, tz = 1;
            var vis = new List<Fighter>(); if (A != null && A.State != "bench") vis.Add(A); if (E != null && E.State != "bench") vis.Add(E);
            if (Mode == "intro") { float z0 = 320f / St.W; tz = ModeT < .6f ? z0 : z0 + Mathf.Min(1, (ModeT - .6f) / 1.6f) * (.95f - z0); ty = (St.Fy0 + St.Fy1) / 2 - 20; }
            else if (Mode == "end" && EndT < .8f) tz = .5f;
            else if (vis.Count > 0)
            {
                tx = vis.Average(f => f.X); ty = vis.Average(f => f.Y) - 40;
                float d = vis.Count > 1 ? Dist(vis[0], vis[1]) : 0;
                tz = Util.Clamp(1.12f - d / 900, St.Kind == "stadium" ? .66f : .72f, 1.05f);
            }
            if (Mode == "catch" && Catch != null) tx = (Catch.X + (A != null ? A.X : Catch.X)) / 2;
            Cam.z += (tz - Cam.z) * Mathf.Min(1, dt * 3);
            Cam.x += (tx - Cam.x) * Mathf.Min(1, dt * 4);
            Cam.y += (ty - Cam.y) * Mathf.Min(1, dt * 4);
        }

        // ---------- 終了 ----------
        public void EndBattle(string res)
        {
            if (Mode == "end") return;
            Mode = "end"; Result = res; EndT = res == "caught" ? 1.6f : 1.4f;
            var lines = ResLines; lines.Clear();
            int caps0 = S.capsules;
            foreach (var kv in _exp)
            {
                var m = S.party.Find(x => x.uid == kv.Key); if (m == null) continue;
                int before = m.lvl, ups = SaveData.GainExp(m, kv.Value);
                lines.Add($"{Data.Species[m.sid].N} は けいけんち {kv.Value} を もらった");
                if (ups > 0) lines.Add($"<color=#ffd166>{Data.Species[m.sid].N} は Lv{before} → Lv{m.lvl} に あがった！</color>");
            }
            if (Kind == "wild")
            {
                if (res == "caught")
                {
                    var e = Active(1); var nm = S.NewMon(e.Mon.sid, e.Mon.lvl);
                    S.caught++;
                    if (S.party.Count < 6) { S.party.Add(nm); lines.Insert(0, $"{Data.Species[nm.sid].N}（Lv{nm.lvl}）が パーティに くわわった！"); }
                    else { S.box.Add(nm); lines.Insert(0, $"{Data.Species[nm.sid].N}（Lv{nm.lvl}）は ボックスに おくられた"); }
                    var me = Active(0);
                    if (me != null) { int gain = 6 + e.Lvl * 3, ups = SaveData.GainExp(me.Mon, gain); lines.Add($"{me.Sp.N} は けいけんち {gain} を もらった{(ups > 0 ? $"（Lv{me.Mon.lvl}！）" : "")}"); }
                }
                else if (res == "win") S.capsules += 1;
                else if (res == "lose") lines.Insert(0, "ちからつきて しまった… でも モンスターたちは すぐに げんきに なった");
                else if (res == "run") lines.Insert(0, "くさむらから ぶじに にげだした");
            }
            else
            {
                if (res == "win")
                {
                    S.wins++;
                    var r = Data.Rounds[S.round];
                    S.capsules += 3;
                    foreach (var f in Sides[0].Fs) { int ups = SaveData.GainExp(f.Mon, 4 + r.Lv); if (ups > 0) lines.Add($"<color=#ffd166>{f.Sp.N} は Lv{f.Mon.lvl} に あがった！（ボーナス）</color>"); }
                    S.round++;
                    if (S.round >= Data.Rounds.Length)
                    {
                        S.round = 0; S.trophies++;
                        lines.Insert(0, $"<color=#ffd166>{Data.CupName(S.tier)} ゆうしょう！</color>");
                        S.tier++;
                        lines.Add($"つぎは {Data.CupName(S.tier)} に ちょうせんできる！");
                    }
                    else lines.Insert(0, $"{r.N} とっぱ！ つぎは {Data.Rounds[S.round].N}");
                }
                else if (res == "lose") { S.round = 0; lines.Insert(0, "まけてしまった… たいかいは 1かいせんから やりなおし"); }
            }
            if (S.capsules > caps0) lines.Add($"カプセルを {S.capsules - caps0}こ てにいれた");
            S.Save();
        }
    }
}
