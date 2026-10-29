# Parts specification, Phase II (numbers only)

One row per part, giving what it measures, the current number, and the paper and ruler it
was measured on.

- **"Not measured" means not measured.** Nothing is estimated.
- **Implementation stays private.** All action-layer implementation, rule tables and thresholds
  are not published. This table gives behaviour only.

Source: the internal parts table as of the v1.11 freeze (2026-10-29), with pointers to private
files removed. Paper names follow [`../results/phase2/README.md`](../results/phase2/README.md).

## Parts

| Part | What it measures | Number | Paper / ruler |
| --- | --- | --- | --- |
| Reading (extraction) recall, type only | Share of gold constraints for which a constraint of the same type was read (parameters not checked) | **83.0%** (258 / 311) at v1.7; 35.0% at v1.6 | S2, 117 articles; reviewer gold |
| Reading precision, type only | Share of read constraints whose type exists in the gold | **80.6%** (258 / 320; 62 extra reads, mostly relative-length and heading-structure items outside the gold) | Same |
| Reading hits, type **and** parameters | Share of a benchmark's mappable gold instances read with matching type and parameters. **A different ruler from the two rows above; do not compare across.** | Multi-IF (362 instances): v1.7 34 (9.4%) → v1.10 167 (46.1%) → v1.11 **320 (88.4%)**; colloquial rewrite **301 (83.1%)**. **In-sample**: Multi-IF became development material after it was scored. ComplexBench (252 rules): v1.10 49 (19.4%) → v1.11 **145 (57.5%)**, **out-of-sample**; the denominator includes 43 rules with no matching type | Multi-IF; ComplexBench rule-only subset |
| Reading hallucination rate | Share of reads that match no gold instance | Multi-IF original: v1.10 41 / 227 (18.1%) → v1.11 **51 (13.0%)**; colloquial rewrite **52 (14.0%)** | Multi-IF |
| Retry ceiling (oracle) | Gain in all-constraints-kept rate when gold constraints are fed into the retry flow | **+11.1 points** (51.3% vs 40.2%; improved 22 / worsened 2). **Precondition:** the v1.6 flow without the generation-time intervention. The S3 v1.8 architecture later exceeded it (+14.5) | S2 oracle arm; reviewer checker (development, same paper scored twice) |
| Retry, measured gain | All-constraints-kept gain from reading + retry | 3B **+9.4** (v1.7, no generation-time intervention); full v1.8: 3B **+14.5**, 7B **+17.1** | S3, 117 articles; reviewer checker |
| Generation-time intervention (length) | Independent gain of the intervention (v1.8 minus v1.7 without it) | **+5.1 points**; Chinese length items in range after retry 28 / 29 vs 12 / 41 (different denominators; same-denominator 33 / 43 vs 12 / 41) | S3; reviewer checker and architecture-side checker, both shown |
| Retry trigger rate | Share of items where a retry fired | Multi-IF (v1.9): 3B 36 / 454 (8%), 7B 35 / 454 (8%). ComplexBench (v1.11): 3B **102 / 209 (48.8%)**, 7B **89 / 209 (42.6%)** | Architecture-side count |
| External blind gain (v1.11, full) | Bare model vs. the same model plus v1.11, judged by the benchmark's own checker | ComplexBench rule-only subset, 252 rules. Rule passes: 3B 57.1 → 60.3 (**+3.2**), 7B 63.9 → 69.0 (**+5.1**). Question all-pass: 52.2 → 57.9 (+5.7), 58.9 → 66.0 (+7.1). Mappable 208 rules: 59.6 → 65.4, 63.9 → 72.1. Rule-level: fixed 30 / 27, broken 22 / 14 (3 per arm were the retry target itself) | Official `con_rule.py`. **Evaluated object = whole response** (the official GPT-4 object extraction was not run). Fixed seed per item; one sample per arm; no interval |
| Count action, applied everywhere (v1.9b, not adopted) | Count items equal to N | **46 / 46** (3B and 7B), but articles that were already right fell 25 → 14 (3B, 37-article subset) and 28 → 15 (7B); all 46: 12 → 25 → 20 (3B) | S3, 46 articles; architecture-side checker on an already-scored paper (development); not confirmed by gold |
| Count action, conditional (v1.9) | Count action on a subset of articles (the conditions are not published) | Articles acted on that passed count: 3B 10 / 12, 7B 11 / 11. All 46 count articles fully in range: 3B 25 → 29, 7B 28 → 30. All 120 articles: 77 → 81 / 83 → 85 (no drop) | S3; architecture-side checker (development). **On Multi-IF the count action fired on 10 questions, all misreads** (9 "no more than N sentences" read as "at least N items", 1 more misread), so these numbers do not carry over to sentence-limit phrasings |
| Ask (ASK) | Asking when uncertain; asking correctly | **Not measured.** Would-ask is logged, never sent (S2 3B 14 articles; S3 6 per arm). ASK was closed after M2, where it was the only negative component (precision 0 / 8) | S2 / S3 |
| Number-faithfulness detector | Numbers in the answer that are absent from the source, caught | **9 / 10** (denominator: the 10 answers the gold marked as "invented numbers"; against all 23 fabrications in M2: 9, 39%); false positives 8% among usable answers. Not attached after S2 | M2 |
| Self-assessment | The model's calibration signal about its own answer | **0**: no usable part. 3B and 7B each put almost all mass on one side of a binary self-check (AUC 0.60 / 0.66). A mechanical extraction-confidence score reached AUC 0.73 (n = 48) but is not wired into any decision | S1 / S2 |

## Versions

| Rules version | Adds | Frozen | Signed |
| --- | --- | --- | --- |
| v1.3 | Single-constraint reading + retry | 2026-10-17 | PI |
| v1.6 | v1.3 + three fixes to the retry | 2026-10-19 | PI |
| v1.7 | Every constraint in the main request sentence is read (type-only recall 35 → 83%) | 2026-10-19 | Reviewer, PI-authorised |
| v1.8 | v1.7 + generation-time intervention (length) | 2026-10-22 | Reviewer, PI-authorised |
| v1.9 | v1.8 + conditional count action | 2026-10-22 | Reviewer, PI-authorised |
| v1.10 | v1.9 + reading patterns filled in from Multi-IF phrasings (length, sentence count, character classes; sentence-limit direction fixed; letter case) | 2026-10-24 | Reviewer, on PI's order |
| v1.11 | v1.10 + script normalisation before reading (Simplified → Traditional), five more reading types, relaxed position, two mechanical fixes; closing fixes (language needs a request form in the same clause and not a question; colloquial "no commas at all"; retry support for the new types) | 2026-10-29 | Reviewer, PI-authorised; used for the ComplexBench blind shot |
