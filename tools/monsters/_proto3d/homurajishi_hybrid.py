import sys, math, json, subprocess, io
sys.path.insert(0, '/home/user/auto-battle-game/tools/monsters/_lib'); sys.path.insert(0, '.'); sys.path.insert(0, '../vc')
from sdf import *
import rig
from lion_svg import flame, P as VP, path as vpath
from PIL import Image
SS = 4; RES = int(__import__('os').environ.get('RES', 64)); SC = RES / 64; VC = '/root/tools/vectorcraft-0.3.1-linux-x86_64/bin/vectorcraft-cli'
FIRE = ['#8c1c20', '#e0401c', '#ff9a1c', '#ffe066']   # 立体の 炎素材と 同じ 色
def grad(id_, cols, cx, cy, r, stops):
    s = '<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" r="%s">' % (id_, cx * SS, cy * SS, r * SS)
    e = [0, *stops, 1]
    for i, c in enumerate(cols): s += '<stop offset="%s" stop-color="%s"/><stop offset="%s" stop-color="%s"/>' % (e[i], c, e[i + 1] - .002, c)
    return s + '</radialGradient>'
def svg(body, defs=''):
    W = 64 * SS
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs>%s</defs>%s</svg>' % (RES * SS, RES * SS, W, W, defs, body)
def raster(s, name):
    open(name + '.svg', 'w').write(s); subprocess.run([VC, 'convert', name + '.svg', name + '.png'], check=True, capture_output=True)
    return Image.open(name + '.png')
def frame(P, eye='open', fx_fire=False, name='f'):
    P = dict(P, vec=1); m, (HX, HY) = rig.lion(P)
    fl = P.get('flame', 0); mane = P.get('mane', 1); jaw = P.get('jaw', 0)
    # たてがみ：頭の うしろの 炎の 輪（中心ほど 明るい 炎色）
    defs = grad('fire', FIRE[::-1], HX - 1, HY + 1, 23 * mane, (.5, .72, .9)) + grad('fire2', FIRE[::-1], HX + 1, HY + 6, 11 * mane, (.45, .7, .9))
    back = ''
    for i in range(12):
        ang = 62 + 196 * i / 11 + 5 * math.sin(fl * 1.7 + i)
        Lm = (15 + 4.5 * (i % 2) + 1.5 * math.sin(fl * 2.3 + i * 2.1)) * mane
        back += vpath(flame(HX - 2, HY + 1, ang, Lm, 6.4), 'url(#fire)').replace('stroke="#140e18"', 'stroke="#120e18"').replace('stroke-width="4.0"', 'stroke-width="3.4"')
    front = ''.join(vpath(flame(HX + 1, HY + 6, a, 7.5 * mane, 3.3), 'url(#fire2)') for a in (-15, -45, -75, -105))
    front = front.replace('stroke="#140e18"', 'stroke="#120e18"').replace('stroke-width="4.0"', 'stroke-width="3.4"')
    # 顔：つり目・牙・鼻・炎の 隈（立体の 頭の 位置に 合わせる）
    ex, ey = HX + 4.5, HY - 3
    if eye in ('open', 'angry'):
        front += '<path d="M %s %s Q %s %s %s %s Q %s %s %s %s Z" fill="#ffe066" stroke="#120e18" stroke-width="%s"/>' % (
            VP(ex - 1.5), VP(ey), VP(ex + 1), VP(ey - 2), VP(ex + 4), VP(ey - 1.2), VP(ex + 1.5), VP(ey + 1.6), VP(ex - 1.5), VP(ey), SS * .9)
        front += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#120e18"/>' % (VP(ex + 2), VP(ey - .2), SS * .6, SS * 1.2)
        front += '<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff"/>' % (VP(ex - .2), VP(ey - 1.2), SS, SS)
        front += '<path d="M %s %s L %s %s" stroke="#120e18" stroke-width="%s" stroke-linecap="round"/>' % (VP(ex - 3.2), VP(ey - 3.2 - (eye == 'angry')), VP(ex + 5.5), VP(ey - 1.5 + (eye == 'angry')), SS * 1.4)
    elif eye == 'shut':
        front += '<path d="M %s %s Q %s %s %s %s" fill="none" stroke="#120e18" stroke-width="%s"/>' % (VP(ex - 2.5), VP(ey), VP(ex + 1), VP(ey + 1.8), VP(ex + 4.5), VP(ey - .5), SS * 1.1)
    else:
        front += '<path d="M %s %s l %s %s M %s %s l %s %s" stroke="#120e18" stroke-width="%s"/>' % (VP(ex - 1), VP(ey - 2), SS * 4, SS * 4, VP(ex + 3), VP(ey - 2), -SS * 4, SS * 4, SS * 1.1)
    front += '<path d="M %s %s q %s %s %s %s" fill="none" stroke="#e0401c" stroke-width="%s" stroke-linecap="round"/>' % (VP(ex + 3.5), VP(ey + 2.4), SS * -.6, SS * 2.6, SS * -3.6, SS * 3.6, SS * 1.1)
    nx, ny = HX + 13.5, HY + 1
    front += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#120e18"/>' % (VP(nx), VP(ny), SS * 1.7, SS * 1.2)
    my = HY + 7 + jaw * .4
    if jaw > 1:
        front += '<path d="M %s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z" fill="#8c1c20" stroke="#120e18" stroke-width="%s"/>' % (
            VP(HX + 6), VP(my - 1), VP(HX + 9), VP(my - 1.5), VP(HX + 13), VP(my - 2), VP(HX + 15), VP(my - 2), VP(HX + 13), VP(my + jaw), VP(HX + 9), VP(my + jaw + .5), VP(HX + 6), VP(my - 1), SS)
    else:
        front += '<path d="M %s %s Q %s %s %s %s" fill="none" stroke="#120e18" stroke-width="%s" stroke-linecap="round"/>' % (VP(HX + 6), VP(my - 1), VP(HX + 10), VP(my), VP(HX + 15), VP(my - 2), SS * 1.1)
    front += '<path d="M %s %s l %s %s l %s %s Z M %s %s l %s %s l %s %s Z" fill="#ffffff" stroke="none" stroke-width="%s"/>' % (
        VP(HX + 12.5), VP(my - 1.6), SS * 1.1, SS * 2.6, SS * 1.1, -SS * 2.6, VP(HX + 8), VP(my - 1), SS * 1, SS * 2.2, SS * 1, -SS * 2.2, SS * .6)
    if fx_fire:
        fxx, fxy = fx_fire
        front += vpath(flame(fxx, fxy, 0, 12, 5.5), 'url(#fire3)').replace('stroke="#140e18"', 'stroke="#120e18"')
        defs += grad('fire3', FIRE[::-1], fxx + 8, fxy, 8, (.3, .55, .8))
    ib = raster(svg(back, defs), name + '_b'); ifr = raster(svg(front, defs), name + '_f')
    rows, pal = m.render(RES, RES, ss=SS, overlays=[(ib, 'back'), (ifr, 'front')], extras={'w': '#ffffff'}, scale=SC)
    return rows, pal
if __name__ == '__main__':
    out = {}
    for k, (P, eye) in rig.POSES.items():
        fx = (54, 34) if k == 'atk1' else (57, 33) if k == 'atk2' else False
        rows, pal = frame(P, eye, fx, 'tmp_' + k); out[k] = rows; print(k, flush=True)
        if len(sys.argv) > 1: break
    if len(sys.argv) == 1:
        P = dict(by=6, hy=10, hx=2, legs={'fn': (6, 0), 'ff': (4, 0), 'hn': (-6, 0), 'hf': (-6, 0)}, mane=.7, tail=4)
        rows, pal = frame(P, 'x', False, 'tmp_ko'); out['ko'] = rows
    json.dump(dict(frames=out, pal=pal), open('lion3d/frames.json', 'w'))
    im = Image.new('RGBA', (RES, RES))
    for y, r in enumerate(out['idle0']):
        for x, c in enumerate(r):
            if c != '.': im.putpixel((x, y), tuple(int(pal[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    b = Image.new('RGBA', im.size, (236, 236, 242, 255)); b.alpha_composite(im); b.convert('RGB').resize((RES * 6, RES * 6), Image.NEAREST).save('hyb%d.png' % RES)
