# public_manifest — 公開版雜湊表

本表列**本倉每一個檔**的 sha256（LF 正規化後計算）。檔名全數 ASCII。

**`papers/` 的四個存放檔另有一張表**：[`../papers/zenodo_v1.2/CHECKSUMS.md`](../papers/zenodo_v1.2/CHECKSUMS.md)
列的是**原始位元組**的 sha256 與 md5。本表對所有檔一律 LF 正規化後計算，
所以本表的 `papers/` 那幾列與那張表的值**對不上，而且應該對不上**——
兩張表問的是不同的問題。要跟 Zenodo 比對的是那一張。

**ASCII 改名不動內容**——被改名的九個檔中有八個與原始發佈 `ade2734`
逐位元組相同；第九個差一行（連結指向同被改名的檔）。對照見
[`../MANIFEST.md`](../MANIFEST.md) §七。

**本表不含兩個檔**：`manifest/public_manifest.md` 與 `.json`（本表自己）。
一張表沒辦法蓋住自己的雜湊——寫出來的瞬間就變了。**這一條照實記，不藏。**

| # | 檔 | sha256 | 位元 |
| --- | --- | --- | --- |
| 1 | `.gitattributes` | `ba167fe150d07505879a5555e449cbefda419f1463b99a821e7b1c162be46da0` | 264 |
| 2 | `COMMITMENT_2026-09-24.md` | `ee4fdbf0c1c2dbb87932871da4974527781f7ee629da7d2475f187bb1ce238c7` | 1174 |
| 3 | `docs/literature_mapping.md` | `8a10c693e2b9a1cec1ec73f7b9f5b94c9e08d8e24d4094d36db86ad8e7335f4f` | 17800 |
| 4 | `docs/method/2026-07-22_adjacent-literature-lines.md` | `a50cc3b2fc841024af15cbde83716f12e44f8a55fd9f60de2bbb1bbc896a62e6` | 3692 |
| 5 | `docs/method/2026-07-29_framework_gps-analogy.md` | `82c47e4d0d68593796447ff0570d5d79ba5c8c04d564b8b0df56788d7271886c` | 3800 |
| 6 | `docs/method/2026-07-29_methodology-defense_model-labeling.md` | `a4f995913af6b0afd3a76fc55cf2ee93f0eeda110799b794270ae43bab782ee6` | 6598 |
| 7 | `docs/PORTING.md` | `02a8854fb975c4d5173f2f068f5968cd8c0803898832f30b352ef952edbac4eb` | 9347 |
| 8 | `docs/PORTING.zh-TW.md` | `a7431539d03c54f30096953767cf43e0f11dd69ba285ddc8a2b7df430724031d` | 7911 |
| 9 | `docs/protocol/blind-test-protocol.md` | `9c63c7b94185764a0906749d96f996451bbc8d4a89acb36ef40e2ffdec4270bb` | 7105 |
| 10 | `docs/theory/behavioral-confabulation_mechanism-and-literature.md` | `35677340fca14043f5567bf2801d09591be018c0d3bcfce8a1b468d8766f56ef` | 4187 |
| 11 | `docs/theory/runaway-mechanism_theory-and-literature.md` | `0d5ba4399f925427fbdcd25887e7f1908d9bd35efe55ebbf0079e50b2f4f83e0` | 3723 |
| 12 | `LICENSE` | `6ac9e44619713aa8dd4c4e57362e7a2b5911db90d60148f324bdb2d670be8871` | 1083 |
| 13 | `LICENSE-docs` | `1ec1b3d515d885939000ca28250c4887bfa0ccad571860cb1cfb775d8c34405c` | 1883 |
| 14 | `manifest/v45_manifest.json` | `ab05661190ff303fe63ead8f545469111d18fb5a34f450d2976d5655977e7958` | 10167 |
| 15 | `manifest/v45_manifest.md` | `40d3b839efbaa000c32945175ec83ebd9990619ec12bd2879aad92ab3bb485de` | 4863 |
| 16 | `manifest/v45_manifest.py` | `c87a5cb7e9ef7bc8f6707032d0304fd2c458f9556915a29c1ce20c729ff82cee` | 8514 |
| 17 | `MANIFEST.md` | `7e04bbdf1a80d1d6c9686fbe469dc2984a4911f9ede344df4bcfba88c452d965` | 20274 |
| 18 | `papers/zenodo_v1.2/abstract_zh.md` | `c2437b0bca2ead34d4ebd513c9f06867c0bd06df5ba88387ae036ce3b0dc4e72` | 5099 |
| 19 | `papers/zenodo_v1.2/CHECKSUMS.md` | `8ca9fef569d6cfd92fe72b360f524f4fd0ce2a60262b53dd2a7fe2e5d53c8ee7` | 2024 |
| 20 | `papers/zenodo_v1.2/references.bib` | `dddc3cc61d226fcf3dd3914b8643dca39419f209a2e5a721083c6b3043a7de9d` | 22360 |
| 21 | `papers/zenodo_v1.2/report_v1.2.md` | `f84ba956e7d4535f1a648df01c5d32587ec1dae63ffe925fc527a1ed17c099c2` | 41012 |
| 22 | `papers/zenodo_v1.2/report_v1.2.pdf` | `b99dbe7b0eb815c59c2b80ef8649623cb54e782d251f38e7e42359bb03cc15eb` | 310044 |
| 23 | `PUBLIC_NOTES.md` | `d016f31c9222dd9583a69e9ce3fa94b2c462b644895e0928b11f428d85510318` | 7909 |
| 24 | `PUBLIC_NOTES.zh-TW.md` | `af1d522daab8b3eee3dd04d903bb62301dc551b228d0d9a169eea88f162f9cf7` | 6216 |
| 25 | `README.md` | `33ff1210e4172c63c06938f43b49604440177935195fe3b7d7003208d1c95166` | 10239 |
| 26 | `README.zh-TW.md` | `8ddb4640b7b181a4f91d5809d464a760ec18adb4a90de9c905a5ee26433a1548` | 8372 |
| 27 | `results/2026-10-05_round5_results_redacted.md` | `8ccf64ed0a901e4ebc731b98fc381d7a53a36501bc7eb77c1b04abde2a22014e` | 2074 |
| 28 | `results/2026-10-06_round6_results_redacted.md` | `9c881080655a9019a84e2351b1e98ad1d651c5a308ff98a9d3ecfb7e7636f67a` | 1374 |
| 29 | `results/2026-10-06_round7_results_recognizer-line-closeout_redacted.md` | `3dbe4328e30fddbc3fe2292feffa520e716d1bfbed4897d6b9f48b8ecdc877ab` | 3403 |
| 30 | `src/blindtest/run_7b_arm.py` | `cb2ed42dee7e6d2f0dee6723c6439fb01ade50ecea9b7886690ce1bd95bebfeb` | 6755 |
| 31 | `src/control/judge_v4.py` | `fe6bdcc92439749196f38719db9809abad94eabbac90f12a3e9980bdaf51eaef` | 32340 |
| 32 | `src/control/request_form.py` | `1c91ba206cc7d2cf0c7cfe171407f9e7f15253534a9cd77872a1aaddf370f0c7` | 10428 |
| 33 | `src/mechanical/clause_v2.py` | `b96461d163eb1700af5db2a3d65885e9869a68ddee7d82e38839c95819b140e8` | 29123 |
| 34 | `src/mechanical/detectors.py` | `0ceb57f7d24ed0530edb2ef30af6936a3f612e7fc52a52dda5d50fe80c476e14` | 29021 |
| 35 | `src/mechanical/lexicon_v2.py` | `2e07b50acee1d74c5a1416bf2652927f29edcb15d7e0e119d5a3ff3b2f3aaa28` | 34874 |
| 36 | `src/mechanical/pipeline_v2.py` | `092c1c715ad454d4c43fdb924c7e3a970962234d44855f15c898543a2e8bf5ee` | 8497 |
| 37 | `src/mechanical/reorder_v2.py` | `d1c022bee13ee2c02eae98d25c91bc140a445aca7f5bb36d2393403242c43675` | 10561 |
| 38 | `src/mechanical/rules_v2.py` | `1e3fc5e9ec09c15fa5a6d5ab934f3fd9e89709fd76894997100769ca98cbcd5e` | 11450 |
| 39 | `src/mechanical/signed_tables/function_layer.json` | `dd4a3d4a2557d205c460166c2be14fe8286d8b48b563809b43f1a76066b75f1a` | 1876 |
| 40 | `src/mechanical/signed_tables/knife2_one_classifier.json` | `b106667fd4350cbea24be094ff92f02bb21afca41627434c28aa30934e4f751d` | 2409 |
| 41 | `src/mechanical/signed_tables/lexicon_registry.json` | `52586129f1461d6b88fb35eca98394e47fbc75f1f6271a55353fac456a23025d` | 1891 |
| 42 | `src/perf/early_stop.py` | `3e60d5a62f3ff9fcdd197a3f831b35488954164ff988c536d5fdd227dad99aab` | 3451 |
| 43 | `src/perf/run_perf.py` | `60c211e02ccd5c397bb5192fc1e348db77a6f7867cb8f3f233aef10413e8024e` | 28860 |
| 44 | `src/perf/schema_v1.py` | `3118b84b017ffd7eab9308b46de5097528109bdf3db7bb78caf6a4269cd0ca4d` | 5401 |
| 45 | `src/tools/split_sentences.py` | `34bfcbf9d1c82cfeddd6508d8140f349dc5fcad9cae3491697b2256cd3fd554a` | 16616 |

| 項 | 值 |
| --- | --- |
| 涵蓋檔數 | **45** |
| 其中 `papers/`（Zenodo 存放） | 5 |
| 其中檔名改過（2026-10-08 ASCII 改名） | 9 |
| 本表未涵蓋（本表自己） | 2 |
| 本倉檔數合計 | 47 |

### 自行核驗

```bash
find . -type f -not -path './.git/*' -not -path './manifest/public_manifest.*' -print0 \
  | xargs -0 -I{} sh -c 'printf "%s  " "{}"; tr -d "\r" < "{}" | sha256sum | cut -d" " -f1'
```
