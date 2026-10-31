"""Excerpt of the internal `scripts/canon_v3/prompts.py`: the two table-5 functions only, verbatim.

The rest of that file builds the prompts of the model-labelling tool and is not published. The two functions
below call nothing in it. Record: PUBLIC_NOTES.md section 7.
"""
from __future__ import annotations

from .cue_anchor import limiting_head_is_interrogative_frame
from .lexicon import TABLE5_LIMITING_HEAD_PATTERN
from .quantity import annotate_quantities


def build_table5_cue_phrase(text: str, start: int, end: int) -> str:
	left_boundary = max(text.rfind(mark, 0, start) for mark in ["，", "。", "？", "！", "；", ",", "\n"])
	right_candidates = [index for index in [text.find(mark, end) for mark in ["，", "。", "？", "！", "；", ",", "\n"]] if index >= 0]
	right_boundary = min(right_candidates) if right_candidates else len(text)
	phrase = text[left_boundary + 1 : right_boundary].strip()
	if len(phrase) <= 15:
		return phrase
	cue = text[start:end]
	space = max(0, 15 - len(cue))
	left_take = min(start - left_boundary - 1, max(0, space // 2 + space % 2))
	right_take = min(right_boundary - end, max(0, space // 2))
	phrase = text[start - left_take : end + right_take].strip()
	if len(phrase) <= 15:
		return phrase
	return cue


def detect_table5_constraint_cues(text: str) -> list[dict[str, str]]:
	cues: list[dict[str, str]] = []
	# gen-3: quantities are recognised in the text as it stands, never rewritten. The parsed
	# value rides along in metadata; the cue phrase quoted to the model is always the original.
	for annotation in annotate_quantities(text):
		cues.append(
			{
				"cue": str(annotation["surface"]),
				"source": "table5_numeric_unit",
				"phrase": build_table5_cue_phrase(text, int(annotation["start"]), int(annotation["end"])),
				"value": annotation["value"],
				"approximate": annotation["approximate"],
				"unit": annotation["unit"],
				"measure": annotation["measure"],
			}
		)
	for match in TABLE5_LIMITING_HEAD_PATTERN.finditer(text):
		# C3 rule 2: 要不要 is one interrogative morpheme, not 要 followed by a prohibition.
		if limiting_head_is_interrogative_frame(text, match.start()):
			continue
		cues.append({"cue": match.group(0), "source": "table5_limiting_head", "phrase": build_table5_cue_phrase(text, match.start(), match.end())})
	return cues
