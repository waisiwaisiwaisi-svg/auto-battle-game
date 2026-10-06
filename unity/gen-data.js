const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const grab = (name, open) => { const i = src.indexOf(`const ${name} = ${open}`); let d = 0, j = src.indexOf(open, i); const st = j; for (; j < src.length; j++) { if (src[j] === open) d++; else if (src[j] === (open === '{' ? '}' : ']')) { d--; if (!d) break; } } return eval('(' + src.slice(st, j + 1) + ')'); };
const TYPES = grab('TYPES', '{'), CHART = grab('CHART', '{'), MOVES = grab('MOVES', '{'), SPECIES = grab('SPECIES', '{'), ROUNDS = grab('ROUNDS', '['), TR = grab('TRAINER_ROWS', '[');
const q = (s) => JSON.stringify(s);
const f = (v) => (v === undefined ? '0f' : `${v}f`);
let o = `// このファイルは index.html のデータから自動生成しています（gen.js）。
using System.Collections.Generic;

namespace PixelMonsterArena
{
    public static partial class Data
    {
        public static readonly Dictionary<string, TypeInfo> Types = new Dictionary<string, TypeInfo>
        {
${Object.entries(TYPES).map(([k, v]) => `            { ${q(k)}, new TypeInfo(${q(v.n)}, ${q(v.c)}) },`).join('\n')}
        };

        public static readonly Dictionary<string, Dictionary<string, float>> Chart = new Dictionary<string, Dictionary<string, float>>
        {
${Object.entries(CHART).map(([k, v]) => `            { ${q(k)}, new Dictionary<string, float> { ${Object.entries(v).map(([a, b]) => `{ ${q(a)}, ${b}f }`).join(', ')} } },`).join('\n')}
        };

        public static readonly Dictionary<string, Move> Moves = new Dictionary<string, Move>
        {
${Object.entries(MOVES).map(([k, m]) => `            { ${q(k)}, new Move { Id = ${q(k)}, N = ${q(m.n)}, T = ${q(m.t)}, K = ${q(m.k)}, Pow = ${f(m.pow)}, Cd = ${f(m.cd)}, Wind = ${f(m.wind)}, Spd = ${f(m.spd)}, Cnt = ${m.cnt || 1}, Spread = ${f(m.spread)}, R = ${f(m.r)}, Len = ${f(m.len)}, Rad = ${f(m.rad)}, Wid = ${f(m.wid)}, Homing = ${f(m.homing)}, Life = ${f(m.life)} } },`).join('\n')}
        };

        public static readonly Dictionary<string, Species> Species = new Dictionary<string, Species>
        {
${Object.entries(SPECIES).map(([k, s]) => `            { ${q(k)}, new Species {
                Id = ${q(k)}, N = ${q(s.n)}, Type = ${q(s.type)}, Hp = ${s.base.hp}, Atk = ${s.base.atk}, Def = ${s.base.def}, Spd = ${s.base.spd},
                Moves = new[] { ${s.moves.map(q).join(', ')} }, Style = ${q(s.style)}, Catch = ${s.catch}f, Rare = ${s.rare ? 'true' : 'false'},
                Desc = ${q(s.desc)},
                Pal = new Dictionary<char, string> { ${Object.entries(s.pal).map(([a, b]) => `{ '${a}', ${q(b)} }`).join(', ')} },
                Rows = new[] {
${s.rows.map(r => `                    ${q(r)},`).join('\n')}
                } } },`).join('\n')}
        };

        public static readonly Round[] Rounds =
        {
${ROUNDS.map(r => `            new Round { N = ${q(r.n)}, Tr = ${q(r.tr)}, Lv = ${r.lv}, Size = ${r.size}, Hat = ${q(r.hat)}, Coat = ${q(r.coat)}, Rare = ${r.rare} },`).join('\n')}
        };

        public static readonly string[] TrainerRows =
        {
${TR.map(r => `            ${q(r)},`).join('\n')}
        };
    }
}
`;
fs.writeFileSync(process.argv[3], o);
