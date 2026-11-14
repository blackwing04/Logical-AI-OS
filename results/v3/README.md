# v3 results

## `per_item/`

Verdicts for every arm, article and constraint item, computed with the published checker
([`../../eval/v3/checker/`](../../eval/v3/checker/)) on the answers as generated (before the
redactions described in [`../../data/v3/README.md`](../../data/v3/README.md)).

| File | One line per | Fields |
| --- | --- | --- |
| `item_verdicts.csv` | arm × article × item (22,882) | `bank`, `id`, `arm`, `sid`, `check_type`, `v1`, `v2_no_length`, `v2_full` |
| `article_allpass.csv` | arm × article (11,186) | `bank`, `id`, `arm`, `allpass_v1`, `allpass_v2_no_length`, `allpass_v2_full` |
| `allpass_by_arm.csv` | arm (34) | `arm`, `articles`, all-pass counts under each scale |

- Verdicts: `1` satisfied, `0` violated, empty = cannot be judged by rule.
- Three scales: `v1` (the original checker), `v2_full` (the revised checker), `v2_no_length`
  (the revised checker, except that length items use the v1 count).
- **All-pass** means no item of the article is judged violated. The 25 articles with no checkable
  item (3 in S3, 22 in ComplexBench) are therefore all-pass in every arm. They are concordant in
  every paired comparison, so they do not change any McNemar p-value, but they add 25 to every
  arm's all-pass count.
- Paired tests in the paper are exact two-sided binomial McNemar tests on the discordant pairs, with
  no continuity correction: p = min(1, 2 · Σ_{i ≤ min(b,c)} C(b+c, i) / 2^(b+c)).
- The item list per article is in [`../../data/v3/items/checkable_items.jsonl`](../../data/v3/items/checkable_items.jsonl).
  It is the output of the reading layer, which is not published; the checker can re-judge any answer
  against this list, but cannot derive the list from a prompt.

Checks run before release: for the 24 arms of the original analysis, all 48,456 verdicts (three scales)
equal those of the frozen research checker, and the all-pass counts of all 34 arms equal the data pack
(`pack/scale_arms.csv`, including the L1 v2 rerun column).

## `pack/`

Data pack 3.1: one CSV per table of the paper, plus `v3_pack_zh.md`, the full pack text in Chinese,
in which every number cites the run file it was read from. The programs that produced it are in
[`../../eval/v3/pack_generators/`](../../eval/v3/pack_generators/); they read internal run files
and are published for provenance. The per-item files above are the public route to recompute the
tables.
