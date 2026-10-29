# Failure taxonomy and boundary map, Phase II

This file has three parts, and their subjects differ. **Do not add up counts across parts.**

| Part | What failed | Source |
| --- | --- | --- |
| A | The **model's own** failures: answers judged unusable | Real-traffic papers M2 and M3 |
| B | Failures the **architecture caused**: it changed an answer that was right, or made a retry worse | S1, S2, Multi-IF, ComplexBench |
| C | Boundary map: what a shape layer reaches and what it cannot | Combines A and B |

Redaction:

- No prompt text, answer text or item identifiers appear. Behaviours are described abstractly.
- Detection thresholds and all action-layer implementation are not published. Only whether a
  failure *has a mechanically checkable shape* is given.

## A. The model's own failures (3B), with a 7B comparison

**Set:** 32 unusable 3B answers: M2, 26, taken from the first-generation 512-token answers, plus
M3, 6. The 7B comparison is 15 unusable answers. Labels come from the reviewer's per-answer gold.
Some answers carry two types.

| Type | 3B answers | What the model did instead | What the prompt looked like | Mechanically checkable? |
| --- | ---: | --- | --- | --- |
| A. First person not applied | 7 | Rewrote in the third person | Request asks for first person | Yes (person check; already in the architecture) |
| B. Fabrication: numbers | 3 | Added numbers or amounts absent from the source | CVs, bookkeeping | Yes (number-faithfulness detector, 9 / 10) |
| C. Fabrication: name swaps, added plot | 4 | Changed a person's name; inserted scenes | Fiction rewriting | **Half-shaped**: a name-variant detector exists but has a high false-positive rate |
| D. False statement about its own output | 1 | Claimed the deliverable contained something it did not | "A title that contains X" | Yes (required term, plus a claim-vs-content contradiction) |
| E. Role reversed or confused | 5 | Spoke as the other role; echoed the question; swapped subjects | Role-play prompts ("you are X") or letters | Split. Role-play with an explicit role statement, yes. Question echo, yes. **Subject swap or letter roles, no shape** |
| F. Refusal | 4 | "Sorry, I can't" | Fiction rewriting with violence or sexual hints; copyright | Refusal: yes. **Whether the refusal was mistaken: not mechanically decidable** |
| G. Copy / no expansion / no reduction | 7 | Copied the source; "expanded" text came out shorter; advice instead of a rewrite | Expand / reduce / polish requests | Yes (relative length; sentence-level verbatim ratio; non-delivery) |
| H. Format / quantity | 3 | Repeated list items; too few items; forbidden symbols | "N items", "X characters", "no digits" | Yes (list uniqueness, count, per-item length, character classes) |
| I. Model self-insertion | 1 | Replaced a character's self-introduction with the model's own name | — | Yes (trivial) |
| J. Language not read | 1 | Did not translate | "Translate into English" phrasing missing from the closed set | Yes (closed-set addition) |
| K. Other | 2 | Typo; a case that should have been asked | — | — |

- About **24 of the 32** have a shape that pure rules can check.
- The truly shapeless ones are subject swaps, name swaps (half-shaped) and typos.
- **The 7B is different.** Its 15 unusable answers were mostly *content* errors: fabrication 4,
  mixed-in English 3, person 2, length 1, half-written 1, wrong element 1, no title 1.
- A shape layer can help the 7B on person and mixed-script, and little else.

## B. Failures the architecture caused

| Cause | Where seen | What happened |
| --- | --- | --- |
| Direction read backwards | S1 (5 cases among B1's breakages) | A length limit read in the wrong direction; the retry pushed the answer the wrong way |
| Material sentence taken as a constraint | S1 (3 cases); M3 (1) | Words inside the material ("shorten", "table") were read as requests. The retry rewrote a correct answer |
| Retry lost unread constraints | S1; S2 (most of the 13 constraints broken) | After a retry, constraints the reading step had not found (count, person, language) were lost. Reduced in v1.6; still capped by reading recall |
| Sentence limit read as an item count | Multi-IF (9 questions, plus 1 related misread) | "No more than N sentences" was read as "at least N items", and the count action then acted in the wrong direction. Per-instruction pass on that instruction fell 31 → 22 (3B) and 32 → 22 (7B) |
| Scoped length read as a whole-answer limit | ComplexBench (5 questions) | Limits on one part ("a title under 10 characters", "each point under 50 characters", or a limit inside a conditional branch) were applied to the whole answer. The generation-time intervention then cut answers to a fraction, in one case from 475 characters to 7 |
| JSON ended early | ComplexBench (4 rules) | The generation-time intervention ended an answer inside a JSON object, so braces were left unclosed |
| Count action on a JSON task | ComplexBench (2 rules) | The count action changed the format of a JSON deliverable |
| Rewrite drift | ComplexBench (e.g. 2 end-of-answer rules) | A retry for one constraint changed something else, such as the closing line |

ComplexBench totals:

- The architecture broke 22 (3B) and 14 (7B) rules that the bare arm had passed.
- Only **3 per arm** were the rule that triggered the retry. The rest were collateral.
- Of the 3B's 22, the causes above account for a located part. The others are **not yet
  attributed**: 4 keyword, 3 forbidden-word, 2 length, 1 start, plus 2 JSON key mismatches and
  1 JSON syntax error.

## C. Boundary map

| Region | Reached by a shape layer? | Evidence |
| --- | --- | --- |
| Explicit lexical constraints: length, count, required / forbidden terms, language, character classes, simple formats, person | **Yes**, when the reading step finds them. On an out-of-sample benchmark the reading step found 57.5% of rules; on its in-sample development benchmark, 88.4% | S3 +14.5 / +17.1; ComplexBench +3.2 / +5.1 rule passes |
| Approximate length ("about N") | Weakly. It is the weakest type for every model, and retries recover only a few | S1, S2, S3 per-type tables |
| Item counts under retry | **Fragile.** Retries drop counts; the count action fixes counts but costs format and length | S3 count 22 → 17; count-action rows in `parts_spec_v2.md` |
| Scoped constraints ("each point", "the title", "if … then") | **Not yet.** Read as global, and harmful when acted on | ComplexBench scope cases |
| Start / end of answer | No reading type exists. 43 of ComplexBench's 252 rules are here | ComplexBench |
| Content faithfulness (fabrication) | Only numbers. Names and plot are half-shaped or shapeless | Part A, types B and C |
| Roles, intent, misunderstood task | Mostly not. An explicit role statement is the exception | Part A, type E |
| Semantic requirements with no lexical form (tone, register, wording) | **No.** This ceiling was shared with the Phase I recognizer line | Phase I results |
