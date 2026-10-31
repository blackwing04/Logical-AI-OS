English | [繁體中文](PUBLIC_NOTES.zh-TW.md)

# Statement of processing for the public release

This repository is not a mirror of the internal working repository. Every file went
through a selection step, and some went through edits. This statement says **what was
edited, why, and what was lost as a result.**

The per-file, per-instance record is in [`MANIFEST.md`](MANIFEST.md).

## 1. Two kinds of edit

### 1a Corpus redaction

The project's test corpus comes from **WildChat**, which contains conversations by
real users. This repository **redistributes no user sentence**, so:

- **The seven rounds' sentence files, candidate files and rejection logs are not in
  this repository.**
- Where a code comment quoted a test case verbatim, that content was deleted and
  **rewritten as a statement of the linguistic point.** Example: a comment originally
  quoted a sentence to illustrate that "what follows the pointing word is a
  specification, not pasted material"; the public version keeps the point and drops
  the quotation.
- Verbatim fragments in the results reports were handled the same way, while the
  **statistics, the typology, the attributions and the conclusions were all kept.**

**Sentence ids are kept** (identifiers like `D17/s01`). Reason: the sentence files are
not public, so an id on its own cannot be traced back to the corpus; and removing the
ids too would break the attribution chain — a reader would no longer be able to
confirm how the same sentence was treated across different rounds.

### 1b Name redaction

Internally the project refers to the human principal by a short handle. It is a
project handle rather than a legal name, but for consistency it is **replaced
throughout by `PI`**, in every kind of file.

**One exception, stated here rather than left to be noticed:** the project's public
pen name, **Joe Yuan**, is not redacted. It is the name this work is published and
cited under (see the citation section of the [README](README.md)), it is a pen name
rather than a legal name, and redacting the name a work is published under would make
the work uncitable. The rule covers internal handles and third parties, not this.

The names of cited researchers (Austin, Searle, Fillmore, Goldberg, Li & Thompson,
Chao, Her, Ribeiro, Gardner, Efron, Koehn, Katz, Alshiekh, Chow, Madras, Belinkov,
Turpin, Kalai, McCoy, Gazzaniga and so on) are **all kept** — those are citations, not
personal data, and removing them would make the claims uncheckable.

## 2. What did not come in

| Not public | Why |
| --- | --- |
| The seven rounds' sentence files, candidate files, rejection logs | Contain content derived from real user conversations |
| All answer keys (gold) | Publishing them would void these rounds |
| The sha256 of the answer keys | A hash has verification value only alongside the key it covers; publishing it alone is decoration |
| Each round's correction orders and progress files | Internal workflow, and they contain unpublished criteria |
| The round-by-round event record (the behavioural-confabulation document) | Only the mechanism hypotheses and the literature correspondence were kept |
| Any credential | — |

## 3. How to check the hashes — two tables, each covering one side

This repository carries **two hash tables**:

| Table | What it lists | Which question it answers |
| --- | --- | --- |
| [`manifest/v45_manifest.md`](manifest/v45_manifest.md) | The 31 components of the **internal sealed build** | "What did the internal version seal?" |
| [`manifest/public_manifest.md`](manifest/public_manifest.md) | **Every file in this repository** | "What is the copy in front of you?" |

**The two tables' hashes do not match, and the difference is exactly the corpus
redaction and the name redaction**; the per-instance record is in
[`MANIFEST.md`](MANIFEST.md) §2. This is not a recording error but the unavoidable
cost of corpus redaction — none of the three options is clean, and the second is the
one in force:

| Option | Cost |
| --- | --- |
| Publish the unprocessed code, hashes match | Violates "do not redistribute the corpus"; not available |
| **Publish the redacted version, with two tables and a per-instance record (in force)** | The two tables disagree, but every difference is checkable |
| Publish only the manifest, not the code | The code becomes unreadable; most of the point of publishing is lost |

**How to verify:**

1. **Is the copy in front of you the right one?** Compute the hashes yourself and
   check them against `public_manifest` (that file carries the command). **This step
   is verifiable in one move.**
2. **How does it differ from the internal sealed build?** Take the "internal source
   sha256" column of `public_manifest` against `v45_manifest`, then read the
   per-instance record in `MANIFEST.md` §2. **This step takes two moves, which is
   weaker than the internal one-move check. Said plainly.**

The only thing `public_manifest` cannot cover is **its own two files** — a table
cannot cover its own hash, since writing it changes it. That limitation is stated
inside that table rather than hidden.

## 4. The self-checks this repository ran, and what they caught

[`MANIFEST.md`](MANIFEST.md) §4 has the full results. Four gates:

- **A, corpus reverse-search**: starting from the **candidate-source side** of the
  seven rounds, every article split into 10-character fragments, each fragment
  searched against the whole of this repository. **0 hits.** This gate began as a
  sample of 20 articles; before the first push it was changed to a **full scan**
  (6867 fragments) and the full scan **caught two fragments the sample had missed** —
  so: passing a sample is not the same as not leaking.
- **A2, whole-sentence reverse-search**: all **1134** sentences of the seven rounds,
  each compared whole against this repository. **0 hits.**
- **B, names and third-party handles**: the project handle, the name and handle
  patterns of a social platform, @-handles, email addresses. **A first pass caught
  four files that had slipped through** (they were marked "unmodified" but still
  contained the handle, 7 instances); after re-marking and re-running, zero.
- **C, credentials**: five patterns. **0 hits.**
- **D, release boundary**: nine patterns for the non-public operational layer
  (see the release-discipline section of the [README](README.md)). A component's
  own exits are **inside** the public line; the architecture-level B gate, which
  is not implemented, is outside it. That distinction is in the README, and
  getting it wrong is what this gate exists to catch — it did not catch it, a
  full rescan did (see below).
  **One rule this gate learned the hard way:** which side of the line a file is on is decided by **what it does** — what it takes in, what it gives out, which layer calls it — not by what its own header claims. A header can borrow a name; the code cannot. A file here was once stopped as a leak on the strength of its docstring alone, and the docstring was wrong about the file.

**The limits of the self-checks themselves**, also stated: A2 is a full scan but
compares **whole sentences only**, so it is blind to corpus that was **paraphrased**
before being written in. That layer rests on per-file reading, recorded in
`MANIFEST.md` §2. Gate D is pattern matching, not meaning: the same operational-layer
fact described in different words would pass it.

## 5. One thing kept, with its source stated

`src/mechanical/lexicon_v2.py` contains a few **test sentences written by the PI**.
Those are not WildChat corpus, so they were not deleted under "do not redistribute the
corpus"; but they are sentences written by a real person, and that is stated here so a
reader can judge for themselves.

## 6. The ASCII rename (2026-10-08)

Nine files under `docs/` and `results/` were renamed from Chinese to ASCII filenames.
**The rename changed no content** — eight of the nine are byte-identical to the
original release `ade2734`. The ninth, the round-6 results file, differs by **exactly
one line**: it links to the round-7 results file, whose name also changed, so the link
had to be updated or it would point at a file that no longer exists. The old-to-new
mapping is in [`MANIFEST.md`](MANIFEST.md) §7 and in that commit's message.

The lexicon's `v2*` identifiers were renamed to ASCII at the same time (9 keys). The
lexicon's **other 61 Chinese keys were left untouched**: they are the structure of a
signed table, and changing them is a criterion-layer change that has to be signed off
first.

## 7. Correction: `src/` did not run outside our machine (2026-10-31)

**Correction record.** From the first release (`ade2734`, 2026-10-07) until this correction, the recognizer in
`src/` **could not be run on any machine but ours**. Three causes:

- the internal module `canon_v3` was missing;
- the internal module `classifier` was missing;
- 8 files added an absolute local path to `sys.path`.

During that period the README line "`src/` runs directly" was **not true**. It was found on 2026-10-31,
while every command in [`QUICKSTART.md`](QUICKSTART.md) was being run in a clean environment. It is corrected
as described below, and the README line now points to QUICKSTART.

**What was wrong, in detail.** The first release copied 23 of the v4.5 build's 31 components. Two modules that
the published recognizer imports were not among them:

- the table-5 cue detector, imported by `detectors.py`;
- a weight and route mapping, imported by `pipeline_v2.py`.

So `src/` did not run on any machine but ours, and the README line saying it did was not true. On our
machine it seemed to work, because some files add a path of the internal working tree to `sys.path`.

**What was added.** Six files, plus a new command-line entry, `src/run_recognizer.py`. The new modules sit
in `src/mechanical/`, where the published files already look for them.

| Public file | Internal source | Internal sha256 (LF) | Processing |
| --- | --- | --- | --- |
| `src/mechanical/canon_v3/lexicon.py` | `scripts/canon_v3/lexicon.py` | `ecd15074b211bee434eedbea763549df32aef7d947efa26b6c6bce4039eb8ca6` | Name redaction, 4 places; corpus redaction, 2 examples; 1 internal order reference rewritten; 1 comment word changed |
| `src/mechanical/canon_v3/cue_anchor.py` | `scripts/canon_v3/cue_anchor.py` | `bb96e23abd20dfd5116dae927d4ec667f533f001e72ae1f1387ea5dd27b312fb` | Name redaction, 1 place; corpus redaction, 4 examples |
| `src/mechanical/canon_v3/quantity.py` | `scripts/canon_v3/quantity.py` | `8b7ac0433ab69186a827d2057195474f9bb169d79ddf1ca9458b1ebba38330a8` | 1 docstring word changed; 1 loop variable renamed in one function |
| `src/mechanical/canon_v3/prompts.py` | `scripts/canon_v3/prompts.py` | `bc2558da42f912359d07db890a8e9b23b5f4bffc30578003acf8628359987faa` | **Excerpt** |
| `src/mechanical/classifier.py` | `experiments/composite-classifier/src/classifier.py` | `7ed901dcd3e278c69a08651882ee4a20f29aa146b7f0cc80b2903b565e253521` | **Excerpt** |
| `src/mechanical/canon_v3/__init__.py` | — | — | New; a docstring only. The internal package's `__init__` only puts the internal repository root on `sys.path` |

Each file states its source and processing in its own header.

**About the excerpts.**

- **`prompts.py`** keeps two functions verbatim, `build_table5_cue_phrase` and `detect_table5_constraint_cues`. The
  rest of the internal file builds the prompts of the model-labelling tool and is not published.
- **`classifier.py`** keeps three things verbatim: `weight_of`, `LexiconNotRegistered` and `route_of`. It also keeps
  the registry read and its fail-loud guard; only the path to the same signed table is made relative.
  The rest of the internal file asks the model and is not published.
- **No model code is involved.** No prompt template, system prompt, threshold or model code came in, and nothing
  here needs a model library.

**The edits, instance by instance.**

- **Name redaction:** the internal handle is replaced by `PI`, as in section 1b.
- **Order reference:** the reference to an internal order file now reads "internal order, not published".
- **Corpus redaction.** The rule applied: an example that occurs in our test banks is treated as corpus,
  because those banks cannot be traced to their source item by item. Each such example is replaced by a
  statement of the point and marked `(example corpus-redacted)`. That covered six:
  - `lexicon.py`:
    - a numeral-plus-measure-word example;
    - a test-bank sentence showing 就可以 as a modal.
  - `cue_anchor.py`:
    - a bare count anchored by an earlier sentence;
    - a prohibition with nothing checkable to exclude;
    - a budget written as a number followed by 內;
    - a count of one under 只能.
- **Wording:** two comment words were changed to plainer ones (one in `lexicon.py`, one in `quantity.py`). In
  `quantity.py`, the loop variable of `_is_approximate_context` was renamed to `hedge`, the name the file already
  uses for the tables it iterates over. Behaviour is unchanged; see the check below.
- **Kept on purpose:** common word forms used as examples of morphology or of a guard, such as 哪一個,
  第一次, 下半年, 要不要, 一打開, 24小時 and 100萬. They also occur in the test banks, but only because
  they are common.

**Against the sealed build.**

- `manifest/v45_manifest.md` lists `prompts.py` and `classifier.py`, and the internal hashes above are the ones it lists.
- It does **not** list `lexicon.py`, `quantity.py` or `cue_anchor.py`. The manifest was built by following imports,
  and that walk did not follow the package's relative imports. This is a gap in that manifest, stated here
  rather than repaired in it.
- For those three, the internal hashes are given in the table above. Their last internal changes (2026-08-25,
  2026-08-08 and 2026-08-22) all predate the v4.5 seal.

**How it was checked.** We ran every text field of the published S1–S3 items (4,482 sentences) through two set-ups:

- this public chain;
- the internal chain.

The outputs were byte-identical. The test exercised table 5 on 1,293 sentences and every frame type.

**The absolute paths.** In 8 published files, the absolute path of the internal repository became a path
relative to the file, `Path(__file__).resolve().parents[2]`, marked with a comment. It is one line in each file, and two in
`detectors.py`. The files are:

- `clause_v2.py`, `pipeline_v2.py`, `reorder_v2.py` and `detectors.py` in `src/mechanical/`;
- `src/control/judge_v4.py`;
- `src/perf/run_perf.py`;
- `src/blindtest/run_7b_arm.py`;
- `src/tools/split_sentences.py`.

The subdirectories those paths name are internal and do not exist here, so on any machine the recognizer now finds
only the modules in this repository.

In the three model-running scripts, two further kinds of change were made:

- **Model directory.** The absolute model directory (5 places) now comes from the environment variable `MODEL_DIR`,
  default `models`, with the same sub-paths. Each of these files gained `import os`.
- **Internal file names.** Two references to internal order files were made neutral:
  - in `judge_v4.py`, the ask-template source file, which is internal and not published, is now named `ask_template_source.md`;
  - in a comment in `split_sentences.py`, the reference now reads "internal order, not published".

Nothing else in these files changed.

**What still does not run.** The exit adjudicator (`src/control/judge_v4.py`), the performance station
(`src/perf/`) and the comparison arm (`src/blindtest/`) still import internal modules that are not
published. They run models and are not part of the recognizer.
