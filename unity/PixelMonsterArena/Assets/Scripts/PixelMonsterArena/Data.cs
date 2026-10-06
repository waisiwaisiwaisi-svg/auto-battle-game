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

    /// <summary>わざ。K: melee=近接 / proj=弾 / beam=直線 / aoe=自分の周囲 / strike=相手の足元 / dash=突進</summary>
    public class Move
    {
        public string Id, N, T, K;
        public float Pow, Cd, Wind, Spd, Spread, R, Len, Rad, Wid, Homing, Life;
        public int Cnt = 1;
    }

    public class Species
    {
        public string Id, N, Type, Style, Desc;
        public int Hp, Atk, Def, Spd;
        public string[] Moves;
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
        /// <summary>見た目を大きくしたぶん、距離・速さも K 倍にそろえる（index.html と同じ）</summary>
        public const float K = 1.6f;
        /// <summary>足元から体の中心までの高さ</summary>
        public const float Body = 22f;

        public static readonly string[] Starters = { "hinokon", "mizupuku", "happamogu" };
        public static readonly string[] Fields = { "grass", "dirt", "concrete", "water" };
        public static readonly Dictionary<string, string> FieldNames = new Dictionary<string, string>
        {
            { "grass", "しばふの" }, { "dirt", "つちの" }, { "concrete", "コンクリートの" }, { "water", "みずべの" },
        };
        static readonly string[] CupNames = { "ルーキーカップ", "スーパーカップ", "マスターカップ", "レジェンドカップ" };

        static bool _scaled;
        public static void Init()
        {
            if (_scaled) return;
            _scaled = true;
            foreach (var m in Moves.Values) { m.Len *= K; m.Rad *= K; m.Wid *= K; m.Spd *= K; m.R *= K; }
        }

        public static float Eff(string moveType, string defType)
        {
            if (Chart.TryGetValue(moveType, out var row) && row.TryGetValue(defType, out var v)) return v;
            return 1f;
        }

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
