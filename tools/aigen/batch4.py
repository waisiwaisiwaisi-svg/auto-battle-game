import sys, os
sys.argv = [sys.argv[0]]
from gen import gen
S = ', big head, simple bold shapes, flat colors, minimal details, clean'
P = {
    'yorukoumo': 'a chubby little stone gargoyle monster sitting, smooth light grey stone skin, big purple bat wings, two small horns, big glowing red eyes, tiny fangs, curled tail' + S,
    'gouen': 'a chubby chibi minotaur monster, brown bull head with big white curved horns, gold nose ring, big cute angry eyes, red loincloth, holding a battle axe with a burning fire blade' + S,
    'tsuraran': 'a tiny chibi ice fairy monster, big round head with white hair and big blue eyes, an ice crystal tiara, small light blue dress, two pairs of translucent icy crystal wings, flying' + S,
    'mizupuku': 'a round blue jelly slime blob monster with no limbs, droplet shaped glossy body, a blue gem inside, a tiny gold crown on top, two big cute eyes' + S,
    'gorotan': 'a chubby grey stone golem monster made of rounded boulders, huge rock fists, short legs, glowing cyan rune lines on its chest, small round glowing eyes, a little moss on top' + S,
}
for k, v in P.items(): gen(k, 400, 8, v)
