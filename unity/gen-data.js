// index.html のデータ（モンスター・わざ・タイプ表・おぼえるわざ・大会）を C# に変換する。
// 使い方: node unity/gen-data.js index.html unity/PixelMonsterArena/Assets/Scripts/PixelMonsterArena/Data.Generated.cs
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const body = src.slice(src.indexOf("'use strict';") + 13, src.indexOf('/* =====================================================================\n   スプライト焼き込み'));
global.location = { search: '' };
const D = new Function(body + ';return { TYPES, CHART, MOVES, SPECIES, LEARN, TRAINER_ROWS, K, BODY };')();
{ const i = src.indexOf('const ROUNDS = ['), j = src.indexOf('];', i); D.ROUNDS = eval(src.slice(i + 15, j + 1)); }
const q = (s) => JSON.stringify(s);
const f = (v) => (v === undefined || v === null ? '0f' : `${+v}f`);
const b = (v) => (v ? 'true' : 'false');
const stages = (o) => o ? `new Dictionary<string, int> { ${Object.entries(o).map(([k, v]) => `{ ${q(k)}, ${v} }`).join(', ')} }` : 'null';
const mv = (id, m) => {
  const e = m.e || {};
  return `            { ${q(id)}, new Move { Id = ${q(id)}, N = ${q(m.n)}, T = ${q(m.t)}, K = ${q(m.k)}, Cat = ${q(m.cat)}, Aim = ${q(m.aim)}, Acc = ${m.acc || 0}, Prio = ${m.prio || 0}, Power = ${m.power || 0},
                Pow = ${f(m.pow)}, Cd = ${f(m.cd)}, Wind = ${f(m.wind)}, Spd = ${f(m.spd)}, Cnt = ${m.cnt || 1}, Spread = ${f(m.spread)}, R = ${f(m.r)}, Len = ${f(m.len)}, Rad = ${f(m.rad)}, Wid = ${f(m.wid)}, Half = ${f(m.half)}, Homing = ${f(m.homing)}, Life = ${f(m.life)},
                Pattern = ${q(m.pattern || '')}, Look = ${q(m.look || '')}, Sp = ${q(m.sp || '')}, Hz = ${q(m.hz || '')}, Fld = ${q(m.fld || '')}, Ctr = ${q(m.ctr || '')}, Mult = ${f(m.mult)}, Hits = ${m.hits || 0}, BurstMin = ${m.burst ? m.burst[0] : 0}, BurstMax = ${m.burst ? m.burst[1] : 0},
                SwitchOut = ${b(m.switchOut)}, Sucker = ${b(m.sucker)}, UseDef = ${b(m.useDef)}, UseFoeAtk = ${b(m.useFoeAtk)}, HitDef = ${b(m.hitDef)}, Crit = ${b(m.crit)}, Ohko = ${b(m.ohko)}, Rampage = ${b(m.rampage)}, RapidSpin = ${b(m.rapidSpin)}, HealBlock = ${b(m.healBlock)}, SuperVsWater = ${b(m.superVsWater)}, ConfuseIfBoosted = ${b(m.confuseIfBoosted)}, Fakeout = ${b(m.fakeout)},
                E = new MoveEffect { St = ${q(e.st || '')}, StCh = ${e.stCh || 0}, Flinch = ${e.flinch || 0}, Drain = ${e.drain || 0}, Recoil = ${e.recoil || 0}, Heal = ${e.heal || 0}, Self = ${stages(e.self)}, Foe = ${stages(e.foe)}, FoeCh = ${e.foeCh || 0}, Seed = ${b(e.seed)} } } },`;
};
const o = `// このファイルは index.html のデータから自動生成しています（unity/gen-data.js）。手で編集しないでください。
using System.Collections.Generic;

namespace PixelMonsterArena
{
    public static partial class Data
    {
        public const float K = ${D.K}f, Body = ${D.BODY}f;

        public static readonly Dictionary<string, TypeInfo> Types = new Dictionary<string, TypeInfo>
        {
${Object.entries(D.TYPES).map(([k, v]) => `            { ${q(k)}, new TypeInfo(${q(v.n)}, ${q(v.c)}) },`).join('\n')}
        };

        public static readonly Dictionary<string, Dictionary<string, float>> Chart = new Dictionary<string, Dictionary<string, float>>
        {
${Object.entries(D.CHART).map(([k, v]) => `            { ${q(k)}, new Dictionary<string, float> { ${Object.entries(v).map(([a, c]) => `{ ${q(a)}, ${c}f }`).join(', ')} } },`).join('\n')}
        };

        public static readonly Dictionary<string, Move> Moves = new Dictionary<string, Move>
        {
${Object.entries(D.MOVES).map(([k, m]) => mv(k, m)).join('\n')}
        };

        public static readonly Dictionary<string, Species> Species = new Dictionary<string, Species>
        {
${Object.entries(D.SPECIES).map(([k, s]) => `            { ${q(k)}, new Species {
                Id = ${q(k)}, N = ${q(s.n)}, Type = ${q(s.type)}, Type2 = ${q(s.type2 || '')}, Hp = ${s.base.hp}, Atk = ${s.base.atk}, Def = ${s.base.def}, Spd = ${s.base.spd},
                Style = ${q(s.style)}, Catch = ${s.catch}f, Rare = ${b(s.rare)},
                Desc = ${q(s.desc)},
                Pal = new Dictionary<char, string> { ${Object.entries(s.pal).map(([a, c]) => `{ '${a}', ${q(c)} }`).join(', ')} },
                Learn = new[] { ${D.LEARN[k].map(([l, id]) => `new LearnEntry(${l}, ${q(id)})`).join(', ')} },
                Rows = new[] {
${s.rows.map(r => `                    ${q(r)},`).join('\n')}
                } } },`).join('\n')}
        };

        public static readonly Round[] Rounds =
        {
${D.ROUNDS.map(r => `            new Round { N = ${q(r.n)}, Tr = ${q(r.tr)}, Lv = ${r.lv}, Size = ${r.size}, Hat = ${q(r.hat)}, Coat = ${q(r.coat)}, Rare = ${r.rare} },`).join('\n')}
        };

        public static readonly string[] TrainerRows =
        {
${D.TRAINER_ROWS.map(r => `            ${q(r)},`).join('\n')}
        };
    }
}
`;
fs.writeFileSync(process.argv[3], o);
console.log('moves', Object.keys(D.MOVES).length, 'species', Object.keys(D.SPECIES).length);
