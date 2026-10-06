using System;
using System.Collections.Generic;
using UnityEngine;

namespace PixelMonsterArena
{
    [Serializable]
    public class MonData
    {
        public int uid;
        public string sid;
        public int lvl;
        public int exp;
    }

    /// <summary>セーブデータ。PlayerPrefs に JSON で保存する。</summary>
    [Serializable]
    public class SaveData
    {
        const string Key = "pixel-monster-arena-v1";

        public List<MonData> party = new List<MonData>();
        public List<MonData> box = new List<MonData>();
        public int capsules = 10, tier, round, trophies, uid = 1, caught, wins;
        public bool auto;

        public static SaveData Load()
        {
            var json = PlayerPrefs.GetString(Key, "");
            if (string.IsNullOrEmpty(json)) return null;
            try
            {
                var s = JsonUtility.FromJson<SaveData>(json);
                return s != null && s.party != null && s.party.Count > 0 ? s : null;
            }
            catch (Exception) { return null; }
        }

        public static bool Exists() => Load() != null;
        public static void Delete() { PlayerPrefs.DeleteKey(Key); PlayerPrefs.Save(); }

        public void Save()
        {
            PlayerPrefs.SetString(Key, JsonUtility.ToJson(this));
            PlayerPrefs.Save();
        }

        public MonData NewMon(string sid, int lvl) => new MonData { uid = uid++, sid = sid, lvl = lvl, exp = 0 };

        public static int GainExp(MonData m, int x)
        {
            m.exp += x;
            int ups = 0;
            while (m.exp >= Data.ExpNext(m.lvl) && m.lvl < 99) { m.exp -= Data.ExpNext(m.lvl); m.lvl++; ups++; }
            return ups;
        }

        public float AvgLevel()
        {
            int n = Mathf.Min(3, party.Count);
            float s = 0;
            for (int i = 0; i < n; i++) s += party[i].lvl;
            return n > 0 ? s / n : 5;
        }
    }
}
