using System.Collections.Generic;
using UnityEngine;

namespace PixelMonsterArena
{
    public class TypeInfo
    {
        public readonly string N;
        public readonly Color C;
        public TypeInfo(string n, string hex) { N = n; C = Util.Hex(hex); }
    }

    /// <summary>わざの追加効果</summary>
    public class MoveEffect
    {
        public string St;              // brn / par / psn / tox / frz
        public int StCh, Flinch, Drain, Recoil, Heal, FoeCh;
        public Dictionary<string, int> Self, Foe; // 能力ランク変化
        public bool Seed;
    }

    /// <summary>
    /// わざ。K: melee=近接 / swipe=前方おうぎ / proj=弾 / beam=直線 / cone=おうぎ / aoe=自分の周囲 / strike=相手の足元 /
    /// multi=複数の範囲 / dash=突進 / それ以外は補助。Aim: lock=相手をねらう（命中100）, dir=方向・範囲指定（命中100未満）
    /// </summary>
    public class Move
    {
        public string Id, N, T, K, Cat, Aim, Pattern, Look, Sp, Hz, Fld, Ctr;
        public int Acc, Prio, Power, Cnt = 1, Hits, BurstMin, BurstMax;
        public float Pow, Cd, Wind, Spd, Spread, R, Len, Rad, Wid, Half, Homing, Life, Mult;
        public bool SwitchOut, Sucker, UseDef, UseFoeAtk, HitDef, Crit, Ohko, Rampage, RapidSpin, HealBlock, SuperVsWater, ConfuseIfBoosted, Fakeout;
        public MoveEffect E;
        public bool Damaging => Cat != "stat";
        public bool IsZone => K == "aoe" || K == "strike" || K == "multi" || K == "cone" || K == "swipe" || K == "beam" || K == "dash";
    }

    public struct LearnEntry
    {
        public readonly int Lv; public readonly string Id;
        public LearnEntry(int lv, string id) { Lv = lv; Id = id; }
    }

    public class Species
    {
        public string Id, N, Type, Type2, Style, Desc;
        public int Hp, Atk, Def, Spd;
        public LearnEntry[] Learn;
        public float Catch;
        public bool Rare;
        public Dictionary<char, string> Pal;
        public string[] Rows;
        public bool Flying => Id == "birikurage" || Id == "soyodori" || Id == "yorukoumo" || Id == "tsuraran";
    }

    public class Round
    {
        public string N, Tr, Hat, Coat;
        public int Lv, Size;
        public bool Rare;
    }

    public static partial class Data
    {
        public static readonly string[] Starters = { "hinokon", "mizupuku", "happamogu" };
        public static readonly string[] Fields = { "grass", "dirt", "concrete", "water" };
        public static readonly Dictionary<string, string> FieldNames = new Dictionary<string, string>
        {
            { "grass", "しばふの" }, { "dirt", "つちの" }, { "concrete", "コンクリートの" }, { "water", "みずべの" },
        };
        static readonly string[] CupNames = { "ルーキーカップ", "スーパーカップ", "マスターカップ", "レジェンドカップ" };

        public static float Eff(string moveType, string defType)
        {
            if (Chart.TryGetValue(moveType, out var row) && row.TryGetValue(defType, out var v)) return v;
            return 1f;
        }
        /// <summary>2タイプなら掛け算</summary>
        public static float EffVs(string moveType, Species sp) => Eff(moveType, sp.Type) * (string.IsNullOrEmpty(sp.Type2) ? 1 : Eff(moveType, sp.Type2));

        public static List<string> Learned(MonData m)
        {
            var list = new List<string>();
            foreach (var e in Species[m.sid].Learn) if (e.Lv <= m.lvl) list.Add(e.Id);
            return list;
        }

        /// <summary>そうび中のわざ（最大4つ）。未設定なら おぼえた順の さいごの4つ</summary>
        public static List<string> Equipped(MonData m)
        {
            var L = Learned(m);
            if (m.moves == null || m.moves.Count == 0) m.moves = L.GetRange(Mathf.Max(0, L.Count - 4), Mathf.Min(4, L.Count));
            m.moves = m.moves.FindAll(L.Contains);
            if (m.moves.Count > 4) m.moves = m.moves.GetRange(0, 4);
            if (m.moves.Count == 0) m.moves = L.GetRange(Mathf.Max(0, L.Count - 4), Mathf.Min(4, L.Count));
            return m.moves;
        }

        /// <summary>あいての わざ：おぼえている中から ランダムに4つ（こうげきわざを 2つ以上）</summary>
        public static List<string> PickMoves(MonData m)
        {
            var L = Learned(m);
            var atk = L.FindAll(id => Moves[id].Damaging); var sup = L.FindAll(id => !Moves[id].Damaging);
            Shuffle(atk); Shuffle(sup);
            var res = atk.GetRange(0, Mathf.Min(atk.Count, Mathf.Max(2, 4 - Mathf.Min(2, sup.Count))));
            res.AddRange(sup);
            return res.GetRange(0, Mathf.Min(4, res.Count));
        }
        static void Shuffle<T>(List<T> a) { for (int i = a.Count - 1; i > 0; i--) { int j = Util.RandI(0, i); (a[i], a[j]) = (a[j], a[i]); } }

        public static string CupName(int tier) => tier < CupNames.Length ? CupNames[tier] : $"レジェンドカップ {tier - 2}";
        public static int RoundLv(Round r, int tier) => r.Lv + tier * 8;
        public static int ExpNext(int lvl) => 8 + lvl * 6;

        public struct Stats { public int Hp; public float Atk, Def; public int Spd; }
        public static Stats CalcStats(MonData m)
        {
            var b = Species[m.sid];
            int L = m.lvl;
            return new Stats { Hp = Mathf.RoundToInt(b.Hp * (L + 10) / 12f + 10), Atk = b.Atk * (L + 10) / 30f, Def = b.Def * (L + 10) / 30f, Spd = b.Spd };
        }
    }

    public static class Util
    {
        static readonly System.Random Rng = new System.Random();
        public static float Rand(float a, float b) => a + (float)Rng.NextDouble() * (b - a);
        public static int RandI(int a, int b) => Rng.Next(a, b + 1);
        public static float Value => (float)Rng.NextDouble();
        public static T Choice<T>(IList<T> list) => list[Rng.Next(list.Count)];
        public static float Clamp(float v, float a, float b) => v < a ? a : v > b ? b : v;
        public static float WrapAng(float d)
        {
            while (d > Mathf.PI) d -= Mathf.PI * 2;
            while (d < -Mathf.PI) d += Mathf.PI * 2;
            return d;
        }

        static readonly Dictionary<string, Color> HexCache = new Dictionary<string, Color>();
        public static Color Hex(string hex)
        {
            if (HexCache.TryGetValue(hex, out var c)) return c;
            ColorUtility.TryParseHtmlString(hex, out c);
            HexCache[hex] = c;
            return c;
        }
        public static Color Shade(Color c, float k)
        {
            if (k > 0) return new Color(c.r + (1 - c.r) * k, c.g + (1 - c.g) * k, c.b + (1 - c.b) * k, c.a);
            return new Color(c.r * (1 + k), c.g * (1 + k), c.b * (1 + k), c.a);
        }
        public static Color A(Color c, float a) => new Color(c.r, c.g, c.b, a);
    }
}
