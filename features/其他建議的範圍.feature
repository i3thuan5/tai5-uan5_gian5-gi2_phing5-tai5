Feature: 其他建議的範圍
  華語/正規化前/正規化後」用「對不起/拍謝/歹勢」做例
  實際上遇到的，也有可能是「小豬/豬仔囡/豬仔囝」漢字正規化

    Scenario: 包含全部關鍵字的華語
       Given 有人求 對不起 的講法
       And 有人答 拍謝 的講法
       When 有人共 拍謝 的講法正規化做 歹勢
       Then 查 對 會當揣著其他建議 歹勢

    Scenario: 完全仝款的華語應該揣著，袂使出現佇其他建議
       Given 有人求 對不起 的講法
       And 有人答 拍謝 的講法
       When 有人共 拍謝 的講法正規化做 歹勢
       Then 查 對不起 揣袂著其他建議 對不起

    Scenario: 關鍵字佮民眾提供的講法仝款
       Given 有人求 對不起 的講法
       And 有人答 拍謝 的講法
       When 有人共 拍謝 的講法正規化做 歹勢
       Then 查 拍謝 會當揣著其他建議 歹勢

    Scenario: 關鍵字佮臺語提供的講法仝款
       Given 有人求 對不起 的講法
       And 有人答 拍謝 的講法
       When 有人共 拍謝 的講法正規化做 歹勢
       Then 查 歹勢 會當揣著其他建議 歹勢

    Scenario: 關鍵字華語臺語攏有出現
       Given 有人求 小豬 的講法
       And 有人答 豬仔囡 的講法
       When 有人正規化 豬仔囝 的講法
       Then 查 豬 會當揣著其他建議 豬仔囡

    Scenario: 部份臺語寫法無應該出現
       Given 有人求 對不起 的講法
       And 有人答 拍謝 的講法
       When 有人共 拍謝 的講法正規化做 歹勢
       Then 查 拍 揣袂著其他建議 對不起
       and 查 歹 揣袂著其他建議 對不起

    Scenario: 華語臺語共同詞
       Given 有人求 火車 的講法
       And 有人答 火車 的講法
       When 有人正規化 火車 的講法
       Then 查 火車 揣袂著其他建議 火車
 
