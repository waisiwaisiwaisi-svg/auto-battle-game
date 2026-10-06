using System.Collections.Generic;
using UnityEngine;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

namespace PixelMonsterArena
{
    /// <summary>
    /// タッチ・マウス・キーボードを まとめて読む。
    /// プロジェクト設定が「旧 Input Manager」でも「Input System パッケージ」でも動くようにしている。
    /// 座標は GUI 座標（左上原点・y 下向き）に変換して返す。
    /// </summary>
    public static class InputAdapter
    {
        public struct Pointer { public int Id; public Vector2 Pos; public bool Began, Ended; }

        static readonly List<Pointer> _ptrs = new List<Pointer>();
        static bool _mouseWasDown;

        static Vector2 ToGui(Vector2 screen) => new Vector2(screen.x, Screen.height - screen.y);

        public static List<Pointer> Pointers()
        {
            _ptrs.Clear();
#if ENABLE_INPUT_SYSTEM
            var ts = Touchscreen.current;
            if (ts != null)
            {
                foreach (var t in ts.touches)
                {
                    var ph = t.phase.ReadValue();
                    if (ph == UnityEngine.InputSystem.TouchPhase.None) continue;
                    bool ended = ph == UnityEngine.InputSystem.TouchPhase.Ended || ph == UnityEngine.InputSystem.TouchPhase.Canceled;
                    bool began = ph == UnityEngine.InputSystem.TouchPhase.Began;
                    if (ended && !t.press.wasReleasedThisFrame) continue;
                    _ptrs.Add(new Pointer { Id = t.touchId.ReadValue(), Pos = ToGui(t.position.ReadValue()), Began = began, Ended = ended });
                }
            }
            var ms = Mouse.current;
            if (_ptrs.Count == 0 && ms != null)
            {
                bool down = ms.leftButton.isPressed;
                if (down || _mouseWasDown) _ptrs.Add(new Pointer { Id = -1, Pos = ToGui(ms.position.ReadValue()), Began = down && !_mouseWasDown, Ended = !down });
                _mouseWasDown = down;
            }
#else
            for (int i = 0; i < Input.touchCount; i++)
            {
                var t = Input.GetTouch(i);
                _ptrs.Add(new Pointer { Id = t.fingerId, Pos = ToGui(t.position), Began = t.phase == TouchPhase.Began, Ended = t.phase == TouchPhase.Ended || t.phase == TouchPhase.Canceled });
            }
            if (Input.touchCount == 0)
            {
                bool down = Input.GetMouseButton(0);
                if (down || _mouseWasDown) _ptrs.Add(new Pointer { Id = -1, Pos = ToGui(Input.mousePosition), Began = down && !_mouseWasDown, Ended = !down });
                _mouseWasDown = down;
            }
#endif
            return _ptrs;
        }

        public enum Key { Up, Down, Left, Right, Attack, Move1, Move2, Move3, Move4, Dodge, Capsule, Swap }

        public static bool Held(Key k)
        {
#if ENABLE_INPUT_SYSTEM
            var kb = Keyboard.current; if (kb == null) return false;
            switch (k)
            {
                case Key.Up: return kb.wKey.isPressed || kb.upArrowKey.isPressed;
                case Key.Down: return kb.sKey.isPressed || kb.downArrowKey.isPressed;
                case Key.Left: return kb.aKey.isPressed || kb.leftArrowKey.isPressed;
                case Key.Right: return kb.dKey.isPressed || kb.rightArrowKey.isPressed;
            }
            return false;
#else
            switch (k)
            {
                case Key.Up: return Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow);
                case Key.Down: return Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow);
                case Key.Left: return Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow);
                case Key.Right: return Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow);
            }
            return false;
#endif
        }

        public static bool Pressed(Key k)
        {
#if ENABLE_INPUT_SYSTEM
            var kb = Keyboard.current; if (kb == null) return false;
            switch (k)
            {
                case Key.Attack: return kb.jKey.wasPressedThisFrame;
                case Key.Move1: return kb.kKey.wasPressedThisFrame;
                case Key.Move2: return kb.lKey.wasPressedThisFrame;
                case Key.Move3: return kb.uKey.wasPressedThisFrame;
                case Key.Move4: return kb.iKey.wasPressedThisFrame;
                case Key.Dodge: return kb.spaceKey.wasPressedThisFrame;
                case Key.Capsule: return kb.cKey.wasPressedThisFrame;
                case Key.Swap: return kb.xKey.wasPressedThisFrame;
            }
            return false;
#else
            switch (k)
            {
                case Key.Attack: return Input.GetKeyDown(KeyCode.J);
                case Key.Move1: return Input.GetKeyDown(KeyCode.K);
                case Key.Move2: return Input.GetKeyDown(KeyCode.L);
                case Key.Move3: return Input.GetKeyDown(KeyCode.U);
                case Key.Move4: return Input.GetKeyDown(KeyCode.I);
                case Key.Dodge: return Input.GetKeyDown(KeyCode.Space);
                case Key.Capsule: return Input.GetKeyDown(KeyCode.C);
                case Key.Swap: return Input.GetKeyDown(KeyCode.X);
            }
            return false;
#endif
        }
    }
}
