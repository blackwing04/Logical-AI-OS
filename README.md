English | [繁體中文](README.zh-TW.md)

# Logical AI OS — public release

[![DOI, this version](https://zenodo.org/badge/DOI/10.5281/zenodo.23226740.svg)](https://doi.org/10.5281/zenodo.23226740)
[![DOI, all versions](https://zenodo.org/badge/DOI/10.5281/zenodo.23226739.svg)](https://doi.org/10.5281/zenodo.23226739)
[![prior work: LoRA line, software](https://zenodo.org/badge/DOI/10.5281/zenodo.17848554.svg)](https://doi.org/10.5281/zenodo.17848554)
[![prior work: LoRA line, preprint](https://zenodo.org/badge/DOI/10.5281/zenodo.17848305.svg)](https://doi.org/10.5281/zenodo.17848305)

An attempt at replacing parameter search with logical mapping. Behaviour equation
`B = f(I, C, R)`; verification equation `M = i × e`.

This repository is the **public release made after the recognizer line was closed
out**: one research line that was carried to completion, reached a conclusion, and
whose conclusion is bounded — released together with its code, its criterion tables,
its literature positioning and its evaluation protocol.

## What this line did, and what came out of it

The goal: use an **external mechanical layer** (zero model calls, linguistic
criteria) plus a **small model** (3B) to separate, in open-domain user requests,
"constraints on the answer" from "material to be processed"; where there is a gap,
ask rather than guess.

Seven blind rounds, three-party separation of duties, two arms (this system vs. a
bare 7B). **The conclusion is bounded:**

- **We cannot claim "external framework + 3B ≥ bare 7B."** Two valid rounds, one
  loss and one win, and the win's bootstrap 95% interval contains zero.
- **The stable differences we can state (same direction in both rounds):** on the
  defensive sentinels the framework scored 0/10 and 1/7, the bare 7B 4/10 and 5/7
  — the bare model classifies narrative copywriting and a truncated self-report as
  constraint-bearing; the framework does not. The two arms' false positives also
  differ in shape.
- **The ceiling both paths share:** semantic constraints with no lexical form
  (requirements to change phrasing, tone, vocabulary level and so on). Neither
  reaches them.

Details in [`results/`](results/).

## Part II: the verification layer (2026-10-17 to 2026-10-29)

The second line asked a narrower question: **does the same small model follow explicit
constraints better when an external, zero-inference architecture is wrapped around it?**
The architecture reads the constraints from the prompt, checks the answer by rule, retries at
most once after generation, and from v1.8 adds a generation-time intervention.
The comparison is always bare model vs. the same model plus the architecture.

- **Synthetic, constraint-dense paper S3** (rules frozen before generation, gold blind to the
  rules): all-constraints-kept rate 3B 39.3 → 53.8%, 7B 51.3 → 68.4%. Scored by an independent
  checker written by the reviewer.
- **External blind shot, ComplexBench rule-only subset** (252 rules, official `con_rule.py`,
  rules frozen at v1.11): rule passes 3B 57.1 → 60.3%, 7B 63.9 → 69.0%. This is one sample per
  arm, and the whole response is the evaluated object (the official GPT-4 extraction step was
  not run).
- **Negative results kept beside them:**
  - Multi-IF zh was −1.8 / −1.3 points. Sentence limits were read as item counts.
  - Real-traffic papers (WildChat) showed an effect near zero.
  - On ComplexBench, rewrites broke 22 / 14 rules the bare model had passed. Only 3 per arm
    were the retried rule itself.
- **Reading coverage is the ceiling.** The reading step found 57.5% of ComplexBench's rules
  (out-of-sample). Gains concentrate in the rules it found; unread rules almost never improved.

Tables in [`results/phase2/`](results/phase2/); protocol in [`docs/protocol/phase2/`](docs/protocol/phase2/);
scoring scripts in [`eval/`](eval/); failure taxonomy and boundary map in
[`docs/failure_taxonomy.md`](docs/failure_taxonomy.md). All action-layer implementation, rule tables and
thresholds are **not published** (see the release discipline below).

Gold in Phase II was labelled by the reviewer session (an LLM), not by a human; the PI spot-checked.

Part II report: Zenodo DOI [10.5281/zenodo.23826978](https://doi.org/10.5281/zenodo.23826978).

## Honesty list (read this first)

This release deliberately places the **unfavourable findings** on the same footing
as the results:

- [`docs/literature_mapping.md`](docs/literature_mapping.md) — a 39-row literature
  correspondence table. Every row is labelled with its relation:
  `matches` / **`borrowed name`** / **`prior work exists`** / `partial overlap` /
  `provenance pending`. Among them:
  - of three candidate original contributions, the de-duplication search found
    **two to be prior work and one a partial overlap**;
  - the word "frame" for the five entry gates is a **borrowed name** (our gate is
    not the same construct as a frame in frame semantics);
  - "adversarial sampling" is a **borrowed name** (the sentinels correspond to a
    minimum functionality test, not to a contrast set);
  - the "empty-frame request" category has **no support in the literature** and is
    not placed under speech-act theory;
  - the bootstrap has a methodological gap in its resampling unit (resampled by
    sentence, while sentences within one article are not independent).
- [`docs/protocol/blind-test-protocol.md`](docs/protocol/blind-test-protocol.md) §9
  — the **three things this evaluation protocol does not solve.**

## Contents

| Path | Contents |
| --- | --- |
| [`docs/literature_mapping.md`](docs/literature_mapping.md) | Literature correspondence table (our component vs. nearest prior work vs. relation vs. source) |
| [`docs/method/`](docs/method/) | Line-by-line verdicts on four adjacent literature lines; the methodology defence; the external explanation framework |
| [`docs/theory/`](docs/theory/) | The runaway-mechanism theory and its literature positioning; mechanism hypotheses and literature correspondence for behavioural confabulation |
| [`docs/protocol/`](docs/protocol/) | The blind-test protocol (three-party separation of duties, seed rules, answer-key freezing, artifact self-evidence) |
| [`docs/PORTING.md`](docs/PORTING.md) | What transfers, what must be rebuilt, and what must be re-signed when porting this measurement layer to another language |
| [`results/`](results/) | Round 5 / 6 / 7 results reports (corpus-redacted) |
| [`src/`](src/) | The v4.5 judgement chain: mechanical layer, control layer, performance station, comparison arm, sentence splitter |
| [`src/mechanical/signed_tables/`](src/mechanical/signed_tables/) | Signed tables (numeral-classifier classifier, function layer, lexicon registry) |
| [`manifest/`](manifest/) | The v4.5 sealing manifest: sha256 of 31 components plus the flag table |
| [`papers/`](papers/) | The technical report (Zenodo deposit): the PDF, the Markdown body, the Chinese abstract, the bibliography, and their checksums |
| [`results/phase2/`](results/phase2/) | Part II aggregate tables (CSV + Markdown): scores per arm, improved / worsened, per-type pass rates, trigger rates, reading coverage |
| [`results/phase2/per_item/`](results/phase2/per_item/) | Part II per-item results: every constraint of every synthetic item, every Multi-IF instruction and every ComplexBench rule, per arm; the paired statistics and the script that recomputes them; the reading-variant table |
| [`data/phase2/`](data/phase2/) | Part II items and answers: S1–S3 prompts (original and rewritten) and every arm's full answer; every arm's full answer on Multi-IF zh and the ComplexBench rule-only subset (keyed by item id; benchmark prompts not included) |
| [`docs/protocol/phase2/`](docs/protocol/phase2/) | Part II evaluation protocol: synthetic-paper rules, oracle and record-only arms, stop lines, the external-benchmark ("bullet") rules, and the history of every gate change |
| [`eval/`](eval/) | Part II scoring scripts: glue around the official Multi-IF and ComplexBench checkers, the reviewer's independent checkers for S1–S3, the reading-coverage statistics |
| [`docs/parts_spec_v2.md`](docs/parts_spec_v2.md) | Part II parts specification: what each part measures and the number it reached (numbers only) |
| [`docs/failure_taxonomy.md`](docs/failure_taxonomy.md) | Part II failure taxonomy (the model's own failures; failures the architecture caused) and boundary map |

## Scope of this release, and what is not in it

**Not in this repository**, and that is deliberate:

- **The seven rounds' sentence files and anything derived from the source corpus.**
  The test corpus comes from WildChat, which contains real user conversations; this
  repository redistributes no user sentence.
- **All answer keys (gold).** Publishing them would void these rounds.
- Each round's correction orders and progress files (internal workflow).
- Any credential.
- **Part II:** prompts and answers from WildChat and LMSYS-Chat-1M (rounds M1–M3); the prompts of
  Multi-IF and ComplexBench (only item ids are given; the answers are in `data/phase2/`); all gold
  files (the synthetic papers' constraint lists appear only as the per-constraint columns of
  `results/phase2/per_item/`); and all action-layer implementation, rule tables and thresholds.

### Release discipline: what is public and what is not

The scope of this project's public releases has been, since 2026-10-08, an
**institutional line** rather than a case-by-case judgement:

| | Contents |
| --- | --- |
| **Public line = the measurement layer** | Recognition components (code, criterion tables), the evaluation protocol, the failure theory, the literature correspondence, the corpus-redacted round reports |
| **Non-public line = the operational layer** | How the behaviour equation is gated and wired, the computation and thresholds of the verification equation, the control layer, the integrity-protocol design, and the handling of defects not yet closed out |

**One distinction inside that line, stated because it is the one that was got wrong.** A component's *own* exits — the sentence-level three exits and the ASK quota — are part of the measurement layer and are public. The **architecture-level B gate** — deciding whether a whole request is answered or asked back about, based on how complete `C` is — is the operational layer. It **is not implemented**, and it will not be published.

**Part II addendum (2026-10-29, PI's ruling).** All action-layer implementation, rule tables and
thresholds added from 2026-10-17 to 2026-10-29 fall on the non-public side, for the same reason as
the original line. Public text names only the two actions, a retry once after generation and a
generation-time intervention, and does not describe how either works. Part II publishes effects,
protocol, coverage, the failure taxonomy, boundaries and part-level numbers.

Non-public items **do not appear in this repository, nor in any outward-facing
text**; their design drafts stay in the internal working repository. Where a record
is needed, it takes the form of a hash commitment — **the content is sealed and only
the hash is published**, as in
[`COMMITMENT_2026-09-24.md`](COMMITMENT_2026-09-24.md).

The reason for this line is stated here rather than hidden: **the measurement layer
can be inspected by outsiders, and before the operational layer can be inspected
there has to be a measurement layer that can be.** Releasing the half that is
verifiable first is a question of order, not of withholding.

**Every file that came from an internal file by corpus redaction or name redaction
states the processing in its own header**; the per-file, per-instance record of
deletions and edits is in [`PUBLIC_NOTES.md`](PUBLIC_NOTES.md).

## The honest boundary of reproducibility

The code and the criterion tables are here, but **the corpus is not**, so this
repository **cannot reproduce the seven rounds' numbers byte for byte**. What it can
reproduce is:

- the behaviour of the judgement chain on **your own** sentences (`src/` runs
  directly);
- the complete state of the signed tables and the flags (`manifest/`);
- the attribution chain behind every conclusion (the breakdowns in `results/`);
- for Part II, the **scoring** of your own responses on Multi-IF and ComplexBench with the
  scripts in `eval/` (rerun on the private responses before release: 0 differing verdicts).
  The architecture arms themselves cannot be rerun from this repository.
- for Part II, an **audit of every published number except M1–M3**: the per-item verdicts are in
  `results/phase2/per_item/`, the answers they were computed from are in `data/phase2/`, and
  `stats_paired.py` recomputes the paired statistics from the per-item files alone.

The hashes in `manifest/` are those of the **internal source files** and **do not
match** this repository's corpus-redacted versions; the reason and the way to check
across them are in [`PUBLIC_NOTES.md`](PUBLIC_NOTES.md) §3. That is the unavoidable
cost of corpus redaction, not a recording error.

## Licence and citation

**Dual licence, split by path:**

| Path | Licence | File |
| --- | --- | --- |
| [`src/`](src/), [`manifest/`](manifest/), [`eval/`](eval/) | **MIT** | [`LICENSE`](LICENSE) |
| [`docs/`](docs/), [`results/`](results/), [`papers/`](papers/), [`data/`](data/), `README.md`, `PUBLIC_NOTES.md`, `MANIFEST.md` | **CC BY 4.0** | [`LICENSE-docs`](LICENSE-docs) |

**Except** the Qwen2.5-3B-Instruct answer files (`data/phase2/**/*_answers_3b.jsonl`): they are
marked **research use only (Qwen Research License)** and are not under CC BY. The licences of the
models and of the two benchmarks are stated in [`data/phase2/README.md`](data/phase2/README.md).

The paper (Zenodo) side is **CC BY**.

**Under no licence here**: the test corpus. It comes from WildChat, whose licence
governs it; this repository redistributes none of its content (see
[`PUBLIC_NOTES.md`](PUBLIC_NOTES.md)).

### Citation

**Author: Joe Yuan.** That is the project's public pen name, not a legal name, and it
is the name to cite. The name-redaction rule described in
[`PUBLIC_NOTES.md`](PUBLIC_NOTES.md) §1b covers internal handles and third parties;
it does not cover this pen name.

The technical report is published at Zenodo. Citation as Zenodo gives it:

> Yuan, J. (2026). Logical AI OS, Measurement Layer: An External Mechanical Extractor of Answer Constraints — Protocol, Failure Theory, and Bounded Results from Seven Blind Rounds (Version v1.2). Zenodo. https://doi.org/10.5281/zenodo.23226740

**Two DOIs, and they are not interchangeable.** Cite **all versions** with
[10.5281/zenodo.23226739](https://doi.org/10.5281/zenodo.23226739) — it always resolves to the latest one. Cite **this
version** with [10.5281/zenodo.23226740](https://doi.org/10.5281/zenodo.23226740). Use the version DOI when a claim you
make depends on the numbers as they stood in v1.2.

The deposit files are in [`papers/zenodo_v1.2/`](papers/zenodo_v1.2/) with
their checksums; the PDF there is byte-identical to the published one, and
[`papers/zenodo_v1.2/CHECKSUMS.md`](papers/zenodo_v1.2/CHECKSUMS.md) says
which of those files the deposit does and does not contain.

If you cite this project, please **cite it together with
[`docs/literature_mapping.md`](docs/literature_mapping.md)** — that table lists the
nearest prior work for each component and the relation to it (including three
borrowed names and two findings of prior work). **That table is this line's honest
position.** Citing the conclusions without the table would leave a reader thinking
the components are new.

An earlier line of this project (LoRA fine-tuning of a 3B model) is deposited
separately at [10.5281/zenodo.17848554](https://doi.org/10.5281/zenodo.17848554) and
[10.5281/zenodo.17848305](https://doi.org/10.5281/zenodo.17848305); the work in this
repository does not depend on it.
