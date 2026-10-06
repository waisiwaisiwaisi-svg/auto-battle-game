using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace PixelMonsterArena.EditorTools
{
    /// <summary>
    /// プロジェクトを初めて開いたときに Assets/Scenes/Main.unity を作り、Build Settings に登録する。
    /// ゲーム本体は Game.cs が再生時に自動で組み立てるので、シーンは空のままで OK。
    /// </summary>
    [InitializeOnLoad]
    public static class PixelMonsterArenaSetup
    {
        const string ScenePath = "Assets/Scenes/Main.unity";

        static PixelMonsterArenaSetup()
        {
            EditorApplication.delayCall += () =>
            {
                if (!File.Exists(ScenePath)) CreateScene(false);
            };
        }

        [MenuItem("Pixel Monster Arena/メインシーンを作りなおす")]
        static void Recreate() => CreateScene(true);

        static void CreateScene(bool open)
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;
            Directory.CreateDirectory("Assets/Scenes");
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var cam = new GameObject("Main Camera").AddComponent<Camera>();
            cam.tag = "MainCamera";
            cam.orthographic = true;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0x14 / 255f, 0x10 / 255f, 0x22 / 255f);
            cam.transform.position = new Vector3(0, 0, -10);
            EditorSceneManager.SaveScene(scene, ScenePath);
            EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath, true) };
            PlayerSettings.productName = "Pixel Monster Arena";
            Debug.Log("[Pixel Monster Arena] Assets/Scenes/Main.unity を作成し、Build Settings に登録しました。再生ボタンで遊べます。");
            if (open) EditorSceneManager.OpenScene(ScenePath);
        }
    }
}
