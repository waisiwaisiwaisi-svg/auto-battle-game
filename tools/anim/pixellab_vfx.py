# PixelLab の /vfx で わざの エフェクトを つくる（いまの FXEL の かわり）
# usage: PIXELLAB_API_TOKEN=... python3 tools/anim/pixellab_vfx.py OUTDIR key1 key2 ...   （key は vfx_prompts.json の キー、all で ぜんぶ）
#   OUTDIR に <key>.gif / <key>.png / <key>.json（スプライトシートと コマ情報）と <key>_job.json を おく
import sys, os, json, time, urllib.request, urllib.error

API = 'https://api.pixellab.ai/v2'
TOKEN = os.environ.get('PIXELLAB_API_TOKEN')
if not TOKEN: sys.exit('PIXELLAB_API_TOKEN が ありません')
OUT, KEYS = sys.argv[1], sys.argv[2:]
os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.environ.get('PROMPTS') or os.path.join(HERE, 'vfx_prompts.json')))   # PROMPTS=… で べつの 一覧（vfx_prompts_hand.json など）
# いまの コマ数（だいたい これくらいの ながさに する）
N = {'slash': 9, 'claw': 9, 'poof': 9, 'fighting': 13, 'fire': 13}
if KEYS == ['all']: KEYS = [k for k in P if not k.startswith('_')]

def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read())

def get(url, path):
    with urllib.request.urlopen(url, timeout=120) as r: open(path, 'wb').write(r.read())

print('balance', call('GET', '/balance'))
jobs = {}
for k in KEYS:   # まとめて なげてから まつ
    if os.path.exists(f'{OUT}/{k}.png'): print(k, 'skip'); continue
    e = P[k] if isinstance(P[k], dict) else {'d': P[k]}   # {d: せつめい, loop: くりかえし, size: '24x24', n: コマ数}
    com = P['_loop'] if e.get('loop') and '_loop' in P else P['_common']
    desc = com.replace('{n}', str(e.get('n') or N.get(k, 16))).replace('{size}', e.get('size', '48x48')) + ' Effect: ' + e['d'] + '.'
    jf = f'{OUT}/{k}.jobid'   # 429 などで とちゅうで とまっても、なげた ジョブは つかいまわす（二重に つかわない）
    if os.path.exists(jf): jobs[k] = open(jf).read().strip(); print(k, 'reuse job', jobs[k]); continue
    for _try in range(6):
        try:
            r = call('POST', '/vfx', {'description': desc, 'artist': 'lite', 'name': 'pma_' + k}); break
        except urllib.error.HTTPError as e:
            if e.code != 429 or _try == 5: raise
            print(k, '429, wait'); time.sleep(30)
    jobs[k] = r['background_job_id']; open(jf, 'w').write(jobs[k]); print(k, 'job', jobs[k], 'quote', r.get('quoted_generations'))
    time.sleep(15)
for k, jid in jobs.items():
    for _ in range(90):
        j = call('GET', f'/background-jobs/{jid}')
        if j.get('status') in ('completed', 'failed'): break
        time.sleep(8)
    json.dump(j, open(f'{OUT}/{k}_job.json', 'w'), ensure_ascii=False, indent=1)
    print(k, j.get('status'), j.get('usage'))
    lr = j.get('last_response') or {}
    files = lr.get('files') or {}
    items = files.items() if isinstance(files, dict) else [(f.get('name') or f.get('url', '').split('?')[0].split('/')[-1], f.get('url')) for f in files]
    for name, url in items:
        if isinstance(url, dict): url = url.get('url')
        if not url: continue
        ext = os.path.splitext(name.split('?')[0])[1] or '.bin'
        if 'normals' in name or 'game' in name: continue
        get(url, f'{OUT}/{k}{ext}')
print('balance', call('GET', '/balance'))
