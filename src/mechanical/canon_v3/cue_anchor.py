# Public copy of the internal `scripts/canon_v3/cue_anchor.py` (unchanged since before the v4.5 seal, 2026-10-06).
# Name-redacted (internal handle -> PI, 1 place); corpus-redacted (4 examples). Code unchanged. Record: PUBLIC_NOTES.md section 7.
"""C3: cue_anchor_rule v1 -- a cue hit is not yet a constraint.

Stage B collected 52 items against a gold of 9. The failure is not that the cue list is wrong;
it is that a cue hit was treated as sufficient. Appendix A2-a fixes the operative definition,
and its third criterion is the one that bites: a quantity or a prohibition with nothing to
measure or exclude against does not become a constraint by carrying a cue word.

These are mechanisms, not name lists. A list of bad cues is an open set -- one entry per mistake
already made, the N+1 shape the read-only L1 reversal was about. A criterion is closed.

Withdrawn 2026-08-22 by PI: an earlier draft excluded every cue inside an A0=yes unit. It wrote
the 200-bank's register shape (a question is not a constraint) into a rule, and on the 48-grid,
where constraints are routinely embedded in the request, it cut gold recall from 24 to 4. The
lesson is kept here because the replacement below has the same temptation available to it: a
rule must be about what a constraint IS, not about where this corpus happens to put one.
"""
from __future__ import annotations

from .lexicon import TABLE5_LIMITING_HEAD_PATTERN
from .quantity import annotate_quantities

CUE_ANCHOR_RULE_VERSION = 1

INTERROGATIVE_LEFT_NEIGHBOUR = "要"


def limiting_head_is_interrogative_frame(text: str, start: int) -> bool:
	"""Rule 2: a limiting head whose left neighbour is 要 is the tail of a 要不要 question frame.

	要不要 is one interrogative morpheme wearing the surface of a prohibition.
	"""
	return start > 0 and text[start - 1] == INTERROGATIVE_LEFT_NEIGHBOUR


def row_has_objective_parameter(unit_texts: list[str]) -> bool:
	"""Criterion 3, branch (a): does the row carry anything convertible at all?

	A unit-bearing quantity -- 24小時, 兩萬, 三天 -- is measurable against the world by an outside
	reader. A bare measure word -- 一部, 一遍, 一句 -- is not. The test is at row level because a
	constraint's anchor need not sit in the same sentence: a bare one-plus-measure-word count can be anchored by
	the budget or the setting stated a sentence earlier (example corpus-redacted).
	"""
	for text in unit_texts:
		for annotation in annotate_quantities(text):
			if str(annotation.get("unit") or ""):
				return True
	return False


def _quantity_in(text: str) -> bool:
	return bool(annotate_quantities(text))


def _limiting_head_in(text: str) -> bool:
	return any(
		not limiting_head_is_interrogative_frame(text, match.start())
		for match in TABLE5_LIMITING_HEAD_PATTERN.finditer(text)
	)


def cue_is_anchored(cue: dict[str, object], *, unit_text: str, objective_parameter_in_row: bool) -> tuple[bool, str]:
	"""Return (anchored, reason). Reason names the branch that decided it."""
	source = str(cue.get("source"))

	if source == "table5_limiting_head":
		# A prohibition needs something checkable to exclude. 不要超過兩萬 excludes a number;
		# 不要 before a complaint about style (example corpus-redacted) excludes nothing an outside
		# reader could adjudicate.
		#
		# The target may sit on either side. The signed table holds both grammars: 不要, 只能,
		# 最多 take what follows, while 內, 以內, 以上, 為止, 封頂 are postpositions and take what
		# precedes -- a budget written as a number followed by 內 puts the number in front of the head
		# (example corpus-redacted). Requiring the target to
		# follow cost 09a and 09b their budget, which is a fact about Chinese word order and not
		# about those rows.
		if _quantity_in(unit_text):
			return True, "limiting_head_with_measurable_target"
		if objective_parameter_in_row:
			return True, "limiting_head_under_row_objective_parameter"
		return False, "limiting_head_without_verifiable_exclusion_target"

	if objective_parameter_in_row:
		return True, "row_carries_objective_parameter"

	value = cue.get("value")
	if isinstance(value, (int, float)) and value > 1:
		# Criterion 2, non-empty exclusion space. Asking for a method already implies one, so
		# 一個方法 rules nothing out; 十個方法 rules out every answer with fewer than ten.
		return True, "count_above_the_unmarked_default"

	if _limiting_head_in(unit_text):
		# A count of one under 只能 (example corpus-redacted): the cap is what makes the one restrictive, and 只能 is signed Table 5.
		return True, "count_of_one_under_a_limiting_head"

	return False, "unmarked_count_excludes_nothing"


def partition_cues(cues: list[dict[str, object]], *, unit_text: str, objective_parameter_in_row: bool) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
	kept: list[dict[str, object]] = []
	dropped: list[dict[str, object]] = []
	for cue in cues:
		if not isinstance(cue, dict):
			continue
		anchored, reason = cue_is_anchored(cue, unit_text=unit_text, objective_parameter_in_row=objective_parameter_in_row)
		(kept if anchored else dropped).append({**cue, "anchor_reason": reason})
	return kept, dropped


def anchor_audit_entry(*, sid: str, text: str, dropped: list[dict[str, object]]) -> dict[str, object]:
	return {
		"sid": sid,
		"text": text,
		"rule": "cue_anchor_rule",
		"cue_anchor_rule_version": CUE_ANCHOR_RULE_VERSION,
		"dropped": [{"cue": str(cue.get("cue")), "reason": str(cue.get("anchor_reason"))} for cue in dropped],
	}
