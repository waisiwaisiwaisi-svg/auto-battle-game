using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace PixelMonsterArena
{
    public class MoveExec
    {
        public string Id; public Move M; public float T, Wind, Ang, Tx, Ty, D; public int Uid, Hits; public bool Hit;
        public List<Vector2> Pts;
    }

    public class Plan { public bool Will; public float At; public string Guard; }
    public class Shot { public float T, Ang; public Move M; }

    /// <summary>ひとときの状態（交代すると消える）</summary>
    public class Volatile
    {
        public float Taunt, HealBlock, Confuse, Protect, DBond, Yawn;
        public string EncoreId; public float EncoreT;
        public int Seed;           // 0=なし, 1/2 = 植えた側+1
        public bool Curse;
        public float Sub;
        public string CounterCtr; public float CounterMult, CounterT;
        public int Rampage;
    }

    public class Fighter
    {
        public MonData Mon; public Species Sp; public int Side, Lvl;
        public float Hp, MaxHp, Atk, Def; public int BaseSpd;
        public List<string> Moves;
        public float X, Y, R = 23; public int Face;
        public string State = "bench"; public float StT;
        public Dictionary<string, float> Cd = new Dictionary<string, float>();
        public string Queued; public MoveExec Cur;
        public float Inv, Flash, Kx, Ky, DodgeCd, AiT = 1, Dizzy, Scale = 1, Walk, GhostT, SplashT, StratT, Dvx, Dvy;
        public Plan Plan; public int PlanFor; public int Strafe = 1;
        public bool Fainted, Moving;
        public Dictionary<string, int> St = NewStages();
        public string Status = ""; public float StatusT, TickT = Battle.Tick, ParT = 2.5f; public int ToxN = 1;
        public Volatile V = new Volatile();
        public float EnterT, LastProtect = -9; public string LastMove;
        public List<Shot> Shots = new List<Shot>();
        public int PendingOut = -1;
        public float SwapLag, LagMax, SwapT = 3;
        /// <summary>技を 出した 時刻（攻撃アニメの フレーム選び用）</summary>
        public float FireT = -9;
        public float CdOf(string id) => Cd.TryGetValue(id, out var v) ? v : 0;
        public bool HasType(string t) => Sp.Type == t || Sp.Type2 == t;
        public static Dictionary<string, int> NewStages() => new Dictionary<string, int> { { "atk", 0 }, { "def", 0 }, { "spa", 0 }, { "spd", 0 }, { "spe", 0 } };
    }

    public class Proj { public Fighter F; public int Side; public Move M; public float X, Y, Vx, Vy, R, Life, Rot; public bool Rolled, Will; }
    public class Fx { public string Type, Look; public float X, Y, Ang, Len, Wid, Rad, Half, Life, Max, Rot, X0, Y0, X1, Y1; public Color Col; public string Sid; public int Face; }
    public class Part { public float X, Y, Vx, Vy, Life, Max, G; public Color Col; public int Size; }
    /// <summary>Big: 0=ふつう 1=大きい 2=マンガ文字（BONK! など）</summary>
    public class FText { public float X, Y, Life, Max; public string Txt; public Color Col; public int Big; }
    public class Decal { public float X, Y, R; public string Kind; public int Seed; }
    public class TrainerInfo { public string Name; public PixelArt.MonSprites Spr; public float X, Y, Shout; }
    public class Hazards { public int Rocks, Spikes, TSpikes; }
    public class Side { public List<Fighter> Fs; public int Act; public TrainerInfo Trainer; public Hazards Hz = new Hazards(); public float Tail, SwapCd; }
    public class CatchO { public string Phase; public float T, Sx, Sy, Tx, Ty, X, Y, P; public int Shakes; }

    public class BattleConfig
    {
        public string Kind, Field, Title, Intro;
        public List<MonData> Enemies;
        public float Skill;
        public TrainerInfo Trainer;
    }

    /// <summary>リアルタイムバトルの中身（描画は BattleRenderer が担当）。index.html の処理を そのまま移植。</summary>
    public class Battle
    {
        const float K = Data.K, BODY = Data.Body;
        public const float Tick = 3; // 状態異常ダメージの間隔（秒）＝「1ターン」相当
        // 交代したあと 出てきた モンスターは しばらく スキだらけ（うごけない・ダメージ増）
        public const float SwapLag = 1.6f, SwapCdMax = 4, LagDmg = 1.3f;
        public static readonly string[] StageKeys = { "atk", "def", "spa", "spd", "spe" };
        public static readonly Dictionary<string, string> StageNames = new Dictionary<string, string> { { "atk", "こうげき" }, { "def", "ぼうぎょ" }, { "spa", "とくこう" }, { "spd", "とくぼう" }, { "spe", "すばやさ" } };
        public static readonly Dictionary<string, string> StatusNames = new Dictionary<string, string> { { "brn", "やけど" }, { "par", "まひ" }, { "psn", "どく" }, { "tox", "もうどく" }, { "slp", "ねむり" }, { "frz", "こおり" } };
        static float StageMul(int s) => s >= 0 ? (2 + s) / 2f : 2f / (2 - s);

        public readonly SaveData S;
        public readonly string Kind;
        public readonly Stage St;
        public readonly Side[] Sides;
        public readonly List<Proj> Projs = new List<Proj>();
        public readonly List<Part> Parts = new List<Part>();
        public readonly List<FText> Texts = new List<FText>();
        public readonly List<Fx> Fxs = new List<Fx>();
        public readonly List<Decal> Decals = new List<Decal>();
        public float T, ModeT, Cheer = .3f, Shake, Hitstop, EndT, TrickRoom;
        public string Mode = "intro";
        public bool Paused;
        public CatchO Catch;
        public string Result;
        public readonly List<string> ResLines = new List<string>();
        public Vector3 Cam; // x, y, zoom
        public readonly float Skill;
        public Vector2 InputVec; public bool InputActive;
        public List<string> Log;
        public event Action<string> OnSay;

        int _uidc, _sent, _swapTo;
        (Dictionary<string, int> st, float sub)? _swapPass;
        readonly Dictionary<int, int> _exp = new Dictionary<int, int>();
        class Pending { public int Side, Idx; public float T; public (Dictionary<string, int> st, float sub)? Pass; public bool Lag; }
        Pending _pendingSend;

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
                Mon = mon, Sp = Data.Species[mon.sid], Side = side, Lvl = mon.lvl, Hp = st.Hp, MaxHp = st.Hp, Atk = st.Atk, Def = st.Def, BaseSpd = st.Spd,
                Moves = new List<string>(Data.Equipped(mon)), Face = side == 1 ? -1 : 1,
            };
        }

        public Fighter Active(int side) { var sd = Sides[side]; return sd.Fs.Count > sd.Act ? sd.Fs[sd.Act] : null; }
        Fighter Opp(Fighter f) => Active(1 - f.Side);
        public static bool Targetable(Fighter f) => f != null && (f.State == "free" || f.State == "wind" || f.State == "dash" || f.State == "act" || f.State == "stun" || f.State == "dodge" || f.State == "lag");
        static float Dist(Fighter a, Fighter b) => Mathf.Sqrt((a.X - b.X) * (a.X - b.X) + (a.Y - b.Y) * (a.Y - b.Y));
        static float Hyp(float a, float b) => Mathf.Sqrt(a * a + b * b);
        string Prefix(Fighter f) => f.Side == 0 ? "" : (Kind == "wild" ? "やせいの " : "あいての ");
        public static bool CanAct(Fighter f) => f.Status != "slp" && f.Status != "frz";
        float SpeedOf(Fighter f)
        {
            float b = f.BaseSpd;
            if (TrickRoom > 0) b = 170 - b; // さかさまフィールド：おそいほど はやい
            float s = (46 + b * .5f) * K * StageMul(f.St["spe"]);
            if (f.Status == "par") s *= .5f;
            if (Sides[f.Side].Tail > 0) s *= 1.5f;
            return s;
        }

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
        public static Color TC(string t) => Data.Types[t].C;
        static Color MoveCol(Move m) => m.T == "normal" ? Color.white : TC(m.T);
        static Color H(string hex) => Util.Hex(hex);

        void SendOut(int side, int idx, (Dictionary<string, int> st, float sub)? pass = null, bool lag = false)
        {
            var sd = Sides[side]; sd.Act = idx;
            var f = sd.Fs[idx];
            f.X = side == 1 ? St.Fx1 - 120 : St.Fx0 + 120; f.Y = (St.Fy0 + St.Fy1) / 2 + Util.Rand(-20, 20);
            f.State = "enter"; f.StT = .5f; f.Inv = .6f; f.Cur = null; f.Queued = null; f.Kx = f.Ky = 0; f.Face = side == 1 ? -1 : 1; f.AiT = Util.Rand(.6f, 1.2f); f.Scale = 0;
            f.EnterT = 0; f.V = new Volatile(); f.St = Fighter.NewStages(); f.LastMove = null; f.Shots.Clear();
            if (pass.HasValue) { f.St = new Dictionary<string, int>(pass.Value.st); if (pass.Value.sub > 0) f.V.Sub = pass.Value.sub; }
            f.SwapLag = lag ? SwapLag : 0; if (lag) f.Inv = 0;
            var tr = sd.Trainer;
            if (tr != null) { Fxs.Add(new Fx { Type = "beamIn", X0 = tr.X, Y0 = tr.Y - 30, X1 = f.X, Y1 = f.Y - 20, Life = .45f, Max = .45f }); tr.Shout = .7f; }
            else Burst(f.X, f.Y - 4, H("#3f9040"), 16, 90, .5f);
            Burst(f.X, f.Y - 10, Color.white, 12, 80, .45f);
            Cheer = Mathf.Max(Cheer, .7f);
            if (side == 0) Say($"いけっ！ {f.Sp.N}！");
            else if (tr != null) Say($"{tr.Name}は {f.Sp.N}を くりだした！");
            else Say($"あっ！ やせいの {f.Sp.N}（Lv{f.Lvl}）が とびだしてきた！");
            ApplyHazards(f);
        }

        void ApplyHazards(Fighter f)
        {
            var hz = Sides[f.Side].Hz;
            if (hz.Rocks > 0) { int d = Mathf.Max(1, Mathf.RoundToInt(f.MaxHp / 8 * Data.EffVs("rock", f.Sp))); f.Hp = Mathf.Max(1, f.Hp - d); PopText(f.X, f.Y - 66, $"-{d}", H("#c49a6c")); Burst(f.X, f.Y - BODY, H("#c49a6c"), 8, 80, .4f); }
            if (hz.Spikes > 0 && !f.HasType("wind")) { float[] k = { 0, 1 / 8f, 1 / 6f, 1 / 4f }; int d = Mathf.Max(1, Mathf.RoundToInt(f.MaxHp * k[hz.Spikes])); f.Hp = Mathf.Max(1, f.Hp - d); PopText(f.X + 10, f.Y - 56, $"-{d}", H("#d8b060")); }
            if (hz.TSpikes > 0 && !f.HasType("wind"))
            {
                if (f.HasType("poison")) { hz.TSpikes = 0; Say($"{f.Sp.N}が どくのトゲを かたづけた！"); }
                else SetStatus(f, hz.TSpikes >= 2 ? "tox" : "psn", null);
            }
        }

        // ---------- 当たり判定（その瞬間に はんいに いるか） ----------
        static bool InSector(float x, float y, float ox, float oy, float ang, float rad, float half, float r)
        {
            float dx = x - ox, dy = y - oy, d = Hyp(dx, dy);
            if (d > rad + r) return false;
            if (d < r + 8) return true;
            return Mathf.Abs(Util.WrapAng(Mathf.Atan2(dy, dx) - ang)) <= half + r / d;
        }
        public static bool InZone(MoveExec cur, Fighter owner, float x, float y, float r)
        {
            var m = cur.M;
            switch (m.K)
            {
                case "aoe": return Hyp(x - owner.X, y - owner.Y) <= m.Rad + r;
                case "strike": return Hyp(x - cur.Tx, y - cur.Ty) <= m.Rad + r;
                case "multi": return cur.Pts.Any(p => Hyp(x - p.x, y - p.y) <= m.Rad + r);
                case "cone": return InSector(x, y, owner.X, owner.Y, cur.Ang, m.Rad, m.Half, r);
                case "swipe": return InSector(x, y, owner.X, owner.Y, cur.Ang, m.Rad + owner.R, .95f, r);
                case "beam":
                case "dash":
                    {
                        float wid = m.K == "dash" ? owner.R * 2 + 8 : m.Wid;
                        float c = Mathf.Cos(cur.Ang), s = Mathf.Sin(cur.Ang), dx = x - owner.X, dy = y - owner.Y;
                        float along = dx * c + dy * s, perp = -dx * s + dy * c;
                        return along >= -10 && along <= m.Len + 10 && Mathf.Abs(perp) <= wid / 2 + r;
                    }
            }
            return false;
        }
        void ClampF(Fighter f) { f.X = Util.Clamp(f.X, St.Fx0 + f.R, St.Fx1 - f.R); f.Y = Util.Clamp(f.Y, St.Fy0 + f.R, St.Fy1 - f.R); }

        // ---------- わざが つかえるか ----------
        public string MoveBlocked(Fighter f, string id)
        {
            var m = Data.Moves[id];
            if (f.V.Taunt > 0 && m.Cat == "stat") return "ちょうはつ中";
            if (f.V.EncoreId != null && f.V.EncoreId != id) return "アンコール中";
            if (f.V.HealBlock > 0 && (m.K == "heal" || m.E.Drain > 0)) return "かいふく ふうじ";
            if (m.Fakeout && f.EnterT > 2) return "でてすぐ だけ";
            return null;
        }

        // ---------- わざ ----------
        void BeginMove(Fighter f, string id)
        {
            var o = Opp(f); if (o == null) return;
            var m = Data.Moves[id];
            float ang = Mathf.Atan2(o.Y - f.Y, o.X - f.X), tx = o.X, ty = o.Y;
            // ◎（命中100未満）：プレイヤーは スティックを たおした方向に ねらえる
            if (f.Side == 0 && !S.auto && m.Aim == "dir" && InputActive)
            {
                var v = InputVec.normalized; ang = Mathf.Atan2(v.y, v.x); float d = Dist(f, o);
                tx = Util.Clamp(f.X + v.x * d, St.Fx0, St.Fx1); ty = Util.Clamp(f.Y + v.y * d, St.Fy0, St.Fy1);
            }
            // 命中100未満の わざは この瞬間の むき・いち で固定（追尾しない）
            var cur = new MoveExec { Id = id, M = m, Wind = m.Wind, Ang = ang, Uid = ++_uidc, Tx = tx, Ty = ty };
            if (m.K == "multi") cur.Pts = MultiPoints(f, tx, ty, m, ang);
            f.Cur = cur;
            f.Cd[id] = (f.V.Rampage > 0 && id == "outrage") ? 0 : m.Cd;
            f.State = "wind";
            f.LastMove = id;
            Log?.Add(id);
            if (id != "tackle")
            {
                Say($"{Prefix(f)}{f.Sp.N}の {m.N}！");
                if (Sides[f.Side].Trainer != null) Sides[f.Side].Trainer.Shout = .6f;
            }
        }

        List<Vector2> MultiPoints(Fighter f, float ox, float oy, Move m, float ang)
        {
            var pts = new List<Vector2>();
            if (m.Pattern == "fan")
            { // がけくずれ：むいた方向に 3つ ならべて落とす
                float d = Util.Clamp(Hyp(ox - f.X, oy - f.Y), 90, 220);
                for (int i = -1; i <= 1; i++) { float a = ang + i * .38f; pts.Add(new Vector2(f.X + Mathf.Cos(a) * d, f.Y + Mathf.Sin(a) * d)); }
            }
            else
            { // スターフォール：あいての いた あたりに 4つ
                pts.Add(new Vector2(ox, oy));
                for (int i = 0; i < 3; i++) { float a = Util.Rand(0, Mathf.PI * 2), r = Util.Rand(55, 95); pts.Add(new Vector2(ox + Mathf.Cos(a) * r, oy + Mathf.Sin(a) * r)); }
            }
            for (int i = 0; i < pts.Count; i++) pts[i] = new Vector2(Util.Clamp(pts[i].x, St.Fx0 + 10, St.Fx1 - 10), Util.Clamp(pts[i].y, St.Fy0 + 10, St.Fy1 - 10));
            return pts;
        }

        void SpawnProj(Fighter f, Move m, float a) =>
            Projs.Add(new Proj { F = f, Side = f.Side, M = m, X = f.X + Mathf.Cos(a) * 20, Y = f.Y - BODY + Mathf.Sin(a) * 20, Vx = Mathf.Cos(a) * m.Spd, Vy = Mathf.Sin(a) * m.Spd, R = m.R, Life = m.Life > 0 ? m.Life : 1.8f });

        void FireMove(Fighter f)
        {
            var cur = f.Cur; var m = cur.M; var o = Opp(f);
            f.FireT = T;
            var col = TC(m.T);
            if (o != null && m.Aim == "lock" && (m.K == "proj" || m.K == "melee")) cur.Ang = Mathf.Atan2(o.Y - f.Y, o.X - f.X);
            if (m.Fakeout && f.EnterT > 2.3f) { FailMove(f, "でも うまく きまらなかった！"); return; }
            if (m.Sucker && !(o != null && o.State == "wind" && o.Cur != null && o.Cur.M.Damaging)) { FailMove(f, "でも うまく きまらなかった！"); return; }
            switch (m.K)
            {
                case "melee":
                    Fxs.Add(new Fx { Type = "swipe", X = f.X, Y = f.Y - BODY, Ang = cur.Ang, Life = .14f, Max = .14f, Col = MoveCol(m) });
                    if (Targetable(o) && Dist(f, o) <= f.R + o.R + 20) Hit(f, o, m, cur.Ang);
                    EndAct(f, .22f); break;
                case "swipe":
                    Fxs.Add(new Fx { Type = "sector", X = f.X, Y = f.Y, Ang = cur.Ang, Rad = m.Rad + f.R, Half = .95f, Col = col, Life = .18f, Max = .18f });
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, cur.Ang, cur.Hits);
                    cur.Hits++;
                    if (m.Hits > 0 && cur.Hits < m.Hits && f.State == "wind") { cur.T = cur.Wind - .16f; return; } // さんれんスピン
                    EndAct(f, .25f); break;
                case "proj":
                    if (m.BurstMax > 0)
                    { // いしつぶてれんぱつ：同じ向きに 2〜5発
                        int n = Util.RandI(m.BurstMin, m.BurstMax);
                        for (int i = 0; i < n; i++) f.Shots.Add(new Shot { T = i * .14f, M = m, Ang = cur.Ang + Util.Rand(-.04f, .04f) });
                    }
                    else for (int i = 0; i < m.Cnt; i++) SpawnProj(f, m, cur.Ang + (m.Cnt > 1 ? (i - (m.Cnt - 1) / 2f) * m.Spread : 0));
                    EndAct(f, .25f); break;
                case "beam":
                    Fxs.Add(new Fx { Type = "beam", X = f.X, Y = f.Y - BODY, Ang = cur.Ang, Len = m.Len, Wid = m.Wid, Col = col, Look = m.Look, Life = .3f, Max = .3f });
                    Shake = Mathf.Max(Shake, 3);
                    if (!string.IsNullOrEmpty(m.Look)) AddDecal(f.X + Mathf.Cos(cur.Ang) * m.Len / 2, f.Y + Mathf.Sin(cur.Ang) * m.Len / 2, 16, "crater");
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, cur.Ang);
                    EndAct(f, .35f); break;
                case "cone":
                    Fxs.Add(new Fx { Type = "sector", X = f.X, Y = f.Y, Ang = cur.Ang, Rad = m.Rad, Half = m.Half, Col = col, Life = .35f, Max = .35f });
                    for (int i = 0; i < 26; i++) { float a = cur.Ang + Util.Rand(-m.Half, m.Half), s = Util.Rand(150, 320); Parts.Add(new Part { X = f.X, Y = f.Y - BODY, Vx = Mathf.Cos(a) * s, Vy = Mathf.Sin(a) * s, Life = .6f, Max = .6f, Col = col, Size = 3 }); }
                    Shake = Mathf.Max(Shake, 3);
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, cur.Ang);
                    EndAct(f, .35f); break;
                case "aoe":
                    Fxs.Add(new Fx { Type = "ring", X = f.X, Y = f.Y, Rad = m.Rad, Col = col, Life = .35f, Max = .35f });
                    Shake = Mathf.Max(Shake, 6);
                    Burst(f.X, f.Y, col, 24, 160, .55f);
                    if (m.T == "ground" || m.T == "rock" || m.T == "fire") AddDecal(f.X, f.Y, m.Rad * .4f, m.T == "fire" ? "scorch" : "crater");
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, Mathf.Atan2(o.Y - f.Y, o.X - f.X));
                    EndAct(f, .4f); break;
                case "strike":
                    Fxs.Add(new Fx { Type = m.T == "elec" ? "bolt" : (m.T == "rock" || m.T == "ground") ? "rocks" : "pop", X = cur.Tx, Y = cur.Ty, Rad = m.Rad, Col = col, Life = .35f, Max = .35f });
                    Shake = Mathf.Max(Shake, 5);
                    Burst(cur.Tx, cur.Ty, col, 18, 130, .5f);
                    AddDecal(cur.Tx, cur.Ty, m.Rad * .5f, m.T == "elec" || m.T == "fire" ? "scorch" : "crater");
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, Mathf.Atan2(o.Y - cur.Ty, o.X - cur.Tx));
                    EndAct(f, .3f); break;
                case "multi":
                    foreach (var p in cur.Pts) { Fxs.Add(new Fx { Type = "rocks", X = p.x, Y = p.y, Rad = m.Rad, Col = col, Life = .35f, Max = .35f }); AddDecal(p.x, p.y, m.Rad * .5f, "crater"); Burst(p.x, p.y, col, 10, 120, .45f); }
                    Shake = Mathf.Max(Shake, 7);
                    if (Targetable(o) && InZone(cur, f, o.X, o.Y, o.R)) Hit(f, o, m, Mathf.Atan2(o.Y - f.Y, o.X - f.X));
                    EndAct(f, .35f); break;
                case "dash":
                    cur.D = 0; cur.Hit = false; f.State = "dash"; break;
                default:
                    UseStatusMove(f, o, m);
                    if (f.State == "wind") EndAct(f, .3f);
                    break;
            }
        }

        void EndAct(Fighter f, float t)
        {
            if (f.State == "wind" || f.State == "dash") { f.State = "act"; f.StT = t; }
            AfterMoveUsed(f);
        }
        void FailMove(Fighter f, string msg) { Say(msg); PopText(f.X, f.Y - 66, "しっぱい", H("#a49ac0")); EndAct(f, .3f); }
        // げきりん系：つづけて あばれた あと こんらん
        void AfterMoveUsed(Fighter f)
        {
            var cur = f.Cur; if (cur == null || !cur.M.Rampage) return;
            if (f.V.Rampage == 0) f.V.Rampage = Util.RandI(1, 2) + 1;
            f.V.Rampage--;
            if (f.V.Rampage > 0) f.Queued = cur.Id;
            else { f.V.Confuse = 3; Say($"{Prefix(f)}{f.Sp.N}は つかれはてて こんらんした！"); }
        }

        // ---------- 補助わざ ----------
        void UseStatusMove(Fighter f, Fighter o, Move m)
        {
            var sd = Sides[f.Side]; var osd = Sides[1 - f.Side]; var e = m.E;
            switch (m.K)
            {
                case "self": ChangeStages(f, e.Self); Aura(f, H("#ffd166")); break;
                case "heal":
                    if (f.V.HealBlock > 0) { FailMove(f, "かいふくが ふうじられている！"); return; }
                    HealHp(f, f.MaxHp * (e.Heal > 0 ? e.Heal : 50) / 100f); Aura(f, H("#7bd88f")); break;
                case "protect":
                    if (T - f.LastProtect < 3 && Util.Value < .5f) { FailMove(f, "れんぞくでは うまく まもれなかった！"); f.LastProtect = -9; return; }
                    f.V.Protect = 1; f.LastProtect = T; break;
                case "sub":
                    if (f.V.Sub > 0) { FailMove(f, "デコイは もう でている！"); return; }
                    if (f.Hp <= f.MaxHp / 4) { FailMove(f, "たいりょくが たりない！"); return; }
                    f.Hp -= Mathf.Floor(f.MaxHp / 4); f.V.Sub = Mathf.Floor(f.MaxHp / 4); Burst(f.X, f.Y - BODY, Color.white, 12, 80, .4f); break;
                case "dbond": f.V.DBond = 2.5f; Say($"{Prefix(f)}{f.Sp.N}は あいてを みちづれに しようとしている！"); break;
                case "counter": f.V.CounterCtr = m.Ctr; f.V.CounterMult = m.Mult; f.V.CounterT = 1.2f; break;
                case "curse":
                    if (f.HasType("ghost")) { if (Targetable(o)) { f.Hp = Mathf.Max(1, f.Hp - Mathf.Floor(f.MaxHp / 2)); o.V.Curse = true; Say($"{o.Sp.N}に のろいを かけた！"); } }
                    else ChangeStages(f, new Dictionary<string, int> { { "atk", 1 }, { "def", 1 }, { "spe", -1 } });
                    Aura(f, H("#8a78c8")); break;
                case "field":
                    if (m.Fld == "trickroom") { TrickRoom = TrickRoom > 0 ? 0 : 9; Say(TrickRoom > 0 ? "じくうが ねじれて おそいものが はやくなった！" : "ねじれた じくうが もとに もどった！"); }
                    else { sd.Tail = 9; Say($"{(f.Side == 0 ? "みかた" : "あいて")}の せなかに おいかぜが ふきはじめた！"); }
                    Cheer = Mathf.Min(1, Cheer + .4f); break;
                case "hazard":
                    {
                        var hz = osd.Hz;
                        int cur = m.Hz == "rocks" ? hz.Rocks : m.Hz == "spikes" ? hz.Spikes : hz.TSpikes, max = m.Hz == "rocks" ? 1 : m.Hz == "spikes" ? 3 : 2;
                        if (cur >= max) { FailMove(f, "でも もう しかけられない！"); return; }
                        if (m.Hz == "rocks") hz.Rocks++; else if (m.Hz == "spikes") hz.Spikes++; else hz.TSpikes++;
                        float tx = f.Side == 0 ? St.Fx1 - 120 : St.Fx0 + 120;
                        Fxs.Add(new Fx { Type = "toss", X0 = f.X, Y0 = f.Y - BODY, X1 = tx, Y1 = (St.Fy0 + St.Fy1) / 2, Col = TC(m.T), Life = .5f, Max = .5f });
                        Say(m.Hz == "rocks" ? "あいての まわりに いしが うかんだ！" : m.Hz == "spikes" ? "あいての あしもとに トゲが ちらばった！" : "あいての あしもとに どくのトゲが ちらばった！");
                        break;
                    }
                case "baton":
                    {
                        int idx = BenchIdx(f.Side, false);
                        if (Kind == "wild" || idx < 0) { FailMove(f, "でも かわりが いない！"); return; }
                        DoSwitch(f, idx, (new Dictionary<string, int>(f.St), f.V.Sub), false);
                        break;
                    }
                case "ray":
                    if (!Targetable(o)) return;
                    Fxs.Add(new Fx { Type = "ray", X0 = f.X, Y0 = f.Y - BODY, X1 = o.X, Y1 = o.Y - BODY, Col = TC(m.T), Life = .25f, Max = .25f });
                    if (o.V.Protect > 0) { PopText(o.X, o.Y - 66, "ガード！", H("#9ff0ff")); return; }
                    if (o.Inv > 0) { PopText(o.X, o.Y - 66, "かわした！", H("#7fd8ff")); return; }
                    RayEffect(f, o, m);
                    break;
            }
        }

        void RayEffect(Fighter f, Fighter o, Move m)
        {
            switch (m.Sp)
            {
                case "taunt": o.V.Taunt = 6; Say($"{o.Sp.N}は ちょうはつに のってしまった！ ほじょわざが だせない！"); break;
                case "encore":
                    if (o.LastMove == null || o.LastMove == "tackle") { Say("でも うまく きまらなかった！"); return; }
                    o.V.EncoreId = o.LastMove; o.V.EncoreT = 5; o.Queued = null; Say($"{o.Sp.N}は {Data.Moves[o.LastMove].N}しか だせなくなった！"); break;
                case "yawn":
                    if (o.Status != "" || o.V.Yawn > 0 || o.V.Sub > 0) { Say("でも うまく きまらなかった！"); return; }
                    o.V.Yawn = 2.5f; Say($"{o.Sp.N}は ねむけを さそわれた！"); break;
                case "trick": { var t = f.St; f.St = o.St; o.St = t; Say("おたがいの のうりょく変化を いれかえた！"); break; }
                case "roar":
                    if (Kind == "wild") { Say($"{o.Sp.N}は おどろいて にげだした！"); EndBattle(o.Side == 1 ? "run" : "lose"); return; }
                    { int idx = BenchIdx(o.Side, true); if (idx < 0) { Say("でも かわりが いない！"); return; } DoSwitch(o, idx, null, true); }
                    break;
            }
        }

        int BenchIdx(int side, bool random)
        {
            var sd = Sides[side];
            var list = Enumerable.Range(0, sd.Fs.Count).Where(i => i != sd.Act && !sd.Fs[i].Fainted && sd.Fs[i].Hp > 0).ToList();
            if (list.Count == 0) return -1;
            return random ? Util.Choice(list) : list[0];
        }
        void DoSwitch(Fighter f, int idx, (Dictionary<string, int> st, float sub)? pass, bool forced)
        {
            f.State = "return"; f.StT = .3f; f.Cur = null; f.Queued = null;
            _swapTo = idx; _swapPass = pass;
            Sides[f.Side].SwapCd = SwapCdMax;
            Say(forced ? $"{f.Sp.N}は ひきずりだされた！" : $"{Prefix(f)}{f.Sp.N}は もどっていった！");
        }
        void Aura(Fighter f, Color col) { Fxs.Add(new Fx { Type = "ring", X = f.X, Y = f.Y, Rad = 34, Col = col, Life = .45f, Max = .45f }); Burst(f.X, f.Y - BODY, col, 12, 60, .5f); }
        void HealHp(Fighter f, float amt) { int a = Mathf.Min(Mathf.RoundToInt(f.MaxHp - f.Hp), Mathf.RoundToInt(amt)); if (a <= 0) return; f.Hp += a; PopText(f.X, f.Y - 66, $"+{a}", H("#7bd88f")); }
        void ChangeStages(Fighter f, Dictionary<string, int> ch)
        {
            if (ch == null) return;
            var parts = new List<string>(); bool up = false;
            foreach (var kv in ch)
            {
                int before = f.St[kv.Key]; f.St[kv.Key] = Mathf.Clamp(f.St[kv.Key] + kv.Value, -6, 6);
                if (f.St[kv.Key] != before) { parts.Add(StageNames[kv.Key] + (kv.Value > 0 ? new string('↑', Mathf.Min(2, kv.Value)) : new string('↓', Mathf.Min(2, -kv.Value)))); up |= kv.Value > 0; }
            }
            if (parts.Count > 0) PopText(f.X, f.Y - 80, string.Join(" ", parts), up ? H("#ffd166") : H("#7fb2ff"));
        }
        bool SetStatus(Fighter f, string s, Fighter by)
        {
            if (f.Status != "" || f.Hp <= 0) return false;
            if (by != null && f.V.Sub > 0) return false;
            if ((s == "brn" && f.HasType("fire")) || (s == "par" && f.HasType("elec")) || ((s == "psn" || s == "tox") && (f.HasType("poison") || f.HasType("steel"))) || (s == "frz" && f.HasType("ice"))) return false;
            f.Status = s; f.ToxN = 1; f.TickT = Tick;
            if (s == "slp" || s == "frz") { f.StatusT = s == "slp" ? 3 : 2.5f; f.Cur = null; f.Queued = null; if (f.State == "wind" || f.State == "dash") f.State = "free"; }
            var msg = new Dictionary<string, string> { { "brn", "やけどを おった" }, { "par", "まひして うごきにくくなった" }, { "psn", "どくを あびた" }, { "tox", "もうどくを あびた" }, { "slp", "ねむってしまった" }, { "frz", "こおりついた" } };
            Say($"{Prefix(f)}{f.Sp.N}は {msg[s]}！");
            return true;
        }

        // ---------- ダメージ ----------
        static readonly string[] Comic = { "BONK!", "POW!", "WHAM!", "SMASH!" };
        bool Hit(Fighter att, Fighter def, Move m, float ang, int hitNo = 0)
        {
            if (def.Inv > 0) { PopText(def.X, def.Y - 66, "かわした！", H("#7fd8ff")); Burst(def.X, def.Y - BODY, H("#7fd8ff"), 6, 50, .3f); return false; }
            if (def.V.Protect > 0) { PopText(def.X, def.Y - 66, "ガード！", H("#9ff0ff")); Fxs.Add(new Fx { Type = "ring", X = def.X, Y = def.Y - BODY, Rad = 30, Col = H("#9ff0ff"), Life = .3f, Max = .3f }); return false; }
            if (m.Cat == "stat") return StatusHit(att, def, m);
            float eff = Data.EffVs(m.T, def.Sp);
            if (m.SuperVsWater && def.HasType("water")) eff = eff / Data.Eff("ice", "water") * 2;
            if (eff == 0) { PopText(def.X, def.Y - 66, "こうかなし", H("#a49ac0")); Say($"{def.Sp.N}には こうかが ないようだ…"); return false; }
            if (m.Ohko)
            { // だいちのさけめ：あたれば いちげき（レベルが上の あいてには きかない）
                if (def.Lvl > att.Lvl) { Say("でも あいてには きかなかった！"); return false; }
                def.Hp = 0; PopText(def.X, def.Y - 92, "いちげき！", H("#ffd84a"), 2); Shake = 10; Faint(def); return true;
            }
            bool phys = m.Cat == "phys";
            float A = phys ? att.Atk * StageMul(att.St["atk"]) : att.Atk * StageMul(att.St["spa"]);
            if (m.UseDef) A = att.Def * StageMul(att.St["def"]);
            if (m.UseFoeAtk) A = def.Atk * StageMul(def.St["atk"]);
            if (phys && att.Status == "brn" && !m.UseDef) A *= .5f;
            float D = (phys || m.HitDef) ? def.Def * StageMul(def.St["def"]) : def.Def * StageMul(def.St["spd"]);
            bool crit = Util.Value < (m.Crit ? 1 / 8f : 1 / 24f);
            float stab = att.HasType(m.T) ? 1.25f : 1;
            float pow = m.Pow; if (m.Hits > 0) pow *= hitNo + 1;
            bool lagHit = def.State == "lag";
            int dmg = Mathf.Max(1, Mathf.RoundToInt(pow * A / D * stab * eff * (crit ? 1.5f : 1) * (lagHit ? LagDmg : 1) * Util.Rand(.88f, 1.12f)));
            if (lagHit) PopText(def.X, def.Y - 118, "スキあり！", H("#ff9a8a"), 1);
            bool heavy = pow >= 19;
            if (def.V.Sub > 0 && m.Id != "hyper-voice" && m.Id != "alluring-voice" && m.Id != "psychic-noise")
            {
                def.V.Sub -= dmg; PopText(def.X, def.Y - 66, dmg.ToString(), H("#e8e0cc"));
                Fxs.Add(new Fx { Type = "impact", X = def.X, Y = def.Y - BODY, Rad = 22, Rot = Util.Value, Life = .28f, Max = .28f });
                if (def.V.Sub <= 0) { def.V.Sub = 0; Say($"{def.Sp.N}の デコイは こわれた！"); Burst(def.X, def.Y - BODY, Color.white, 16, 120, .5f); }
                AfterHitSelf(att, def, m, dmg);
                return true;
            }
            dmg = Mathf.Min(dmg, Mathf.CeilToInt(def.Hp));
            def.Hp = Mathf.Max(0, def.Hp - dmg); def.Flash = .12f;
            def.Cur = null; if (def.V.Rampage == 0) def.Queued = null;
            if (!lagHit) { def.State = "stun"; def.StT = heavy ? .45f : .25f; }
            def.Kx = Mathf.Cos(ang) * (heavy ? 230 : 140) * K; def.Ky = Mathf.Sin(ang) * (heavy ? 230 : 140) * K;
            Hitstop = Mathf.Max(Hitstop, heavy ? .08f : .04f);
            Shake = Mathf.Max(Shake, heavy ? 5 : 2);
            Cheer = Mathf.Min(1, Cheer + (heavy ? .7f : .3f));
            PopText(def.X + Util.Rand(-6, 6), def.Y - 66, dmg.ToString(), eff > 1 ? H("#ffd166") : eff < 1 ? H("#a49ac0") : Color.white, eff > 1 || heavy ? 1 : 0);
            Burst(def.X, def.Y - BODY, MoveCol(m), heavy ? 16 : 8, 110, .4f);
            Fxs.Add(new Fx { Type = "impact", X = def.X, Y = def.Y - BODY, Rad = heavy ? 34 : 22, Rot = Util.Value, Life = .28f, Max = .28f });
            if (crit) PopText(def.X, def.Y - 104, "きゅうしょ！", H("#ff9ad0"), 1);
            if (heavy || eff > 1 || crit) { PopText(def.X + Util.Rand(-10, 10), def.Y - 92, Util.Choice(Comic), H("#ffd84a"), 2); def.Dizzy = 1; }
            if (eff > 1) Say("ばつぐんの いりょくだ！");
            else if (eff < 1) Say("あまり きいていない ようだ…");
            if (def.Status == "frz" && m.T == "fire") { def.Status = ""; Say($"{def.Sp.N}の こおりが とけた！"); }
            var e = m.E;
            if (def.Hp > 0)
            {
                if (!string.IsNullOrEmpty(e.St) && Util.Value * 100 < e.StCh) SetStatus(def, e.St, att);
                if (e.Flinch > 0 && !lagHit && Util.Value * 100 < e.Flinch) { def.State = "stun"; def.StT = Mathf.Max(def.StT, .7f); PopText(def.X, def.Y - 80, "ひるんだ！", Color.white); }
                if (e.Foe != null && Util.Value * 100 < e.FoeCh) ChangeStages(def, e.Foe);
                if (m.HealBlock) def.V.HealBlock = 6;
                if (m.ConfuseIfBoosted && StageKeys.Any(k => def.St[k] > 0)) { def.V.Confuse = 3; Say($"{def.Sp.N}は こんらんした！"); }
            }
            AfterHitSelf(att, def, m, dmg);
            // カウンター（はんしゃのまく・はがねのしかえし）
            if (def.V.CounterT > 0 && (def.V.CounterCtr == "any" || (def.V.CounterCtr == "spec" && m.Cat == "spec")) && def.Hp > 0 && Targetable(att))
            {
                int back = Mathf.RoundToInt(dmg * def.V.CounterMult); def.V.CounterT = 0;
                att.Hp = Mathf.Max(0, att.Hp - back); att.Flash = .12f;
                Fxs.Add(new Fx { Type = "ray", X0 = def.X, Y0 = def.Y - BODY, X1 = att.X, Y1 = att.Y - BODY, Col = Color.white, Life = .3f, Max = .3f });
                PopText(att.X, att.Y - 66, back.ToString(), H("#ffd166"), 1); Say($"{def.Sp.N}は ダメージを はねかえした！");
                if (att.Hp <= 0) Faint(att);
            }
            if (def.Hp <= 0)
            {
                if (def.V.DBond > 0 && att.Hp > 0) { Say($"{def.Sp.N}は {att.Sp.N}を みちづれにした！"); att.Hp = 0; Faint(att); }
                Faint(def);
            }
            return true;
        }

        // 攻撃した側への効果（吸収・反動・能力変化・いれかえ）
        void AfterHitSelf(Fighter att, Fighter def, Move m, int dmg)
        {
            var e = m.E;
            if (e.Drain > 0 && att.Hp > 0 && att.V.HealBlock <= 0) HealHp(att, dmg * e.Drain / 100f);
            if (e.Recoil > 0 && att.Hp > 0) { int r = Mathf.Max(1, Mathf.RoundToInt(dmg * e.Recoil / 100f)); att.Hp = Mathf.Max(0, att.Hp - r); PopText(att.X, att.Y - 66, $"-{r}", H("#ff9a8a")); if (att.Hp <= 0) Faint(att); }
            if (e.Self != null && att.Hp > 0) ChangeStages(att, e.Self);
            if (m.RapidSpin) { var hz = Sides[att.Side].Hz; hz.Rocks = hz.Spikes = hz.TSpikes = 0; att.V.Seed = 0; }
            if (m.SwitchOut && att.Hp > 0 && Kind == "cup" && att == Active(att.Side)) { int idx = BenchIdx(att.Side, false); if (idx >= 0) att.PendingOut = idx; }
        }

        bool StatusHit(Fighter att, Fighter def, Move m)
        {
            var e = m.E;
            if (e.Seed)
            {
                if (def.HasType("grass") || def.V.Seed > 0 || def.V.Sub > 0) { Say("でも うまく きまらなかった！"); return false; }
                def.V.Seed = att.Side + 1; Say($"{def.Sp.N}に タネを うえつけた！"); return true;
            }
            if (!string.IsNullOrEmpty(e.St) && !SetStatus(def, e.St, att)) { Say("でも うまく きまらなかった！"); return false; }
            return true;
        }

        void Faint(Fighter f)
        {
            if (f.State == "faint" || f.Fainted) return;
            f.State = "faint"; f.StT = 1.2f; f.Cur = null; f.Queued = null;
            Cheer = 1; Shake = Mathf.Max(Shake, 6);
            Say($"{Prefix(f)}{f.Sp.N}は たおれた！");
            Burst(f.X, f.Y - BODY, Color.white, 24, 140, .7f);
            if (f.Side == 1)
            {
                var me = Active(0);
                if (me != null) { _exp.TryGetValue(me.Mon.uid, out var e0); _exp[me.Mon.uid] = e0 + Mathf.RoundToInt((f.Lvl * 6 + 4) * (Kind == "cup" ? 1.5f : 1)); }
            }
        }
        void AfterFaint(Fighter f)
        {
            f.Fainted = true; f.State = "bench";
            int next = BenchIdx(f.Side, false);
            if (next < 0) { EndBattle(f.Side == 0 ? "lose" : "win"); return; }
            _pendingSend = new Pending { Side = f.Side, Idx = next, T = .5f };
        }

        // ---------- 回避 ----------
        (float, Func<float, float, bool>) ThreatDir(Fighter f, Fighter o)
        {
            if (o != null && o.Cur != null && o.State == "wind" && o.Cur.M.IsZone)
            {
                var cur = o.Cur; var m = cur.M; float b;
                if (m.K == "beam" || m.K == "dash") { float s = Mathf.Sign(-(f.X - o.X) * Mathf.Sin(cur.Ang) + (f.Y - o.Y) * Mathf.Cos(cur.Ang)); if (s == 0) s = 1; b = cur.Ang + s * Mathf.PI / 2; }
                else if (m.K == "strike") b = Mathf.Atan2(f.Y - cur.Ty, f.X - cur.Tx);
                else if (m.K == "cone" || m.K == "swipe") { float s = Mathf.Sign(Util.WrapAng(Mathf.Atan2(f.Y - o.Y, f.X - o.X) - cur.Ang)); if (s == 0) s = 1; b = cur.Ang + s * 1.6f; }
                else b = Mathf.Atan2(f.Y - o.Y, f.X - o.X);
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
            float reach = 250 * K * .22f, dir;
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
            f.Cur = null; if (f.V.Rampage == 0) f.Queued = null;
            f.State = "dodge"; f.StT = .22f; f.Dvx = Mathf.Cos(dir) * 250 * K; f.Dvy = Mathf.Sin(dir) * 250 * K;
            f.Inv = .3f; f.DodgeCd = f.Side == 0 ? .9f : 1.4f; f.GhostT = 0;
        }

        // ---------- AI ----------
        void AiDodgeCheck(Fighter f, Fighter o)
        {
            float skill = f.Side == 0 ? (S.auto ? .5f : 0) : Skill;
            if (skill <= 0 || f.DodgeCd > 0 || !(f.State == "free" || f.State == "act") || !CanAct(f)) return;
            if (o != null && o.State == "wind" && o.Cur != null && o.Cur.M.IsZone && o.Cur.M.Damaging)
            {
                if (f.PlanFor != o.Cur.Uid)
                {
                    f.PlanFor = o.Cur.Uid;
                    var guard = f.Moves.FirstOrDefault(id => (Data.Moves[id].K == "protect" || Data.Moves[id].K == "counter") && f.CdOf(id) <= 0 && MoveBlocked(f, id) == null);
                    f.Plan = new Plan { Will = Util.Value < skill, At = Util.Rand(.12f, .4f) * o.Cur.Wind / .8f, Guard = guard != null && Util.Value < .4f ? guard : null };
                }
                if (f.Plan.Will && o.Cur.T >= f.Plan.At && InZone(o.Cur, o, f.X, f.Y, f.R))
                {
                    var g = f.Plan.Guard; var gm = g != null ? Data.Moves[g] : null;
                    if (gm != null && (gm.K == "protect" || gm.Ctr == "any" || o.Cur.M.Cat == "spec")) { f.Plan.Guard = null; BeginMove(f, g); return; }
                    StartDodge(f, null); return;
                }
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

        // AI の わざえらび：状況に あわせて 重みづけ
        string AiPickMove(Fighter f, Fighter o)
        {
            var opts = new List<(string, float)>();
            foreach (var id in f.Moves)
            {
                if (f.CdOf(id) > 0 || MoveBlocked(f, id) != null) continue;
                var m = Data.Moves[id]; var e = m.E; float w = 0;
                if (m.Damaging)
                {
                    float eff = Data.EffVs(m.T, o.Sp) * (m.SuperVsWater && o.HasType("water") ? 4 : 1);
                    if (eff == 0) continue;
                    w = (m.Pow > 0 ? m.Pow : 8) / 10 * eff * (f.HasType(m.T) ? 1.3f : 1);
                    if (m.Ohko && o.Lvl > f.Lvl) continue;
                    if (m.Fakeout && f.EnterT > 1.8f) continue;
                    if (m.Sucker && !(o.State == "wind" && o.Cur != null && o.Cur.M.Damaging)) continue;
                    if (m.SwitchOut && Kind != "cup") w *= .8f;
                }
                else switch (m.K)
                    {
                        case "heal": w = f.Hp < f.MaxHp * .5f ? 4 : 0; break;
                        case "self": w = e.Self != null && e.Self.Keys.All(k => f.St[k] < 2) && f.Hp > f.MaxHp * .5f ? 2.2f : 0; break;
                        case "protect": case "counter": w = 0; break;
                        case "sub": w = f.V.Sub <= 0 && f.Hp > f.MaxHp * .55f ? 1.5f : 0; break;
                        case "dbond": w = f.Hp < f.MaxHp * .3f ? 2.5f : 0; break;
                        case "curse": w = f.St["atk"] < 2 ? 1.2f : 0; break;
                        case "field": w = m.Fld == "trickroom" ? (TrickRoom <= 0 && f.BaseSpd < o.BaseSpd ? 2.5f : 0) : (Sides[f.Side].Tail <= 0 ? 1.8f : 0); break;
                        case "hazard":
                            {
                                var hz = Sides[1 - f.Side].Hz; int cur = m.Hz == "rocks" ? hz.Rocks : m.Hz == "spikes" ? hz.Spikes : hz.TSpikes, max = m.Hz == "rocks" ? 1 : m.Hz == "spikes" ? 3 : 2;
                                w = cur < max && Sides[1 - f.Side].Fs.Count > 1 ? 1.6f : 0; break;
                            }
                        case "baton": w = StageKeys.Any(k => f.St[k] >= 2) && BenchIdx(f.Side, false) >= 0 ? 2 : 0; break;
                        case "ray":
                            if (m.Sp == "taunt") w = o.V.Taunt <= 0 && o.Moves.Any(x => Data.Moves[x].Cat == "stat") ? 1.5f : 0;
                            else if (m.Sp == "encore") w = o.LastMove != null && Data.Moves[o.LastMove].Cat == "stat" && o.V.EncoreId == null ? 2.5f : 0;
                            else if (m.Sp == "yawn") w = o.Status == "" && o.V.Yawn <= 0 ? 1.8f : 0;
                            else w = StageKeys.Any(k => o.St[k] > 0) ? 2 : 0;
                            break;
                        default:
                            if (e.Seed) w = o.V.Seed == 0 && !o.HasType("grass") ? 1.6f : 0;
                            else w = o.Status == "" ? 1.8f : 0;
                            break;
                    }
                if (w > 0) opts.Add((id, w));
            }
            if (opts.Count == 0) return null;
            float r = Util.Value * opts.Sum(x => x.Item2);
            foreach (var (id, w) in opts) { r -= w; if (r <= 0) return id; }
            return opts[0].Item1;
        }

        static float MoveReach(Fighter f, Fighter o, Move m)
        {
            switch (m.K)
            {
                case "melee": return f.R + o.R + 18;
                case "swipe": return m.Rad + f.R + o.R * .5f;
                case "dash": return m.Len * .8f;
                case "aoe": return m.Rad * .75f;
                case "beam": return m.Len * .8f;
                case "cone": return m.Rad * .8f;
                case "multi": return 260;
                default: return 999;
            }
        }

        // あいてトレーナーの交代：タイプで ふりなら ひかえと いれかえる（出てきた直後は スキ）
        bool AiSwitch(Fighter f, Fighter o, float dt)
        {
            var sd = Sides[f.Side];
            if (Kind != "cup" || sd.SwapCd > 0 || f.State != "free" || f.V.Rampage > 0) return false;
            f.SwapT -= dt; if (f.SwapT > 0) return false;
            f.SwapT = Util.Rand(2.5f, 4.5f);
            float Threat(Fighter x) => Mathf.Max(1, o.Moves.Where(id => Data.Moves[id].Damaging).Select(id => Data.EffVs(Data.Moves[id].T, x.Sp)).DefaultIfEmpty(1).Max());
            float now = Threat(f);
            if (now < 2 || f.Hp < f.MaxHp * .3f) return false;
            int best = -1; float bv = now;
            for (int i = 0; i < sd.Fs.Count; i++) { var x = sd.Fs[i]; if (i != sd.Act && !x.Fainted && x.Hp > 0) { float v = Threat(x); if (v < bv) { bv = v; best = i; } } }
            if (best < 0 || Util.Value > .3f + Skill * .5f) return false;
            DoSwitch(f, best, null, false);
            return true;
        }

        void AiMove(Fighter f, Fighter o, float dt, bool autoSpecial)
        {
            float d = Dist(f, o), ang = Mathf.Atan2(o.Y - f.Y, o.X - f.X);
            if (f.Side == 1 && AiSwitch(f, o, dt)) return;
            if (autoSpecial && f.Queued == null)
            {
                f.AiT -= dt;
                if (f.AiT <= 0)
                {
                    f.AiT = Util.Rand(.5f, 1.3f) * (f.Side == 1 ? (1.2f - Skill * .5f) : 1);
                    if (Util.Value < .8f) f.Queued = AiPickMove(f, o);
                }
            }
            if (f.Queued != null && MoveBlocked(f, f.Queued) != null) f.Queued = null;
            if (f.Queued != null)
            {
                var m = Data.Moves[f.Queued];
                if (d <= MoveReach(f, o, m)) { var q = f.Queued; f.Queued = null; BeginMove(f, q); return; }
                MoveDir(f, Mathf.Cos(ang), Mathf.Sin(ang), dt); return;
            }
            float reach = f.R + o.R + 14;
            if (d < reach && f.CdOf("tackle") <= 0 && f.V.EncoreId == null) { BeginMove(f, "tackle"); return; }
            f.StratT -= dt;
            if (f.StratT <= 0) { f.StratT = Util.Rand(.4f, .9f); if (Util.Value < .3f) f.Strafe *= -1; }
            bool allCd = f.Moves.All(id => f.CdOf(id) > 1.2f);
            float pref = f.Sp.Style == "melee" ? 0 : f.Sp.Style == "mid" ? 96 : 160;
            if (allCd || !autoSpecial) pref = f.Sp.Style == "ranged" && autoSpecial ? 96 : 0;
            float k = Util.Clamp((d - pref) / 48, -1, 1), tang = ang + f.Strafe * Mathf.PI / 2;
            float mx = Mathf.Cos(ang) * k + Mathf.Cos(tang) * .6f, my = Mathf.Sin(ang) * k + Mathf.Sin(tang) * .6f;
            // 予兆の はんいの中なら 外へ にげる（命中100未満の わざは これで よけられる）
            if (o.State == "wind" && o.Cur != null && o.Cur.M.IsZone && InZone(o.Cur, o, f.X, f.Y, f.R) && Util.Value < (f.Side == 1 ? Skill : .5f) + .3f)
            {
                var (b, _) = ThreatDir(f, o); mx = Mathf.Cos(b) * 1.5f; my = Mathf.Sin(b) * 1.5f;
            }
            const float mg = 40;
            if (f.X < St.Fx0 + mg) mx += 1; if (f.X > St.Fx1 - mg) mx -= 1; if (f.Y < St.Fy0 + mg) my += 1; if (f.Y > St.Fy1 - mg) my -= 1;
            float L = Hyp(mx, my); if (L > 1) { mx /= L; my /= L; }
            MoveDir(f, mx, my, dt);
        }

        void MoveDir(Fighter f, float mx, float my, float dt)
        {
            if (f.V.Confuse > 0) { float a = Mathf.Atan2(my, mx) + Mathf.Sin(T * 3 + f.Side) * 2.2f, L = Hyp(mx, my); mx = Mathf.Cos(a) * L; my = Mathf.Sin(a) * L; }
            float sp = SpeedOf(f);
            if (St.Pools.Count > 0 && St.InPool(f.X, f.Y))
            {
                sp *= f.Sp.Type == "water" ? 1.2f : .6f;
                f.SplashT -= dt;
                if (f.SplashT <= 0 && (mx != 0 || my != 0)) { f.SplashT = .12f; Parts.Add(new Part { X = f.X + Util.Rand(-5, 5), Y = f.Y, Vx = Util.Rand(-20, 20), Vy = -40, Life = .3f, Max = .3f, Col = H("#bfe4ff"), Size = 2, G = 200 }); }
            }
            f.X += mx * sp * dt; f.Y += my * sp * dt;
            f.Moving = Hyp(mx, my) > .15f; if (f.Moving) f.Walk += dt;
        }

        // ---------- 時間で すすむ 効果 ----------
        void UpdateEffects(Fighter f, float dt)
        {
            var v = f.V;
            v.Taunt = Mathf.Max(0, v.Taunt - dt); v.HealBlock = Mathf.Max(0, v.HealBlock - dt); v.Confuse = Mathf.Max(0, v.Confuse - dt);
            v.Protect = Mathf.Max(0, v.Protect - dt); v.DBond = Mathf.Max(0, v.DBond - dt); v.CounterT = Mathf.Max(0, v.CounterT - dt);
            if (v.EncoreId != null) { v.EncoreT -= dt; if (v.EncoreT <= 0) v.EncoreId = null; }
            if (v.Yawn > 0) { v.Yawn -= dt; if (v.Yawn <= 0) { v.Yawn = 0; SetStatus(f, "slp", null); } }
            if (f.Status == "slp" || f.Status == "frz")
            {
                f.StatusT -= dt;
                if (f.StatusT <= 0) { Say($"{Prefix(f)}{f.Sp.N}は {(f.Status == "slp" ? "めを さました" : "こおりが とけた")}！"); f.Status = ""; }
            }
            if (f.Status == "par")
            {
                f.ParT -= dt;
                if (f.ParT <= 0) { f.ParT = 2.5f; if (Util.Value < .25f && (f.State == "free" || f.State == "act")) { f.State = "stun"; f.StT = .8f; PopText(f.X, f.Y - 80, "しびれて うごけない！", H("#ffd84a")); } }
            }
            f.TickT -= dt;
            if (f.TickT <= 0)
            {
                f.TickT = Tick;
                float dmg = 0; var col = H("#b86ad8");
                if (f.Status == "brn") { dmg += f.MaxHp / 16; col = H("#ff8a3d"); }
                if (f.Status == "psn") dmg += f.MaxHp / 8;
                if (f.Status == "tox") { dmg += f.MaxHp * f.ToxN / 16; f.ToxN = Mathf.Min(15, f.ToxN + 1); }
                if (v.Curse) { dmg += f.MaxHp / 4; col = H("#8a78c8"); }
                if (v.Seed > 0)
                {
                    int s = Mathf.Max(1, Mathf.RoundToInt(f.MaxHp / 8)); dmg += s; col = H("#62d26f");
                    var tgt = Active(v.Seed - 1); if (tgt != null && tgt.Hp > 0 && tgt != f && tgt.V.HealBlock <= 0) HealHp(tgt, s);
                }
                if (dmg > 0)
                {
                    int di = Mathf.Max(1, Mathf.RoundToInt(dmg)); f.Hp = Mathf.Max(0, f.Hp - di);
                    PopText(f.X, f.Y - 66, $"-{di}", col); Burst(f.X, f.Y - BODY, col, 6, 40, .4f);
                    if (f.Hp <= 0) Faint(f);
                }
            }
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
            if (Targetable(f)) { f.EnterT += dt; UpdateEffects(f, dt); if (f.State == "faint") return; }
            if (f.Shots.Count > 0)
            {
                foreach (var s in f.Shots) s.T -= dt;
                foreach (var s in f.Shots.Where(s => s.T <= 0).ToList()) SpawnProj(f, s.M, s.Ang);
                f.Shots.RemoveAll(s => s.T <= 0);
            }
            if (f.PendingOut >= 0 && (f.State == "act" || f.State == "free")) { int idx = f.PendingOut; f.PendingOut = -1; DoSwitch(f, idx, null, false); }
            switch (f.State)
            {
                case "bench": case "capt": return;
                case "enter":
                    f.StT -= dt; f.Scale = Util.Clamp(1 - f.StT / .5f, 0, 1);
                    if (f.StT <= 0)
                    {
                        f.Scale = 1;
                        if (f.SwapLag > 0) { f.State = "lag"; f.StT = f.LagMax = f.SwapLag; f.SwapLag = 0; PopText(f.X, f.Y - 80, "スキ！", H("#ff9a8a"), 1); }
                        else f.State = "free";
                    }
                    break;
                case "lag": // 交代直後：うごけない（かわす も だめ）
                    f.StT -= dt; if (f.StT <= 0) { f.State = "free"; PopText(f.X, f.Y - 80, "じゅんびOK", H("#7bd88f")); }
                    break;
                case "return":
                    f.StT -= dt; f.Scale = Util.Clamp(f.StT / .3f, 0, 1);
                    if (f.StT <= 0)
                    {
                        f.State = "bench"; f.Scale = 1; f.V = new Volatile(); f.St = Fighter.NewStages(); if (f.Status == "tox") f.ToxN = 1;
                        _pendingSend = new Pending { Side = f.Side, Idx = _swapTo, T = .2f, Pass = _swapPass, Lag = true }; _swapPass = null;
                    }
                    return;
                case "faint":
                    f.StT -= dt; if (f.StT <= 0) AfterFaint(f); return;
                case "free":
                    {
                        if (!CanAct(f)) break; // ねむり・こおり
                        if (!oT) break;
                        AiDodgeCheck(f, o);
                        if (f.State != "free") break;
                        if (f.V.EncoreId != null && f.Queued != null && f.Queued != f.V.EncoreId) f.Queued = null;
                        // 移動は モンスター自身が おこなう。オートOFFなら わざは プレイヤーの 指示だけ
                        AiMove(f, o, dt, f.Side == 0 ? (S.auto && f.V.Rampage == 0) : f.V.Rampage == 0);
                        break;
                    }
                case "wind":
                    {
                        var cur = f.Cur; if (cur == null) { f.State = "free"; break; }
                        cur.T += dt; var m = cur.M;
                        // 命中100（ロック）の わざだけ 予兆の とちゅうまで あいてを 追う
                        if (oT && m.Aim == "lock")
                        {
                            if ((m.K == "beam" || m.K == "dash" || m.K == "cone") && cur.T < cur.Wind * .6f)
                            {
                                float want = Mathf.Atan2(o.Y - f.Y, o.X - f.X);
                                cur.Ang += Util.Clamp(Util.WrapAng(want - cur.Ang), -3 * dt, 3 * dt);
                            }
                            if (m.K == "strike" && cur.T < cur.Wind * .75f) { cur.Tx += (o.X - cur.Tx) * Mathf.Min(1, dt * 8); cur.Ty += (o.Y - cur.Ty) * Mathf.Min(1, dt * 8); }
                        }
                        if (m.K == "melee" && oT && Dist(f, o) > f.R + o.R + 6) { float a = Mathf.Atan2(o.Y - f.Y, o.X - f.X); f.X += Mathf.Cos(a) * 120 * dt; f.Y += Mathf.Sin(a) * 120 * dt; }
                        if (cur.T >= cur.Wind) FireMove(f);
                        if (f.Side != 0) AiDodgeCheck(f, o);
                        break;
                    }
                case "dash":
                    {
                        var cur = f.Cur; if (cur == null) { f.State = "free"; break; }
                        float sp = (cur.M.Prio > 0 ? 420 : 300) * K;
                        float px = f.X + Mathf.Cos(cur.Ang) * sp * dt, py = f.Y + Mathf.Sin(cur.Ang) * sp * dt;
                        f.X = px; f.Y = py; cur.D += sp * dt; f.Moving = true; f.Walk += dt * 3;
                        if (Util.Value < .6f) Parts.Add(new Part { X = f.X + Util.Rand(-6, 6), Y = f.Y + 2, Vy = -10, Life = .3f, Max = .3f, Col = MoveCol(cur.M), Size = 3 });
                        if (!cur.Hit && oT && Dist(f, o) < f.R + o.R + 4) { cur.Hit = true; Hit(f, o, cur.M, cur.Ang); }
                        if (f.State != "dash") break;
                        ClampF(f);
                        bool wall = Mathf.Abs(f.X - px) > .5f || Mathf.Abs(f.Y - py) > .5f;
                        if (cur.D >= cur.M.Len || wall)
                        {
                            if (wall) { Shake = Mathf.Max(Shake, 4); AddDecal(f.X, f.Y, 14, "crater"); Burst(f.X, f.Y, H("#c9b8ff"), 8, 70, .35f); }
                            EndAct(f, wall ? .6f : .35f);
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
        float CatchProb(Fighter e) => Util.Clamp(e.Sp.Catch * (1.6f - 1.3f * e.Hp / e.MaxHp) * (e.State == "stun" ? 1.15f : 1) * (e.Status == "slp" || e.Status == "frz" ? 2 : e.Status != "" ? 1.5f : 1), .04f, .95f);
        public void CmdCapsule()
        {
            if (Kind != "wild" || Mode != "fight" || Catch != null || Paused) return;
            if (S.capsules <= 0) { Say("クリスタルが もう ない！"); return; }
            var e = Active(1); if (!Targetable(e)) return;
            S.capsules--; S.Save();
            var tr = Sides[0].Trainer; tr.Shout = .6f;
            Mode = "catch";
            Catch = new CatchO { Phase = "throw", Sx = tr.X, Sy = tr.Y - 30, Tx = e.X, Ty = e.Y - 12, P = CatchProb(e), X = tr.X, Y = tr.Y };
            Say("いけっ！ ふういんクリスタル！");
        }
        static readonly string[] FailLines = { "ああっ！ クリスタルから でてしまった！", "おしい！ もうすこしだったのに！", "だめだ！ にげだした！" };
        void UpdateCatch(float dt)
        {
            var c = Catch; var e = Active(1); c.T += dt;
            if (c.Phase == "throw")
            {
                float k = Mathf.Min(1, c.T / .55f);
                c.X = c.Sx + (c.Tx - c.Sx) * k; c.Y = c.Sy + (c.Ty - c.Sy) * k - Mathf.Sin(k * Mathf.PI) * 80;
                if (k >= 1) { c.Phase = "suck"; c.T = 0; e.State = "capt"; Burst(c.Tx, c.Ty, H("#9ff0ff"), 20, 100, .5f); Fxs.Add(new Fx { Type = "ring", X = c.Tx, Y = c.Ty, Rad = 20, Col = H("#9ff0ff"), Life = .3f, Max = .3f }); }
            }
            else if (c.Phase == "suck") { c.Y = c.Ty + Mathf.Min(1, c.T / .3f) * 6; if (c.T > .45f) { c.Phase = "shake"; c.T = 0; } }
            else if (c.Phase == "shake" && c.T >= .6f)
            {
                c.T = 0;
                if (Util.Value < Mathf.Pow(c.P, 1f / 3))
                {
                    c.Shakes++;
                    if (c.Shakes >= 3) { c.Phase = "done"; Burst(c.X, c.Y, H("#ffd166"), 24, 90, .8f); Say($"やった！ {e.Sp.N}を つかまえた！"); Cheer = 1; EndBattle("caught"); }
                }
                else
                {
                    c.Phase = "fail"; e.State = "stun"; e.StT = .4f; e.Inv = .4f;
                    Burst(c.X, c.Y, Color.white, 20, 120, .5f); Say(Util.Choice(FailLines));
                    Catch = null; Mode = "fight";
                }
            }
        }

        // ---------- コマンド ----------
        bool CanCommand => Mode == "fight" && !Paused;
        public void CmdMove(int i)
        {
            if (!CanCommand) return;
            var f = Active(0); if (f == null || i >= f.Moves.Count) return;
            var id = f.Moves[i];
            var blk = MoveBlocked(f, id); if (blk != null) { Say($"{Data.Moves[id].N}は いま つかえない！（{blk}）"); return; }
            if (f.CdOf(id) > 0) return;
            f.Queued = id;
        }
        public void CmdAttack()
        {
            if (!CanCommand) return;
            var f = Active(0); if (f == null || f.CdOf("tackle") > 0 || f.V.EncoreId != null) return;
            f.Queued = "tackle";
        }
        public void CmdDodge()
        {
            if (!CanCommand) return;
            var f = Active(0); if (f == null || f.DodgeCd > 0 || !(f.State == "free" || f.State == "act" || f.State == "wind") || !CanAct(f)) return;
            StartDodge(f, InputActive ? Mathf.Atan2(InputVec.y, InputVec.x) : (float?)null);
        }
        public bool CanSwap(out List<int> bench)
        {
            bench = new List<int>();
            if (!CanCommand || Sides[0].SwapCd > 0) return false;
            var f = Active(0); if (f == null || !(f.State == "free" || f.State == "act" || f.State == "stun")) return false;
            for (int i = 0; i < Sides[0].Fs.Count; i++) { var x = Sides[0].Fs[i]; if (i != Sides[0].Act && !x.Fainted && x.Hp > 0) bench.Add(i); }
            return bench.Count > 0;
        }
        public void DoPlayerSwap(int idx)
        {
            if (!CanSwap(out var bench) || !bench.Contains(idx)) return;
            var f = Active(0); DoSwitch(f, idx, null, false); Say($"もどれ、{f.Sp.N}！ いけっ、{Sides[0].Fs[idx].Sp.N}！");
        }
        public void CmdRun() { if (!CanCommand || Kind != "wild") return; Say("うまく にげきれた！"); EndBattle("run"); }
        /// <summary>動作確認用：次にこのわざを使わせる</summary>
        public void Force(string id) { var f = Active(0); if (f != null && Mode == "fight") { f.Cd[id] = 0; f.Queued = id; } }

        // ---------- メインループ ----------
        public void Step(float dt)
        {
            if (Paused) return;
            foreach (var sd in Sides) if (sd.Trainer != null) sd.Trainer.Shout = Mathf.Max(0, sd.Trainer.Shout - dt);
            if (Hitstop > 0) { Hitstop -= dt; return; }
            T += dt; ModeT += dt;
            Cheer = Mathf.Max(.15f, Cheer - dt * .4f);
            Shake = Mathf.Max(0, Shake - dt * 20);
            if (TrickRoom > 0) { TrickRoom -= dt; if (TrickRoom <= 0) Say("ねじれた じくうが もとに もどった！"); }
            foreach (var sd in Sides) sd.SwapCd = Mathf.Max(0, sd.SwapCd - dt);
            foreach (var sd in Sides) if (sd.Tail > 0) { sd.Tail -= dt; if (sd.Tail <= 0) Say("おいかぜが やんだ"); }

            if (Mode == "intro")
            {
                if (_sent == 0 && ModeT > .8f) { _sent = 1; SendOut(1, 0); }
                if (_sent == 1 && ModeT > 1.7f) { _sent = 2; SendOut(0, 0); }
                if (ModeT > 2.3f) { Mode = "fight"; ModeT = 0; Say("バトル スタート！"); }
            }
            if (_pendingSend != null) { _pendingSend.T -= dt; if (_pendingSend.T <= 0) { var p = _pendingSend; _pendingSend = null; SendOut(p.Side, p.Idx, p.Pass, p.Lag); } }

            if (Mode == "catch") UpdateCatch(dt);
            else if (Mode == "fight" || Mode == "intro")
            {
                Fighter a = Active(0), e = Active(1);
                UpdateFighter(a, dt);
                if (Mode == "fight" || Mode == "intro") UpdateFighter(e, dt);
                if (Targetable(a) && Targetable(e))
                {
                    float d = Dist(a, e), min = a.R + e.R - 2;
                    if (d < min && d > .001f) { float p = min - d, nx = (a.X - e.X) / d, ny = (a.Y - e.Y) / d; a.X += nx * p * .5f; a.Y += ny * p * .5f; e.X -= nx * p * .5f; e.Y -= ny * p * .5f; ClampF(a); ClampF(e); }
                }
                foreach (var p in Projs.ToList())
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
                    if (p.X < St.Fx0 - 10 || p.X > St.Fx1 + 10 || p.Y < St.Fy0 - 40 || p.Y > St.Fy1 + 4) { p.Life = 0; Burst(p.X, p.Y, MoveCol(p.M), 4, 40, .25f); }
                }
                Projs.RemoveAll(p => p.Life <= 0);
            }
            if (Mode == "end") EndT -= dt;

            foreach (var q in Parts) { q.X += q.Vx * dt; q.Y += q.Vy * dt; q.Vy += q.G * dt; q.Vx *= .96f; q.Life -= dt; }
            Parts.RemoveAll(q => q.Life <= 0);
            if (Parts.Count > 600) Parts.RemoveRange(0, Parts.Count - 600);
            foreach (var t in Texts) { t.Y -= 22 * dt; t.Life -= dt; }
            Texts.RemoveAll(t => t.Life <= 0);
            foreach (var fx in Fxs) fx.Life -= dt;
            Fxs.RemoveAll(fx => fx.Life <= 0);

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
                tz = Util.Clamp(1.02f - d / 900, St.Kind == "stadium" ? .6f : .66f, .96f);
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
            void Grant(MonData m, int x, string tag = "")
            {
                int before = m.lvl, ups = SaveData.GainExp(m, x);
                lines.Add($"{Data.Species[m.sid].N} は けいけんち {x} を もらった{tag}");
                if (ups > 0)
                {
                    lines.Add($"<color=#ffd166>{Data.Species[m.sid].N} は Lv{before} → Lv{m.lvl} に あがった！</color>");
                    foreach (var le in Data.Species[m.sid].Learn)
                        if (le.Lv > before && le.Lv <= m.lvl)
                        {
                            lines.Add($"{Data.Species[m.sid].N}は あたらしく 「{Data.Moves[le.Id].N}」を おぼえた！");
                            var eq = Data.Equipped(m); if (eq.Count < 4 && !eq.Contains(le.Id)) eq.Add(le.Id);
                        }
                }
            }
            foreach (var kv in _exp) { var m = S.party.Find(x => x.uid == kv.Key); if (m != null) Grant(m, kv.Value); }
            if (Kind == "wild")
            {
                if (res == "caught")
                {
                    var e = Active(1); var nm = S.NewMon(e.Mon.sid, e.Mon.lvl);
                    S.caught++;
                    if (S.party.Count < 6) { S.party.Add(nm); lines.Insert(0, $"{Data.Species[nm.sid].N}（Lv{nm.lvl}）が パーティに くわわった！"); }
                    else { S.box.Add(nm); lines.Insert(0, $"{Data.Species[nm.sid].N}（Lv{nm.lvl}）は ボックスに おくられた"); }
                    var me = Active(0); if (me != null) Grant(me.Mon, 6 + e.Lvl * 3);
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
                    foreach (var f in Sides[0].Fs) Grant(f.Mon, 4 + r.Lv, "（ボーナス）");
                    S.round++;
                    if (S.round >= Data.Rounds.Length) { S.round = 0; S.trophies++; lines.Insert(0, $"<color=#ffd166>{Data.CupName(S.tier)} ゆうしょう！</color>"); S.tier++; lines.Add($"つぎは {Data.CupName(S.tier)} に ちょうせんできる！"); }
                    else lines.Insert(0, $"{r.N} とっぱ！ つぎは {Data.Rounds[S.round].N}");
                }
                else if (res == "lose") { S.round = 0; lines.Insert(0, "まけてしまった… たいかいは 1かいせんから やりなおし"); }
            }
            if (S.capsules > caps0) lines.Add($"クリスタルを {S.capsules - caps0}こ てにいれた");
            S.Save();
        }
    }
}
