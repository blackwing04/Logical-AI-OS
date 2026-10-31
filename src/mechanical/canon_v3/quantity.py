# Public copy of the internal `scripts/canon_v3/quantity.py` (unchanged since before the v4.5 seal, 2026-10-06).
# One docstring word changed; one loop variable renamed in one function. Code unchanged. Record: PUBLIC_NOTES.md section 7.
"""Quantity annotator: recognise quantities in the raw text without rewriting it.

gen-3 architecture. Before this, L1 rewrote Chinese numerals into Arabic digits so that a
digit-based cue pattern could see them. That made every misjudgement an input contamination:
the rewritten text fed every atomic judgement on the row and no downstream layer could see that
the input had been damaged, because the miscollection count checks what was collected and
never whether the input was intact. Defending it required an open set of guards and exclusions,
each added because the last mistake demanded it.

Here the text is left alone and the recognition moves to the cue layer, where the three-layer
net already exists. A false annotation is collection noise, which is catchable. The parsed
value lives in metadata and is never shown in the text; a confirmation ASK still quotes the
original sentence by unit id.

The signed guards carry over unchanged in meaning. They stop being rules about what to rewrite
and become rules about what counts as a quantity mention.
"""
from __future__ import annotations

import re

from .lexicon import (
	MEASURE_WORD_EXCLUSIONS,
	TABLE5_MEASURE_WORD_TERMS,
	TABLE5_UNIT_TERMS,
)

# Closed grammar. Nothing outside these characters is a Chinese numeral.
CHINESE_DIGITS: dict[str, int | float] = {
	"零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
	"五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
	"兩": 2, "半": 0.5,
}
SMALL_UNITS: dict[str, int] = {"十": 10, "百": 100, "千": 1000}
LARGE_UNITS: dict[str, int] = {"萬": 10000, "億": 100000000}
DECIMAL_MARK = "點"

_NUMERAL_CHARS = "".join([*CHINESE_DIGITS, *SMALL_UNITS, *LARGE_UNITS, DECIMAL_MARK])

# Approximate forms. A run of two or more bare digits with an optional magnitude means "around
# this many": 三四千, 二三十. There is no single value to report.
AMBIGUOUS_RUN = re.compile(r"^[一二三四五六七八九兩]{2,}(?:十|百|千|萬|億)?$")

# Hedges that make a nearby quantity approximate. Left-side hedges precede the number, right-side
# ones follow it.
APPROXIMATE_LEFT = ("幾", "大概", "大約", "約", "差不多", "將近", "接近", "起碼", "至少", "頂多")
APPROXIMATE_RIGHT = ("上下", "左右", "出頭", "多")

# Determiners that make a following numeral part of a determiner phrase rather than a count:
# 哪一個, 這一次, 每一天, 第一次. Carried over from the signed L1 guard, unchanged in meaning.
DETERMINER_GUARD = "哪這那每某任第"

# 半 keeps its own left guard. 上半年, 下半年, 多半, 大半 are lexicalised. 下 must not join the
# general guard: 剩下一個小時 is a real quantity.
HALF_LEFT_GUARD = "上下多大"

# Measure words that count as quantity carriers. Exclusions are already filtered out of the
# signed table, and are re-stated here so the annotator reads as one place.
MEASURE_TERMS = tuple(term for term in TABLE5_MEASURE_WORD_TERMS if term not in MEASURE_WORD_EXCLUSIONS)

_ARABIC = r"\d+(?:\.\d+)?"
_CHINESE = r"[" + _NUMERAL_CHARS + r"]+"
_NUMERAL = r"(?:" + _ARABIC + r"|" + _CHINESE + r")+"
_MEASURE_ALT = "|".join(map(re.escape, MEASURE_TERMS))
_UNIT_ALT = "|".join(map(re.escape, TABLE5_UNIT_TERMS))

# A quantity mention is a numeral followed by a unit, or by a measure word, optionally with the
# measure word sitting between the numeral and the unit. The unit-bearing branch comes first so
# 5個月 annotates as 5個月 rather than stopping at 5個.
QUANTITY_PATTERN = re.compile(
	r"(?P<numeral>" + _NUMERAL + r")\s*"
	r"(?:"
	r"(?P<measure1>" + _MEASURE_ALT + r")?\s*(?P<unit>" + _UNIT_ALT + r")"
	r"|(?P<measure2>" + _MEASURE_ALT + r")"
	r")"
)


def parse_numeral(surface: str) -> tuple[float | int | None, bool]:
	"""Parse a numeral surface into a value, and say whether it is approximate.

	Returns `(None, True)` for approximate runs such as 三四千, where reporting a single number
	would be a claim the text does not make.
	"""
	surface = surface.strip()
	if not surface:
		return None, False
	if AMBIGUOUS_RUN.match(surface):
		return None, True
	if DECIMAL_MARK in surface:
		whole, _mark, fraction = surface.partition(DECIMAL_MARK)
		whole_value, approximate = parse_numeral(whole) if whole else (0, False)
		if whole_value is None:
			return None, True
		digits = "".join(str(int(CHINESE_DIGITS[char])) for char in fraction if char in CHINESE_DIGITS)
		if not digits:
			return whole_value, approximate
		return float(f"{whole_value}.{digits}"), approximate

	total = 0
	section = 0
	number: float | int = 0
	pending = False
	last_unit = 0
	# 零 is a place holder: it says the digit after it sits at the lowest place, which is what
	# separates 一百零一 (101) from 兩千五 (2500). Seeing one disables the shorthand below.
	shorthand_blocked = False
	index = 0
	while index < len(surface):
		char = surface[index]
		if char.isdigit():
			run = index
			while run < len(surface) and (surface[run].isdigit() or surface[run] == "."):
				run += 1
			chunk = surface[index:run]
			number = float(chunk) if "." in chunk else int(chunk)
			pending = True
			index = run
			continue
		if char in CHINESE_DIGITS:
			number = CHINESE_DIGITS[char]
			pending = True
			if char == "零":
				shorthand_blocked = True
		elif char in SMALL_UNITS:
			unit = SMALL_UNITS[char]
			section += (number if pending else 1) * unit
			number = 0
			pending = False
			last_unit = unit
		elif char in LARGE_UNITS:
			unit = LARGE_UNITS[char]
			section = (section + number) if (section or pending) else 1
			total += section * unit
			section = 0
			number = 0
			pending = False
			last_unit = unit
		else:
			return None, False
		index += 1

	# A bare digit left at the end is shorthand for the next place down: 兩千五 is 2500 and 3萬5
	# is 35000, while 一百二十三 is 123 because the last unit there was 十.
	if pending and last_unit >= 10 and not shorthand_blocked:
		number = number * (last_unit // 10)
	value = total + section + number
	if isinstance(value, float) and value.is_integer() and DECIMAL_MARK not in surface and "." not in surface:
		integral = int(value)
		return (integral if float(integral) == value else value), False
	return value, False


def _is_approximate_context(text: str, start: int, end: int) -> bool:
	left = text[max(0, start - 4):start]
	right = text[end:end + 2]
	if any(left.endswith(hedge) for hedge in APPROXIMATE_LEFT):
		return True
	return any(right.startswith(hedge) for hedge in APPROXIMATE_RIGHT)


def _guard_blocks(text: str, start: int, numeral: str) -> bool:
	"""Signed guards, restated as recognition rules rather than rewriting rules."""
	previous = text[start - 1] if start > 0 else ""
	if previous and previous in DETERMINER_GUARD:
		return True
	if numeral.startswith("半") and previous and previous in HALF_LEFT_GUARD:
		return True
	# 零 is admitted before a unit but not before a measure word: 零 plus a measure word is not
	# how a quantity is said, while 零件, 零錢 and 零食 are word formation.
	return False


def annotate_quantities(text: str) -> list[dict[str, object]]:
	"""Find quantity mentions in `text`. The text is never modified."""
	annotations: list[dict[str, object]] = []
	for match in QUANTITY_PATTERN.finditer(text):
		numeral = match.group("numeral")
		measure = match.group("measure1") or match.group("measure2") or ""
		unit = match.group("unit") or ""
		# 萬 is both a magnitude in the grammar and a member of the signed 5a unit table, so a
		# mention like 100萬 matches with 萬 parsed as the unit and the value read as 100. The
		# magnitude belongs to the number. Resolved here in the recognition layer rather than by
		# editing a signed table.
		if not measure and (unit in SMALL_UNITS or unit in LARGE_UNITS):
			numeral, unit = numeral + unit, ""
		if _guard_blocks(text, match.start("numeral"), numeral):
			continue
		if numeral.startswith("零") and not unit:
			continue
		value, ambiguous = parse_numeral(numeral)
		approximate = ambiguous or _is_approximate_context(text, match.start(), match.end())
		annotations.append(
			{
				"surface": match.group(0),
				"start": match.start(),
				"end": match.end(),
				"numeral": numeral,
				"measure": measure,
				"unit": unit,
				"value": value,
				"approximate": approximate,
			}
		)
	return annotations
