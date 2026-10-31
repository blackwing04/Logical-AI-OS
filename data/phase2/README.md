# Phase II items and answers

The material behind [`../../results/phase2/per_item/`](../../results/phase2/per_item/): the synthetic
prompts and every arm's full answer, so that each published verdict can be checked against the text
it was computed from. Nothing from the user corpora (WildChat, LMSYS-Chat-1M; rounds M1–M3) is here,
and the prompts of the two public benchmarks are referenced by item id only.

Answers are split by model, because the two models are under different licences (see the last section):
`*_answers_3b.jsonl` holds the Qwen2.5-3B-Instruct arms (`B*`), `*_answers_7b.jsonl` the
Qwen2.5-7B-Instruct arms (`A*`).

## `synthetic/` — S1, S2, S3

| File | One line per | Fields |
| --- | --- | --- |
| `s1_items.jsonl`, `s2_items.jsonl`, `s3_items.jsonl` | item (117 per paper) | `item`, `source_class`, `orig`, `final`, `model_input` |
| `s1_answers_3b.jsonl`, `s2_answers_3b.jsonl`, `s3_answers_3b.jsonl` | item × 3B arm | `item`, `arm`, `model`, `rules_version`, `status`, `answer`, `answer_kind` |
| `s1_answers_7b.jsonl`, `s2_answers_7b.jsonl`, `s3_answers_7b.jsonl` | item × 7B arm | same |

- `source_class`: `A` = written by the reviewer session; `B` = written by the executor from forum topics
  (the executor states these are original; this cannot be checked mechanically). Both are released
  under CC BY 4.0.
- `orig` is the item as written; `final` is the rewritten version (phrasing and layout changed,
  every constraint parameter kept verbatim). Only `final` was given to the models.
- `model_input` is the exact text the model read (wrapped in the model's chat template). It equals
  `final` except that sentence splitting removed some line breaks: 0 items in S1, 17 in S2, 18 in S3.
  No other character differs.
- The 3 sentinel items per paper (protocol checks, not scored) are not included.
- Arms, rules versions and status labels are the same as in the per-item tables.

## `public_benchmarks/` — Multi-IF zh and the ComplexBench rule-only subset

| File | One line per | Fields |
| --- | --- | --- |
| `multiif_zh_answers_3b.jsonl`, `multiif_zh_answers_7b.jsonl` | item × arm (454 × 2 per file) | `item`, `source_key`, `arm`, `model`, `rules_version`, `answer`, `answer_kind` |
| `complexbench_rule_answers_3b.jsonl`, `complexbench_rule_answers_7b.jsonl` | item × arm (209 × 2 per file) | `item`, `main_id`, `arm`, `model`, `rules_version`, `answer`, `answer_kind` |
| `extract_multiif_zh_turn1.py` | — | Rebuilds the 454 Multi-IF prompts and their keys from the dataset |

To join answers with prompts, fetch the benchmarks yourself:

- **Multi-IF**: `facebook/Multi-IF` on Hugging Face, file `multiIF_20241018.csv` at revision
  `0ab97ce0b45c7f57772e8ba2ac1616f4b00bd3aa`. `extract_multiif_zh_turn1.py` filters the Chinese
  first turns, assigns `MIF001`… in source order, and checks that its output is byte-identical to the
  file used in Phase II. `source_key` is the dataset's own `key`.
- **ComplexBench**: `data_final.json` from `thu-coai/ComplexBench` at commit
  `749f4575d5dc981182ecaebb8c292b2a61213cf3`. `main_id` is the item's position in that file;
  [`../../eval/complexbench/extract_rule_subset.py`](../../eval/complexbench/extract_rule_subset.py)
  rebuilds the 209-item / 252-rule subset.

## Redactions

The answers are the models' outputs as generated, with two kinds of span replaced by a placeholder. The
per-item verdicts were computed on the original text and are unchanged.

| Placeholder | What was replaced | Count |
| --- | --- | --- |
| `[retry-prompt echo redacted, N chars]` | After a retry, the model sometimes copied part of the retry message into its answer. The wording of that message is not published, so each copied block is replaced. A block is a run of the answer that matches the retry message, contains at least 8 characters found neither in the item's prompt nor in the bare arm's answer, and is extended over adjacent matching text (gaps of up to 4 characters) | 20 blocks in 20 item × arm answers |
| `[benchmark prompt text redacted, N chars]` | Multi-IF answers that repeat at least 40 consecutive characters (whitespace ignored) of a Multi-IF prompt, mostly because the instruction asks the model to repeat the request. Multi-IF is licensed CC BY-NC 2.0 and its prompts are not redistributed here | 43 spans in Multi-IF answers |

`N` is the number of characters replaced. ComplexBench answers that quote their prompt are left as
generated (the repository is MIT-licensed). The full list of redactions is in
[`../../MANIFEST_phase2_repro.md`](../../MANIFEST_phase2_repro.md).

## Generation

Qwen2.5-3B-Instruct (arms `B*`) and Qwen2.5-7B-Instruct (arms `A*`), temperature 0.7, top_p 0.9,
`max_new_tokens` 2048, one sample per item with a fixed per-item seed. For architecture arms, `answer`
is the final answer the arm delivered (after the retry, when one fired). `answer_kind` is the
measurement layer's answer-type label: `deliver` (an answer), `ask` (the model asked back instead of
answering), `refuse`.

## Licences

| Material | Licence |
| --- | --- |
| Synthetic prompts (`*_items.jsonl`) | CC BY 4.0 (this project) |
| `*_answers_7b.jsonl` (Qwen2.5-7B-Instruct outputs) | CC BY 4.0; the model is distributed under Apache-2.0 |
| `*_answers_3b.jsonl` (Qwen2.5-3B-Instruct outputs) | **Research use only (Qwen Research License).** Not under CC BY |
| Multi-IF (prompts not included) | CC BY-NC 2.0, as stated by the dataset |
| ComplexBench (prompts not included) | MIT, as stated by the repository's `LICENSE` file |

Why the 3B files are separated: Qwen2.5-3B-Instruct is distributed under the
[Qwen Research License Agreement](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/LICENSE)
(release date September 19, 2024). Its grant covers the "Materials" (the model, code and documentation)
"FOR NON-COMMERCIAL PURPOSES ONLY" (§2a), where "Non-Commercial" means "for research or evaluation
purposes only" (§1i). The agreement does not define outputs as Materials; it mentions them in §4b
("If you use the Materials or any outputs or results therefrom to create, train, fine-tune, or improve
an AI model that is distributed or made available, you shall prominently display “Built with Qwen” or
“Improved using Qwen” in the related product documentation"), and §9a requires a separate licence "if
you use the Materials in ways not expressly agreed to in this Agreement". Because the agreement does
not expressly license the outputs for other uses, the 3B answers are published for research and audit
only and kept apart from the CC BY material.
