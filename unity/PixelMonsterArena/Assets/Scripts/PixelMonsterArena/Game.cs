using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace PixelMonsterArena
{
    /// <summary>
    /// ゲーム全体（起動・画面遷移・UI・入力）。シーンに何も置かなくても、再生すると自動で作られる。
    /// UI は IMGUI（OnGUI）で描いているので、プレハブやシーン設定は不要。
    /// </summary>
    public class Game : MonoBehaviour
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        static void Boot()
        {
            if (FindObjectOfType<Game>() != null) return;
            var go = new GameObject("PixelMonsterArena");
            DontDestroyOnLoad(go);
            go.AddComponent<Game>();
        }

        enum Scr { Title, Starter, Hub, Team, Battle }
        Scr _scr = Scr.Title;
        SaveData S;
        Battle B;
        BattleRenderer _rend;
        Camera _cam;
        string _banner = "";
        float _bannerT;

        // バトルUIの状態
        bool _swapOpen, _pauseOpen, _resultOpen;
        int _joyId = int.MinValue; Vector2 _joyVec;
        Rect _rView, _rJoy; readonly Dictionary<string, Rect> _btnRects = new Dictionary<string, Rect>();
        // へんせい画面
        int _openUid = -1; Vector2 _scroll; float _dragLastY; int _dragId = int.MinValue; float _dragDist;
        string _confirmMsg; System.Action _confirmYes;
        string _toast; float _toastT;

        void Awake()
        {
            Application.targetFrameRate = 60;
            _cam = Camera.main;
            if (_cam == null)
            {
                var cg = new GameObject("Main Camera");
                _cam = cg.AddComponent<Camera>();
                cg.tag = "MainCamera";
            }
            _cam.orthographic = true;
            _cam.clearFlags = CameraClearFlags.SolidColor;
            _cam.backgroundColor = Util.Hex("#141022");
            _cam.nearClipPlane = .1f; _cam.farClipPlane = 100;
            var root = new GameObject("BattleSprites");
            root.transform.SetParent(transform, false);
            _rend = new BattleRenderer(root.transform);
            S = SaveData.Load();
        }

        // =====================================================================
        //   バトル開始
        // =====================================================================
        void StartBattle(BattleConfig cfg)
        {
            B = new Battle(S, cfg);
            B.OnSay += t => { _banner = t; _bannerT = 2.2f; };
            B.Start(cfg.Intro);
            _swapOpen = _pauseOpen = _resultOpen = false;
            _scr = Scr.Battle;
        }

        void StartWild()
        {
            var pool = Data.Species.Keys.Where(id => !Data.Starters.Contains(id) || Util.Value < .35f).ToList();
            var weights = pool.Select(id => Data.Species[id].Rare ? .5f : 3f).ToList();
            float r = Util.Value * weights.Sum(); string sid = pool[0];
            for (int i = 0; i < pool.Count; i++) { r -= weights[i]; if (r <= 0) { sid = pool[i]; break; } }
            int lv = Mathf.Max(2, Mathf.RoundToInt(S.AvgLevel()) - 3 + Util.RandI(0, 3) + (Data.Species[sid].Rare ? 1 : 0));
            var em = new MonData { uid = -1, sid = sid, lvl = lv }; em.moves = Data.PickMoves(em);
            StartBattle(new BattleConfig { Kind = "wild", Enemies = new List<MonData> { em }, Skill = .15f, Title = "くさむら", Intro = "くさむらが ガサガサ ゆれている…" });
        }

        void StartCup()
        {
            var r = Data.Rounds[S.round]; int lv = Data.RoundLv(r, S.tier);
            var pool = Data.Species.Keys.Where(id => r.Rare || !Data.Species[id].Rare).ToList();
            var enemies = new List<MonData>();
            for (int i = 0; i < r.Size; i++)
            {
                string sid; int guard = 0;
                do { sid = Util.Choice(pool); } while (enemies.Any(e => e.sid == sid) && pool.Count > r.Size && guard++ < 50);
                var em = new MonData { uid = -1 - i, sid = sid, lvl = Mathf.Max(2, lv + Util.RandI(-1, 1) + (i == r.Size - 1 ? 1 : 0)) };
                em.moves = Data.PickMoves(em); enemies.Add(em);
            }
            string field = Util.Choice(Data.Fields);
            StartBattle(new BattleConfig
            {
                Kind = "cup", Enemies = enemies, Field = field, Skill = Mathf.Clamp(.3f + S.round * .1f + S.tier * .06f, 0, .8f),
                Trainer = new TrainerInfo { Name = r.Tr, Spr = PixelArt.Trainer(r.Hat, r.Coat) },
                Title = $"{Data.CupName(S.tier)}　{r.N}", Intro = $"{Data.CupName(S.tier)} {r.N}！ {Data.FieldNames[field]}フィールドで しあい かいし！",
            });
        }

        // =====================================================================
        //   毎フレーム
        // =====================================================================
        void Update()
        {
            float dt = Mathf.Min(.05f, Time.deltaTime);
            _bannerT -= dt; _toastT -= dt;
            if (_scr == Scr.Battle && B != null)
            {
                HandleBattleInput();
                if (!_pauseOpen) // こうたいの えらび中も バトルは とまらない
                {
                    float rest = dt;
                    while (rest > 0) { float s = Mathf.Min(rest, 1 / 30f); B.Step(s); rest -= s; }
                }
                _cam.enabled = true;
                _rend.Render(B, _cam);
                if (B.Mode == "end" && B.EndT <= 0) _resultOpen = true;
            }
            else
            {
                _rend.P.Clear();
                _cam.rect = new Rect(0, 0, 1, 1);
                _cam.transform.position = new Vector3(-99999, 0, -10); // 何も映さない
            }
            if (_scr == Scr.Team) HandleDragScroll();
        }

        void HandleBattleInput()
        {
            var ptrs = InputAdapter.Pointers();
            bool overlay = _pauseOpen || _resultOpen;
            foreach (var p in ptrs)
            {
                if (p.Began && !overlay)
                {
                    if (_rJoy.Contains(p.Pos)) _joyId = p.Id;
                    else foreach (var kv in _btnRects.ToList()) if (kv.Value.Contains(p.Pos)) { PressButton(kv.Key); break; }
                }
                if (p.Id == _joyId)
                {
                    if (p.Ended) { _joyId = int.MinValue; _joyVec = Vector2.zero; }
                    else
                    {
                        var c = _rJoy.center; float R = _rJoy.width / 2;
                        var d = p.Pos - c; if (d.magnitude > R) d = d.normalized * R;
                        _joyVec = d / R; // GUI 座標なので y 下向き＝ゲーム座標と同じ
                    }
                }
            }
            if (!ptrs.Any(p => p.Id == _joyId)) { _joyId = int.MinValue; _joyVec = Vector2.zero; }
            var v = _joyVec;
            if (InputAdapter.Held(InputAdapter.Key.Left)) v.x -= 1; if (InputAdapter.Held(InputAdapter.Key.Right)) v.x += 1;
            if (InputAdapter.Held(InputAdapter.Key.Up)) v.y -= 1; if (InputAdapter.Held(InputAdapter.Key.Down)) v.y += 1;
            if (v.magnitude > 1) v.Normalize();
            B.InputVec = v; B.InputActive = v.magnitude > .2f;
            if (overlay) return;
            if (InputAdapter.Pressed(InputAdapter.Key.Attack)) PressButton("atk");
            if (InputAdapter.Pressed(InputAdapter.Key.Move1)) PressButton("mv0");
            if (InputAdapter.Pressed(InputAdapter.Key.Move2)) PressButton("mv1");
            if (InputAdapter.Pressed(InputAdapter.Key.Move3)) PressButton("mv2");
            if (InputAdapter.Pressed(InputAdapter.Key.Move4)) PressButton("mv3");
            if (InputAdapter.Pressed(InputAdapter.Key.Dodge)) PressButton("dodge");
            if (InputAdapter.Pressed(InputAdapter.Key.Capsule)) PressButton("cap");
            if (InputAdapter.Pressed(InputAdapter.Key.Swap)) PressButton("swap");
        }

        void PressButton(string id)
        {
            switch (id)
            {
                case "mv0": B.CmdMove(0); break;
                case "mv1": B.CmdMove(1); break;
                case "mv2": B.CmdMove(2); break;
                case "mv3": B.CmdMove(3); break;
                case "atk": B.CmdAttack(); break;
                case "dodge": B.CmdDodge(); break;
                case "swap":
                    if (_swapOpen) _swapOpen = false;
                    else if (B.Sides[0].SwapCd > 0) B.Say($"まだ こうたい できない！（あと {Mathf.CeilToInt(B.Sides[0].SwapCd)}びょう）");
                    else if (B.CanSwap(out _)) _swapOpen = true;
                    else B.Say("こうたいできる モンスターが いない！");
                    break;
                case "swapCancel": _swapOpen = false; break;
                default:
                    if (id.StartsWith("swapTo")) { B.DoPlayerSwap(int.Parse(id.Substring(6))); _swapOpen = false; }
                    break;
                case "cap": B.CmdCapsule(); break;
                case "run": B.CmdRun(); break;
                case "auto": S.auto = !S.auto; S.Save(); break;
                case "pause": if (B.Mode != "end") _pauseOpen = true; break;
            }
        }

        void HandleDragScroll()
        {
            foreach (var p in InputAdapter.Pointers())
            {
                if (p.Began) { _dragId = p.Id; _dragLastY = p.Pos.y; _dragDist = 0; }
                else if (p.Id == _dragId)
                {
                    float dy = p.Pos.y - _dragLastY; _dragLastY = p.Pos.y; _dragDist += Mathf.Abs(dy);
                    if (_dragDist > 10) _scroll.y = Mathf.Max(0, _scroll.y - dy);
                    if (p.Ended) _dragId = int.MinValue;
                }
            }
        }

        // =====================================================================
        //   UI（IMGUI）
        // =====================================================================
        float U; Rect _col;
        GUIStyle _lbl, _small, _title, _btn, _btnSub, _box, _center, _rich;
        Texture2D _tPanel, _tPanel2, _tEdge, _tDark, _tAcc, _tGood, _tWhite;
        Font _font;

        static Texture2D Tex(string hex) { var t = new Texture2D(1, 1) { filterMode = FilterMode.Point }; t.SetPixel(0, 0, Util.Hex(hex)); t.Apply(); return t; }

        void SetupStyles()
        {
            float colW = Mathf.Min(Screen.width, Screen.height * .6f);
            _col = new Rect((Screen.width - colW) / 2, 0, colW, Screen.height);
            U = colW / 30f;
            if (_tPanel == null)
            {
                _tPanel = Tex("#241d38"); _tPanel2 = Tex("#2e2648"); _tEdge = Tex("#4a4070"); _tDark = Tex("#0d0b14"); _tAcc = Tex("#ffd166"); _tGood = Tex("#4fd1a5"); _tWhite = Tex("#ffffff");
                _font = Resources.Load<Font>("JPFont");
            }
            int fs = Mathf.RoundToInt(U * .95f);
            if (_lbl != null && _lbl.fontSize == fs) return;
            var ink = Util.Hex("#f6f0e0");
            _lbl = new GUIStyle(GUI.skin.label) { fontSize = fs, wordWrap = true, richText = true }; _lbl.normal.textColor = ink;
            if (_font) _lbl.font = _font;
            _small = new GUIStyle(_lbl) { fontSize = Mathf.RoundToInt(U * .72f) }; _small.normal.textColor = Util.Hex("#a49ac0");
            _title = new GUIStyle(_lbl) { fontSize = Mathf.RoundToInt(U * 1.8f), alignment = TextAnchor.MiddleCenter, fontStyle = FontStyle.Bold }; _title.normal.textColor = Util.Hex("#ffd166");
            _center = new GUIStyle(_lbl) { alignment = TextAnchor.MiddleCenter };
            _rich = new GUIStyle(_lbl) { alignment = TextAnchor.UpperCenter };
            _btn = new GUIStyle(GUI.skin.button) { fontSize = fs, fontStyle = FontStyle.Bold, wordWrap = true, richText = true };
            if (_font) _btn.font = _font;
            _btn.normal.background = _tAcc; _btn.hover.background = _tAcc; _btn.active.background = Tex("#e0b050");
            _btn.normal.textColor = _btn.hover.textColor = _btn.active.textColor = Util.Hex("#1a1626");
            _btnSub = new GUIStyle(_btn); _btnSub.normal.background = _tPanel2; _btnSub.hover.background = _tPanel2; _btnSub.active.background = _tEdge;
            _btnSub.normal.textColor = _btnSub.hover.textColor = _btnSub.active.textColor = ink;
            _box = new GUIStyle(GUI.skin.box); _box.normal.background = _tPanel;
        }

        void Panel(Rect r, Texture2D fill = null, Texture2D edge = null)
        {
            GUI.DrawTexture(new Rect(r.x - 2, r.y - 2, r.width + 4, r.height + 4), edge ?? _tEdge);
            GUI.DrawTexture(r, fill ?? _tPanel);
        }
        void DrawSprite(Rect r, Sprite s, bool flip = false)
        {
            if (s == null) return;
            var t = s.texture; float k = Mathf.Max(1, Mathf.Floor(Mathf.Min(r.width / t.width, r.height / t.height)));
            var rr = new Rect(r.x + (r.width - t.width * k) / 2, r.y + (r.height - t.height * k) / 2, t.width * k, t.height * k);
            GUI.DrawTextureWithTexCoords(rr, t, flip ? new Rect(1, 0, -1, 1) : new Rect(0, 0, 1, 1));
        }
        void Chip(Rect r, string type)
        {
            var ti = Data.Types[type];
            var old = GUI.color; GUI.color = ti.C; GUI.DrawTexture(r, _tWhite); GUI.color = old;
            var st = new GUIStyle(_small) { alignment = TextAnchor.MiddleCenter, fontStyle = FontStyle.Bold }; st.normal.textColor = Util.Hex("#1a1626");
            GUI.Label(r, ti.N, st);
        }

        void OnGUI()
        {
            SetupStyles();
            GUI.depth = 0;
            if (_scr != Scr.Battle) GUI.DrawTexture(new Rect(0, 0, Screen.width, Screen.height), Tex2("#141022"));
            switch (_scr)
            {
                case Scr.Title: TitleGUI(); break;
                case Scr.Starter: StarterGUI(); break;
                case Scr.Hub: HubGUI(); break;
                case Scr.Team: TeamGUI(); break;
                case Scr.Battle: BattleGUI(); break;
            }
            if (_confirmMsg != null) ConfirmGUI();
            if (_toastT > 0 && _toast != null)
            {
                var r = new Rect(_col.x + U, Screen.height - U * 5, _col.width - U * 2, U * 3);
                Panel(r, _tDark); GUI.Label(r, _toast, _center);
            }
        }
        readonly Dictionary<string, Texture2D> _texCache = new Dictionary<string, Texture2D>();
        Texture2D Tex2(string hex) { if (!_texCache.TryGetValue(hex, out var t)) _texCache[hex] = t = Tex(hex); return t; }

        void Toast(string s) { _toast = s; _toastT = 2.2f; }
        void Confirm(string msg, System.Action yes) { _confirmMsg = msg; _confirmYes = yes; }
        void ConfirmGUI()
        {
            GUI.DrawTexture(new Rect(0, 0, Screen.width, Screen.height), Tex2("#0d0b14cc"));
            var r = new Rect(_col.x + U * 2, Screen.height * .35f, _col.width - U * 4, U * 9);
            Panel(r);
            GUI.Label(new Rect(r.x + U, r.y + U, r.width - U * 2, U * 4), _confirmMsg, _center);
            if (GUI.Button(new Rect(r.x + U, r.yMax - U * 3.5f, r.width / 2 - U * 1.5f, U * 2.5f), "はい", _btn)) { var a = _confirmYes; _confirmMsg = null; a?.Invoke(); }
            if (GUI.Button(new Rect(r.center.x + U * .5f, r.yMax - U * 3.5f, r.width / 2 - U * 1.5f, U * 2.5f), "いいえ", _btnSub)) _confirmMsg = null;
        }

        // ---------- タイトル ----------
        void TitleGUI()
        {
            float x = _col.x, w = _col.width, y = Screen.height * .14f;
            GUI.Label(new Rect(x, y, w, U * 5), "PIXEL MONSTER\nARENA", _title); y += U * 5.5f;
            GUI.Label(new Rect(x, y, w, U * 1.5f), "ピクセル モンスター アリーナ", _center); y += U * 2.5f;
            var ids = Data.Species.Keys.Take(8).ToList(); float s = Mathf.Min(U * 3.2f, (w - U * 2) / ids.Count);
            for (int i = 0; i < ids.Count; i++) DrawSprite(new Rect(x + (w - s * ids.Count) / 2 + i * s, y, s, s), PixelArt.Mon(ids[i]).Normal);
            y += s + U;
            GUI.Label(new Rect(x + U, y, w - U * 2, U * 3), "くさむらで モンスターを つかまえて\nスタジアムの たいかいで リアルタイムバトル！", _center); y += U * 4;
            float bw = w * .6f, bx = x + (w - bw) / 2;
            if (S != null && GUI.Button(new Rect(bx, y, bw, U * 3), "つづきから", _btn)) _scr = Scr.Hub;
            y += U * 4;
            if (GUI.Button(new Rect(bx, y, bw, U * 3), "はじめから", _btnSub))
            {
                if (S != null) Confirm("セーブデータを けして\nはじめから あそびますか？", () => _scr = Scr.Starter);
                else _scr = Scr.Starter;
            }
        }

        // ---------- さいしょの1匹 ----------
        void StarterGUI()
        {
            float x = _col.x + U, w = _col.width - U * 2, y = U * 2;
            GUI.Label(new Rect(x, y, w, U * 2), "<b>さいしょの あいぼうを えらぼう</b>", _center); y += U * 2.2f;
            GUI.Label(new Rect(x, y, w, U * 1.5f), "タイプには あいしょうが あります", new GUIStyle(_small) { alignment = TextAnchor.MiddleCenter }); y += U * 2.5f;
            foreach (var id in Data.Starters)
            {
                var sp = Data.Species[id]; var r = new Rect(x, y, w, U * 7);
                Panel(r);
                DrawSprite(new Rect(r.x + U * .5f, r.y + U * .5f, U * 6, U * 6), PixelArt.Mon(id).Normal);
                GUI.Label(new Rect(r.x + U * 7, r.y + U * .4f, r.width - U * 7.5f, U * 1.6f), $"<b>{sp.N}</b>", _lbl);
                Chip(new Rect(r.x + U * 7 + U * 6, r.y + U * .6f, U * 3.5f, U * 1.3f), sp.Type);
                GUI.Label(new Rect(r.x + U * 7, r.y + U * 2.2f, r.width - U * 7.5f, U * 4.5f), sp.Desc, _small);
                if (GUI.Button(r, "", GUIStyle.none))
                {
                    S = new SaveData(); S.party.Add(S.NewMon(id, 5)); S.Save(); _scr = Scr.Hub;
                }
                y += U * 8;
            }
        }

        // ---------- ハブ ----------
        void HubGUI()
        {
            float x = _col.x + U, w = _col.width - U * 2, y = U * 1.5f;
            GUI.Label(new Rect(x, y, w * .6f, U * 4), "PIXEL MONSTER\nARENA", new GUIStyle(_title) { fontSize = Mathf.RoundToInt(U * 1.2f), alignment = TextAnchor.UpperLeft });
            GUI.Label(new Rect(x + w * .55f, y, w * .45f, U * 4.5f), $"トロフィー <b>{S.trophies}</b>\nカプセル <b>{S.capsules}</b>\nつかまえた <b>{S.caught}</b>", new GUIStyle(_small) { alignment = TextAnchor.UpperRight, richText = true });
            y += U * 5;
            var r = Data.Rounds[S.round];
            var cr = new Rect(x, y, w, U * 6.5f); Panel(cr);
            GUI.Label(new Rect(cr.x + U * .6f, cr.y + U * .3f, cr.width - U, U * 5), $"<color=#ffd166><b>{Data.CupName(S.tier)}</b></color>\nつぎ：<b>{r.N}</b> vs {r.Tr}\n<size={Mathf.RoundToInt(U * .72f)}>あいての レベル {Data.RoundLv(r, S.tier)} ぜんご ／ {r.Size}たい</size>", _lbl);
            float bw = (cr.width - U * 1.2f) / 4;
            for (int i = 0; i < 4; i++) GUI.DrawTexture(new Rect(cr.x + U * .6f + i * bw, cr.yMax - U * 1.1f, bw - 4, U * .6f), i < S.round ? _tAcc : i == S.round ? Tex2("#ff6b5b") : _tDark);
            y += U * 7.5f;
            float hw = (w - U) / 2;
            if (GUI.Button(new Rect(x, y, hw, U * 4), "たいかいへ\n<size=" + Mathf.RoundToInt(U * .7f) + ">スタジアムで しあい</size>", _btn)) StartCup();
            if (GUI.Button(new Rect(x + hw + U, y, hw, U * 4), "くさむらへ\n<size=" + Mathf.RoundToInt(U * .7f) + ">モンスターを つかまえる</size>", _btn)) StartWild();
            y += U * 5;
            GUI.Label(new Rect(x, y, w * .7f, U * 1.5f), "パーティ（上から3たいが しゅつじょう）", _small);
            if (GUI.Button(new Rect(x + w - U * 6, y, U * 6, U * 1.6f), "へんせい ›", _btnSub)) { _scr = Scr.Team; _scroll = Vector2.zero; }
            y += U * 2;
            float pw = (w - U) / 3;
            for (int i = 0; i < S.party.Count; i++)
            {
                var m = S.party[i]; var pr = new Rect(x + (i % 3) * (pw + U / 2), y + (i / 3) * U * 6.5f, pw, U * 6);
                Panel(pr);
                DrawSprite(new Rect(pr.x, pr.y + U * .3f, pr.width, U * 3.5f), PixelArt.Mon(m.sid).Normal);
                GUI.Label(new Rect(pr.x, pr.y + U * 3.8f, pr.width, U * 2), $"{Data.Species[m.sid].N}\nLv{m.lvl}", new GUIStyle(_small) { alignment = TextAnchor.UpperCenter });
                if (i < 3) { GUI.DrawTexture(new Rect(pr.x + 3, pr.y + 3, U * 2, U), _tAcc); GUI.Label(new Rect(pr.x + 3, pr.y + 2, U * 2, U * 1.1f), "出場", new GUIStyle(_small) { alignment = TextAnchor.MiddleCenter, normal = { textColor = Util.Hex("#1a1626") } }); }
            }
            y += Mathf.CeilToInt(S.party.Count / 3f) * U * 6.5f + U * .5f;
            GUI.Label(new Rect(x, y, w, U * 6), "<b>そうさ</b>：左のスティックで いどう／右のボタンで こうげき・わざ・かわす。赤い はんいは あいての わざの よちょう。◎の わざ（命中100未満）は むいた方向・はんいに うつので よけられる。\nPC：WASD=移動 J=こうげき K/L/U/I=わざ Space=かわす", _small);
            if (GUI.Button(new Rect(x + w / 2 - U * 6, Screen.height - U * 2.5f, U * 12, U * 1.6f), "セーブデータを けす", _btnSub))
                Confirm("セーブデータを けしますか？\nもとに もどせません。", () => { SaveData.Delete(); S = null; _scr = Scr.Title; });
        }

        // ---------- へんせい ----------
        void TeamGUI()
        {
            float x = _col.x + U, w = _col.width - U * 2;
            GUI.Label(new Rect(x, U, w, U * 2), "<b>パーティ</b>", _lbl);
            if (GUI.Button(new Rect(x + w - U * 6, U, U * 6, U * 2), "もどる", _btnSub)) { _scr = Scr.Hub; _openUid = -1; }
            var view = new Rect(_col.x, U * 3.5f, _col.width, Screen.height - U * 3.5f);
            float contentH = EstimateTeamHeight();
            _scroll.y = Mathf.Min(_scroll.y, Mathf.Max(0, contentH - view.height));
            _scroll = GUI.BeginScrollView(view, _scroll, new Rect(0, 0, _col.width - 20, contentH), false, false, GUIStyle.none, GUIStyle.none);
            float y = 0;
            for (int i = 0; i < S.party.Count; i++) y = MonCard(S.party[i], true, i, U, y, w);
            GUI.Label(new Rect(U, y + U * .5f, w, U * 1.6f), $"ボックス（{S.box.Count}たい）", _small); y += U * 2.5f;
            if (S.box.Count == 0) { GUI.Label(new Rect(U, y, w, U * 3), "（からっぽ）パーティは6たいまで。7たいめから ボックスに おくられます。", _small); y += U * 3; }
            for (int i = 0; i < S.box.Count; i++) y = MonCard(S.box[i], false, i, U, y, w);
            GUI.EndScrollView();
        }
        float EstimateTeamHeight()
        {
            float h = (S.party.Count + S.box.Count) * U * 8.5f + U * 8;
            var open = S.party.Concat(S.box).FirstOrDefault(m => m.uid == _openUid);
            if (open != null) h += (Data.Species[open.sid].Learn.Length * U * 4.2f + U * 2);
            return h;
        }

        float MonCard(MonData m, bool inParty, int i, float x, float y, float w)
        {
            var sp = Data.Species[m.sid]; var st = Data.CalcStats(m);
            var r = new Rect(x, y, w, U * 7.5f);
            Panel(r, null, inParty && i < 3 ? _tAcc : null);
            DrawSprite(new Rect(r.x + U * .3f, r.y + U * .7f, U * 5, U * 5), PixelArt.Mon(m.sid).Normal);
            float tx = r.x + U * 5.7f, tw = r.width - U * 5.7f - U * 6;
            GUI.Label(new Rect(tx, r.y + U * .2f, tw, U * 1.6f), $"<b>{sp.N}</b> <size={Mathf.RoundToInt(U * .72f)}>Lv{m.lvl}{(inParty && i < 3 ? "  出場" : "")}</size>", _lbl);
            Chip(new Rect(tx, r.y + U * 1.9f, U * 3.6f, U * 1.2f), sp.Type);
            if (!string.IsNullOrEmpty(sp.Type2)) Chip(new Rect(tx + U * 3.8f, r.y + U * 1.9f, U * 3.6f, U * 1.2f), sp.Type2);
            GUI.Label(new Rect(tx, r.y + U * 3.2f, tw, U * 1.3f), $"HP{st.Hp} こう{Mathf.RoundToInt(st.Atk)} ぼう{Mathf.RoundToInt(st.Def)} はや{st.Spd}", _small);
            GUI.Label(new Rect(tx, r.y + U * 4.4f, tw, U * 2.6f), string.Join(" / ", Data.Equipped(m).Select(id => Data.Moves[id].N)), _small);
            GUI.DrawTexture(new Rect(tx, r.yMax - U * .6f, tw, U * .3f), _tDark);
            GUI.DrawTexture(new Rect(tx, r.yMax - U * .6f, tw * Mathf.Min(1, m.exp / (float)Data.ExpNext(m.lvl)), U * .3f), Tex2("#7fb2ff"));
            float bx = r.xMax - U * 5.6f, bw = U * 5.3f, bh = U * 1.6f, by = r.y + U * .3f;
            if (GUI.Button(new Rect(bx, by, bw, bh), "わざ", _btnSub)) _openUid = _openUid == m.uid ? -1 : m.uid;
            by += bh + 2;
            if (inParty)
            {
                GUI.enabled = i > 0; if (GUI.Button(new Rect(bx, by, bw, bh), "▲ うえへ", _btnSub)) { (S.party[i - 1], S.party[i]) = (S.party[i], S.party[i - 1]); S.Save(); } by += bh + 2;
                GUI.enabled = i < S.party.Count - 1; if (GUI.Button(new Rect(bx, by, bw, bh), "▼ したへ", _btnSub)) { (S.party[i + 1], S.party[i]) = (S.party[i], S.party[i + 1]); S.Save(); } by += bh + 2;
                GUI.enabled = S.party.Count > 1; if (GUI.Button(new Rect(bx, by, bw, bh), "あずける", _btnSub)) { S.box.Add(m); S.party.RemoveAt(i); S.Save(); }
                GUI.enabled = true;
            }
            else
            {
                GUI.enabled = S.party.Count < 6; if (GUI.Button(new Rect(bx, by, bw, bh), "つれていく", _btnSub)) { S.party.Add(m); S.box.RemoveAt(i); S.Save(); } by += bh + 2;
                GUI.enabled = true;
                if (GUI.Button(new Rect(bx, by, bw, bh), "にがす", _btnSub)) { var idx = i; Confirm($"{sp.N}（Lv{m.lvl}）を にがしますか？", () => { S.box.RemoveAt(idx); S.Save(); }); }
            }
            y += U * 8;
            if (_openUid == m.uid) y = MoveEditor(m, x, y, w);
            return y + U * .5f;
        }

        float MoveEditor(MonData m, float x, float y, float w)
        {
            var eq = Data.Equipped(m);
            GUI.Label(new Rect(x, y, w, U * 1.5f), "わざを 4つまで えらべます（タップで つける／はずす）", _small); y += U * 1.7f;
            foreach (var le in Data.Species[m.sid].Learn)
            {
                var mv = Data.Moves[le.Id]; bool ok = le.Lv <= m.lvl, on = eq.Contains(le.Id);
                var r = new Rect(x, y, w, U * 4);
                Panel(r, on ? Tex2("#3d3360") : _tPanel, on ? _tAcc : null);
                var old = GUI.color; GUI.color = Data.Types[mv.T].C; GUI.DrawTexture(new Rect(r.x, r.y, U * .35f, r.height), _tWhite); GUI.color = old;
                string cat = mv.Cat == "phys" ? "ぶつり" : mv.Cat == "spec" ? "とくしゅ" : "へんか";
                GUI.Label(new Rect(r.x + U * .6f, r.y + U * .1f, r.width - U, U * 1.5f), $"<b>{mv.N}</b>  <size={Mathf.RoundToInt(U * .7f)}>{Data.Types[mv.T].N}・{cat}{(ok ? "" : $"・Lv{le.Lv}で おぼえる")}</size>", _lbl);
                GUI.Label(new Rect(r.x + U * .6f, r.y + U * 1.6f, r.width - U, U * 2.4f), MoveText.Describe(mv), _small);
                GUI.enabled = ok;
                if (GUI.Button(r, "", GUIStyle.none) && _dragDist < 10)
                {
                    if (on) { if (eq.Count > 1) eq.Remove(le.Id); }
                    else if (eq.Count < 4) eq.Add(le.Id);
                    else Toast("4つまでです。どれかを はずしてから えらんでね");
                    m.moves = eq; S.Save();
                }
                GUI.enabled = true;
                y += U * 4.2f;
            }
            return y;
        }

        // ---------- バトル ----------
        void BattleGUI()
        {
            float x = _col.x + U * .5f, w = _col.width - U, y = U * .4f;
            // 上の帯
            GUI.Label(new Rect(x, y, w * .7f, U * 1.5f), _bTitle(), _small);
            var pr = new Rect(x + w - U * 5, y, U * 5, U * 1.5f);
            _btnRects["pause"] = pr; GUI.Box(pr, "ポーズ", _btnSub);
            y += U * 1.9f;
            // プレート
            float pw = (w - U * .6f) / 2;
            Plate(new Rect(x, y, pw, U * 4.6f), 0); Plate(new Rect(x + pw + U * .6f, y, pw, U * 4.6f), 1);
            y += U * 5.2f;
            // ゲーム画面（4:3）
            float vh = Mathf.Min(w * .75f, Screen.height * .45f), vw = vh / .75f;
            _rView = new Rect(_col.x + (_col.width - vw) / 2, y, vw, vh);
            _cam.rect = new Rect(_rView.x / Screen.width, 1 - _rView.yMax / Screen.height, _rView.width / Screen.width, _rView.height / Screen.height);
            GUI.DrawTexture(new Rect(_rView.x - 3, _rView.y - 3, _rView.width + 6, _rView.height + 6), _tEdge);
            WorldTextsGUI();
            if (B.TrickRoom > 0) { var o = GUI.color; GUI.color = new Color(1, .47f, .78f, .12f); GUI.DrawTexture(_rView, _tWhite); GUI.color = o; }
            Minimap();
            y += vh + U * .5f;
            // バナー
            var br = new Rect(x, y, w, U * 2.6f); Panel(br, _tDark);
            GUI.Label(br, _bannerT > -30 ? _banner : "", _center);
            y += U * 3.1f;
            // 操作
            ControlsGUI(new Rect(x, y, w, Screen.height - y - U * .6f));
            if (_pauseOpen) PauseGUI();
            if (_resultOpen) ResultGUI();
        }
        string _bTitle() => B.Kind == "wild" ? "くさむら" : $"{Data.CupName(S.tier)}　{Data.Rounds[Mathf.Min(S.round, Data.Rounds.Length - 1)].N}";

        void Plate(Rect r, int side)
        {
            Panel(r);
            var f = B.Active(side); if (f == null) return;
            var right = side == 1;
            var al = new GUIStyle(_lbl) { alignment = right ? TextAnchor.UpperRight : TextAnchor.UpperLeft, wordWrap = false, clipping = TextClipping.Clip };
            GUI.Label(new Rect(r.x + U * .4f, r.y + U * .1f, r.width - U * .8f, U * 1.5f), right ? $"<size={Mathf.RoundToInt(U * .72f)}>Lv{f.Lvl}</size>  <b>{f.Sp.N}</b>" : $"<b>{f.Sp.N}</b>  <size={Mathf.RoundToInt(U * .72f)}>Lv{f.Lvl}</size>", al);
            var hb = new Rect(r.x + U * .4f, r.y + U * 1.7f, r.width - U * .8f, U * .6f);
            GUI.DrawTexture(hb, _tDark);
            float k = f.Hp / f.MaxHp;
            GUI.DrawTexture(new Rect(hb.x, hb.y, hb.width * k, hb.height), k > .5f ? _tGood : k > .2f ? _tAcc : Tex2("#ff6b5b"));
            var sm = new GUIStyle(_small) { alignment = right ? TextAnchor.UpperRight : TextAnchor.UpperLeft, wordWrap = false, clipping = TextClipping.Clip };
            GUI.Label(new Rect(r.x + U * .4f, r.y + U * 2.4f, r.width - U * .8f, U * 1.1f), $"{Mathf.CeilToInt(f.Hp)}/{f.MaxHp}   {string.Concat(B.Sides[side].Fs.Select(x => x.Fainted ? "□" : "■"))}", sm);
            var cs = new GUIStyle(sm); cs.normal.textColor = Util.Hex("#ffd166");
            GUI.Label(new Rect(r.x + U * .4f, r.y + U * 3.4f, r.width - U * .8f, U * 1.1f), CondText(f), cs);
        }
        static string CondText(Fighter f)
        {
            var a = new List<string>();
            if (f.Status != "") a.Add(Battle.StatusNames[f.Status]);
            foreach (var k in Battle.StageKeys) if (f.St[k] != 0) a.Add($"{Battle.StageNames[k].Substring(0, 2)}{(f.St[k] > 0 ? "+" : "")}{f.St[k]}");
            if (f.V.Sub > 0) a.Add("デコイ"); if (f.V.Taunt > 0) a.Add("ちょうはつ"); if (f.V.EncoreId != null) a.Add("アンコール");
            if (f.V.Seed > 0) a.Add("タネ"); if (f.V.Confuse > 0) a.Add("こんらん"); if (f.V.HealBlock > 0) a.Add("かいふくふうじ"); if (f.V.Yawn > 0) a.Add("ねむけ");
            return string.Join(" ", a);
        }

        void WorldTextsGUI()
        {
            foreach (var (pos, txt, col, size) in _rend.WorldTexts)
            {
                var sp = _cam.WorldToScreenPoint(new Vector3(pos.x, -pos.y, 0));
                var gp = new Vector2(sp.x, Screen.height - sp.y);
                if (!_rView.Contains(gp)) continue;
                float scale = _rView.height / 240f * _rend.ViewZ;
                var st = new GUIStyle(_lbl) { fontSize = Mathf.Max(8, Mathf.RoundToInt(size * scale)), alignment = TextAnchor.MiddleCenter, fontStyle = FontStyle.Bold, wordWrap = false };
                var r = new Rect(gp.x - 200, gp.y - 30, 400, 60);
                st.normal.textColor = new Color(.07f, .05f, .11f, col.a);
                foreach (var o in new[] { new Vector2(-2, 0), new Vector2(2, 0), new Vector2(0, -2), new Vector2(0, 2) }) GUI.Label(new Rect(r.x + o.x, r.y + o.y, r.width, r.height), txt, st);
                st.normal.textColor = col; GUI.Label(r, txt, st);
            }
        }

        void Minimap()
        {
            var st = B.St;
            float mw = _rView.width * .17f, mh = mw * (st.Fy1 - st.Fy0) / (st.Fx1 - st.Fx0);
            var r = new Rect(_rView.xMax - mw - 6, _rView.y + 6, mw, mh);
            var o = GUI.color; GUI.color = new Color(.05f, .04f, .08f, .6f); GUI.DrawTexture(r, _tWhite); GUI.color = o;
            for (int s = 0; s < 2; s++)
            {
                var f = B.Active(s); if (f == null || f.State == "bench") continue;
                float px = r.x + (f.X - st.Fx0) / (st.Fx1 - st.Fx0) * mw, py = r.y + (f.Y - st.Fy0) / (st.Fy1 - st.Fy0) * mh;
                GUI.DrawTexture(new Rect(px - 3, py - 3, 6, 6), s == 1 ? Tex2("#ff6b5b") : Tex2("#4aa8ff"));
            }
        }

        void ControlsGUI(Rect area)
        {
            // スティック
            float js = Mathf.Min(area.width * .38f, area.height * .8f);
            _rJoy = new Rect(area.x + (area.width * .4f - js) / 2, area.y + (area.height - js) / 2, js, js);
            var o = GUI.color;
            GUI.color = Util.Hex("#2e2648"); GUI.DrawTexture(_rJoy, CircleTex());
            var knob = new Rect(_rJoy.center.x + _joyVec.x * js * .3f - js * .2f, _rJoy.center.y + _joyVec.y * js * .3f - js * .2f, js * .4f, js * .4f);
            GUI.color = Util.Hex("#ffd166"); GUI.DrawTexture(new Rect(knob.x - 3, knob.y - 3, knob.width + 6, knob.height + 6), CircleTex());
            GUI.color = Util.Hex("#3d3360"); GUI.DrawTexture(knob, CircleTex());
            GUI.color = o;
            // ボタン
            float bx = area.x + area.width * .42f, bw = area.width * .58f;
            var f = B.Active(0);
            var list = new List<(string id, string a, string b, Color c, float cd, bool hot, bool dim)>();
            for (int i = 0; i < 4; i++)
            {
                if (f == null || i >= f.Moves.Count) continue;
                var mv = Data.Moves[f.Moves[i]];
                list.Add(("mv" + i, mv.N, $"{Data.Types[mv.T].N}{(mv.Aim == "dir" && mv.Damaging ? "◎" : "")}", Data.Types[mv.T].C, f.CdOf(mv.Id) / mv.Cd, f.Queued == mv.Id, B.MoveBlocked(f, mv.Id) != null));
            }
            list.Add(("atk", "こうげき", "たいあたり", Util.Hex("#d8d0c0"), f != null ? f.CdOf("tackle") / Data.Moves["tackle"].Cd : 0, f != null && f.Queued == "tackle", false));
            list.Add(("dodge", "かわす", "むてき", Util.Hex("#7fd8ff"), f != null ? f.DodgeCd / .9f : 0, false, false));
            if (B.Sides[0].Fs.Count > 1) list.Add(("swap", "こうたい", "ひかえと", Util.Hex("#a49ac0"), B.Sides[0].SwapCd / Battle.SwapCdMax, _swapOpen, false));
            if (B.Kind == "wild") { list.Add(("cap", "カプセル", $"のこり {S.capsules}", Util.Hex("#3ad0c8"), 0, false, false)); list.Add(("run", "にげる", "", Util.Hex("#a49ac0"), 0, false, false)); }
            list.Add(("auto", "オート", S.auto ? "ON" : "OFF", S.auto ? Util.Hex("#4fd1a5") : Util.Hex("#a49ac0"), 0, S.auto, false));
            foreach (var key in _btnRects.Keys.Where(k => k != "pause").ToList()) _btnRects.Remove(key);
            if (_swapOpen) { SwapBar(new Rect(bx, area.y, bw, area.height)); return; }
            int rows = Mathf.CeilToInt(list.Count / 2f);
            float gh = (area.height - (rows - 1) * U * .4f) / rows, gw = (bw - U * .4f) / 2;
            var sa = new GUIStyle(_lbl) { alignment = TextAnchor.MiddleCenter, fontStyle = FontStyle.Bold, wordWrap = false, fontSize = Mathf.RoundToInt(U * .85f) };
            var sb = new GUIStyle(_small) { alignment = TextAnchor.MiddleCenter, wordWrap = false };
            for (int i = 0; i < list.Count; i++)
            {
                var it = list[i];
                var r = new Rect(bx + (i % 2) * (gw + U * .4f), area.y + (i / 2) * (gh + U * .4f), gw, gh);
                _btnRects[it.id] = r;
                Panel(r, it.hot ? Tex2("#3d3360") : _tPanel, it.hot ? _tAcc : null);
                GUI.color = it.c; GUI.DrawTexture(new Rect(r.x, r.y, U * .35f, r.height), _tWhite); GUI.color = o;
                if (it.dim) { GUI.color = new Color(1, 1, 1, .4f); }
                GUI.Label(new Rect(r.x, r.y + r.height * .1f, r.width, r.height * .5f), it.a, sa);
                GUI.Label(new Rect(r.x, r.y + r.height * .55f, r.width, r.height * .35f), it.b, sb);
                GUI.color = o;
                if (it.cd > 0) { GUI.color = new Color(0, 0, 0, .55f); GUI.DrawTexture(new Rect(r.x, r.yMax - r.height * Mathf.Clamp01(it.cd), r.width, r.height * Mathf.Clamp01(it.cd)), _tWhite); GUI.color = o; }
            }
        }
        Texture2D _circle;
        Texture2D CircleTex()
        {
            if (_circle) return _circle;
            int d = 64; _circle = new Texture2D(d, d) { filterMode = FilterMode.Bilinear };
            for (int y = 0; y < d; y++) for (int x = 0; x < d; x++) { float r = Vector2.Distance(new Vector2(x + .5f, y + .5f), new Vector2(d / 2f, d / 2f)); _circle.SetPixel(x, y, new Color(1, 1, 1, Mathf.Clamp01(d / 2f - r))); }
            _circle.Apply(); return _circle;
        }

        void Overlay() { var o = GUI.color; GUI.color = new Color(.05f, .04f, .08f, .84f); GUI.DrawTexture(_rView, _tWhite); GUI.color = o; }
        // こうたいの えらび：ボタンの場所に ひかえを ならべる（バトルは とまらない）
        void SwapBar(Rect area)
        {
            if (!B.CanSwap(out var bench)) { _swapOpen = false; return; }
            float rowH = Mathf.Min(U * 3.4f, (area.height - U * 3) / Mathf.Max(1, bench.Count));
            var head = new GUIStyle(_small) { alignment = TextAnchor.MiddleCenter }; head.normal.textColor = Util.Hex("#ffd166");
            GUI.Label(new Rect(area.x, area.y, area.width, U * 1.2f), "こうたい（バトルは とまりません）", head);
            float y = area.y + U * 1.4f;
            foreach (var i in bench)
            {
                var x = B.Sides[0].Fs[i]; var r = new Rect(area.x, y, area.width, rowH - U * .3f);
                _btnRects["swapTo" + i] = r;
                Panel(r);
                DrawSprite(new Rect(r.x + U * .2f, r.y + U * .1f, r.height - U * .2f, r.height - U * .2f), PixelArt.Mon(x.Mon.sid).Normal);
                GUI.Label(new Rect(r.x + r.height + U * .2f, r.y + U * .1f, r.width - r.height - U * .4f, r.height * .6f), $"<b>{x.Sp.N}</b> <size={Mathf.RoundToInt(U * .7f)}>Lv{x.Lvl}{(x.Status != "" ? "・" + Battle.StatusNames[x.Status] : "")}</size>", _lbl);
                var hb = new Rect(r.x + r.height + U * .2f, r.yMax - U * .9f, r.width - r.height - U * .6f, U * .4f);
                GUI.DrawTexture(hb, _tDark); GUI.DrawTexture(new Rect(hb.x, hb.y, hb.width * x.Hp / x.MaxHp, hb.height), _tGood);
                y += rowH;
            }
            var cr = new Rect(area.x, area.yMax - U * 2.2f, area.width, U * 2.2f);
            _btnRects["swapCancel"] = cr; Panel(cr); GUI.Label(cr, "やめる", _center);
        }
        void PauseGUI()
        {
            Overlay();
            GUI.Label(new Rect(_rView.x, _rView.y + _rView.height * .2f, _rView.width, U * 3), "PAUSE", _title);
            if (GUI.Button(new Rect(_rView.center.x - U * 6, _rView.center.y, U * 12, U * 2.4f), "つづける", _btn)) _pauseOpen = false;
            if (GUI.Button(new Rect(_rView.center.x - U * 8, _rView.center.y + U * 3, U * 16, U * 2.2f), "しあいを やめる（まけ あつかい）", _btnSub))
            { _pauseOpen = false; B.EndBattle(B.Kind == "wild" ? "run" : "lose"); B.EndT = 0; }
        }
        void ResultGUI()
        {
            Overlay();
            string t; Color c;
            switch (B.Result) { case "win": t = "WIN!"; c = Util.Hex("#ffd166"); break; case "lose": t = "LOSE…"; c = Util.Hex("#ff6b5b"); break; case "caught": t = "GET!"; c = Util.Hex("#4fd1a5"); break; default: t = "にげた"; c = Util.Hex("#a49ac0"); break; }
            var ts = new GUIStyle(_title); ts.normal.textColor = c;
            GUI.Label(new Rect(_rView.x, _rView.y + U * .5f, _rView.width, U * 3), t, ts);
            GUI.Label(new Rect(_rView.x + U, _rView.y + U * 3.8f, _rView.width - U * 2, _rView.height - U * 7.5f), string.Join("\n", B.ResLines.Count > 0 ? B.ResLines : new List<string> { "…" }), new GUIStyle(_small) { richText = true, alignment = TextAnchor.UpperCenter, normal = { textColor = Util.Hex("#f6f0e0") } });
            if (GUI.Button(new Rect(_rView.center.x - U * 5, _rView.yMax - U * 3.2f, U * 10, U * 2.4f), "つぎへ", _btn))
            { _resultOpen = false; B = null; _rend.P.Clear(); _scr = Scr.Hub; }
        }
    }

    /// <summary>わざの説明文（データから自動で作る。index.html の moveDesc と同じ）</summary>
    public static class MoveText
    {
        public static string Describe(Move m)
        {
            var e = m.E; var a = new List<string>();
            if (m.Damaging) a.Add($"いりょく{(m.Power > 0 ? m.Power : Mathf.RoundToInt(m.Pow * 5))}");
            a.Add(m.Acc > 0 ? $"めいちゅう{m.Acc}" : "めいちゅう—");
            if (m.Damaging) a.Add(m.Aim == "dir" ? "◎ほうこう・はんいを ねらう（よけられる）" : "あいてを ねらう");
            if (m.Prio > 0) a.Add("せんせい");
            if (!string.IsNullOrEmpty(e.St)) a.Add($"{(e.StCh < 100 ? e.StCh + "%で " : "")}{Battle.StatusNames[e.St]}にする");
            if (e.Seed) a.Add("HPを すいとる タネ");
            if (e.Flinch > 0) a.Add($"{e.Flinch}%で ひるませる");
            if (e.Drain > 0) a.Add($"ダメージの{e.Drain}%回復");
            if (e.Recoil > 0) a.Add($"ダメージの{e.Recoil}%はんどう");
            if (e.Heal > 0) a.Add($"HPを{e.Heal}%回復");
            string Sc(Dictionary<string, int> o) => string.Join("・", o.Select(kv => $"{Battle.StageNames[kv.Key]}{(kv.Value > 0 ? "+" : "")}{kv.Value}"));
            if (e.Self != null) a.Add($"じぶんの {Sc(e.Self)}");
            if (e.Foe != null) a.Add($"{(e.FoeCh < 100 ? e.FoeCh + "%で " : "")}あいての {Sc(e.Foe)}");
            switch (m.Sp) { case "taunt": a.Add("ほじょわざを ふうじる"); break; case "encore": a.Add("同じわざしか だせなくする"); break; case "yawn": a.Add("すこしあとに ねむらせる"); break; case "trick": a.Add("のうりょく変化を いれかえる"); break; case "roar": a.Add("あいてを ひっこめる"); break; }
            switch (m.K) { case "protect": a.Add("1びょう すべて ふせぐ"); break; case "sub": a.Add("HP1/4で デコイ"); break; case "dbond": a.Add("たおされたら あいても たおれる"); break; case "counter": a.Add($"ダメージを {m.Mult}ばいで かえす"); break; case "baton": a.Add("のうりょく変化を ひきついで こうたい"); break; }
            if (m.Fld == "trickroom") a.Add("おそいほど はやくなる"); if (m.Fld == "tailwind") a.Add("みかたの すばやさ1.5ばい");
            if (!string.IsNullOrEmpty(m.Hz)) a.Add("でてくる あいてに ダメージ／どく");
            if (m.SwitchOut) a.Add("あてたら こうたい"); if (m.Ohko) a.Add("あたれば いちげき"); if (m.Rampage) a.Add("あばれて こんらん");
            if (m.Fakeout) a.Add("でてすぐ だけ"); if (m.Sucker) a.Add("あいてが こうげき予兆中だけ"); if (m.Hits > 0) a.Add("3かい れんぞく"); if (m.BurstMax > 0) a.Add("2〜5はつ");
            return string.Join(" ／ ", a);
        }
    }
}
