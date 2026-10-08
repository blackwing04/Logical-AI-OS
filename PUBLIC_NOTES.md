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
