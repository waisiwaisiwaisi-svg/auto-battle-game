# 10体ぶんの 候補を まとめて 生成（パイプラインの 読みこみは 1回）
import sys, os
sys.argv = [sys.argv[0]]
from gen import gen
PROMPTS = {
    'hinokon': 'a chibi crimson red fire salamander newt monster on four stubby legs, small flames burning along its back, yellow spots, big round eyes, long curled tail',
    'mizupuku': 'a chibi translucent blue water slime monster with a sparkling blue gem inside its jelly body and a tiny golden crown on top, big cute eyes',
    'happamogu': 'a chibi mandrake root monster, round brown turnip-shaped body with a tuft of green leaves on its head, little root arms and legs, open screaming mouth',
    'birikurage': 'a chibi floating electric will-o-wisp spirit monster, glowing yellow body made of lightning with zigzag spiky top, wispy lightning bolt tail, blue sparks',
    'gorotan': 'a chibi stone golem monster with huge rocky fists and short legs, glowing cyan runes carved on its body, green moss on its shoulders',
    'soyodori': 'a chibi baby griffin monster with white eagle head and yellow beak, tan lion body and tail, brown feathered wings folded up, standing on four legs',
    'dokukino': 'a chibi mushroom wizard monster with a big purple pointed mushroom cap like a witch hat with green spots, holding a wooden staff with a green orb, tiny legs',
    'yorukoumo': 'a chibi stone gargoyle monster crouching, grey-purple stone skin, spread bat wings, small curved horns, glowing red eyes, little fangs',
    'gouen': 'a chibi minotaur warrior monster, brown bull head with big curved horns and gold nose ring, muscular body, holding a flaming battle axe',
    'tsuraran': 'a chibi ice fairy pixie monster with sparkling crystal ice wings, white hair with an ice crown, light blue dress, flying',
}
names = sys.stdin.read().split() if not sys.stdin.isatty() else list(PROMPTS)
seed0 = int(os.environ.get('SEED0', 100)); n = int(os.environ.get('N', 8))
for k in names: gen(k, seed0, n, PROMPTS[k])
