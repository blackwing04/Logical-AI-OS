# Phase II results — summary tables

Generated from the four CSV files in this directory; see [`README.md`](README.md) for metric definitions and caveats.

## M1

Scorer: reviewer gold (separate LLM session, blind to rules; not human labelling). Metric: usable (reviewer gold, 0/1 per answer).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | Qwen2.5-3B-Instruct | bare | - | usable (reviewer gold, 0/1 per answer) | 97 | 115 | 84.3 | official |
| A0 | Qwen2.5-7B-Instruct | bare | - | usable (reviewer gold, 0/1 per answer) | 111 | 115 | 96.5 | official |

## M2

Scorer: reviewer gold (separate LLM session, blind to rules; not human labelling). Metric: usable (reviewer gold, 0/1 per answer).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare (max_new 2048) | - | usable (reviewer gold, 0/1 per answer) | 95 | 122 | 77.9 | official |
| B1 | 3B | +architecture | v1.1 | usable (reviewer gold, 0/1 per answer) | 88 | 122 | 72.1 | official |
| B1 | 3B | +architecture | v1.2 | usable (reviewer gold, 0/1 per answer) | 97 | 122 | 79.5 | development (same paper, second pass) |
| A0 | 7B | bare (max_new 2048) | - | usable (reviewer gold, 0/1 per answer) | 111 | 122 | 91.0 | official |

## M3

Scorer: reviewer gold (separate LLM session, blind to rules; not human labelling). Metric: usable (reviewer gold, 0/1 per answer).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare | - | usable (reviewer gold, 0/1 per answer) | 110 | 116 | 94.8 | official |
| B1 | 3B | +architecture | v1.3 | usable (reviewer gold, 0/1 per answer) | 110 | 116 | 94.8 | official |
| A0 | 7B | bare | - | usable (reviewer gold, 0/1 per answer) | 112 | 116 | 96.6 | official |

## S1

Scorer: independent checker grade_s1.py (chat-end; not the architecture's rules). Metric: all constraints kept (per article).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare | - | all constraints kept (per article) | 54 | 117 | 46.2 | official |
| B1 | 3B | +architecture | v1.3 | all constraints kept (per article) | 60 | 117 | 51.3 | official |
| B2 | 3B | +architecture | v1.4 (candidate) | all constraints kept (per article) | 57 | 117 | 48.7 | candidate arm |
| B3 | 3B | +architecture | v1.5 (candidate) | all constraints kept (per article) | 58 | 117 | 49.6 | candidate arm |
| A0 | 7B | bare | - | all constraints kept (per article) | 55 | 117 | 47.0 | official |
| A1 | 7B | +architecture | v1.3 | all constraints kept (per article) | 54 | 117 | 46.2 | official |
| A2 | 7B | +architecture | v1.4 (candidate) | all constraints kept (per article) | 55 | 117 | 47.0 | candidate arm |

## S2

Scorer: independent checker grade_s2.py (chat-end; not the architecture's rules). Metric: all constraints kept (per article).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare | - | all constraints kept (per article) | 47 | 117 | 40.2 | official |
| B1 | 3B | +architecture | v1.6 | all constraints kept (per article) | 49 | 117 | 41.9 | official |
| B1 | 3B | +architecture | v1.7 | all constraints kept (per article) | 55 | 117 | 47.0 | development (same paper, second pass) |
| B_oracle | 3B | v1.6 retry flow, gold constraints fed directly, no generation-time intervention | oracle | all constraints kept (per article) | 60 | 117 | 51.3 | ceiling of the v1.6 flow (development) |
| A0 | 7B | bare | - | all constraints kept (per article) | 57 | 117 | 48.7 | official |
| A1' | 7B | +architecture (retry arm) | v1.6 | all constraints kept (per article) | 56 | 117 | 47.9 | official |

## S3

Scorer: independent checker grade_s3.py (chat-end; not the architecture's rules). Metric: all constraints kept (per article).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare | - | all constraints kept (per article) | 46 | 117 | 39.3 | official |
| B1 | 3B | +architecture | v1.8 | all constraints kept (per article) | 63 | 117 | 53.8 | official |
| B2 | 3B | +architecture without the generation-time intervention | v1.7 | all constraints kept (per article) | 57 | 117 | 48.7 | official (ablation arm) |
| A0 | 7B | bare | - | all constraints kept (per article) | 60 | 117 | 51.3 | official |
| A1 | 7B | +architecture | v1.8 | all constraints kept (per article) | 80 | 117 | 68.4 | official |

## Multi-IF zh (turn 1)

Scorer: official Multi-IF checker (facebookresearch/Multi-IF@1cdb53e, metrics.gen_acc_strict, unmodified). Metric: all instructions pass, strict (per question).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare | - | all instructions pass, strict (per question) | 262 | 454 | 57.7 | official (blind) |
| B1 | 3B | +architecture | v1.9 | all instructions pass, strict (per question) | 254 | 454 | 55.9 | official (blind) |
| A0 | 7B | bare | - | all instructions pass, strict (per question) | 295 | 454 | 65.0 | official (blind) |
| A1 | 7B | +architecture | v1.9 | all instructions pass, strict (per question) | 289 | 454 | 63.7 | official (blind) |

## ComplexBench rule-only subset

Scorer: official ComplexBench con_rule.py (unmodified); evaluated object = whole response (official GPT-4 object extraction not run).

| Arm | Model | System | Rules | Metric | Passed | Total | % | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B0 | 3B | bare | - | rule passes (252 rules) | 144 | 252 | 57.1 | official (blind) |
| B0 | 3B | bare | - | all rules pass (per question) | 109 | 209 | 52.2 | official (blind) |
| B0 | 3B | bare | - | rule passes, mappable subset (208 rules) | 124 | 208 | 59.6 | official (blind) |
| B0 | 3B | bare | - | all mappable rules pass (per question) | 106 | 188 | 56.4 | official (blind) |
| B1 | 3B | +architecture | v1.11 | rule passes (252 rules) | 152 | 252 | 60.3 | official (blind) |
| B1 | 3B | +architecture | v1.11 | all rules pass (per question) | 121 | 209 | 57.9 | official (blind) |
| B1 | 3B | +architecture | v1.11 | rule passes, mappable subset (208 rules) | 136 | 208 | 65.4 | official (blind) |
| B1 | 3B | +architecture | v1.11 | all mappable rules pass (per question) | 120 | 188 | 63.8 | official (blind) |
| A0 | 7B | bare | - | rule passes (252 rules) | 161 | 252 | 63.9 | official (blind) |
| A0 | 7B | bare | - | all rules pass (per question) | 123 | 209 | 58.9 | official (blind) |
| A0 | 7B | bare | - | rule passes, mappable subset (208 rules) | 133 | 208 | 63.9 | official (blind) |
| A0 | 7B | bare | - | all mappable rules pass (per question) | 114 | 188 | 60.6 | official (blind) |
| A1 | 7B | +architecture | v1.11 | rule passes (252 rules) | 174 | 252 | 69.0 | official (blind) |
| A1 | 7B | +architecture | v1.11 | all rules pass (per question) | 138 | 209 | 66.0 | official (blind) |
| A1 | 7B | +architecture | v1.11 | rule passes, mappable subset (208 rules) | 150 | 208 | 72.1 | official (blind) |
| A1 | 7B | +architecture | v1.11 | all mappable rules pass (per question) | 133 | 188 | 70.7 | official (blind) |

## Improved / worsened against the bare arm

| Paper | Arm | Baseline | Unit | Improved | Worsened | Violations fixed | Violations broken | Note |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| M2 | B1 v1.1 | B0 | usable answers |  |  |  |  | net -7 (8 wrong ASKs; 4 retries no gain) |
| M2 | B1 v1.2 | B0 | usable answers | 4 | 2 |  |  | net +2; ASK net contribution -2 |
| M3 | B1 v1.3 | B0 | usable answers | 1 | 1 |  |  | net 0; 11 triggers, 5 genuine / 6 spurious |
| S1 | B1 v1.3 | B0 | articles (fewer / more violated constraints) | 16 | 9 | 16 | 10 |  |
| S1 | A1 v1.3 | A0 | articles (fewer / more violated constraints) | 12 | 15 | 12 | 16 | net +4 violations on 7B |
| S2 | B1 v1.6 | B0 | articles (fewer / more violated constraints) | 7 | 7 | 11 | 13 |  |
| S2 | B1 v1.7 | B0 | articles (fewer / more violated constraints) | 14 | 8 | 22 | 17 | development |
| S2 | B_oracle | B0 | articles (fewer / more violated constraints) | 22 | 2 | 26 | 5 | ceiling of v1.6 flow |
| S2 | A1' v1.6 | A0 | articles (fewer / more violated constraints) | 10 | 9 | 11 | 12 |  |
| S3 | B1 v1.8 | B0 | articles (fewer / more violated constraints) | 29 | 9 | 38 | 17 |  |
| S3 | B2 v1.7 | B0 | articles (fewer / more violated constraints) | 20 | 6 | 26 | 11 |  |
| S3 | A1 v1.8 | A0 | articles (fewer / more violated constraints) | 26 | 7 | 33 | 13 |  |
| Multi-IF zh | B1 v1.9 | B0 | questions (all-pass flips) | 5 | 13 | 9 | 17 | violations columns = instruction-level fixes / breaks |
| ComplexBench rule-only subset | B1 v1.11 | B0 | questions (all-pass flips) | 26 | 14 | 30 | 22 | violations columns = rule-level fixes / breaks |
| Multi-IF zh | A1 v1.9 | A0 | questions (all-pass flips) | 5 | 11 | 10 | 12 | violations columns = instruction-level fixes / breaks |
| ComplexBench rule-only subset | A1 v1.11 | A0 | questions (all-pass flips) | 22 | 7 | 27 | 14 | violations columns = rule-level fixes / breaks |

## Triggers and reading coverage

| Paper | Arm | Rules | Quantity | Num | Den | % | Note |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| M3 | B1 | v1.3 | retry triggered (articles) | 11 | 116 | 9.5 | 5 genuine / 6 spurious |
| S1 | B1 | v1.3 | retry triggered (articles) | 48 | 117 | 41.0 |  |
| S1 | B1 | v1.3 | trap sentences that triggered a retry | 9 | 18 | 50.0 |  |
| S1 | A1 | v1.3 | retry triggered (articles) | 43 | 117 | 36.8 |  |
| S2 | B1 | v1.6 | retry triggered (articles, incl. 3 sentinels) | 43 | 120 | 35.8 |  |
| S2 | B1 | v1.6 | trap sentences that triggered a retry | 10 | 22 | 45.5 |  |
| S2 | A1' | v1.6 | retry triggered (articles, incl. 3 sentinels) | 41 | 120 | 34.2 |  |
| S2 | - | v1.6 | extraction recall, type only (no parameter check) |  |  |  | 35.0% |
| S2 | - | v1.7 | extraction recall, type only (no parameter check) | 258 | 311 | 83.0 |  |
| S3 | B1 | v1.8 | retry triggered (articles, incl. 3 sentinels) | 74 | 120 | 61.7 |  |
| S3 | B2 | v1.7 | retry triggered (articles, incl. 3 sentinels) | 72 | 120 | 60.0 |  |
| S3 | A1 | v1.8 | retry triggered (articles, incl. 3 sentinels) | 64 | 120 | 53.3 |  |
| Multi-IF zh | B1 | v1.9 | retry triggered (questions) | 36 | 454 | 7.9 |  |
| Multi-IF zh | A1 | v1.9 | retry triggered (questions) | 35 | 454 | 7.7 |  |
| Multi-IF zh | - | v1.7 | reading hits, same type only | 59 | 362 | 16.3 | different ruler from rows below |
| Multi-IF zh | - | v1.7 | reading hits, type and parameters match | 34 | 362 | 9.4 |  |
| Multi-IF zh | - | v1.10 | reading hits, type and parameters match | 167 | 362 | 46.1 |  |
| Multi-IF zh | - | v1.11 | reading hits, type and parameters match | 320 | 362 | 88.4 | in-sample: Multi-IF became development material after it was scored |
| Multi-IF zh (colloquial rewrite V2) | - | v1.10 | reading hits, type and parameters match | 155 | 362 | 42.8 | in-sample |
| Multi-IF zh (colloquial rewrite V2) | - | v1.11 | reading hits, type and parameters match | 301 | 362 | 83.1 | in-sample |
| Multi-IF zh | - | v1.10 | reading hallucination rate (unmatched reads / reads) | 41 | 227 | 18.1 |  |
| Multi-IF zh | - | v1.11 | reading hallucination rate (unmatched reads / reads) |  |  |  | 13.0% (51 unmatched) |
| Multi-IF zh (colloquial rewrite V2) | - | v1.11 | reading hallucination rate (unmatched reads / reads) |  |  |  | 14.0% (52 unmatched) |
| ComplexBench rule-only subset | - | v1.10 | reading hits, type and parameters match | 49 | 252 | 19.4 | dry run before the blind shot; denominator includes 43 rules with no matching type |
| ComplexBench rule-only subset | - | v1.11 | reading hits, type and parameters match | 145 | 252 | 57.5 | out-of-sample; same denominator |
| ComplexBench rule-only subset | B1 | v1.11 | retry triggered (questions) | 102 | 209 | 48.8 |  |
| ComplexBench rule-only subset | A1 | v1.11 | retry triggered (questions) | 89 | 209 | 42.6 |  |

Per-type pass rates (S1, S2, S3, Multi-IF instruction ids, ComplexBench rule kinds) are in [`per_type.csv`](per_type.csv).
