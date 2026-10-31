# Phase II results (verification layer) — aggregate tables

Phase II asked one question: **does the same small model follow explicit constraints
better when an external, zero-inference architecture is wrapped around it?** The
comparison is always *bare model vs. the same model plus the architecture*. A small
model beating a larger one is not the claim.

The CSV files at this level are **aggregate numbers**. The per-item records behind them are in
[`per_item/`](per_item/) (see the last section), and the synthetic prompts and every arm's answers
are in [`../../data/phase2/`](../../data/phase2/). Not published: anything from the user corpora
(WildChat, LMSYS-Chat-1M; rounds M1–M3) and the prompts of the third-party benchmarks (Multi-IF,
ComplexBench), which are referenced by item id only.

## Files

| File | Contents |
| --- | --- |
| [`summary.md`](summary.md) | All tables in readable form, generated from the CSV files below |
| [`headline.csv`](headline.csv) | One row per paper × arm: metric, passed, total, %, status, scorer |
| [`deltas.csv`](deltas.csv) | Improved / worsened counts against the bare arm, and constraint-level fixes / breaks |
| [`per_type.csv`](per_type.csv) | Pass counts per constraint type (S1–S3), per instruction id (Multi-IF) and per rule kind (ComplexBench) |
| [`triggers_coverage.csv`](triggers_coverage.csv) | How often the retry fired, and how much of the gold the reading step recovered |

## Arms

| Arm | Meaning |
| --- | --- |
| `B0` / `A0` | Bare Qwen2.5-3B-Instruct / bare Qwen2.5-7B-Instruct |
| `B1` / `A1` | The same model plus the architecture at the frozen rules version named in the row |
| `B2`, `B3`, `A2` | Ablation or candidate arms. Each row says which. |
| `B_oracle` | Gold constraints fed directly into the retry flow (an upper bound for that flow, not for the method) |

"The architecture" means:

1. A rule-based reading step that turns the prompt into a checklist of constraints.
2. A rule-based checker.
3. **At most one** retry after generation.
4. From v1.8, a generation-time intervention (length).
5. From v1.9, a conditional count action.

All action-layer implementation, rule tables and thresholds are **not published**; see [`../../docs/PORTING.md`](../../docs/PORTING.md).

## Three different metrics — do not compare across them

| Papers | Metric | Who scored |
| --- | --- | --- |
| M1–M3 (real traffic, WildChat) | **Usable rate**: the reviewer read every answer in full and marked it usable 0/1 | The reviewer, a separate LLM session blind to the rules. This is not human labelling; the PI spot-checked. |
| S1–S3 (synthetic, constraint-dense) | **All constraints kept**, per article | Independent checkers `grade_s1/2/3.py` ([`../../eval/synthetic/`](../../eval/synthetic/)), written by the reviewer and not sharing code with the architecture |
| Multi-IF zh, ComplexBench | The benchmark's **own checker**, unmodified | Multi-IF `gen_acc_strict`; ComplexBench `con_rule.py` |

## Status labels

| Label | Meaning |
| --- | --- |
| `official` | Rules frozen (sha256 recorded) before generation; gold blind to the rules; scored once |
| `official (blind)` | As above, on an external benchmark never used for development before it was scored |
| `development` | Same paper scored a second time after a fix; **not** evidence of generalisation |
| `candidate arm` | An unfrozen variant run beside the frozen arm |

## Caveats that apply to the numbers

- **ComplexBench, evaluated object.** The official pipeline first uses GPT-4 to extract
  the "evaluation object" (for example, the first sentence or the closing line) and then
  applies the rule. We did not call any API, so every rule was applied to the **whole
  response**. Rules about starts, ends or specific paragraphs are therefore judged more
  strictly than the official pipeline would judge them.
- **ComplexBench, dependencies.** 36 of the 252 rules depend on an LLM-judged condition.
  They were judged independently instead of being chained.
- **ComplexBench, sampling.** Generation used temperature 0.7 and top_p 0.9, with a fixed
  seed per item (base seed plus item index). Each arm was sampled **once**, so run-to-run
  generation variance is not estimated; the intervals in [`per_item/stats_paired.csv`](per_item/stats_paired.csv)
  cover item sampling only.
- **Multi-IF.** After it was scored, it was turned into development material. Every later
  Multi-IF *reading* number (v1.10, v1.11) is **in-sample**. The only out-of-sample reading
  number is ComplexBench's.
- **Real traffic.** LMSYS-Chat-1M was screened but **never became a paper**: after
  filtering, 2 Chinese first-turn prompts remained (94.4% were too short). The real-traffic
  effect rests on WildChat M2 and M3 only. M3's bare baseline was near ceiling.
- **Version mismatch.** S3's architecture scores are v1.8. ComplexBench used v1.11. S3 was
  not regenerated at v1.9–v1.11; only a zero-GPU trigger-set regression was run.
- **Reading rulers.** Two different rulers were used for reading coverage:
  - "Same type" counts a read as correct when the constraint type matches.
  - "Type and parameters" also requires the parameters to match.

  They are listed in separate rows and must not be joined by an arrow.

## What did not work (also in the tables)

- M2 v1.1 had a net −7, caused by wrong ASKs. ASK is closed in later versions.
- S1 on 7B had a net +4 violations.
- On Multi-IF the architecture was **negative** (−1.8 / −1.3 points). Nine "no more than
  N sentences" constraints were read as "at least N items", and one more constraint was
  misread the same way.
- On ComplexBench, rewrites broke 22 / 14 rules that the bare arm had passed. Only 3 per
  arm were the rule that triggered the retry. Three causes were located; the rest are not
  yet attributed:
  1. Scoped length limits ("each point under 50 characters") read as whole-answer limits.
  2. A JSON object ended early by the generation-time intervention.
  3. A format was changed on a JSON task by the intervention.

  See [`../../docs/failure_taxonomy.md`](../../docs/failure_taxonomy.md).

## Per-item results (`per_item/`)

Every number in the Part II report except rounds M1–M3 can be recomputed from these files. They were
generated from the delivered score files and checked against them: every per-constraint verdict of
S1–S3 equals the reviewer's grading output, and every total, trigger count and coverage figure equals
the published tables.

| File | One row per | Report section |
| --- | --- | --- |
| [`s1_items.csv`](per_item/s1_items.csv), [`s2_items.csv`](per_item/s2_items.csv), [`s3_items.csv`](per_item/s3_items.csv) | item × arm × constraint | §5 table and paired statistics |
| [`multiif_zh_items.csv`](per_item/multiif_zh_items.csv) | item × arm × instruction | §6 shot 1 |
| [`complexbench_rule_items.csv`](per_item/complexbench_rule_items.csv) | item × arm × rule | §6 shot 2, observe-only arm |
| [`stats_paired.csv`](per_item/stats_paired.csv), [`stats_paired.py`](per_item/stats_paired.py) | comparison | paired statistics in §5 and §6 |
| [`reading_variants.csv`](per_item/reading_variants.csv) | variant × rules build × constraint type | §6 reading-generalization diagnosis |

### Common columns

| Column | Meaning |
| --- | --- |
| `item` | Item id. Synthetic `Q001`…; Multi-IF `MIF001`…; ComplexBench `CB0001`… |
| `arm`, `model`, `rules_version` | Arm code as in the tables above; `-` = bare model |
| `status` | `formal`, `formal (ablation)`, `candidate`, `development`, `record-only` (S files only; the benchmark files hold formal blind arms only) |
| `all_pass` / `all_strict` | 1 = every constraint (rule, instruction) of the item passed — the "full compliance" metric |

### `s*_items.csv` (synthetic papers)

| Column | Meaning |
| --- | --- |
| `source_class` | `A` = written by the reviewer session; `B` = written by the executor from forum topics |
| `c_idx`, `c_type`, `c_param` | The constraint as the reviewer's checker reads it. Types: `len_ge` / `len_le` (at least / at most N), `len_ab` (about N: 0.8N–1.2N), `count` (N items), `term_req` / `term_forb` (required / forbidden term), `person_first` / `person_third`, `lang_en`, `no_digit`, `no_latin`, `no_emoji`, `fmt_list`, `fmt_table`, `fmt_para3` |
| `c_pass` | 1 = passed, by [`../../eval/synthetic/grade_s*.py`](../../eval/synthetic/) |

Length is counted in CJK characters, or in English words when English dominates the answer. When
English is required, the constraints that conflict with it are dropped before scoring (required /
forbidden Chinese terms, no Latin letters, person); this is why S1 has fewer `term_req` and
`person_first` rows than its items carry. Each paper has 120 items; the 3 sentinel items per paper
are protocol checks, are not scored, and are not included (117 remain). S2 includes two development
arms not in the frozen comparison: `B1_v1.7` and `B_oracle`; they were scored with the same checker
against the same constraint lists. S2 `A1` is a record-only arm whose answers are the bare arm's.
"Improved / worsened" in [`deltas.csv`](deltas.csv) compares the number of failed constraints per
item between two arms.

### `multiif_zh_items.csv`

| Column | Meaning |
| --- | --- |
| `source_key` | The item's `key` in the Multi-IF dataset |
| `instruction_id` | Multi-IF instruction id (its parameters are not reproduced; they are in the dataset) |
| `our_type`, `mappable` | The project's constraint type the instruction maps to; empty / 0 = no matching type |
| `strict`, `loose` | Official verdicts (`gen_acc_strict` / `gen_acc_loose`, unmodified checker) |
| `mappable_all_strict` | All mappable instructions passed; empty when the item has none |
| `retry_triggered` | Architecture arms only: whether the retry fired |

### `complexbench_rule_items.csv`

| Column | Meaning |
| --- | --- |
| `main_id`, `point_id` | Position in `data_final.json` (thu-coai/ComplexBench @ `749f4575`) and the rule's scoring-point id. Rule text and scoring questions are not reproduced; [`../../eval/complexbench/extract_rule_subset.py`](../../eval/complexbench/extract_rule_subset.py) rebuilds them |
| `kind`, `dims` | Rule kind and the benchmark's constraint dimensions |
| `mappable`, `dep_on_llm` | Rule has a matching project type; rule's condition depends on an LLM-judged rule (judged independently) |
| `pass` | Official `con_rule.py` verdict on the whole response |
| `mappable_all_pass` | All mappable rules of the item passed; empty when the item has none (21 items) |
| `retry_triggered` | Architecture arms only |
| `obs_read` | What the record-only arm's reading step did with this rule: `hit`, `right type, wrong parameters`, `missed`, `no matching type`. Reading depends only on the prompt and is identical for both models |
| `obs_would_trigger` | Record-only arm: whether a retry would have fired |

### `stats_paired.csv`

Up / down are discordant items (fail → pass, pass → fail). `mcnemar_p` is the two-sided exact McNemar
test; `ci_low` / `ci_high` are a percentile bootstrap of the item-level difference (B = 10,000,
seed in the file). Against the report, the up / down counts and p values reproduce exactly; the
report's bootstrap seed was not recorded, so interval ends differ by up to 0.8 points. `delta_pts`
is computed from counts; the report subtracts rounded percentages, so two ComplexBench 7B cells
differ by 0.1.

### `reading_variants.csv`

Reading hits (type and parameters both correct) on the Multi-IF zh prompts and their rewrites; the
rewritten prompts are not published. `rules_build`: `v1.10`; `v1.11 candidate` (the build measured
on all eight columns); `v1.11 frozen` (the released v1.11, measured on the original and V2 only —
the report's 320/362 and 301/362, hallucination 13.0% / 14.0%). All Multi-IF reading numbers are
in-sample.
