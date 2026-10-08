English | [繁體中文](PORTING.zh-TW.md)

# Porting this measurement layer to another language

For someone who wants to rebuild this measurement layer in a different language —
English, say. **Facts only, no promises.** Nothing here is a claim that a port will
work; it is a statement of which parts are language-independent, which are not, and
which cannot be translated at all.

Read the [README](../README.md) honesty list first. This document assumes it.

---

## 1. What transfers unchanged

These are language-independent and usable as they stand.

| Part | Where | Note |
| --- | --- | --- |
| Three-party separation of duties; seed rule; answer-key freezing | [`protocol/blind-test-protocol.md`](protocol/blind-test-protocol.md) | The protocol names no language. The seed rule (seed = the timestamp of the order that opened the round, self-checked by both sides) and the freezing sequence port as written. |
| The three-exit design (constraint / not a constraint / ASK) | [`../src/control/judge_v4.py`](../src/control/judge_v4.py) | The exits and the ASK cap are structural. What feeds them is not (see §2). |
| The seven-label routing **as a concept** | [`../src/mechanical/signed_tables/lexicon_registry.json`](../src/mechanical/signed_tables/lexicon_registry.json) | The idea that a lexicon may only be consulted in a registered domain, and that unregistered use raises rather than silently proceeds. The labels themselves have to be re-signed (§3). |
| The failure theory | [`theory/runaway-mechanism_theory-and-literature.md`](theory/runaway-mechanism_theory-and-literature.md) | A claim about autoregressive systems, not about Chinese. |
| The literature correspondence table | [`literature_mapping.md`](literature_mapping.md) | The prior-work positioning holds regardless of target language. Add rows for the target language's own grammar literature. |
| The bootstrap procedure, by sentence and by article | Described in the report §4.2 | The procedure ports; the numbers do not. |
| Manifest and hash self-evidence tooling | [`../manifest/`](../manifest/) | Walks an import graph and hashes files. Language-blind. |

## 2. What is language-specific and must be rebuilt

Listed file by file. For each: why it is language-bound, and what grammatical problem
the English equivalent has to solve.

### 2a `src/mechanical/lexicon_v2.py` — all of the tables

**Why it is language-bound:** these are closed sets of Chinese surface forms. Every
entry is a string that only exists in Chinese.

| Table | What it holds | The problem an English version has to solve |
| --- | --- | --- |
| Constraint-shape cues ("Table 5") | Surface forms that count as evidence of a constraint on the answer | English marks requirements differently — modals (`must`, `should`), infinitival purpose clauses, and bare adjectives in imperative frames. A cue list of Chinese strings has no English image; the categories have to be re-derived from English data, not translated. |
| Numeral-classifier closed set | Which "one + classifier" sequences are *naming* rather than *constraining* | **English has no classifier system, so this whole component does not apply.** The nearest English problem is different in kind: determiners and quantifying expressions (`a`, `one`, `a couple of`, `a piece of`) carry the work, with their own morphology. A port must decide whether there is any analogous naming-versus-constraining ambiguity at all, and may well find there is not. |
| Writing-specification exemption | Forms that specify *how to process material*, hence are never material | Partially transferable as a category (`at least N words`, `in the format of`), but the surface forms and the morphology of number expressions differ. |
| Request-verb object guards | When a requesting verb takes an object that redirects who is being asked | Depends on Chinese word order and on the specific verbs. English has its own pattern (`ask me to` vs. `ask me about`), which is a different distinction, not a translation of this one. |

### 2b `src/mechanical/clause_v2.py` and `src/tools/split_sentences.py` — segmentation and punctuation

**Why language-bound:** the splitter's rules are a decision about Chinese punctuation.
Full-width `？` and `！` are **not** split points, half-width `?` and `!` are, isolated
punctuation merges into the preceding sentence, and newlines split and are discarded.
That rule set was derived by working backwards from one round's hand-segmented gold,
not chosen.

**What an English version has to solve:** English has no full-width/half-width
distinction, so the rule that produced it is void. In exchange it has abbreviation
periods (`Dr.`, `e.g.`), decimals, and quotation marks that interact with sentence
boundaries — a problem this splitter does not have. The clause splitter likewise
depends on Chinese comma usage.

### 2c `src/mechanical/rules_v2.py` — the rules that rest on Chinese grammar

| Rule | Why it is language-bound |
| --- | --- |
| Zero anaphora / subject omission | Chinese is topic-prominent and licenses zero subjects through topic chains. English omits subjects in a narrower set of environments, so a detector built on "no person marker found" behaves differently. Note also that this project's own implementation conflated *zero subject* with *non-human subject*, which it had to correct — a port will meet the same trap in its own shape. |
| Imperative implies second person | Chinese imperatives typically have no subject and the "you" is supplied pragmatically. English imperatives are also subjectless, but the morphology and the competing readings (infinitive, subjunctive) are different. |
| "One + classifier" landing in the task body | **Does not apply**: no classifier system (see §2a). |

### 2d The 3B adapter in the model layer

**Not usable.** It was trained on Chinese gold. A port needs its own adapter, trained
on gold in the target language, or it needs to drop the adapter vote and re-derive the
filter from whatever replaces it.

Note the knock-on effect on the performance figures: the early-stopping condition only
saves when the adapter answers "no", so the cost profile in the report is a property
of that adapter on that corpus and does not carry over.

## 3. What must be re-signed, not translated

**The criterion tables cannot be translated.** The seven-label definitions and the
A1–C4 rules are decisions about one language's grammar; rendering them in English
produces sentences that look like rules but have not been tested against anything.

The required sequence in the target language is:

1. Build a small hand-annotated set in the target language.
2. Re-run a **rule-alignment audit**: compare each rule as written against the code as
   implemented, line by line. (When this project did that, the audit found seven
   divergences, all of them real.)
3. Have a human sign off the resulting tables. Only then do they count as criteria.

**The gold annotation case set has to be rebuilt as well.** It is the accumulated
record of rulings on ambiguous cases, and those rulings are about the source language.

## 4. Minimum viable port

The point at which a port becomes comparable to this work:

- the **same protocol** (three-party separation, seed rule, answer-key freezing,
  defensive sentinels);
- the **same three exits**, with the ASK cap stated in advance;
- the target language's **own** T1 lexicon, re-derived and signed (§2, §3);
- a **bare large-model comparison arm** in the target language, run on the same rounds
  and never concurrently with the system arm;
- the win criterion fixed in advance: the bootstrap 95% interval on the **difference**
  must exclude zero.

**The numbers from such a port cannot be compared directly with the Chinese numbers in
this report.** Different corpus, different positive rate, different model pair. The
comparable object is the protocol and the direction of the differences, not the F1.

## 5. Known ceilings that will follow you

These are not properties of Chinese. They will appear in any language.

1. **Semantic constraints with no lexical form.** Requirements to change phrasing, to
   sound more sincere, to use a higher register, to be simpler, shorter, or to
   emphasise something. In this work all of one round's misses were of this kind, and
   the bare comparison arm missed the same group. **No amount of lexicon work reaches a
   constraint that has no surface form** — a lexicon matches surfaces.
2. **Sparse positives make F1 a noisy instrument.** At a positive rate near 10%, the
   all-positive baseline came within a couple of points of both arms. Below some
   margin, the measurement cannot distinguish an improvement from noise, and that
   margin was larger than the effect of several individual changes.
3. **Early stopping only saves on the "no" branch.** The stop condition fires when a
   negative answer appears, so the cost of the "yes" population is unbounded by it.
   As a corpus gets harder that population grows and the latency profile degrades —
   which is a property of the stopping rule, not of the language.

---

**What this document does not cover:** how this component couples to the project's
downstream decision and verification layers. That is outside the scope of this
release — see the release-discipline section of the [README](../README.md).
