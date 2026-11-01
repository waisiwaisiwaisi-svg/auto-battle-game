// PC版の しるし（ゲームは window.PMA_DESKTOP で PC版 と わかる）
const { contextBridge } = require('electron');
contextBridge.exposeInMainWorld('PMA_DESKTOP', { platform: process.platform });
