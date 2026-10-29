# Evaluation scripts, Phase II

These scripts turn model responses into the scores in [`../results/phase2/`](../results/phase2/).
None of them imports the architecture. They are the *referee side* only.

**Not included:** benchmark data, prompts, model responses, and gold files. The corpora are
not ours to redistribute, and gold for the synthetic papers stays private. The scripts are
published so that the scoring logic can be read and rerun on your own copies.

## Layout

| Path | What it is | Runs standalone? |
| --- | --- | --- |
| [`multi_if/score_multi_if.py`](multi_if/score_multi_if.py) | Glue around the official Multi-IF checker (`metrics.gen_acc_strict` / `gen_acc_loose`, unmodified, pinned commit; fetch instructions and sha256 in the file header) | Yes, with the Multi-IF data and checker files |
| [`complexbench/extract_rule_subset.py`](complexbench/extract_rule_subset.py) | Builds the 252-rule / 209-question rule-only subset from the official `data_final.json` | Yes |
| [`complexbench/score_complexbench.py`](complexbench/score_complexbench.py) | Glue around the official `con_rule.py` (unmodified). Whole response as the evaluated object; see the file header for the deviation from the official GPT-4 extraction step | Yes, with `con_rule.py` from the official repository |
| [`complexbench/rule_mapping.py`](complexbench/rule_mapping.py) | Maps ComplexBench rule strings to this project's constraint types (defines the "mappable subset"); matches recorded reads against rules | Library |
| [`complexbench/obs_coverage.py`](complexbench/obs_coverage.py) | Reading coverage and "missed vs. broke" split for a record-only arm | Needs the architecture's reading records (not public). Included to document the computation |
| [`synthetic/grade_s1.py`](synthetic/grade_s1.py), [`grade_s2.py`](synthetic/grade_s2.py), [`grade_s3.py`](synthetic/grade_s3.py) | The reviewer's independent checkers for S1–S3, **byte-identical** to the versions used for scoring (sha256 in `MANIFEST_phase2.md`) | No: they read private gold and delivery folders through the reviewer's sandbox paths. Published as written so the checking logic can be audited |

## Upstream sources

| Component | Source | Licence |
| --- | --- | --- |
| Multi-IF checker | https://github.com/facebookresearch/Multi-IF @ `1cdb53ed18499ad729e0766e5d3099dd5344406f` (`ifeval.py`, `metrics.py`) | Apache-2.0 |
| Multi-IF data (Chinese turn-1 subset, 454 items) | same repository / its dataset card | Non-commercial licence as stated by the dataset (not redistributed here) |
| ComplexBench `data_final.json`, `con_rule.py` | https://github.com/thu-coai/ComplexBench | Data CC BY 4.0, code MIT (as stated by the repository) |

## Reproduction check

Before release, all three standalone scripts were rerun on the private Phase II responses and
compared with the delivered score files:

| Script | Result |
| --- | --- |
| `score_multi_if.py` | **0** of 1,816 per-question verdict lists differed (454 questions × 4 arms) |
| `score_complexbench.py` | **0** of 836 differed (209 questions × 4 arms) |
| `obs_coverage.py` | Reproduced the published coverage (145 / 252) and the missed-vs-broke tables exactly |

## The synthetic checkers in one paragraph

Each constraint is reduced to a (type, parameter) pair, and the answer is measured directly:

| Type | How the answer is measured |
| --- | --- |
| Length | CJK characters, or English words when English dominates. `len_ab` (about N) accepts 0.8N–1.2N |
| Count | Line-initial numbered or bulleted items |
| Required / forbidden terms | Substring test |
| First person | At least 30% of sentences contain 我 |
| Third person | At most 15% |
| Language | English words outnumber CJK characters |
| Character classes | Regular expressions for digits, Latin letters, emoji |
| Formats | Numbered or bulleted lines, pipe characters, paragraph count |

When English is required, the constraints that conflict with it are dropped (required/forbidden
Chinese terms, no-Latin, person). These checkers were written by the reviewer and share no code
with the architecture's own checker.
