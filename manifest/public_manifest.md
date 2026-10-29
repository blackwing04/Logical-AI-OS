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
| 3 | `docs/failure_taxonomy.md` | `6131a2124c4dd30a6d1e16f2fa0705ec9daefac0291a01442cdf45012254ee54` | 6993 |
| 4 | `docs/literature_mapping.md` | `b17d2031a707e80e7aaecfa6e898ca95fc070537f3e9549d8cbf68b1cf5c260e` | 29250 |
| 5 | `docs/method/2026-07-22_adjacent-literature-lines.md` | `a50cc3b2fc841024af15cbde83716f12e44f8a55fd9f60de2bbb1bbc896a62e6` | 3692 |
| 6 | `docs/method/2026-07-29_framework_gps-analogy.md` | `82c47e4d0d68593796447ff0570d5d79ba5c8c04d564b8b0df56788d7271886c` | 3800 |
| 7 | `docs/method/2026-07-29_methodology-defense_model-labeling.md` | `a4f995913af6b0afd3a76fc55cf2ee93f0eeda110799b794270ae43bab782ee6` | 6598 |
| 8 | `docs/parts_spec_v2.md` | `8e0ac58c10644c3bc6d9142c8c6f923480c39e4f9554b58cdfe83e850e3ea38b` | 6380 |
| 9 | `docs/PORTING.md` | `f643802167fb861a0d76fd91a3442e371b2243b3c17a408b45ee5c239f6a22af` | 12480 |
| 10 | `docs/PORTING.zh-TW.md` | `db1ac30895679606187cc7ddd0200361e2458d2a06ba1faef69227dbe9bc21e2` | 10475 |
| 11 | `docs/protocol/blind-test-protocol.md` | `9c63c7b94185764a0906749d96f996451bbc8d4a89acb36ef40e2ffdec4270bb` | 7105 |
| 12 | `docs/protocol/phase2/evaluation_protocol_phase2.md` | `51e4c5dec651845030158f99aff68c6490b732b485bcc6bd2f3a41a70d5206eb` | 9517 |
| 13 | `docs/theory/behavioral-confabulation_mechanism-and-literature.md` | `35677340fca14043f5567bf2801d09591be018c0d3bcfce8a1b468d8766f56ef` | 4187 |
| 14 | `docs/theory/runaway-mechanism_theory-and-literature.md` | `0d5ba4399f925427fbdcd25887e7f1908d9bd35efe55ebbf0079e50b2f4f83e0` | 3723 |
| 15 | `eval/complexbench/extract_rule_subset.py` | `5a51ff639503bb7dd6854768df71445bb0aac4de3917584ebf733d06f7143636` | 1995 |
| 16 | `eval/complexbench/obs_coverage.py` | `66d6cbef3218a42a9e403d0c69659cc62f156d4a38573e613cd6c1e97ce1b805` | 4479 |
| 17 | `eval/complexbench/rule_mapping.py` | `abb93674f095793786071bd6d8ceb4360bb3563508b8475f9abb4168dfc0f3e1` | 4889 |
| 18 | `eval/complexbench/score_complexbench.py` | `eae331e32a57e646e89711c84381e1106e69c340fef91dced13062ecabae828f` | 4453 |
| 19 | `eval/multi_if/score_multi_if.py` | `ee65442980482c48b1c7a1611897696bf389ece46fd53eca07c5aeee8e8abc92` | 4221 |
| 20 | `eval/README.md` | `69c1d0bb29e3f7df3089ace6fa05d3f7875b6c81ae5817cc3fce7363da0f1d7b` | 4112 |
| 21 | `eval/synthetic/grade_s1.py` | `bdbd9e9377d3682e773d84df37c2bb87d3f9618915a6acaeecc609c9f75ebd36` | 5190 |
| 22 | `eval/synthetic/grade_s2.py` | `a4edaad80f034f95ad17c8e6e0c1f4403c799185dd53577a69653d82225e828a` | 5162 |
| 23 | `eval/synthetic/grade_s3.py` | `5603f0ed9dd24113e7af934871f39feadab452f62511e496a2b0f3468a40bc18` | 5150 |
| 24 | `LICENSE` | `6ac9e44619713aa8dd4c4e57362e7a2b5911db90d60148f324bdb2d670be8871` | 1083 |
| 25 | `LICENSE-docs` | `1ec1b3d515d885939000ca28250c4887bfa0ccad571860cb1cfb775d8c34405c` | 1883 |
| 26 | `manifest/v45_manifest.json` | `ab05661190ff303fe63ead8f545469111d18fb5a34f450d2976d5655977e7958` | 10167 |
| 27 | `manifest/v45_manifest.md` | `40d3b839efbaa000c32945175ec83ebd9990619ec12bd2879aad92ab3bb485de` | 4863 |
| 28 | `manifest/v45_manifest.py` | `c87a5cb7e9ef7bc8f6707032d0304fd2c458f9556915a29c1ce20c729ff82cee` | 8514 |
| 29 | `MANIFEST.md` | `7b1b7b3ba8ff95179b529fbfe237972453904973ec6ab2947ccdb82910f1b124` | 20952 |
| 30 | `MANIFEST_phase2.md` | `86647396e5672c48659dfcbc8774da20d6ec2d2428092906d67dab8494f7d70a` | 19017 |
| 31 | `papers/zenodo_v1.2/abstract_zh.md` | `c2437b0bca2ead34d4ebd513c9f06867c0bd06df5ba88387ae036ce3b0dc4e72` | 5099 |
| 32 | `papers/zenodo_v1.2/CHECKSUMS.md` | `8ca9fef569d6cfd92fe72b360f524f4fd0ce2a60262b53dd2a7fe2e5d53c8ee7` | 2024 |
| 33 | `papers/zenodo_v1.2/references.bib` | `dddc3cc61d226fcf3dd3914b8643dca39419f209a2e5a721083c6b3043a7de9d` | 22360 |
| 34 | `papers/zenodo_v1.2/report_v1.2.md` | `f84ba956e7d4535f1a648df01c5d32587ec1dae63ffe925fc527a1ed17c099c2` | 41012 |
| 35 | `papers/zenodo_v1.2/report_v1.2.pdf` | `b99dbe7b0eb815c59c2b80ef8649623cb54e782d251f38e7e42359bb03cc15eb` | 310044 |
| 36 | `PUBLIC_NOTES.md` | `703bd8d675bd524114426336dddcc25230f899f07d874506bbb2181a44194dd7` | 8574 |
| 37 | `PUBLIC_NOTES.zh-TW.md` | `bbdae2a0ee3a73f4ce276cbbf5cc4c436042dbf7108720fe88242e9cfce52788` | 6774 |
| 38 | `README.md` | `0e1d416398a8637c166559802e3fae6c709a53e5ad3b2a52465e1ae3f0569e57` | 14545 |
| 39 | `README.zh-TW.md` | `e0f2f9dc716a574b561aed6211c1d63f97413d17a516ba3a03e682ba899c0549` | 12048 |
| 40 | `results/2026-10-05_round5_results_redacted.md` | `8ccf64ed0a901e4ebc731b98fc381d7a53a36501bc7eb77c1b04abde2a22014e` | 2074 |
| 41 | `results/2026-10-06_round6_results_redacted.md` | `9c881080655a9019a84e2351b1e98ad1d651c5a308ff98a9d3ecfb7e7636f67a` | 1374 |
| 42 | `results/2026-10-06_round7_results_recognizer-line-closeout_redacted.md` | `3dbe4328e30fddbc3fe2292feffa520e716d1bfbed4897d6b9f48b8ecdc877ab` | 3403 |
| 43 | `results/phase2/deltas.csv` | `efc7ee6e24ff3690c8fe8d3f5ad972de97c97ffbbf996561f1cb44fddc706b0a` | 1481 |
| 44 | `results/phase2/headline.csv` | `aacdc492fb7d38851fe6c3039ac6fb3db8e66eec14f6438270ab0848b715cf6d` | 9292 |
| 45 | `results/phase2/per_type.csv` | `0c62ba373849bb36e981a5685e6f340a3ded9e2c58f043505a111d24166c1365` | 8640 |
| 46 | `results/phase2/README.md` | `013cf4b8e62675bbc41633f3d4db1592aad3c76944ee53fd33957081c7ebf465` | 5802 |
| 47 | `results/phase2/summary.md` | `1cd8d351d8157d9d0a0bd403a479957b98f6fafc1606cfead8676b1b71706cfe` | 12405 |
| 48 | `results/phase2/triggers_coverage.csv` | `ace51d821c1c68ca0d4c7b7bc0201b302774b81d9803d02323d18d8172ce3b1e` | 2342 |
| 49 | `src/blindtest/run_7b_arm.py` | `cb2ed42dee7e6d2f0dee6723c6439fb01ade50ecea9b7886690ce1bd95bebfeb` | 6755 |
| 50 | `src/control/judge_v4.py` | `860262e4447a10990ca79d595c605e36c963aeb0f6d8fec322f56c6ba6ee4f45` | 32730 |
| 51 | `src/control/request_form.py` | `1c91ba206cc7d2cf0c7cfe171407f9e7f15253534a9cd77872a1aaddf370f0c7` | 10428 |
| 52 | `src/mechanical/clause_v2.py` | `b96461d163eb1700af5db2a3d65885e9869a68ddee7d82e38839c95819b140e8` | 29123 |
| 53 | `src/mechanical/detectors.py` | `0ceb57f7d24ed0530edb2ef30af6936a3f612e7fc52a52dda5d50fe80c476e14` | 29021 |
| 54 | `src/mechanical/lexicon_v2.py` | `2e07b50acee1d74c5a1416bf2652927f29edcb15d7e0e119d5a3ff3b2f3aaa28` | 34874 |
| 55 | `src/mechanical/pipeline_v2.py` | `092c1c715ad454d4c43fdb924c7e3a970962234d44855f15c898543a2e8bf5ee` | 8497 |
| 56 | `src/mechanical/reorder_v2.py` | `d1c022bee13ee2c02eae98d25c91bc140a445aca7f5bb36d2393403242c43675` | 10561 |
| 57 | `src/mechanical/rules_v2.py` | `1e3fc5e9ec09c15fa5a6d5ab934f3fd9e89709fd76894997100769ca98cbcd5e` | 11450 |
| 58 | `src/mechanical/signed_tables/function_layer.json` | `dd4a3d4a2557d205c460166c2be14fe8286d8b48b563809b43f1a76066b75f1a` | 1876 |
| 59 | `src/mechanical/signed_tables/knife2_one_classifier.json` | `b106667fd4350cbea24be094ff92f02bb21afca41627434c28aa30934e4f751d` | 2409 |
| 60 | `src/mechanical/signed_tables/lexicon_registry.json` | `52586129f1461d6b88fb35eca98394e47fbc75f1f6271a55353fac456a23025d` | 1891 |
| 61 | `src/perf/early_stop.py` | `3e60d5a62f3ff9fcdd197a3f831b35488954164ff988c536d5fdd227dad99aab` | 3451 |
| 62 | `src/perf/run_perf.py` | `60c211e02ccd5c397bb5192fc1e348db77a6f7867cb8f3f233aef10413e8024e` | 28860 |
| 63 | `src/perf/schema_v1.py` | `3118b84b017ffd7eab9308b46de5097528109bdf3db7bb78caf6a4269cd0ca4d` | 5401 |
| 64 | `src/tools/split_sentences.py` | `34bfcbf9d1c82cfeddd6508d8140f349dc5fcad9cae3491697b2256cd3fd554a` | 16616 |

| 項 | 值 |
| --- | --- |
| 涵蓋檔數 | **64** |
| 其中 `papers/`（Zenodo 存放） | 5 |
| 其中檔名改過（2026-10-08 ASCII 改名） | 9 |
| 本表未涵蓋（本表自己） | 2 |
| 本倉檔數合計 | 66 |

### 自行核驗

```bash
find . -type f -not -path './.git/*' -not -path './manifest/public_manifest.*' -print0 \
  | xargs -0 -I{} sh -c 'printf "%s  " "{}"; tr -d "\r" < "{}" | sha256sum | cut -d" " -f1'
```
