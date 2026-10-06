# public_manifest — 公開版雜湊表

本表列**本倉每一個檔**的 sha256（LF 正規化後計算）。

與 [`v45_manifest.md`](v45_manifest.md) 的分工：

| 表 | 列的是 | 用途 |
| --- | --- | --- |
| `v45_manifest` | **內部封筆件**的 31 個組件 | 答「內部那一版封了什麼」 |
| `public_manifest`（本表） | **本倉**的每一個檔 | 答「你手上這一份是什麼」 |

兩表的雜湊**不相符**，差異＝去語料與去人名。逐處刪改紀錄在
[`../MANIFEST.md`](../MANIFEST.md) §二。對照方式：

1. 本表的「內部來源 sha256」欄 ↔ `v45_manifest` → 確認內部封的是哪一份；
2. `MANIFEST.md` §二 的逐處紀錄 → 確認公開版與它的差異只有那些處。

**本表不含兩個檔**：`manifest/public_manifest.md` 與 `.json`（本表自己）。
一張表沒辦法蓋住自己的雜湊——寫出來的瞬間就變了。**這一條照實記，不藏。**

---

| # | 檔 | 處理 | sha256 | 位元 | 內部來源 | 內部來源 sha256（前16） |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `docs/literature_mapping.md` | 去人名 | `8a10c693e2b9a1cec1ec73f7b9f5b94c9e08d8e24d4094d36db86ad8e7335f4f` | 17800 | `docs/literature_mapping.md` | — |
| 2 | `docs/method/2026-07-22_四條相鄰文獻線查證與定位.md` | 原樣 | `a50cc3b2fc841024af15cbde83716f12e44f8a55fd9f60de2bbb1bbc896a62e6` | 3692 | `docs/timeline/2026-07-22_method_四條相鄰文獻線查證與定位.md` | — |
| 3 | `docs/method/2026-07-29_方法論答辯_模型貼標籤.md` | 去人名 | `a4f995913af6b0afd3a76fc55cf2ee93f0eeda110799b794270ae43bab782ee6` | 6598 | `docs/timeline/2026-07-29_method_模型貼標籤方法論答辯.md` | — |
| 4 | `docs/method/2026-07-29_框架_GPS對外解釋.md` | 去人名 | `82c47e4d0d68593796447ff0570d5d79ba5c8c04d564b8b0df56788d7271886c` | 3800 | `docs/timeline/2026-07-29_framework_GPS對外解釋.md` | — |
| 5 | `docs/protocol/盲測制度說明.md` | 新寫／節錄 | `9c63c7b94185764a0906749d96f996451bbc8d4a89acb36ef40e2ffdec4270bb` | 7105 | —（公開版新寫／節錄） | — |
| 6 | `docs/theory/AI行為虛構_機制假說與文獻對應.md` | 新寫／節錄 | `35677340fca14043f5567bf2801d09591be018c0d3bcfce8a1b468d8766f56ef` | 4187 | —（公開版新寫／節錄） | — |
| 7 | `docs/theory/失控機制理論與文獻定位.md` | 新寫／節錄 | `0d5ba4399f925427fbdcd25887e7f1908d9bd35efe55ebbf0079e50b2f4f83e0` | 3723 | —（公開版新寫／節錄） | — |
| 8 | `LICENSE` | 新寫／節錄 | `6ac9e44619713aa8dd4c4e57362e7a2b5911db90d60148f324bdb2d670be8871` | 1083 | —（公開版新寫／節錄） | — |
| 9 | `LICENSE-docs` | 新寫／節錄 | `1ec1b3d515d885939000ca28250c4887bfa0ccad571860cb1cfb775d8c34405c` | 1883 | —（公開版新寫／節錄） | — |
| 10 | `manifest/v45_manifest.json` | 原樣 | `ab05661190ff303fe63ead8f545469111d18fb5a34f450d2976d5655977e7958` | 10167 | `experiments/control-station/v45_manifest.json` | — |
| 11 | `manifest/v45_manifest.md` | 原樣 | `40d3b839efbaa000c32945175ec83ebd9990619ec12bd2879aad92ab3bb485de` | 4863 | `experiments/control-station/v45_manifest.md` | — |
| 12 | `manifest/v45_manifest.py` | 去人名 | `c87a5cb7e9ef7bc8f6707032d0304fd2c458f9556915a29c1ce20c729ff82cee` | 8514 | `experiments/control-station/v45_manifest.py` | — |
| 13 | `MANIFEST.md` | 新寫／節錄 | `d9e6cc9df34ee373c0278567fc88f3d1f7bedb69ef8079aff7e176e1408450b2` | 17393 | —（公開版新寫／節錄） | — |
| 14 | `PUBLIC_NOTES.md` | 新寫／節錄 | `3ca27d271fc603fd4c092f9e23afa66cb5bc64631db13edc6090df12277925af` | 4813 | —（公開版新寫／節錄） | — |
| 15 | `README.md` | 新寫／節錄 | `e9cc20e3aeef3e966909004c50910dc8ab053b079e10266e2f01fd58b401fba0` | 5182 | —（公開版新寫／節錄） | — |
| 16 | `results/2026-10-05_卷五開獎報告_去語料.md` | 新寫／節錄 | `8ccf64ed0a901e4ebc731b98fc381d7a53a36501bc7eb77c1b04abde2a22014e` | 2074 | —（公開版新寫／節錄） | — |
| 17 | `results/2026-10-06_卷七開獎報告_辨識線結案_去語料.md` | 新寫／節錄 | `3dbe4328e30fddbc3fe2292feffa520e716d1bfbed4897d6b9f48b8ecdc877ab` | 3403 | —（公開版新寫／節錄） | — |
| 18 | `results/2026-10-06_卷六開獎報告_去語料.md` | 新寫／節錄 | `bcc3ca26724f38472263830fc11e2868ceaaf12583128fa2e30fa366236e8b9b` | 1370 | —（公開版新寫／節錄） | — |
| 19 | `src/blindtest/run_7b_arm.py` | 去人名 | `cb2ed42dee7e6d2f0dee6723c6439fb01ade50ecea9b7886690ce1bd95bebfeb` | 6755 | `experiments/blindtest/scripts/run_7b_arm.py` | `cb2ed42dee7e6d2f` |
| 20 | `src/control/judge_v4.py` | 去人名 | `764732bfb7e1596a06068fba4268c0cf141642aa365ee71b63d1c8d19b851482` | 32331 | `experiments/control-station/judge_v4.py` | `8845e46d5aaaa97f` |
| 21 | `src/control/request_form.py` | 去人名 | `7ed23ac8fadc52072725d7f542be869ad61d4487b26101206cd7a8c2bb5e72cc` | 10425 | `experiments/control-station/request_form.py` | `15f0eec929ad946f` |
| 22 | `src/mechanical/clause_v2.py` | 去語料+去人名 | `5b182a8cac27b376131625bdf3f6fa0b5b765510d329641dd17a5ae057a34d67` | 29111 | `experiments/mechanical-v2/clause_v2.py` | `1524a992a869b98f` |
| 23 | `src/mechanical/detectors.py` | 去人名 | `48612cc9095a91fb60109a5785db32a575f7304fe997d99c7e18f30f660d470b` | 28985 | `experiments/mechanical-v2/detectors.py` | `69a6cedefaeaf5f8` |
| 24 | `src/mechanical/lexicon_v2.py` | 去人名 | `c7121d902052697a4a7dba64bd3984e6d0d70d63c079f04311a8783dea69a8c7` | 34829 | `experiments/mechanical-v2/lexicon_v2.py` | `99b6e68b297358c8` |
| 25 | `src/mechanical/pipeline_v2.py` | 去語料+去人名 | `092c1c715ad454d4c43fdb924c7e3a970962234d44855f15c898543a2e8bf5ee` | 8497 | `experiments/mechanical-v2/pipeline_v2.py` | `d8723b37c3ac4017` |
| 26 | `src/mechanical/reorder_v2.py` | 去語料+去人名 | `d1c022bee13ee2c02eae98d25c91bc140a445aca7f5bb36d2393403242c43675` | 10561 | `experiments/mechanical-v2/reorder_v2.py` | `c8aeb6795009d9a8` |
| 27 | `src/mechanical/rules_v2.py` | 去人名 | `1e3fc5e9ec09c15fa5a6d5ab934f3fd9e89709fd76894997100769ca98cbcd5e` | 11450 | `experiments/mechanical-v2/rules_v2.py` | `f979a3095f9b8d82` |
| 28 | `src/mechanical/signed_tables/function_layer.json` | 去人名 | `dd4a3d4a2557d205c460166c2be14fe8286d8b48b563809b43f1a76066b75f1a` | 1876 | `experiments/mechanical-v2/signed_tables/function_layer.json` | `ec1df128cce3e2c0` |
| 29 | `src/mechanical/signed_tables/knife2_one_classifier.json` | 去人名 | `b106667fd4350cbea24be094ff92f02bb21afca41627434c28aa30934e4f751d` | 2409 | `experiments/mechanical-v2/signed_tables/knife2_one_classifier.json` | `bb4a4ccadf6355ef` |
| 30 | `src/mechanical/signed_tables/lexicon_registry.json` | 去人名 | `52586129f1461d6b88fb35eca98394e47fbc75f1f6271a55353fac456a23025d` | 1891 | `experiments/mechanical-v2/signed_tables/lexicon_registry.json` | `c207c1208d9e1670` |
| 31 | `src/perf/early_stop.py` | 去人名 | `3e60d5a62f3ff9fcdd197a3f831b35488954164ff988c536d5fdd227dad99aab` | 3451 | `experiments/perf-station/early_stop.py` | `3e60d5a62f3ff9fc` |
| 32 | `src/perf/run_perf.py` | 去人名 | `60c211e02ccd5c397bb5192fc1e348db77a6f7867cb8f3f233aef10413e8024e` | 28860 | `experiments/perf-station/run_perf.py` | `83b01addf50c804c` |
| 33 | `src/perf/schema_v1.py` | 去人名 | `3118b84b017ffd7eab9308b46de5097528109bdf3db7bb78caf6a4269cd0ca4d` | 5401 | `experiments/perf-station/schema_v1.py` | `712ffc481bd0800d` |
| 34 | `src/tools/split_sentences.py` | 去語料+去人名 | `34bfcbf9d1c82cfeddd6508d8140f349dc5fcad9cae3491697b2256cd3fd554a` | 16616 | `tools/split_sentences.py` | `890a73048d47a3c7` |

| 項 | 值 |
| --- | --- |
| 本表涵蓋檔數 | **34** |
| 其中自內部檔複製 | 23 |
| 其中公開版新寫或節錄 | 11 |
| 本表未涵蓋（本表自己） | 2 |

### 自行核驗

```bash
# 逐檔核（LF 正規化後計算，與本表同法）
find . -type f ! -path './manifest/public_manifest.*' -print0 \
  | xargs -0 -I{} sh -c 'printf "%s  " "{}"; tr -d "\r" < "{}" | sha256sum | cut -d" " -f1'
```
