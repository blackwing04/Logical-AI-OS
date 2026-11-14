# v3 items, answers, annotations and reading exams

The material behind the v3 paper's tables: every prompt the models read, every arm's delivered answer,
the blind packs and labels of the human/AI raters, and the reading exams. Per-item verdicts are in
[`../../results/v3/per_item/`](../../results/v3/per_item/); the table-level data pack is in
[`../../results/v3/pack/`](../../results/v3/pack/).

Two question banks, 329 articles in all:

- **S3** (120 articles, written for this project). Group A: 72 rewritten prompts, including 3 sentinel
  articles. Group B: 48 articles whose topic was taken from the title of a thread on a public forum board
  (`topic_source_board`); only the topic was taken, the text is original. Released under CC BY 4.0.
- **ComplexBench rule-only subset** (209 articles) from `thu-coai/ComplexBench` at commit
  `749f4575d5dc981182ecaebb8c292b2a61213cf3`, MIT. The prompts are included verbatim, exactly as
  upstream, including any e-mail addresses or names that appear in them. See
  [`items/NOTICE_complexbench.md`](items/NOTICE_complexbench.md).

## `items/`

| File | One line per | Fields |
| --- | --- | --- |
| `s3_items.jsonl` | article | `id`, `user_message`, `group`, `sentinel`, `topic_source_board` |
| `complexbench_subset_items.jsonl` | article | `id`, `main_id` (position in upstream `data_final.json`, as in Phase II), `user_message` |

`user_message` is exactly what every bare arm received (checked identical across the four bare arms).
The arms marked "restated input (P)" received this message followed by a restatement of the requests;
that restatement is governance-side output and is not published.

## `answers/`

One file per arm and bank, `<arm>_<bank>.jsonl`, one line per article: `bank`, `id`, `arm`, `model`,
`answer`, `gen_seconds`, `n_new_tokens` (the conservative arms add `conservative_triggered`).
[`answers/arms.csv`](answers/arms.csv) lists each arm's model and method family.

- All arms: greedy decoding (temperature 0), one sample per article, `max_new_tokens` 2048
  (4096 for DeepSeek-R1-Distill-Qwen-7B, thinking included). All four models were loaded in 4-bit
  (bitsandbytes NF4, double quantisation, fp16 compute).
- For governed arms, `answer` is the final answer the arm delivered. `gen_seconds` is the generation
  time recorded by the run; for retry arms it covers the extra generation only.
- Arms suffixed `_L1v2` are the reruns with the revised length control (table 1, last column).
- [`export_counts.csv`](export_counts.csv): exported rows equal source rows for every file.

### Redactions

When a governed arm's answer copied wording from the governance layer (the retry message, a patch
message, or the restated input), each copied block is replaced by
`[governance-side text redacted, N chars]`, where `N` is the number of characters replaced. Same rule as
the Phase II package: a block is a run of at least 8 characters (whitespace ignored) built from 6-character
windows that occur in that wording but neither in the article's prompt nor in the bare arm's answer,
extended over adjacent matching text (gaps up to 4 characters). The list is in
[`answers/REDACTIONS.csv`](answers/REDACTIONS.csv). Per-item verdicts were computed on the original text.

## `annotations/`

Blind packs, rater labels, unblinding results and audit records, copied byte-for-byte into ASCII
folders. Every markdown table is also given as CSV (`<file>.table<N>.csv`, cells verbatim; most
labels and notes are in Chinese). [`annotations/MAP.csv`](annotations/MAP.csv) gives each file's
original path, size, SHA-256 and the paper section it supports;
[`annotations/EXCLUDED.csv`](annotations/EXCLUDED.csv) lists what was left out and why (program files,
run metadata with local paths, files containing retry-message text). `annotations/blind_keys/` holds
the 14 condition keys used to unblind the packs; all were unblinded before this release. The pack
metadata files name each key as `condition_key_private_<pack>.json`; the published copy is
`condition_key_<pack>.json` (same content).

## `reading_exams/`

Exams v2-v4 (table 5): `exam.jsonl` (sentences), `answer_key.csv`, and `reader_output.jsonl` with the
requirements the reader extracted (`id`, `type`, `param`, `quote`) and the conflicts it detected
(`a`, `b`, `kept`). Internal rule codes are not included. `second_annotator_275.csv` is the second
annotator's independent reading of the v2 and v3 sentences.

## Licences

| Material | Licence |
| --- | --- |
| S3 items, annotations, reading exams | CC BY 4.0 (this project) |
| Answers of Qwen2.5-7B-Instruct and Qwen2.5-14B-Instruct (Apache-2.0 models), DeepSeek-R1-Distill-Qwen-7B (MIT model) | CC BY 4.0 |
| Answers of Qwen2.5-3B-Instruct (arms whose `model` is `Qwen2.5-3B-Instruct`: `B0g`, `B1g`, `B1g_L1v2`, `LPq3`, `LPq3_L1v2`, `Conservativeq3`) | **Research use only (Qwen Research License).** Not under CC BY; same reasoning as in [`../phase2/README.md`](../phase2/README.md#licences) |
| ComplexBench prompts | MIT, as stated by the upstream repository |
