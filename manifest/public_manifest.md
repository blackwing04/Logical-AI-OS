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
| 3 | `data/phase2/public_benchmarks/complexbench_rule_answers_3b.jsonl` | `30536c7ca721ab8174a7232b3ff42eccbed764b1bc21b97f17b111cc5181e066` | 658035 |
| 4 | `data/phase2/public_benchmarks/complexbench_rule_answers_7b.jsonl` | `398087f0a5d255289de04fb10deb1a3116ae9acb39263dec5f29a944fa918709` | 699190 |
| 5 | `data/phase2/public_benchmarks/extract_multiif_zh_turn1.py` | `49b45b53200cf0e7af6d34941183c6067725bfc0765807c7b42f0700fc76303b` | 2504 |
| 6 | `data/phase2/public_benchmarks/multiif_zh_answers_3b.jsonl` | `2f2f1948433f79c44339a8d490ac5a2f1ebff502d0effb055b0054f64d548888` | 1100930 |
| 7 | `data/phase2/public_benchmarks/multiif_zh_answers_7b.jsonl` | `92dffc1b177d68b83f905ded547a1894b88f3da69f84df6905d9e2c96ac02f1f` | 1136859 |
| 8 | `data/phase2/README.md` | `2b1b5a74e838b7ed683f4d19cabe130f9af30ef6de1d3d1c279a34fc47743e15` | 6583 |
| 9 | `data/phase2/synthetic/s1_answers_3b.jsonl` | `c4739cd5fbdd35eb4c4e6e47132ff9d24ffd8cb05ed8b5de825c103b449420c7` | 578448 |
| 10 | `data/phase2/synthetic/s1_answers_7b.jsonl` | `9fb1b574aca8255f3a40f678fcc53679edb6397fb47246632ac55574d5917406` | 492567 |
| 11 | `data/phase2/synthetic/s1_items.jsonl` | `10e14b6ddf40a8895ce6dc4f8319e670118ee3476ef56c29bb36f7260d81fd35` | 135672 |
| 12 | `data/phase2/synthetic/s2_answers_3b.jsonl` | `53402d58839759e2f7e5e92ac7ff929ac698c64cc281061304b02d0550c918cd` | 655313 |
| 13 | `data/phase2/synthetic/s2_answers_7b.jsonl` | `bfc20b2bbbe528491ff4d8e536728205090b8675d9e2a558770c14f8d4f5ce38` | 496278 |
| 14 | `data/phase2/synthetic/s2_items.jsonl` | `9ef869134b22fef31b78b067b1bdd0a5d51dc6ab2d2bfabd7deffabb01314f51` | 143728 |
| 15 | `data/phase2/synthetic/s3_answers_3b.jsonl` | `9c7db089bd85bed0da24b8dd02dd3e4b910e157be19cd62a6a8db3b4797fdba7` | 473455 |
| 16 | `data/phase2/synthetic/s3_answers_7b.jsonl` | `04aaa7fb358616a7871a9f08a296e32f952a8c21ded5ae2792fdf44f5a65670f` | 339549 |
| 17 | `data/phase2/synthetic/s3_items.jsonl` | `a02e5364482725bbe65e9a3a8e005f4ac03eb74ab1ad4eee70ecdf99b1a3f364` | 130371 |
| 18 | `docs/failure_taxonomy.md` | `6131a2124c4dd30a6d1e16f2fa0705ec9daefac0291a01442cdf45012254ee54` | 6993 |
| 19 | `docs/literature_mapping.md` | `b17d2031a707e80e7aaecfa6e898ca95fc070537f3e9549d8cbf68b1cf5c260e` | 29250 |
| 20 | `docs/method/2026-07-22_adjacent-literature-lines.md` | `a50cc3b2fc841024af15cbde83716f12e44f8a55fd9f60de2bbb1bbc896a62e6` | 3692 |
| 21 | `docs/method/2026-07-29_framework_gps-analogy.md` | `82c47e4d0d68593796447ff0570d5d79ba5c8c04d564b8b0df56788d7271886c` | 3800 |
| 22 | `docs/method/2026-07-29_methodology-defense_model-labeling.md` | `a4f995913af6b0afd3a76fc55cf2ee93f0eeda110799b794270ae43bab782ee6` | 6598 |
| 23 | `docs/parts_spec_v2.md` | `6185ca88b37cfab26246a8205644f6e7600b686e969ba19fac074f732f02ab90` | 7237 |
| 24 | `docs/PORTING.md` | `f643802167fb861a0d76fd91a3442e371b2243b3c17a408b45ee5c239f6a22af` | 12480 |
| 25 | `docs/PORTING.zh-TW.md` | `db1ac30895679606187cc7ddd0200361e2458d2a06ba1faef69227dbe9bc21e2` | 10475 |
| 26 | `docs/protocol/blind-test-protocol.md` | `9c63c7b94185764a0906749d96f996451bbc8d4a89acb36ef40e2ffdec4270bb` | 7105 |
| 27 | `docs/protocol/phase2/evaluation_protocol_phase2.md` | `51e4c5dec651845030158f99aff68c6490b732b485bcc6bd2f3a41a70d5206eb` | 9517 |
| 28 | `docs/theory/behavioral-confabulation_mechanism-and-literature.md` | `35677340fca14043f5567bf2801d09591be018c0d3bcfce8a1b468d8766f56ef` | 4187 |
| 29 | `docs/theory/runaway-mechanism_theory-and-literature.md` | `0d5ba4399f925427fbdcd25887e7f1908d9bd35efe55ebbf0079e50b2f4f83e0` | 3723 |
| 30 | `eval/complexbench/extract_rule_subset.py` | `5a51ff639503bb7dd6854768df71445bb0aac4de3917584ebf733d06f7143636` | 1995 |
| 31 | `eval/complexbench/obs_coverage.py` | `66d6cbef3218a42a9e403d0c69659cc62f156d4a38573e613cd6c1e97ce1b805` | 4479 |
| 32 | `eval/complexbench/rule_mapping.py` | `abb93674f095793786071bd6d8ceb4360bb3563508b8475f9abb4168dfc0f3e1` | 4889 |
| 33 | `eval/complexbench/score_complexbench.py` | `eae331e32a57e646e89711c84381e1106e69c340fef91dced13062ecabae828f` | 4453 |
| 34 | `eval/multi_if/score_multi_if.py` | `ee65442980482c48b1c7a1611897696bf389ece46fd53eca07c5aeee8e8abc92` | 4221 |
| 35 | `eval/README.md` | `42269932a6de1974642f6edf90fba743ba5117b4675d7b77ad01aed365686afb` | 4435 |
| 36 | `eval/synthetic/grade_s1.py` | `bdbd9e9377d3682e773d84df37c2bb87d3f9618915a6acaeecc609c9f75ebd36` | 5190 |
| 37 | `eval/synthetic/grade_s2.py` | `a4edaad80f034f95ad17c8e6e0c1f4403c799185dd53577a69653d82225e828a` | 5162 |
| 38 | `eval/synthetic/grade_s3.py` | `5603f0ed9dd24113e7af934871f39feadab452f62511e496a2b0f3468a40bc18` | 5150 |
| 39 | `LICENSE` | `6ac9e44619713aa8dd4c4e57362e7a2b5911db90d60148f324bdb2d670be8871` | 1083 |
| 40 | `LICENSE-docs` | `1ec1b3d515d885939000ca28250c4887bfa0ccad571860cb1cfb775d8c34405c` | 1883 |
| 41 | `manifest/v45_manifest.json` | `ab05661190ff303fe63ead8f545469111d18fb5a34f450d2976d5655977e7958` | 10167 |
| 42 | `manifest/v45_manifest.md` | `40d3b839efbaa000c32945175ec83ebd9990619ec12bd2879aad92ab3bb485de` | 4863 |
| 43 | `manifest/v45_manifest.py` | `c87a5cb7e9ef7bc8f6707032d0304fd2c458f9556915a29c1ce20c729ff82cee` | 8514 |
| 44 | `MANIFEST.md` | `7b1b7b3ba8ff95179b529fbfe237972453904973ec6ab2947ccdb82910f1b124` | 20952 |
| 45 | `MANIFEST_phase2.md` | `86647396e5672c48659dfcbc8774da20d6ec2d2428092906d67dab8494f7d70a` | 19017 |
| 46 | `MANIFEST_phase2_repro.md` | `07bb80770b94b158fea457e3b52603aa5b46f6f77d9d0fb3d9a31ba4f94da88b` | 11424 |
| 47 | `papers/zenodo_v1.2/abstract_zh.md` | `c2437b0bca2ead34d4ebd513c9f06867c0bd06df5ba88387ae036ce3b0dc4e72` | 5099 |
| 48 | `papers/zenodo_v1.2/CHECKSUMS.md` | `8ca9fef569d6cfd92fe72b360f524f4fd0ce2a60262b53dd2a7fe2e5d53c8ee7` | 2024 |
| 49 | `papers/zenodo_v1.2/references.bib` | `dddc3cc61d226fcf3dd3914b8643dca39419f209a2e5a721083c6b3043a7de9d` | 22360 |
| 50 | `papers/zenodo_v1.2/report_v1.2.md` | `f84ba956e7d4535f1a648df01c5d32587ec1dae63ffe925fc527a1ed17c099c2` | 41012 |
| 51 | `papers/zenodo_v1.2/report_v1.2.pdf` | `b99dbe7b0eb815c59c2b80ef8649623cb54e782d251f38e7e42359bb03cc15eb` | 310044 |
| 52 | `PUBLIC_NOTES.md` | `06453a18340698ca387a842677834b02cdce8db463bd18d7573496ff8497db9f` | 19048 |
| 53 | `PUBLIC_NOTES.zh-TW.md` | `7962eae786a4c2b04372be2a6bc2bffe791664562f9ffb05f43fd39109173570` | 16167 |
| 54 | `QUICKSTART.md` | `164ab87572473b4a6f97a4fc405635271d660479f90155adaaefcd55ddc6e08d` | 16418 |
| 55 | `QUICKSTART.zh-TW.md` | `10f830e79f9ed7718993a8d81c4685dad67d290086e384707382816b15427af9` | 15539 |
| 56 | `README.md` | `ddddbe515240ac8e8c35e741ca936335b02a97827eb96bfb5b3a1c25c1fc9883` | 16166 |
| 57 | `README.zh-TW.md` | `e3b7c561b02246b1551c75aedb9257dad841457a428ab8b8f2d8b4757a064ec9` | 13442 |
| 58 | `requirements.txt` | `e02eb936d43da2cfef54e65cfd86b5bfff7bec802e42e6aa1e3a0ca3783a6d21` | 465 |
| 59 | `results/2026-10-05_round5_results_redacted.md` | `8ccf64ed0a901e4ebc731b98fc381d7a53a36501bc7eb77c1b04abde2a22014e` | 2074 |
| 60 | `results/2026-10-06_round6_results_redacted.md` | `9c881080655a9019a84e2351b1e98ad1d651c5a308ff98a9d3ecfb7e7636f67a` | 1374 |
| 61 | `results/2026-10-06_round7_results_recognizer-line-closeout_redacted.md` | `3dbe4328e30fddbc3fe2292feffa520e716d1bfbed4897d6b9f48b8ecdc877ab` | 3403 |
| 62 | `results/phase2/deltas.csv` | `efc7ee6e24ff3690c8fe8d3f5ad972de97c97ffbbf996561f1cb44fddc706b0a` | 1481 |
| 63 | `results/phase2/headline.csv` | `aacdc492fb7d38851fe6c3039ac6fb3db8e66eec14f6438270ab0848b715cf6d` | 9292 |
| 64 | `results/phase2/per_item/complexbench_rule_items.csv` | `fa71da7e24452d5efac430910212670529a54133b5695d84d7b899f646f8e2e7` | 81931 |
| 65 | `results/phase2/per_item/multiif_zh_items.csv` | `2a8c901c5b58ec079895f0897ac4c384dcbf0884eedbec074806d6cb072b5e79` | 232553 |
| 66 | `results/phase2/per_item/reading_variants.csv` | `fe741b9c02a9bdda35babc65af98a824c2f416792a7738d24bced3f97f8683c1` | 10963 |
| 67 | `results/phase2/per_item/s1_items.csv` | `304768f95a1bf47cebed69721037abeb073b93fdfa390be88946e86e95892093` | 148811 |
| 68 | `results/phase2/per_item/s2_items.csv` | `bfc9ab4dd11458d5151a71e37c9d71dd8b5e6849666ac4d4073f57467da107bf` | 198135 |
| 69 | `results/phase2/per_item/s3_items.csv` | `a62dc58cf843b2ef7e784648bc387c3b9709f4b7a8c01a4eeb661d786e7daf46` | 120916 |
| 70 | `results/phase2/per_item/stats_paired.csv` | `c395b5b02c21719d6bf92b59bcbc1ff3b7725eb5e80f0fa88605464a801b07ed` | 2139 |
| 71 | `results/phase2/per_item/stats_paired.py` | `801a478d010e45f1ca84ae5161cc0bb34cd1796ce9a908e4a54e5cf08972c22e` | 6455 |
| 72 | `results/phase2/per_type.csv` | `aa8d4b140457201664846b0a5dcb455908d5d88afd45e7cc16fd433db9a4d9a0` | 8640 |
| 73 | `results/phase2/README.md` | `c6bcf961205f8dbfac10e217e97fa368e5b16f2883d2c79a8958a80f06112d5a` | 11845 |
| 74 | `results/phase2/summary.md` | `1cd8d351d8157d9d0a0bd403a479957b98f6fafc1606cfead8676b1b71706cfe` | 12405 |
| 75 | `results/phase2/triggers_coverage.csv` | `ace51d821c1c68ca0d4c7b7bc0201b302774b81d9803d02323d18d8172ce3b1e` | 2342 |
| 76 | `src/blindtest/run_7b_arm.py` | `a27ffe4d358afc998f8083d522fadc4c050d6aeeb00fc38da505b456f6c7ce22` | 6969 |
| 77 | `src/control/judge_v4.py` | `313fa817ed30d86a980b02e0c67e812ea5e44563e83c05fe4a1e9d8a35ac1824` | 32989 |
| 78 | `src/control/request_form.py` | `1c91ba206cc7d2cf0c7cfe171407f9e7f15253534a9cd77872a1aaddf370f0c7` | 10428 |
| 79 | `src/mechanical/canon_v3/__init__.py` | `ba4dd92bfadb6ce06937d6b404c62167e9eafef50c19ca790f61bf88ec763cd5` | 378 |
| 80 | `src/mechanical/canon_v3/cue_anchor.py` | `596ef48c6efe47fb5ad48eea720eb4f72465c661279872a47c5f2c6d936a8e71` | 5515 |
| 81 | `src/mechanical/canon_v3/lexicon.py` | `3cf6a06c778c9bdb547ee8b8b46ac314af27ce5674d39c79167d558101f3c6aa` | 10324 |
| 82 | `src/mechanical/canon_v3/prompts.py` | `c188840ac005c206b82d79feba0f56941ec1075df41f9c6fc10fce3e91c7e324` | 2320 |
| 83 | `src/mechanical/canon_v3/quantity.py` | `bcda7b3cd11cb0e2dde4f2f81cfe5394ea88f41f1802501ed1fb3e74c1ca85d2` | 8504 |
| 84 | `src/mechanical/classifier.py` | `ba88a7a4845d3b23c3b0efdef2b0aebada7954c58d943f02e944867b02f6807b` | 2098 |
| 85 | `src/mechanical/clause_v2.py` | `b08c407d328cd96aef2bb01f9587a7787265742f2c3e8c138d5ca3567365edaf` | 29200 |
| 86 | `src/mechanical/detectors.py` | `e88e23d5c3519b9815e2ef4151ab7e27ed01d34f13256789c8aaa310f2349ee4` | 29089 |
| 87 | `src/mechanical/lexicon_v2.py` | `2e07b50acee1d74c5a1416bf2652927f29edcb15d7e0e119d5a3ff3b2f3aaa28` | 34874 |
| 88 | `src/mechanical/pipeline_v2.py` | `a13abcd840354597ddda9c957d78f7ccd85e8053fa66bf827b1624fa77dd9b84` | 8574 |
| 89 | `src/mechanical/reorder_v2.py` | `06a2f42a7b3cdb15e949f254d2231cb843966a15d98f207da94d73589628fa0e` | 10638 |
| 90 | `src/mechanical/rules_v2.py` | `1e3fc5e9ec09c15fa5a6d5ab934f3fd9e89709fd76894997100769ca98cbcd5e` | 11450 |
| 91 | `src/mechanical/signed_tables/function_layer.json` | `dd4a3d4a2557d205c460166c2be14fe8286d8b48b563809b43f1a76066b75f1a` | 1876 |
| 92 | `src/mechanical/signed_tables/knife2_one_classifier.json` | `b106667fd4350cbea24be094ff92f02bb21afca41627434c28aa30934e4f751d` | 2409 |
| 93 | `src/mechanical/signed_tables/lexicon_registry.json` | `52586129f1461d6b88fb35eca98394e47fbc75f1f6271a55353fac456a23025d` | 1891 |
| 94 | `src/perf/early_stop.py` | `3e60d5a62f3ff9fcdd197a3f831b35488954164ff988c536d5fdd227dad99aab` | 3451 |
| 95 | `src/perf/run_perf.py` | `1e4113c9b37dc3e72ab12f0c80cf183029a7d5e2b62f401d4c3d627fa5c4e7e1` | 29075 |
| 96 | `src/perf/schema_v1.py` | `3118b84b017ffd7eab9308b46de5097528109bdf3db7bb78caf6a4269cd0ca4d` | 5401 |
| 97 | `src/run_recognizer.py` | `b10abb21967432750c0a0deeae5ccbe56745f7bc977933541395af7313470743` | 2440 |
| 98 | `src/tools/split_sentences.py` | `a5376fc5aba427d999ce9188f8bac9af7be84ec8d5a83f366c8b09cf12f0d12b` | 16685 |

| 項 | 值 |
| --- | --- |
| 涵蓋檔數 | **98** |
| 其中 `papers/`（Zenodo 存放） | 5 |
| 其中檔名改過（2026-10-08 ASCII 改名） | 9 |
| 本表未涵蓋（本表自己） | 2 |
| 本倉檔數合計 | 100 |

### 自行核驗

```bash
find . -type f -not -path './.git/*' -not -path './manifest/public_manifest.*' -print0 \
  | xargs -0 -I{} sh -c 'printf "%s  " "{}"; tr -d "\r" < "{}" | sha256sum | cut -d" " -f1'
```
