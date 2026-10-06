# 使い方: python3 tools/monsters/build.py [id ...]   （id を 省くと 全部）
# 各フォルダの mon.py から anim.gif / frames.png / sprite.json / out/*.png を 作り、検査結果を 出す
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '_lib'))
import pix
ids = sys.argv[1:] or sorted(d for d in os.listdir(HERE) if os.path.isfile(os.path.join(HERE, d, 'mon.py')))
bad = 0
for i in ids:
    try:
        if pix.build(os.path.join(HERE, i, 'mon.py')): bad += 1
    except Exception as e:
        bad += 1; print(i, 'ERROR', repr(e))
sys.exit(1 if bad else 0)
