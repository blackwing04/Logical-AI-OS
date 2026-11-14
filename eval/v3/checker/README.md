# LAIOS constraint checker v2 (standalone)

`laios_checker_v2.py` is a rule-based, zero-model checker. Given an answer and a list of
constraint items, it decides for each item whether the answer satisfies it (`True`),
violates it (`False`), or cannot be judged by rule (`None`; such items should be left out of
any compliance rate rather than counted as a pass or a fail).

It is a self-contained re-implementation of the frozen research checker used for the
published numbers (v1 base checkers plus the v2 structural-parsing revision), with the same
per-item verdicts (see "Equivalence" below).

## Dependencies

- Python 3.10+ (developed on 3.13), standard library
- `lemminflect==0.2.3` (pinned; pulls in `numpy`). Only imported when an English
  `term_required` / `term_forbidden` / `term_required_in_title` term is checked.
- `zh_s2t_table.json` and `zh_t2s_table.json`, shipped next to the module. Both are equal-length
  Simplified/Traditional Chinese character and phrase mappings derived from the OpenCC
  dictionaries (Apache-2.0), applied by greedy longest match without word segmentation.

## What it checks

| check_type | what is checked | v2 change |
| --- | --- | --- |
| `length` | character count (or word count when `unit` is `words`), `>=`, `<=` or `~` (+-20%) | characters exclude punctuation / symbols; each Latin alphanumeric run counts as one |
| `sentence_count` | number of sentences | |
| `language` | answer is in the required language / script | for English, leading / trailing Chinese courtesy lines are ignored |
| `language_forbidden` | a language is not used at all | |
| `format` | json, title (`<<...>>`), markdown, table, bullets, numbered, csv, yaml, html | numbered lists recognised in more forms; JSON with only non-ASCII spaces is normalised |
| `count` | at least N list items / paragraphs | counts list lines + table rows, JSON array length, in-line `1. 2. 3.` runs |
| `structure` | paragraphs, heading (opening / closing / summary are returned as `None`) | more heading forms recognised |
| `term_required` / `term_forbidden` | terms present / absent | Simplified/Traditional folding; English words matched on word boundaries with their inflections; sentences that merely talk about the constraint are ignored |
| `term_required_in_title` | the title line contains a term | same term matching as above |
| `person` | first- or third-person narration | quoted speech ignored; short texts pass with one first-person sentence |
| `relative_length` | expand / shrink relative to the material | |
| `copy_ratio`, `verbatim_sentence_ratio` | answer is not a copy of the material | |
| `list_unique_ratio`, `per_item_length` | list items not repeated / each item exactly N characters | |
| `forbidden_charset` | no digits / Latin / punctuation / emoji / commas / periods / upper case | |
| `self_insertion` | the model does not insert itself ("I am an AI ...") | |
| `role_third_person` | a role given to the model is not narrated in the third person | |
| `task_echo` | the answer is not just the request repeated | |
| `script_mix` | a Chinese answer does not mix in many English words | |
| `case` | all lower / all upper case | |
| `other` | skipped (no rule exists) | |

Language, length, format-like and list-shape types are checked on the deliverable part of the
answer (code fence, block between horizontal rules, or text after a lead-in phrase such as
the Chinese for "here is"); the others are checked on the whole answer. The list is `SCOPED_TYPES`.

## How to call it

```python
import laios_checker_v2 as lc

items = [
    {"sid": "Q001/s05", "check_type": "length", "check_arg": {"n": 300, "op": ">="}, "weight": 1.0},
    {"sid": "Q001/s05#term", "check_type": "term_required", "check_arg": {"terms": ["spring"]}, "weight": 1.0},
]
lc.check_items(items, answer)                         # v2:  {"Q001/s05": True, "Q001/s05#term": False}
lc.check_items(items, answer, exclude=("length",))    # v2, but the v1 length checker
lc.check_items_v1(items, answer)                      # v1 (before the v2 revision)
lc.check_items_detailed(items, answer)                # {sid: (verdict, short English detail)}
```

`check_arg` is plain JSON. `weight` is carried through but not used by the verdicts; a weighted
compliance rate is `sum(w for passed) / sum(w for decided)`.

## Where the item lists come from

The items are produced by the project's reading layer, which turns the question text into
constraint items. That layer is not published. Outside readers can therefore re-check any
answer against the **published item list** (`outputs/items.jsonl`), but cannot re-extract the
items from the question text themselves. Disagreements about whether an item reflects what the
question asked are about the reading layer, not about this checker.

This module also contains nothing of the generation-side machinery (topic / embedding
scoring, retries, patching, length control).

## Equivalence with the frozen checker

- `export_items_ref.py` (requires the private research tree) writes `outputs/items.jsonl`
  (329 articles, 673 checkable items), `outputs/ref_verdicts.jsonl` (frozen v1, v2 and
  v2-without-length verdicts for 24 answer arms x 329 articles = 7896 rows), and the two mapping
  tables.
- `test_equivalence.py` recomputes every verdict with this module and compares item by item;
  it writes `outputs/equivalence.md` and exits non-zero on any mismatch.

The reference item set exercises 13 of the 22 check types (length, format, copy_ratio,
language, term_required, count, term_forbidden, forbidden_charset, person, structure,
relative_length, term_required_in_title, sentence_count). The remaining types are ported
line by line but are not covered by the reference verdicts.
