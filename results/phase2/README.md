# Phase II results (verification layer) — aggregate tables

Phase II asked one question: **does the same small model follow explicit constraints
better when an external, zero-inference architecture is wrapped around it?** The
comparison is always *bare model vs. the same model plus the architecture*. A small
model beating a larger one is not the claim.

This directory holds **aggregate numbers only**. It contains no prompts, no answers
and no per-item records. The prompts come from user corpora (WildChat, LMSYS-Chat-1M)
and third-party benchmarks (Multi-IF, ComplexBench) and are not ours to republish.

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
  seed per item (base seed plus item index). Each arm was sampled **once**, so there are
  no confidence intervals.
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
