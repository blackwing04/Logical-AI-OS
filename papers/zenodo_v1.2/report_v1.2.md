---
title: "Logical AI OS, Measurement Layer: An External Mechanical Extractor of Answer Constraints — Protocol, Failure Theory, and Bounded Results from Seven Blind Rounds"
author: "Joe Yuan"
subtitle: "Technical Report v1.2"
date: 2026-10-08
license: CC BY 4.0
doi: "10.5281/zenodo.23226740"
artifact: "https://github.com/blackwing04/Logical-AI-OS @ 846037e997b77cb06bac872d687ff196e6ea3e9b"
---

> **Scope.** This is a technical report, not a conference submission. Every number
> below is taken from the public artifact release at commit `ade2734`; nothing is
> sourced from the project's private working repository. No evaluation corpus,
> no answer keys, and no personal identifiers appear here or in the artifact.
>
> **DOI.** This report: [10.5281/zenodo.23226740](https://doi.org/10.5281/zenodo.23226740).
>
> **License.** This report: CC BY 4.0. Artifact code: MIT. Artifact documents: CC BY 4.0.
>
> **Scope boundary.** This release covers the *measurement layer* only: the
> recognition components, the evaluation protocol, the failure theory, the
> literature positioning, and the de-corpused round reports. How this component
> couples to the project's downstream decision and verification layers is
> deliberately outside this release.

# 0. Abstract

**English.** We built an external, zero-inference mechanical layer that separates,
clause by clause, which sentences of a user request are *constraints on the answer*
and which are *material to be processed*, and we paired it with a 3B model that
resolves what the mechanical layer cannot; gaps are turned into a clarifying
question rather than a guess. Across seven blind rounds — answer keys held by a
separate party, the executing side never seeing them — the configuration scored
F1 22.9 against a bare 7B's 32.4 on one scored round and 22.4 against 16.5 on
another, with a paired bootstrap 95% interval on the second of -19.0 to +7.3.
**We therefore cannot claim that an external framework plus a 3B model matches or
beats a bare 7B**; what we can report are two differences that held in the same
direction across both rounds (sentinel false positives, and the shape of the
false-positive population) and one ceiling that both arms hit (semantic constraints
with no lexical form).

---

# 1. Problem

A user request mixes two kinds of sentence. Some sentences say *what the answer
must satisfy* — a length, a format, a tone, a prohibition. Others are *material*:
text to be rewritten, background to be taken into account, a document pasted in for
processing. A system that treats the second kind as the first over-constrains its
own answer; one that treats the first kind as the second ignores the user.

The separation is **sentence-level and request-internal**. That is what distinguishes
the problem addressed here from the two nearest lines of prior work, both of which
we acknowledge as prior:

- **Instruction-data separation** [@zverev2025sep] measures whether a model
  *executes* instructions that appear inside a data block. The boundary there is a
  *trust* boundary between the user and third-party content.
  [@wallace2024hierarchy] makes that boundary explicit as a privilege ordering
  (system > developer > user > tool output).
- **Task / Context / Constraint decomposition** [@agentif2025] partitions a prompt
  into exactly these three roles, with constraints further split by global and local
  scope. This is the closest prior work to what we do.

Our difference is **not conceptual**. It is (i) *granularity* — we label each clause,
including the case where clauses of one sentence take different roles, rather than
partitioning a prompt into blocks; (ii) a *sign-off discipline* — every object that
decides an outcome (rule tables, thresholds, lexicons, prompt templates) is versioned
and cannot change without a human ruling; and (iii) an *extra exit* — when the
mechanical layer and the model disagree, the system neither overrides nor abstains
but **asks the user**. Section 6 states this plainly against each prior line.

In the project's decision equation B = f(I, C, R), this component is the extractor
of C — the constraints that bound an acceptable answer — and I's action/object come
from the main-request sentence. Its coupling to downstream decision and verification
is outside the scope of this release. The rounds reported here measure the extractor
in isolation against a bare 7B; they are not an acceptance test of the architecture,
and should not be read as one.

**Why an external layer rather than the weights.** Three reasons, in order of how
much evidence we have for each:

1. *Auditability.* A rule table can be read, signed, diffed and rolled back. A weight
   update cannot. Every judgement this system makes names the rule that fired.
2. *Separability of the failure.* When the system is wrong, we can say which layer was
   wrong. Section 4 reports a round that was voided because a single clause in a rule
   specification was wrong — that diagnosis is only available if the rule is a
   readable object.
3. *Cost.* The mechanical layer runs at zero model calls. On the final round it
   resolved 35 of 303 sentences outright and routed 268 to the model layer.

We note the third reason is the weakest: it is an engineering convenience, not an
argument about correctness.

An earlier line of this project (LoRA fine-tuning of a 3B model) is deposited
separately [@aibehavior2025software; @aibehavior2025preprint]; the present report does
not depend on it.

---

# 2. System

Three stages and three exits. All file references are paths inside the public
artifact at `ade2734`.

## 2.1 T1 — the mechanical layer (zero model calls)

`src/mechanical/` contains the whole of it. The layer runs a fixed set of detectors
over each clause (person, interrogative, imperative, reported speech, rhetorical
question, cognitive verbs, empty frame, mood, time anchor, constraint shape, handoff),
then applies an ordered rule list. Two axes come out:

- **Axis 1** — is this clause the *main request*, an *implicit need*, an *empty-frame
  request*, or *not a request*.
- **Axis 2** — is this clause a *constraint*, *material*, or *not applicable*.

Two kinds of signed table drive it:

| Table | File | What it fixes |
|---|---|---|
| Constraint-shape lexicon ("Table 5") | `src/mechanical/lexicon_v2.py` | Which surface forms count as evidence of a constraint |
| Numeral-classifier closed set | `src/mechanical/signed_tables/knife2_one_classifier.json` | When "one + classifier" is *naming* rather than *constraining* |
| Writing-specification exemption | `src/mechanical/lexicon_v2.py` (`v2_writing_spec_form`, 23 entries) | Which forms are specifications *about how to process material*, hence never material themselves |
| Function layer | `src/mechanical/signed_tables/function_layer.json` | When an interrogative form does not carry a request |
| Lexicon registry | `src/mechanical/signed_tables/lexicon_registry.json` | Which domains may consult which lexicon; unregistered use raises |

**Entry gates, not frames.** An earlier version of this work called the gating
conditions "frames". We have renamed them **entry gates** and we do not cite frame
semantics for them. The reason is recorded in the artifact's literature table: our
gate is a conjunction of detector signals that decides whether a lexicon may scan a
clause at all; it has no frame elements and no frame-to-frame relations, so the
borrowed term claimed more than the construct delivers. The one claim we do take from
construction grammar is narrower and survives: **the construction determines the
reading, so sentence-level structure must be settled before a lexicon is allowed to
match** [@goldberg1995].

The gates are: *main-request gate* (axis 1 is a main request → the lexicon does not
scan, axis 2 is void); *past-narrative gate*; *reported-speech gate*; *descriptive
gate* (non-first-person subject, declarative, non-past → does not scan); and
*self-report*, the catch-all, which does scan.

**Form is not Function.** An interrogative *form* does not entail a request. Austin's
distinction between what an utterance says and what it does [@austin1962], and
Searle's indirect speech acts [@searle1975], are the direct source of this. In the
system it is one rule: an interrogative clause that is *simultaneously* declarative
in mood, lacks a final question mark, and carries past aspect is an **embedded
question** and does not raise a main request. We implemented three readings of the
conjunction and measured all three; the two-condition and single-condition readings
each destroyed main-request recall (57/62 and 59/62 against a 60/62 floor), and the
three-condition reading cost nothing. The "no final question mark" condition turns
out to be *protective*, not causal: it is what keeps a genuine question with a past
aspect marker from being silently reclassified.

**A self-imposed discipline worth naming.** Rule tables that contain *pattern*
entries (e.g. "N characters") must be consumed by family, not by literal string.
Twice in this project a consumer compared a generated cue (`600 characters`) against
a table key (`N characters`) and matched nothing, so a signed table entry was
effectively unsigned. Measured across 1033 sentences, **17 of 41** constraint-shape
hits in the writing-specification family were reachable only by family matching.
`src/mechanical/clause_v2.py` now matches on the cue's `source` field.

## 2.2 T3 — the model layer

Sentences the mechanical layer routes as *material* go to a 3B instruct model
(`src/perf/run_perf.py`, `src/perf/schema_v1.py`) at temperature 0, 4-bit. Three
stations: a structured *perception* pass that fills four fields; a two-vote *filter*
(an adapter vote and a rule vote); and a *fold* that reduces to a judgement with a
coverage gate. A final adjudicator applies a fixed identity function over the fold's
output. `src/perf/early_stop.py` holds the generation stop conditions, shared
verbatim between offline validation and production so the two cannot drift.

## 2.3 Exits

`src/control/judge_v4.py` assigns every sentence one of three exits:

- **Execute** — treat as a constraint.
- **Down-weight and decline** — the signal is too weak to act on; the sentence is
  marked and not used.
- **ASK** — return a clarifying question instead of an answer.

ASK is capped at 10% of the round's sentences. The pool is ordered by a
request-form-first criterion computed from already-signed detectors with **no new
lexicon entries**; `src/control/request_form.py` carries a self-audit that inspects
its own feature functions' source and rejects any CJK comparison literal that is not
a key of a signed table.

---

# 3. Evaluation protocol

The protocol is published in full at `docs/protocol/blind-test-protocol.md`. Summary:

## 3.1 Three-party separation of duties

| Party | Does | **Does not** |
|---|---|---|
| Human principal | Sets goals, rules on proposals, signs criterion-layer objects | Does not annotate; does not run batches |
| Evaluation side (one LLM session) | Drafts the answer key, holds it, scores, drafts correction orders | Does not touch code; does not run batches |
| Executing side (a different LLM session) | Implements, runs, delivers artifacts, reports | **Never sees the answer key; does not score; does not rule** |

The two sessions share no context; the only exchange surface is a version-controlled
bridge repository. The configuration that is unusual is not the blinding — it is that
**the human is restricted to adjudication**: in the prior work we found, the key holder
is a person or a platform and the human is also one of the annotators.

This is the right place to record a consequence rather than a feature. **The executing
side cannot compute any score, including the intervals in Section 4**, because scoring
requires the answer key. Section 4 says what that costs us.

## 3.2 Seeds

Each round's sampling seed is **the timestamp of the order that opened the round**,
`YYYYMMDDHHMM`, self-checked by both sides rather than handed over as a number, and
published alongside the sampler file's SHA-256. The sampler itself is never edited;
changing rounds changes only the seed and the exclusion list. A timestamp cannot be
selected after the fact, and the sampler hash shows the filter did not change with it.

## 3.3 Answer-key freezing

Sample with the frozen sampler and that round's seed, logging every rejection code,
not only the acceptances. Exclude previously used material on two tracks — text union
and conversation hash — where what is burned is the **full candidate set**, not the
subset that survived adjudication, because the discarded candidates were seen too.
Present candidates for ruling without removing any (removal is a ruling, not an
execution step). Split articles into sentences with a splitter whose rules are fixed
and which re-runs a verbatim regression against an earlier round on every invocation.
Then the evaluation side proposes the key, the human rules flag by flag, and the
frozen key's SHA-256 goes into the release order. From that point the executing side
runs and the key does not leave the evaluation side.

## 3.4 Sentinels

Each round contains a small number of articles whose key is **entirely
"no constraints"** — narrative or copywriting pieces — to catch false positives. The
executing side knows sentinels exist and not which they are.

This corresponds to the *minimum functionality test* of behavioural testing
[@ribeiro2020checklist]. It is **not** a contrast set [@gardner2020contrast], which
requires minimal edits to one sample that flip its label; our sentinels are whole new
samples. The artifact's literature table records this as a borrowed name corrected.

## 3.5 Scoring rules

Scores count **only rounds not yet opened**. Once a round's key is revealed it becomes
design material: it may be analysed, but it may never be a score again. The two arms
are never run concurrently, since contending for one GPU makes the timing
incomparable. And "winning" is not a higher nominal score but a bootstrap 95%
interval on the *difference* that excludes zero [@koehn2004significance] — applied symmetrically to both arms.

## 3.6 What this protocol does not solve

Verbatim from the artifact, because an honest limitation is worth more than a
paraphrase of it:

1. The evaluation side is also a language model, so **its draft key may carry a
   systematic bias**. The only defences in place are flag-by-flag human ruling and the
   rule that opened rounds cannot score again. There is no third-party re-annotation.
2. The executing side's blindness is **institutional, not technical**. Nothing prevents
   it from reading any file in the bridge repository; it rests on written terms and a
   commit log, not on a sandbox.
3. Both sides come from the same model family, so **same-origin bias cannot be excluded
   by this configuration** — that is true. The same fact has another side, though: the
   two sides are same-origin, and the evaluation side still caught implementation
   divergences and inaccurate self-reports from the executing side across multiple
   rounds (one audit that compared the orders against the actual code line by line
   found seven divergences, all of them real). That indicates **the separation itself
   produced judgements a single session would not have produced**, rather than the
   model family having changed. Same-origin is a limitation *and* a control condition:
   with two different model families, a caught divergence could not be attributed to
   the separation rather than to the model difference. Both sides are recorded.

---

# 4. Results (bounded)

## 4.1 What counts

Three rounds were scored. One of them is void, and we report it rather than drop it.

| Round | Sentences | Positives | Ours (F1) | Bare 7B (F1) | All-positive baseline |
|---|---|---|---|---|---|
| 5 | 103 | 11 (10.7%) | **22.9** | **32.4** | 19.3 |
| 6 | 311 | — | *16.9* | *43.2* | 25.8 |
| 7 | 303 | 32 (10.6%) | **22.4** | **16.5** | 19.1 |

Round 6 is **void and the reason is ours**. The rule specification for article-level
sentence status used "has no first person" as the sole proxy for "this sentence is
pasted material". Writing-specification sentences (a length requirement, a format
requirement) have no first person by nature, so they were locked as material, never
reached the constraint lexicon, and were declined downstream. **22 of 36 misses in
that round came from this one clause.** It is a defect in a criterion-layer object, not
a ceiling of the approach; the repair is two exemptions, visible in the artifact as
`F1_WRITING_SPEC_EXEMPT` (`src/mechanical/clause_v2.py`) and `F2_WS_EXEMPT`
(`src/mechanical/reorder_v2.py`). Measured over 1033 sentences, the two exemptions are
**not additive** — 4 sentences move with the first alone, 7 with the second alone, 18
with both — because the same proxy lived in two gates and patching one let the other
catch what the first released.

Per-round detail for round 7:

| Account | v4.5 | Bare 7B |
|---|---|---|
| Strict F1 (constraint as positive) | 22.4 (P 15.5 / R 40.6; tp 13 / fp 71 / fn 19) | 16.5 (P 11.7 / R 28.1; tp 9 / fp 68 / fn 23) |
| Oracle (ASK counted correct when it hit) | 25.6 (30 asked, 4 hit) | — |
| Per-sentence accuracy | 70.3 | 70.0 |
| Sentinel breaks (2 articles, 10 sentences) | **0** | **4** |
| Of 115 disagreements, which side was right | 58 | 57 |

## 4.2 The interval, and a limitation of it

The paired bootstrap [@efron1979bootstrap; @koehn2004significance] over 2000 resamples
gives a 95% interval on
(bare 7B - v4.5) of **-19.0 to +7.3**. It contains zero. The nominal 5.9-point lead
therefore does not survive the test the protocol commits to in advance, and we do not
claim a win.

**That interval resamples sentences, and sentences in this corpus are not
independent.** Each article contributes several sentences that share an article-level
task string and an article-level status; the correct unit is the article, i.e. a
*cluster bootstrap* [@efron1993bootstrap, ch. 8]. Resampling sentences understates the
interval's width, so the honest reading is that the true interval is **at least this
wide** — which does not change the conclusion, since this one already contains zero.

The key-holding side recomputed it as a cluster bootstrap over the 64 articles
(2000 resamples): 95% interval **-19.2 to +6.6** (a second seed: -18.8 to +7.0). It is
not wider than the sentence-level interval; the sentence-level estimate was not
materially optimistic on this round. The conclusion is unchanged. **The executing side
cannot reproduce this number, by design (§3.1)**; it is reported by the party that
holds the key.

This is the separation of duties doing the work it was built for rather than only
constraining us: the party that cannot compute a number says so, and the party that
can, computes it.

## 4.3 Three conclusions we can write

**(a) We cannot claim parity with or superiority to a bare 7B.** Two valid rounds,
one loss and one win, and the win's interval contains zero. The all-positive baseline
(19.1 on round 7) is close to both arms, which is what a 10.6% positive rate does to
F1; the measurement is weak in exactly the regime we tested.

**(b) Sentinel false positives differ, in the same direction across both rounds.**
Framework 0/10 and 1/7; bare 7B 4/10 and 5/7. The bare model classifies narrative
copywriting and a truncated self-report as constraint-bearing; the framework does not.
This is the one difference we would defend, and its mechanism is visible: the
descriptive and past-narrative entry gates keep the constraint lexicon from scanning
those clauses at all.

**(c) The false-positive populations have different shapes.** Our 71 false positives
on round 7 are 54 from the model layer accepting a fold judgement on article-level
material plus 17 from mechanical direct acceptance (year expressions and a few
idiomatic numeral forms still in the classifier table). The bare model's 68 include
the sentinels. Same count, different failure mode — and only one of those two is
addressable by editing a table.

**(d) — not a conclusion, a shared ceiling.** All 19 of our misses on round 7 had an
**empty constraint-shape hit set**: they are requirements expressed with no lexical
form at all (change the phrasing, be more sincere, use higher-register vocabulary,
simpler language, shorter, emphasise X). The 3B fold answers "no" to that whole group.
The bare 7B misses 23 of the same group. **Neither path reaches them.** No amount of
lexicon work addresses a constraint that has no surface form; this is the boundary of
the approach as built.

## 4.4 Latency

The acceptance line for round 7 was 1059.0 s, scaled from an earlier round by sentence
count. Measured: **1309.7 s, 23.7% over**. The decomposition is multiplicative: the
share of sentences entering the model layer rose from 76.7% to 88.4% (×1.152), and the
cost per such sentence rose from 3.686 s to 4.873 s (×1.322).

The per-sentence rise is concentrated in the filter station, and the cause is
instructive about early stopping: the stop condition fires only when the adapter
answers "no", so only that group is cheap. That group's cost is near-identical across
three rounds (4.0 tokens, 0.385–0.410 s). What changed is the other group — its share
went 10.1% → 29.1% → 30.6%, and its generation length went 11.9 → 28.7 tokens.

This also undermines the line itself. The line was extrapolated from the round whose
"yes" rate was 10.1%, and two later independent rounds both sit near 30%. **The
baseline round is the outlier, so the line is mis-specified rather than the pipeline
degraded.** We report the overrun as a failed acceptance line and do not re-derive the
line after the fact.

---

# 5. Failure theory: the connection that was never there

The theory this project works from is stated in
`docs/theory/runaway-mechanism_theory-and-literature.md`, and was deposited earlier in its own right
[@logicalaios2026runaway]. Its claim is an **integration of four
factors** rather than a new factor:

1. *Goal fidelity* — the system does not deviate from the purpose it was given.
2. *Pattern retrieval with no applicability check* — similar is adopted as applicable.
3. *No causal layer* — human decisions run on causal structure; this does not have that
   component.
4. *No alarm* — there is no mechanism for an expectation to fail.

Together: at the edge of the covered region, the system **confidently executes a
similar-but-wrong solution**.

**Nearest relative.** [@mccoy2024embers] reaches a structurally similar place by a
teleological route — deriving failure modes from the objective the model was trained
on. We treat it as the closest prior work, not as something we extend.

**The parts each have an owner.** Pattern retrieval without an applicability check is
shortcut learning. The absent causal layer is the competence-without-comprehension
line. The absent alarm has a specific modern source: training and evaluation reward
guessing over admitting uncertainty, so a system optimised as a test-taker guesses
[@kalai2025hallucinate].

**What is ours, narrowly.** Not any of the four factors. The claim is the
*integration* — and one step inside it: the literature mostly assumes a connection
between stating a rule and following it, and asks why the connection broke. We assume
**the connection was never built**, and read "said one thing, did another" as three
independent retrievals on three different terrains with no link between them. The
measurement literature is consistent with this and is extensive: words-and-deeds
inconsistency around 30%, with alignment on one side transferring poorly and
unpredictably to the other [@xu2025wdct]; knows-but-violates rates from 8% to 99%
[@driftbench2026]; textual refusal not transferring to tool-call behaviour
[@cartagena2026gap]. Those papers measure the gap. They do not generally offer the
mechanism, and that is the slot we are filling.

**On self-reports.** A model's stated reason is not evidence of its actual process:
chain-of-thought explanations can systematically misstate the cause, and injected
biasing features go unmentioned while accuracy drops by up to 36 points
[@turpin2023cot]. Circuit-level work gives the complementary picture — the stated
text and the internal path can diverge [@anthropic2025biology]. The project's own
behavioural record of this is in
`docs/theory/behavioral-confabulation_mechanism-and-literature.md`, kept to a neutral summary
(an incorrect attribution of who did what; reporting a time with a
verified tone and no tool call, four times asserting it had checked; and
under-counting its own errors in real time), with the mechanism hypotheses marked
**unverified**. We cite it for one point only: the condition under which it happened
was **the rule being present and known**, and we found no literature testing that
condition directly.

**A live instance, bounded.** In October 2026 an AI-vs-AI StarCraft benchmark
published a rule that competitors could practise against reference bots but **not read
their source code** [@hillclimb2026rules]. The organiser reported that one entrant
obtained a copy of a stronger human-written bot while struggling to advance, and
rolled the entrant's code back on 2 October to strip it; the organiser's feed reports
that the entrant subsequently cleared the top tier on its own
[@mcpheeters2026post].

The artifact's literature table records this row as of the commit that accompanies
this report; it was added after the initial artifact release, so a reader checking an
earlier snapshot of that table will not find it.

We cite this as **specification gaming, not a say-do gap.** The distinction matters
and we are keeping to it: the reasoning trace was not published, so there is no
evidence about what the system represented about the rule, and attributing a
"knew-the-rule-and-violated-it" structure would be exactly the inference our own
§3.6(1) warns against. What it does illustrate is the weaker and sufficient point: **a
rule stated in text is not an execution-layer gate.** Independent code review of the
rollback is not available; the timeline is the organiser's.

---

# 6. Related work

Four lines. Each paragraph ends with our difference from it, stated as a difference and
not as an advance.

**(i) Instruction hierarchy and constraint separation.** [@zverev2025sep] formalises
instruction-data separation and provides a benchmark; all tested models separate
poorly and prompt engineering and fine-tuning both help little. [@wallace2024hierarchy]
trains the privilege ordering directly. [@agentif2025] partitions prompts into task,
context and constraint with global and local constraint scope. [@followbench2024] and
[@structflow2025] build constraint taxonomies and extract atomic constraint
expressions. *Our difference:* clause-level labelling inside a single source — the
user's own request — serving a downstream ASK decision, rather than a
trust boundary or a prompt-block partition. The concept is not ours.

**(ii) External guards and rules overriding models.** [@rebedea2023nemo] provides
runtime programmable rails defined in a modelling language, independent of the
underlying model and requiring no fine-tuning — architecturally this is the same claim
we make. [@coucke2018snips] runs a deterministic parser first and a probabilistic one
only when the first extracts nothing; that cascade shape predates ours by seven years.
[@katz2020guarded] names the construct we use for rules beating models — hand-written
**override rules** that overwrite a network's decision when stated conditions hold —
and [@alshiekh2018shielding] synthesises a **shield** from a temporal-logic
specification that corrects an action only when it is unsafe. [@plguard2026] grounds
predicates neurally and reasons symbolically over them. *Our difference:* the
sign-off and regression discipline around the rule table, and a third branch where
disagreement produces a question rather than an override or an abstention. Not the
architecture.

**(iii) Clarifying questions and abstention.** Asking for a missing slot in a
closed-schema dialogue system is standard and documented in textbooks, including the
three-threshold confidence policy (reject / explicit confirm / implicit confirm /
accept) [@jurafsky2024slp3]; learnable clarification policies condition on information
gain and a confidence ceiling [@padmakumar2020clarification]. Abstention has its own
origin in the reject option [@chow1970reject] and its modern framing in learning to
defer, which also shows that pure confidence-threshold deferral is suboptimal because
it ignores the recipient [@madras2018defer; @verma2022calibrated]; a recent position
paper argues abstention should be a design principle and notes that the external
verifier may be a symbolic reasoner or a domain rule engine [@abstention2026vision].
*Our difference is one we want to state precisely, because it is easy to overclaim:*
the abstention literature's action space ends at *not answering* — IDK, or an output
set. **Asking is a different action, not a better one.** A clarifying question is the
step after declining: naming the missing slot and asking for it. The mechanism of
"rule layer decides not to answer" is prior work; what we did not find a same-shaped
instance of is the combination of open-domain operation, three slots fixed by a
behaviour equation, and the ask built into the normalisation pipeline rather than
bolted on as a refusal layer. The nearest items are a seven-field intent decomposition
[@intentgov2026] and conservative normalisation that never fills an unknown slot
[@scop2026].

**(iv) Separation of duties in evaluation.** Withholding test labels from the model's
developer is standard practice, and its effect on leaderboard overfitting has been
measured at scale [@roelofs2019metaanalysis]. Scorers placed outside the model under
hidden tests are documented [@chen2026scorer]. Red/blue separation with
design-time visibility and run-time blinding is established in auditing-game work
[@auditinggames2026; @factortu2026]. And the requirement that creator and evaluator
agents must not share context — because an agent running the optimisation loop grades
its own work — is stated explicitly in the AI-scientist verification-gap literature
[@aiscientists2026survey]. *Our difference:* the key holder here is itself a language
model and the human is confined to adjudication. Every component has prior work; we
did not find the combination, and that is the most we claim.

---

# 7. Honest limitations

Collected rather than scattered, and ordered by how much they would change a reader's
conclusion.

1. **The headline comparison is inconclusive.** One scored loss, one scored win whose
   interval contains zero. §4.3(a).
2. **The headline interval was first computed on the wrong resampling unit**
   (sentences); the key-holding side recomputed it by article and the width did not
   change (§4.2). The number is reproducible only by the key holder.
3. **One of three scored rounds is void by our own defect**, and the defect was in a
   criterion-layer specification, not in code. §4.1.
4. **A shared ceiling we cannot cross as built**: constraints with no lexical form.
   §4.3(d).
5. **The latency acceptance line failed** at 23.7% over, and our own analysis says the
   line's baseline round was an outlier — which is a reason to distrust the line, not a
   reason to pass. §4.4.
6. **Borrowed names, corrected.** The gating conditions are not frame-semantic frames;
   our sentinels are not contrast sets; the "empty-frame request" category has no
   support in speech-act theory and is an engineering category. All three are recorded
   as borrowed in `docs/literature_mapping.md`.
7. **Two of three originality candidates are prior work** and the third is partial
   overlap, by our own search. §6 and the artifact's literature table.
8. **The protocol's three unsolved problems**, verbatim in §3.6: a possibly biased key
   drafter, institutional rather than technical blinding, same-origin sides.
9. **Scale.** Seven rounds, 1134 sentences total, one model pair, one language.
   Positive rates near 10% make F1 a noisy instrument in exactly this regime.
10. **Public hashes do not match internal hashes.** The published code has
    corpus-derived examples and one identifier redacted, so `manifest/v45_manifest`
    (internal) and `manifest/public_manifest` (this release) differ by construction.
    Verifying "is this the file that was sealed" therefore takes two steps rather than
    one. `PUBLIC_NOTES.md` §3.
11. **Two entries of the 2026-09-24 hash commitment cannot be checked against this
    release**: one names a file not included here, and one names a file that has been
    modified in the rounds since, so its fingerprint no longer matches the current
    version. The commitment refers to sealed point-in-time artifacts; this release is
    not that reveal.

---

# 8. Reproducibility

This report is deposited as [@logicalaios2026v12].

| Item | Value |
|---|---|
| Artifact | `https://github.com/blackwing04/Logical-AI-OS` |
| Commit | `846037e997b77cb06bac872d687ff196e6ea3e9b` |
| Files | 41 in the repository at that commit (36 added at the first release `ade2734`, 1 pre-existing hash-commitment file untouched, 4 added later) |
| Per-file hashes of this release | `manifest/public_manifest.md` (39 of the 41; the two it cannot cover are itself) |
| Hashes of the internal sealed build | `manifest/v45_manifest.md` (31 components, walked from the import graph rather than hand-listed) |
| Code license | MIT, `LICENSE` |
| Document license | CC BY 4.0, `LICENSE-docs` |
| This report | CC BY 4.0 |
| This report's DOI | [10.5281/zenodo.23226740](https://doi.org/10.5281/zenodo.23226740) |

The version number **v1.2** follows the project's internal numbering; the two earlier
versions were internal working drafts and were never published.

The files in commit `ade2734` carry Chinese filenames; this report cites the
commit after the ASCII rename. **Eight of the nine renamed files are byte-identical
to `ade2734`.** The ninth — the round-6 results file — differs by exactly one line:
it links to the round-7 results file, whose name also changed, so the link had to be
updated or it would point at a file that no longer exists. The old-to-new mapping is
in the artifact's `MANIFEST.md` section 7, and the renamed files carry the same
hashes as in `ade2734`.

The commit above also carries the English `README.md` and `PUBLIC_NOTES.md`
with their Traditional Chinese counterparts, and `docs/PORTING.md`, which states
which parts of this measurement layer are language-independent, which must be
rebuilt for another language, and which cannot be translated at all.

**What is reproducible and what is not.** The judgement chain runs on any input you
supply: `src/` is complete and self-contained for that. The signed tables and the
complete flag state are published. Every number in §4 has its attribution chain in
`results/`.

**The seven rounds' numbers are not reproducible from this release**, because the
evaluation corpus is not in it. The corpus derives from a public dataset of real user
conversations; we do not redistribute any user sentence, and the answer keys are not
published because publishing them would void the rounds. This is a deliberate
limitation, not an omission — and it means the reported scores rest on the protocol in
§3 rather than on independent recomputation.

---

# 9. References

See `references.bib`. Every entry has a verifiable locator. Items recorded in the
artifact's literature table as **provenance pending** are deliberately **not cited**
here: specifically, a journal version's volume and DOI for one entry, two entries where
the project's notes give only an author name, and two figure numbers we could not
confirm in the source. Where a claim in this report would have rested on one of those,
we either cite the preprint instead or drop the claim.

---

# Appendix A. Chinese abstract（中文摘要）

> This appendix is the Chinese-language abstract. The body of this report
> (sections 0 to 9) is in English; this is the only section in Chinese.
> The same text ships separately as `abstract_zh.md` for the Zenodo
> description field.

## A.1 The three sentences

本研究建了一個外部的、零推論成本的機械層，逐子句分離使用者請求中「對答案的限制」
與「待處理的材料」，並搭一個 3B 模型處理機械層定不了的部分；缺口走**反問**而不猜。

在專案的決策公式 B = f(I, C, R) 裡，本零件是 **C 的抽取器**——界定「可接受答案」的
那些限制——而 I 的動作與受詞來自主請求句。**它與下游決策與驗證的接法不在本次發佈
範圍內。** 本報告所報的各卷，量的是這個抽取器**單獨對比裸 7B**，不是整體架構的
驗收，不應如此解讀。

七輪盲測中（答案本由另一方持有、執行端全程不可見），該配置在一卷得 F1 **22.9**
而裸 7B 得 **32.4**，在另一卷得 **22.4** 而裸 7B 得 **16.5**；後者的配對 bootstrap
95% 區間為 **-19.0 至 +7.3**，含零（以**篇**為重抽單位重算為 **-19.2 至 +6.6**，
未變寬；該數由持答案本的一方計算，執行端依設計無法重現）。

**因此不能宣稱「外部框架加 3B」追上或勝過裸 7B**；能報告的是兩卷同向的兩項差異
——守側哨兵的偽陽性（框架 0/10、1/7 對裸 7B 4/10、5/7）與偽陽性族群的形狀不同
——以及兩臂共同撞到的一道天花板：**無字面形狀的語義限制，兩條路徑都抓不到**。

---

## A.2 Points to be read alongside

**一卷作廢，而原因在我方。** 三卷計分卷中有一卷因判準層規格的一處條文錯誤而作廢：
該條把「無第一人稱」當成「此句為貼上的材料」的唯一代理，而字數、格式這類寫作規格句
天生沒有第一人稱，於是被鎖成材料、碰不到限制詞表。該卷 36 句漏抓中有 **22 句**出於
這一條。那是判準層物件的缺陷，不是方法的上限；修法在產物中可見。

**區間的重抽單位是錯的。** 報告的區間以**句**重抽，但同篇句子共享篇級任務字串與
篇級地位，正確單位是**篇**（cluster bootstrap）。以句重抽會低估區間寬度，所以真實
區間**至少這麼寬**——這不改變結論，因為它已經含零。**而我方無法重算**：cluster
bootstrap 需要逐句對錯，逐句對錯需要答案本，而依協定執行端從不持有答案本，公開產物
也不含答案本。此事列為未結項，不作估算。這是「盲是真的」與「這個數字拿不到」的同一
個協定性質；我們認為這筆交換是對的，並把代價說出來，不藏。

**借名三處，已更正。** 進場閘不是框架語義的 frame（已改稱 entry gate、不引
Fillmore）；守側哨兵對應的是行為測試的 minimum functionality test，**不是** contrast
set；「空框請求」在言語行為論中無對應範疇，是工程類別。三處都記在產物的文獻對照表。

**三件原創候選，兩件是已有前作、一件部分重疊**，由我方自己的檢索認定。外部守衛與
規則否決模型都有成文設計名稱（override rules、shield）；確定性層先跑、抽不到才跑
機率層的級聯形狀比本研究早七年。可主張的差異只在粒度、簽核制度，與「吵架→反問」
這一條出口。

**效能驗收線未過**（超 23.7%），而我方自己的拆帳指出那條線的基準卷是離群值
——這是不該信那條線的理由，不是過關的理由。

**評測協定沒解決的三件事**原文照錄於正文 §3.6：擬答案本的一方也是語言模型、
執行端的盲是制度性而非技術性、兩端同源。第三件另記一面：兩端同源而評測端仍多輪抓出
執行端的實作偏離與自述不實（一次逐條對帳查出七處偏離、全部屬實），表示分權配置本身
產生了單一工作階段不會產生的判斷。**同源是限制，也是對照條件**——若換異源，抓到的
偏離就無法歸因於分權而非模型差異。兩面都記。

---

## A.3 What cannot be reproduced from this artifact

七輪的數字**不可由本產物重算**，因為評測語料不在其中。語料衍生自一個公開的真實使用者
對話資料集，本產物不重新散布任何使用者原句；答案本不公開，因為公開等於作廢那些卷。
這是刻意的限制而非疏漏，也意味著所報成績**靠的是 §3 那套協定，不是獨立重算**。

可重現的是：判定鏈在任何自備輸入上的行為（`src/` 完整自足）、簽核表與完整旗標狀態
（`manifest/`）、以及 §4 每個數字的歸因鏈（`results/`）。
