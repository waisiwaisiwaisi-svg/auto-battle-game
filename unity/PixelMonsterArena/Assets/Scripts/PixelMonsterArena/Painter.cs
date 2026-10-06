using System.Collections.Generic;
using UnityEngine;

namespace PixelMonsterArena
{
    /// <summary>
    /// 毎フレーム「描きたいもの」を順に渡すと、SpriteRenderer のプールを使い回して表示する。
    /// Canvas の drawImage / fillRect に近い感覚でゲーム画面を組み立てられる。
    /// 座標はゲーム座標（y 下向き）。Unity 上では (x, -y) に置く。
    /// </summary>
    public class Painter
    {
        readonly Transform _root;
        readonly List<SpriteRenderer> _pool = new List<SpriteRenderer>();
        int _used;

        public Painter(Transform root) { _root = root; }

        public void Begin() { _used = 0; }

        public void End()
        {
            for (int i = _used; i < _pool.Count; i++) if (_pool[i].enabled) _pool[i].enabled = false;
        }

        public void Clear() { _used = 0; End(); }

        SpriteRenderer Next()
        {
            if (_used >= _pool.Count)
            {
                var go = new GameObject("spr");
                go.transform.SetParent(_root, false);
                _pool.Add(go.AddComponent<SpriteRenderer>());
            }
            var r = _pool[_used++];
            r.enabled = true;
            return r;
        }

        /// <summary>スプライトを描く。ang はゲーム座標系のラジアン（時計回りが正）。</summary>
        public void Sprite(Sprite s, float x, float y, float sx, float sy, Color col, int order, float ang = 0)
        {
            if (s == null || Mathf.Abs(sx) < .001f || Mathf.Abs(sy) < .001f || col.a <= 0) return;
            var r = Next();
            r.sprite = s; r.color = col; r.sortingOrder = order;
            var t = r.transform;
            t.localPosition = new Vector3(x, -y, 0);
            t.localRotation = ang == 0 ? Quaternion.identity : Quaternion.Euler(0, 0, -ang * Mathf.Rad2Deg);
            t.localScale = new Vector3(sx, sy, 1);
        }

        public void Rect(float x, float y, float w, float h, Color col, int order) =>
            Sprite(PixelArt.Pixel, x + w / 2, y + h / 2, w, h, col, order);

        public void Line(float x0, float y0, float x1, float y1, float thick, Color col, int order)
        {
            float dx = x1 - x0, dy = y1 - y0, len = Mathf.Sqrt(dx * dx + dy * dy);
            Sprite(PixelArt.PixelLeft, x0, y0, len, thick, col, order, Mathf.Atan2(dy, dx));
        }

        /// <summary>塗りつぶし楕円（rx, ry は半径）</summary>
        public void Ellipse(float x, float y, float rx, float ry, Color col, int order) =>
            Sprite(PixelArt.Disc, x, y, rx * 2 / 128f, ry * 2 / 128f, col, order);

        /// <summary>リング（太さはスケールに比例するので目安）</summary>
        public void RingE(float x, float y, float rx, float ry, Color col, int order) =>
            Sprite(PixelArt.Ring, x, y, rx * 2 / 128f, ry * 2 / 128f, col, order);

        public void Star(float x, float y, float r, Color col, int order)
        {
            Sprite(PixelArt.Star, x, y, (r + 1) * 2 / 32f, (r + 1) * 2 / 32f, Util.Hex("#5a3a00"), order);
            Sprite(PixelArt.Star, x, y, r * 2 / 32f, r * 2 / 32f, col, order + 1);
        }
    }
}
