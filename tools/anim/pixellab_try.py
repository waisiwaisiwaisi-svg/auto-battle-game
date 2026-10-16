# PixelLab で 走り・攻撃アニメを ためす（いまの 立ち絵を 1コマめに つかう）
# usage: PIXELLAB_API_TOKEN=... python3 tools/anim/pixellab_try.py OUTDIR id1 id2 ...
#   tools/sizes/mons.json（ゲームの 立ち絵）を よみ、走り4コマ・攻撃4コマを 作って OUTDIR に PNG と JSON を おく
import sys, os, json, base64, io, time, urllib.request
from PIL import Image

API = 'https://api.pixellab.ai/v2'
TOKEN = os.environ.get('PIXELLAB_API_TOKEN')
if not TOKEN: sys.exit('PIXELLAB_API_TOKEN が ありません')
OUT, IDS = sys.argv[1], sys.argv[2:]
os.makedirs(OUT, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
mons = json.load(open(os.path.join(ROOT, 'tools/sizes/mons.json')))
mons = {m['id']: m for m in (mons['mons'] if isinstance(mons, dict) else mons)}

def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read())

def first_frame(sid):
    # 立ち絵を 足もと 下よせ・左右 まんなかで 正方形の わくに おく（動く ぶんの よゆう つき）
    im = Image.open(io.BytesIO(base64.b64decode(mons[sid]['img'].split(',')[1]))).convert('RGBA')
    side = max(32, ((max(im.size) * 3 // 2) + 7) // 8 * 8)
    cv = Image.new('RGBA', (side, side), (0, 0, 0, 0)); cv.paste(im, ((side - im.width) // 2, side - im.height - 2), im)
    b = io.BytesIO(); cv.save(b, 'PNG'); return cv, 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

ACTIONS = {
    'run': 'running fast to the right, energetic full sprint cycle, legs alternating; keep the exact same character design, colors and facing',
    'attack': 'winds up by leaning back, then lunges forward to the right with a powerful attack, then recovers; keep the exact same character design, colors and facing',
}
print('balance', call('GET', '/balance'))
for sid in IDS:
    cv, b64 = first_frame(sid); cv.save(f'{OUT}/{sid}_first.png')
    for act, text in ACTIONS.items():
        r = call('POST', '/animate-with-text-v3', {'first_frame': {'base64': b64}, 'action': text, 'frame_count': 4 if act == 'run' else 6, 'no_background': True})
        jid = r['background_job_id']; print(sid, act, 'job', jid, r.get('usage'))
        for _ in range(120):
            time.sleep(5); j = call('GET', f'/background-jobs/{jid}')
            if j.get('status') in ('completed', 'failed'): break
        json.dump(j, open(f'{OUT}/{sid}_{act}.json', 'w'))
        print(sid, act, j.get('status'))
        # 結果の 画像を さがして 保存（レスポンスの 形が かわっても ひろえるように）
        k = 0
        def walk(o):
            global k
            if isinstance(o, dict):
                if isinstance(o.get('base64'), str):
                    s = o['base64'].split(',')[-1]; open(f'{OUT}/{sid}_{act}_{k:02d}.png', 'wb').write(base64.b64decode(s)); k += 1
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(j)
print('balance', call('GET', '/balance'))
