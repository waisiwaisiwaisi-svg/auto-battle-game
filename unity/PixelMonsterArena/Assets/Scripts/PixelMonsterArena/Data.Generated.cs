// このファイルは index.html のデータから自動生成しています（gen.js）。
using System.Collections.Generic;

namespace PixelMonsterArena
{
    public static partial class Data
    {
        public static readonly Dictionary<string, TypeInfo> Types = new Dictionary<string, TypeInfo>
        {
            { "normal", new TypeInfo("ノーマル", "#d8d0c0") },
            { "fire", new TypeInfo("ほのお", "#ff8a3d") },
            { "water", new TypeInfo("みず", "#4aa8ff") },
            { "grass", new TypeInfo("くさ", "#62d26f") },
            { "elec", new TypeInfo("でんき", "#ffd84a") },
            { "rock", new TypeInfo("いわ", "#c49a6c") },
            { "wind", new TypeInfo("かぜ", "#a6ece6") },
        };

        public static readonly Dictionary<string, Dictionary<string, float>> Chart = new Dictionary<string, Dictionary<string, float>>
        {
            { "fire", new Dictionary<string, float> { { "grass", 2f }, { "wind", 1f }, { "water", 0.5f }, { "rock", 0.5f }, { "fire", 0.5f } } },
            { "water", new Dictionary<string, float> { { "fire", 2f }, { "rock", 2f }, { "water", 0.5f }, { "grass", 0.5f } } },
            { "grass", new Dictionary<string, float> { { "water", 2f }, { "rock", 2f }, { "fire", 0.5f }, { "grass", 0.5f }, { "wind", 0.5f } } },
            { "elec", new Dictionary<string, float> { { "water", 2f }, { "wind", 2f }, { "rock", 0.5f }, { "elec", 0.5f }, { "grass", 0.5f } } },
            { "rock", new Dictionary<string, float> { { "fire", 2f }, { "elec", 2f }, { "wind", 2f }, { "grass", 0.5f } } },
            { "wind", new Dictionary<string, float> { { "grass", 2f }, { "rock", 0.5f }, { "elec", 0.5f } } },
        };

        public static readonly Dictionary<string, Move> Moves = new Dictionary<string, Move>
        {
            { "tackle", new Move { Id = "tackle", N = "たいあたり", T = "normal", K = "melee", Pow = 7f, Cd = 0.7f, Wind = 0.12f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 0f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "ember", new Move { Id = "ember", N = "ひのたま", T = "fire", K = "proj", Pow = 13f, Cd = 2.4f, Wind = 0.3f, Spd = 190f, Cnt = 1, Spread = 0f, R = 5f, Len = 0f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "flame", new Move { Id = "flame", N = "かえんうず", T = "fire", K = "aoe", Pow = 24f, Cd = 7f, Wind = 0.85f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 0f, Rad = 62f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "blaze", new Move { Id = "blaze", N = "バーンラッシュ", T = "fire", K = "dash", Pow = 22f, Cd = 5f, Wind = 0.5f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 160f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "bubble", new Move { Id = "bubble", N = "バブルショット", T = "water", K = "proj", Pow = 7f, Cd = 2.8f, Wind = 0.3f, Spd = 160f, Cnt = 3, Spread = 0.22f, R = 4f, Len = 0f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "tide", new Move { Id = "tide", N = "アクアキャノン", T = "water", K = "beam", Pow = 25f, Cd = 7.5f, Wind = 0.9f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 240f, Rad = 0f, Wid = 28f, Homing = 0f, Life = 0f } },
            { "icicle", new Move { Id = "icicle", N = "つららばり", T = "water", K = "proj", Pow = 6f, Cd = 3f, Wind = 0.35f, Spd = 230f, Cnt = 4, Spread = 0.3f, R = 3f, Len = 0f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "leaf", new Move { Id = "leaf", N = "リーフカッター", T = "grass", K = "proj", Pow = 9f, Cd = 2.6f, Wind = 0.25f, Spd = 210f, Cnt = 2, Spread = 0.16f, R = 4f, Len = 0f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "vine", new Move { Id = "vine", N = "ツタウィップ", T = "grass", K = "dash", Pow = 16f, Cd = 4f, Wind = 0.35f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 110f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "spore", new Move { Id = "spore", N = "ほうしボム", T = "grass", K = "strike", Pow = 21f, Cd = 6f, Wind = 1f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 0f, Rad = 38f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "spark", new Move { Id = "spark", N = "エレキタックル", T = "elec", K = "dash", Pow = 16f, Cd = 3.5f, Wind = 0.35f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 130f, Rad = 0f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "thunder", new Move { Id = "thunder", N = "いかずち", T = "elec", K = "strike", Pow = 27f, Cd = 7.5f, Wind = 0.95f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 0f, Rad = 36f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "rockfall", new Move { Id = "rockfall", N = "ロックフォール", T = "rock", K = "strike", Pow = 19f, Cd = 4.5f, Wind = 0.8f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 0f, Rad = 32f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "quake", new Move { Id = "quake", N = "グランドクエイク", T = "rock", K = "aoe", Pow = 26f, Cd = 8f, Wind = 1f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 0f, Rad = 86f, Wid = 0f, Homing = 0f, Life = 0f } },
            { "gust", new Move { Id = "gust", N = "かぜのやいば", T = "wind", K = "beam", Pow = 16f, Cd = 4f, Wind = 0.55f, Spd = 0f, Cnt = 1, Spread = 0f, R = 0f, Len = 200f, Rad = 0f, Wid = 18f, Homing = 0f, Life = 0f } },
            { "tornado", new Move { Id = "tornado", N = "つむじかぜ", T = "wind", K = "proj", Pow = 22f, Cd = 7f, Wind = 0.5f, Spd = 95f, Cnt = 1, Spread = 0f, R = 9f, Len = 0f, Rad = 0f, Wid = 0f, Homing = 1.6f, Life = 3f } },
        };

        public static readonly Dictionary<string, Species> Species = new Dictionary<string, Species>
        {
            { "hinokon", new Species {
                Id = "hinokon", N = "ヒノコン", Type = "fire", Hp = 40, Atk = 54, Def = 44, Spd = 66,
                Moves = new[] { "ember", "flame" }, Style = "mid", Catch = 0.45f, Rare = false,
                Desc = "しっぽの ほのおで きもちを あらわす こぎつね。とおくから ひのたまを うつ。",
                Pal = new Dictionary<char, string> { { 'o', "#ff8a3d" }, { 'O', "#ffc27a" }, { 'w', "#fff3e0" }, { 'k', "#1a1626" }, { 'n', "#3a1a1a" }, { 'r', "#ff4a3d" }, { 'y', "#ffe066" } },
                Rows = new[] {
                    "........o..o..",
                    "........oooo..",
                    "y......oookok.",
                    "ry.....oooooon",
                    "rry...oowwwo..",
                    ".ry..ooowwo...",
                    "..roooooooo...",
                    "...ooooooooo..",
                    "...oOoooooOo..",
                    "...oo.o..o.oo.",
                    "...OO.O..O.OO.",
                } } },
            { "mizupuku", new Species {
                Id = "mizupuku", N = "ミズプク", Type = "water", Hp = 48, Atk = 46, Def = 52, Spd = 50,
                Moves = new[] { "bubble", "tide" }, Style = "ranged", Catch = 0.45f, Rare = false,
                Desc = "まんまるの みずふうせんの ような さかな。ためた みずを いっきに はなつ。",
                Pal = new Dictionary<char, string> { { 'b', "#4aa8ff" }, { 'B', "#9fd3ff" }, { 'w', "#ffffff" }, { 'k', "#1a1626" }, { 'm', "#1d3d7a" }, { 'f', "#2f74d0" }, { 'l', "#d8f0ff" } },
                Rows = new[] {
                    "....bbbb....",
                    "..bbBBbbbb..",
                    ".bBBbbbbbbb.",
                    "bBbbbbbwkbbb",
                    "bbbbbbbwwbbb",
                    "bbbbbbbbbbbm",
                    "fbbbbbbbbbb.",
                    "ffbbllllbb..",
                    "f.bbllllbb..",
                    "...bbbbbb...",
                    "....f..f....",
                } } },
            { "happamogu", new Species {
                Id = "happamogu", N = "ハッパモグ", Type = "grass", Hp = 50, Atk = 52, Def = 50, Spd = 44,
                Moves = new[] { "vine", "spore" }, Style = "melee", Catch = 0.45f, Rare = false,
                Desc = "あたまの はっぱで ひなたぼっこする もぐら。ちかづいて ツタで たたく。",
                Pal = new Dictionary<char, string> { { 'g', "#62d26f" }, { 'G', "#b6f5a0" }, { 's', "#3e8a3a" }, { 'm', "#8a6a4a" }, { 'l', "#d8b890" }, { 'k', "#1a1626" }, { 'n', "#ff8aa0" } },
                Rows = new[] {
                    ".....gg.....",
                    "....gGg.....",
                    ".....s......",
                    "...mmmmm....",
                    "..mmmmmmm...",
                    ".mmmmkmmkm..",
                    ".mmmmmmmmnn.",
                    ".mmmlllllm..",
                    "mmmllllllmm.",
                    "m.mllllllm.m",
                    "..mm....mm..",
                } } },
            { "birikurage", new Species {
                Id = "birikurage", N = "ビリクラゲ", Type = "elec", Hp = 42, Atk = 58, Def = 40, Spd = 70,
                Moves = new[] { "spark", "thunder" }, Style = "mid", Catch = 0.4f, Rare = false,
                Desc = "ふわふわ ういている でんきクラゲ。さわると しびれる。",
                Pal = new Dictionary<char, string> { { 'y', "#ffd84a" }, { 'Y', "#fff5b0" }, { 'k', "#1a1626" }, { 'z', "#ffae3a" } },
                Rows = new[] {
                    "...yyyyyy...",
                    "..yYYyyyyy..",
                    ".yYyyyyyyyy.",
                    ".yyykyykyyy.",
                    ".yyyyyyyyyy.",
                    "..yyyyyyyy..",
                    "..z.z..z.z..",
                    "...z.z..z.z.",
                    "..z.z..z.z..",
                    "...z....z...",
                } } },
            { "gorotan", new Species {
                Id = "gorotan", N = "ゴロタン", Type = "rock", Hp = 60, Atk = 56, Def = 66, Spd = 30,
                Moves = new[] { "rockfall", "quake" }, Style = "melee", Catch = 0.4f, Rare = false,
                Desc = "こうらが いわで できた カメ。うごきは おそいが とても かたい。",
                Pal = new Dictionary<char, string> { { 'r', "#9a8070" }, { 'R', "#c8b098" }, { 's', "#8fc070" }, { 'k', "#1a1626" }, { 'l', "#d8c8a0" } },
                Rows = new[] {
                    "....rrrrr......",
                    "..rrRrrrRrr....",
                    ".rRrrrrrrrrr...",
                    ".rrrrRrrrRrrss.",
                    "rrRrrrrrrrrsssk",
                    "rrrrrrrrrrrssss",
                    ".sllllllllss...",
                    "..ss.....ss....",
                } } },
            { "soyodori", new Species {
                Id = "soyodori", N = "ソヨドリ", Type = "wind", Hp = 40, Atk = 50, Def = 40, Spd = 80,
                Moves = new[] { "gust", "tornado" }, Style = "ranged", Catch = 0.45f, Rare = false,
                Desc = "かぜに のって くらす ことり。はねで かぜの やいばを とばす。",
                Pal = new Dictionary<char, string> { { 'c', "#7fd8d0" }, { 'C', "#c8fff8" }, { 'w', "#ffffff" }, { 'k', "#1a1626" }, { 'y', "#ffc84a" } },
                Rows = new[] {
                    "......ccc....",
                    ".....cCCck...",
                    ".....ccccyy..",
                    "..c..cccc....",
                    ".ccc.cwwcc...",
                    "cccccwwwcc...",
                    ".cccccwwcc...",
                    "..cccccccc...",
                    "....ccccc....",
                    ".....y..y....",
                } } },
            { "dokukino", new Species {
                Id = "dokukino", N = "ドクキノ", Type = "grass", Hp = 46, Atk = 54, Def = 46, Spd = 48,
                Moves = new[] { "leaf", "spore" }, Style = "ranged", Catch = 0.45f, Rare = false,
                Desc = "かさの もようが あやしく ひかる キノコ。ほうしの ばくだんを まく。",
                Pal = new Dictionary<char, string> { { 'p', "#b05ad8" }, { 'P', "#f0a8ff" }, { 'w', "#f4ecd8" }, { 'k', "#1a1626" }, { 'm', "#7a3a3a" } },
                Rows = new[] {
                    "...pppppp...",
                    ".ppPpppPppp.",
                    "pPpppppppPpp",
                    "ppppPppppppp",
                    ".pppppppppp.",
                    "...wwwwww...",
                    "...wkwwkw...",
                    "...wwwwww...",
                    "...wwmmww...",
                    "....w..w....",
                } } },
            { "yorukoumo", new Species {
                Id = "yorukoumo", N = "ヨルコウモ", Type = "wind", Hp = 44, Atk = 58, Def = 42, Spd = 76,
                Moves = new[] { "gust", "spark" }, Style = "melee", Catch = 0.4f, Rare = false,
                Desc = "よるの スタジアムに あらわれる コウモリ。すばやく とびかかる。",
                Pal = new Dictionary<char, string> { { 'd', "#5a4a8a" }, { 'D', "#8a78c0" }, { 'r', "#ff4a5a" }, { 'w', "#ffffff" } },
                Rows = new[] {
                    "d..........d",
                    "dd..d..d..dd",
                    "ddd.dddd.ddd",
                    "ddDdddddddDd",
                    ".ddddrdrddd.",
                    "..dddddddd..",
                    "...dwdwdd...",
                    "....dddd....",
                } } },
            { "gouen", new Species {
                Id = "gouen", N = "ゴウエン", Type = "fire", Hp = 58, Atk = 72, Def = 56, Spd = 58,
                Moves = new[] { "blaze", "quake" }, Style = "melee", Catch = 0.18f, Rare = true,
                Desc = "もえる たてがみの あばれウシ。めったに みられない つよい モンスター。",
                Pal = new Dictionary<char, string> { { 'h', "#f4ecd8" }, { 'b', "#8a3a2a" }, { 'B', "#c0583a" }, { 'k', "#1a1626" }, { 'n', "#e8a080" }, { 'f', "#ff8a3d" }, { 'r', "#ff4a3d" }, { 'y', "#ffe066" } },
                Rows = new[] {
                    ".h.......h...",
                    "..h.....h.f..",
                    "..bbbbbbbbff.",
                    ".bbBbbbbbBbfr",
                    ".bbkbbbbkbbry",
                    ".bbbbbbbbbbf.",
                    "..bnnbbnnbb..",
                    "..bbbbbbbbb..",
                    ".bbbbbbbbbbb.",
                    ".bb.bb.bb.bb.",
                    ".kk.kk.kk.kk.",
                } } },
            { "tsuraran", new Species {
                Id = "tsuraran", N = "ツララン", Type = "water", Hp = 50, Atk = 62, Def = 60, Spd = 64,
                Moves = new[] { "icicle", "tide" }, Style = "ranged", Catch = 0.18f, Rare = true,
                Desc = "こおりの けっしょうから うまれた せいれい。つららを いっせいに とばす。",
                Pal = new Dictionary<char, string> { { 'i', "#9fe0ff" }, { 'I', "#ffffff" }, { 'k', "#1a1626" }, { 'm', "#3a6aa0" } },
                Rows = new[] {
                    ".....i.....",
                    "....iIi....",
                    "...iIIii...",
                    "..iiiiiii..",
                    ".iiikiikii.",
                    ".iiiiiiiii.",
                    "..iiimmii..",
                    "...iiiii...",
                    "..i.iii.i..",
                    ".i...i...i.",
                } } },
        };

        public static readonly Round[] Rounds =
        {
            new Round { N = "1かいせん", Tr = "みならい ソウタ", Lv = 3, Size = 2, Hat = "#4fd1a5", Coat = "#6a5acd", Rare = false },
            new Round { N = "2かいせん", Tr = "キャンパー ミオ", Lv = 6, Size = 3, Hat = "#ffd166", Coat = "#3a9a5a", Rare = false },
            new Round { N = "じゅんけっしょう", Tr = "ベテラン ゴウキ", Lv = 9, Size = 3, Hat = "#8a6a4a", Coat = "#a04a3a", Rare = true },
            new Round { N = "けっしょう", Tr = "チャンピオン レイ", Lv = 12, Size = 3, Hat = "#f4ecd8", Coat = "#2a2a4a", Rare = true },
        };

        public static readonly string[] TrainerRows =
        {
            "..hhhh..",
            ".hhhhhhH",
            "..ssss..",
            "..sksk..",
            "..ssss..",
            ".cccccc.",
            "cccccccc",
            "s.cccc.s",
            "..pppp..",
            "..p..p..",
            "..b..b..",
        };
    }
}
