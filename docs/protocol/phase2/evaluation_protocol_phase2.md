# Evaluation protocol, Phase II (verification layer)

This document describes how the Phase II numbers in [`../../../results/phase2/`](../../../results/phase2/)
were produced. It extends the Phase I protocol in
[`../blind-test-protocol.md`](../blind-test-protocol.md)
(three-party separation of duties, seed rules, answer-key freezing). That document still applies.
Only what changed or was added is written here.

**Not included:** all action-layer implementation, rule tables and thresholds. The protocol can be audited without them, because every score comes from a checker
that does not share code with the architecture.

## 1. Parties

| Party | Does | Does not |
| --- | --- | --- |
| PI (human) | Sets questions and direction, signs off, rules on disputes | Write code |
| Reviewer (a separate LLM session) | Writes papers (class A), labels gold, writes the independent checkers, scores, drafts orders | Run the architecture or see rule-side outputs before labelling |
| Implementer (a separate LLM session) | Builds the architecture, runs generation, delivers raw outputs | Score, label gold, or change frozen rules |

## 2. Freezing and blindness

- **Freeze before generation.** Every scored architecture arm runs a rules version that was
  frozen and signed before generation started. The sha256 of the frozen files is recorded in
  the delivery report. No frozen file changes between freezing and scoring.
- **Gold is blind to the rules.** The reviewer labels gold from the prompts and answers.
  Rule-side outputs (what the architecture read, what it triggered) are delivered in a
  separate folder and opened only after labelling.
- **Raw outputs only.** The implementer delivers answers and rule-side logs and does not
  report scores. Scores come from the reviewer's checker or from the benchmark's own checker.

## 3. Synthetic papers (S1–S3), paper rules v2

Each synthetic paper has 120 articles, including at least 3 sentinels. 117 are scored.

1. **Two sources in a fixed mix, shuffled with a seed.**
   - Class A (60%): material and constraints written by the reviewer.
   - Class B (40%): the implementer takes **only topics and ways of asking** from current
     public forums and writes original material and requests. Copying post text, real
     account names and real personal names is not allowed. Each article records the source
     board name and date.
2. **Rewording step (both classes).** The implementer rewrites how each request is phrased
   (sentence form, order, tone, splitting or merging sentences). **Constraint parameters are
   kept verbatim:**
   - numbers and units
   - quoted required or forbidden words
   - person words
   - language names
   - format names
   - "no digits / no English / no emoji"

   No constraint may be added or removed.
3. **Both versions are kept.** The original and the reworded text are stored side by side.
   **Only the reworded version is given to the models.**
4. **Class B constraint lists** are delivered to the reviewer as a manifest. They may not be
   used to tune rules. When scoring class B, the reviewer checks parameters against this
   manifest. Because 40% of each paper's constraint lists come from the implementer, the
   synthetic papers are not fully independent of the implementer.
5. **Mutually exclusive constraints** caused by a paper-writing defect are dropped from
   scoring; the articles themselves stay in. In S1 this affected 16 articles.

## 4. Arms and generation

| Setting | Value |
| --- | --- |
| Models | Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct (4-bit, local) |
| Sampling | temperature 0.7, top_p 0.9 |
| Seed | fixed per item: base seed + item index (+ arm offset where noted) |
| Max new tokens | 2048 (from M2 onward) |
| Retries | **at most one** per item |
| Bare arms | `B0` (3B), `A0` (7B) |
| Architecture arms | `B1` (3B), `A1` (7B) at a named frozen version; extra arms are labelled as ablation or candidate |

**Oracle arm (`B_oracle`).** The same retry flow, but the constraint list is the reviewer's
gold, not the architecture's reading. It measures the ceiling of *that flow*. In S2 the flow
had no generation-time intervention, and the S3 architecture later exceeded that ceiling
(+14.5 vs. +11.1). An oracle ceiling is therefore a bound on one flow, not on the method.

**Record-only arms (`-obs`).** The answer is the bare arm's answer. The architecture's reading,
triggers and planned retries are recorded but nothing is regenerated. These arms separate
"the reading step missed it" from "the retry broke it". Their statistics were not opened before
generation finished.

## 5. Stop lines

| Line | Value | Note |
| --- | --- | --- |
| Retry trigger rate, synthetic papers | 80% | Raised from 60% **during** S3, after B1 reached 62%. Reason given: the 60% line dated from single-constraint extraction; with multi-constraint extraction, ~60% triggering on papers where the bare model keeps all constraints ~40% of the time was expected. |
| Retry trigger rate, real traffic | 60% | Unchanged |
| Generation time, per paper | S3: 6 h; ComplexBench: 4 h (four arms cumulative) | Neither was reached (S3 2.1 h, ComplexBench 2.9 h) |
| Smoke test | First 10 items through the whole pipeline (generation, scoring, delivery) before every full run | — |

## 6. External benchmarks ("bullets")

**Survey.** Candidate benchmarks were surveyed against two criteria: rule-checkable, and at
least 100 Chinese items. Three qualified:

1. ComplexBench (rule-only subset)
2. Multi-IF Chinese subset
3. CELLO

**Two were used.** CELLO was shelved: there is no licence in its repository, it scores on a
continuous scale, and its overlap with our constraint types sits in our weakest types.

**A benchmark is spent once it is scored.** After Multi-IF was scored, it was turned into
development material (the v1.10 and v1.11 reading patterns come from it). Every later Multi-IF
reading number is in-sample.

**Checkers are the benchmarks' own, unmodified and pinned.**

| Benchmark | Checker | Deviation |
| --- | --- | --- |
| Multi-IF | `metrics.gen_acc_strict` from facebookresearch/Multi-IF@`1cdb53e`, unmodified | None |
| ComplexBench | `con_rule.py` from the official repository, unmodified | The official GPT-4 "evaluation object" extraction was not run, so the object is the whole response. 36 rules that depend on LLM-judged conditions were judged independently, not chained. |

## 7. Gates before the last shot, and their history

The last shot was gated so that it would only be fired if a result could be read clearly.
The gates **changed**, and every change is listed here.

**Gate 1, volume and types.** At least 100 questions, and at least 50% of rules in the
length / bullets / punctuation / start-end families. The subset has 209 questions; the four
families cover 53.6% of rules. The gate passed, narrowly.

**Gate 2, reading coverage (dry run: reading only, no generation, no answers).**

| When | Gate | Result |
| --- | --- | --- |
| First set | ≥40% of ComplexBench rules read correctly | v1.10: 19.4%, failed |
| First change | Raised to ≥70% by the PI ("at 40% the result would be ambiguous") | — |
| Second change | Validation moved to the spent Multi-IF material. A ComplexBench dry run before the shot was forbidden. Target: ≥70% hits per Multi-IF column and ≤41 unmatched reads. | — |
| Third change | v1.11's candidate reached 88.4% hits but 54–55 unmatched reads, so the ≤41 line failed. **After that**, the line was replaced by an unmatched-read *rate* no higher than v1.10's (18.1%) plus "genuine misreads" no more than v1.10's. The absolute line was recorded as a reviewer error, because the number of reads had roughly doubled. | Frozen v1.11: 13.0% (original), 14.0% (colloquial rewrite), passed |

**Gate 3, ruler differences.** For each rule family, the difference between the benchmark's
counting and ours was written down. This gate had no pass/fail condition.

**The one peek.**

- The v1.10 dry run on ComplexBench counts as looking at the benchmark once before the shot.
- It surfaced two mechanical bugs: an upper-bound phrasing read in the wrong direction, and an
  "at least" phrasing off by one. The gate order first said they would not be fixed.
- A later order fixed them, validated on Multi-IF and on self-written sentences, without
  ComplexBench examples.
- In the scored subset, those phrasings occur in 2 questions (2 rules). The upper bound on
  their effect is one rule per arm (≤0.4 points).

## 8. What this protocol does not solve

1. **One sample per arm.** Seeds are fixed, so a rerun on the same software and hardware should
   reproduce the outputs. But there is no variance estimate: differences of a few points are
   within what resampling could move.
2. **The reviewer is a model.** Separation of duties prevents self-scoring, but the reviewer and
   the implementer are both LLM sessions. **No gold in Phase II was labelled by a human.** The
   M1–M3 usable rates and the S1–S3 constraint lists were labelled by the reviewer session; the PI spot-checked.
   The external benchmarks use their own checkers.
3. **Thresholds were edited after results were seen.** Section 7 lists every edit. The
   edits were recorded at the time, but a reader should weigh them.
4. **Development and evaluation share the implementer.** Class B papers and every rule pattern
   were written by the same party that runs the architecture. Only Multi-IF and ComplexBench
   were outside the implementer's hands when they were scored.
