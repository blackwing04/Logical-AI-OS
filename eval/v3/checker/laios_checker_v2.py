# -*- coding: utf-8 -*-
"""LAIOS constraint checker v2 (standalone).

Rule-based, zero-model checker that decides, for each constraint item extracted
from a prompt, whether an answer violates it. Every checker returns one of:

    True   the answer satisfies the item
    False  the answer violates the item
    None   the item cannot be decided on this answer (it is left out of any rate)

This module is a self-contained re-implementation of the frozen research
checker (v1 base checkers plus the v2 structural-parsing revision). It depends
only on the Python standard library, `lemminflect==0.2.3`, and two character
mapping tables shipped next to this file:

    zh_t2s_table.json   Traditional -> Simplified, used by the v1 copy / echo checkers
    zh_s2t_table.json   Simplified -> Traditional, used by v2 term matching

Both tables are equal-length mappings derived from the OpenCC dictionaries
(Apache-2.0) and are applied by greedy longest match, left to right, without
word segmentation.

Public API
----------
check_items(items, answer, exclude=())       v2 verdicts  {sid: True | False | None}
check_items_v1(items, answer)                v1 verdicts  {sid: True | False | None}
check_items_detailed(items, answer, version="v2", exclude=())
                                             {sid: (verdict, detail)}

Each item is a dict with keys `sid`, `check_type` (string), `check_arg`
(JSON value) and `weight`. Items whose `check_type` is "other" are skipped.

Scoping: for the types listed in SCOPED_TYPES the checker sees only the
"deliverable" part of the answer (see `deliverable_of`); all other types see
the whole answer.

`exclude` names check types for which the v1 checker is kept instead of the
v2 revision; `exclude=("length",)` reproduces the "v2 without the character
count revision" variant.

What this module deliberately does not contain: topic / embedding scoring,
retry or patching logic, length control during generation, and the rules that
read constraint items out of the prompt text. Item lists therefore have to be
supplied by the caller (see README.md).

String literals in CJK characters are part of the matching logic and must not
be edited.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

__all__ = ["check_items", "check_items_v1", "check_items_detailed", "deliverable_of",
           "SCOPED_TYPES", "zh_trad", "zh_norm", "__version__"]
__version__ = "2.0.0"

_HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Character mapping tables (equal-length, greedy longest match, no segmentation)
# ---------------------------------------------------------------------------
_TABLES: dict[str, tuple[dict[str, str], int]] = {}


def _table(name: str) -> tuple[dict[str, str], int]:
	if name not in _TABLES:
		data = json.loads((_HERE / name).read_text(encoding="utf-8"))
		tbl = data["map"]
		if not tbl:
			raise ValueError("empty mapping table: %s" % name)
		for k, v in tbl.items():
			if len(k) != len(v):
				raise ValueError("non equal-length mapping in %s: %r -> %r" % (name, k, v))
		_TABLES[name] = (tbl, max(len(k) for k in tbl))
	return _TABLES[name]


def _apply_table(text: str, name: str) -> str:
	if not text:
		return text or ""
	tbl, mx = _table(name)
	out, i, n = [], 0, len(text)
	while i < n:
		for L in range(min(mx, n - i), 0, -1):
			v = tbl.get(text[i:i + L])
			if v is not None:
				out.append(v)
				i += L
				break
		else:
			out.append(text[i])
			i += 1
	s = "".join(out)
	assert len(s) == len(text), "mapping changed the text length"
	return s


def zh_norm(text: str) -> str:
	"""Traditional -> Simplified folding (used by the v1 copy / echo checkers)."""
	return _apply_table(text, "zh_t2s_table.json")


def zh_trad(text: str) -> str:
	"""Simplified -> Traditional folding (used by v2 term matching)."""
	return _apply_table(text, "zh_s2t_table.json")


_CJK_RE = re.compile(r"[一-鿿]")


def cjk_bigrams(text: str) -> set[str]:
	"""CJK character bigrams after Traditional -> Simplified folding."""
	t = zh_norm(text or "")
	return {t[i:i + 2] for i in range(len(t) - 1)
	        if _CJK_RE.match(t[i]) and _CJK_RE.match(t[i + 1])}


# ===========================================================================
# v1 base checkers. Signature: (answer: str, arg) -> (verdict, detail)
# ===========================================================================


def _count_chars(s: str) -> int:
	"""v1 character count: number of non-whitespace characters."""
	return len(re.sub(r"\s", "", s))


_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")


def _count_words(s: str) -> int:
	"""Word count for English deliverables: runs starting with a Latin letter or digit."""
	return len(_WORD_RE.findall(s or ""))


def _check_length(ans: str, arg):
	if not isinstance(arg, dict) or arg.get("n") is None:
		return None, "incomplete arg"
	n, op = int(arg["n"]), arg.get("op", ">=")
	by_words = arg.get("unit") in ("詞", "words")
	got = _count_words(ans) if by_words else _count_chars(ans)
	label = "words" if by_words else "chars"
	if op == "~":
		# "about N": +-20% tolerance (a guideline value, not a derived threshold)
		lo, hi = n * 0.8, n * 1.2
		return lo <= got <= hi, "%s %d vs %d+-20%% (%.0f-%.0f)" % (label, got, n, lo, hi)
	ok = got >= n if op == ">=" else got <= n
	return ok, "%s %d %s %d" % (label, got, op, n)


_ZH = re.compile(r"[一-鿿]")
# Glyph-difference characters: these only discriminate when the two scripts differ;
# neutral or mixed text yields None rather than a guess.
_SIMP_ONLY = set("这么国说对时过还运动单测试验产业书见图长门开关问间东车马龙")
_TRAD_ONLY = set("這麼國說對時過還運動單測試驗產業書見圖長門開關問間東車馬龍")


def _check_language(ans: str, arg):
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	want = arg.get("lang")
	zh = len(_ZH.findall(ans))
	latin = len(re.findall(r"[A-Za-z]", ans))
	if want == "en":
		if zh == 0 and latin > 0:
			return True, "no CJK, has Latin"
		if zh > 0:
			return False, "English required but %d CJK characters" % zh
		return None, "undecidable (no CJK and no Latin)"
	if want in ("zh", "zh-TW", "zh-CN"):
		if zh == 0:
			return False, "Chinese required but no CJK characters"
		if want == "zh":
			return True, "%d CJK characters" % zh
		s = sum(1 for c in ans if c in _SIMP_ONLY)
		t = sum(1 for c in ans if c in _TRAD_ONLY)
		if s == 0 and t == 0:
			return None, "script undecidable (0 glyph-difference hits)"
		if want == "zh-TW":
			return t >= s, "traditional %d / simplified %d" % (t, s)
		return s >= t, "simplified %d / traditional %d" % (s, t)
	return None, "unsupported language code: %s" % want


def _check_language_forbidden(ans: str, arg):
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	ban = arg.get("lang")
	zh = len(_ZH.findall(ans))
	latin = len(re.findall(r"[A-Za-z]", ans))
	if ban == "en":
		return latin == 0, "Latin letters %d" % latin
	if ban in ("zh", "zh-TW", "zh-CN"):
		return zh == 0, "CJK characters %d" % zh
	return None, "unsupported language code: %s" % ban


_SENT_SPLIT = re.compile(r"[。！？!?；;\n]+")
_LEAD_STRIP = "「『“\"'（(【[《〈 　\t*-#・·—"
_TITLE_SUFFIX = ("老師", "老师", "先生", "小姐", "女士", "博士", "經理", "经理", "總", "总",
                 "哥", "姐", "叔", "阿姨", "同學", "同学", "師父", "师父", "師伯", "师伯", "王", "公子")
_LEAD_WORDS = ("說", "说", "道", "問", "问")
_FUNC_CHARS = "的了是在和與及這那我你他她它們这那有不也都着著了過过就才又還还很更"
_PRONOUNS = {"自己", "大家", "我們", "我们", "他們", "他们", "她們", "她们", "對方", "对方",
             "彼此", "別人", "别人", "有人", "眾人", "众人"}


def _protagonist(material: str):
	"""Most frequent titled / speaking name in the material (2-3 CJK chars, seen >= 2 times)."""
	cnt: dict[str, int] = {}
	func = _FUNC_CHARS
	suf = "|".join(re.escape(s) for s in sorted(_TITLE_SUFFIX, key=len, reverse=True))

	def add(x: str):
		i = 0
		while i < len(x) and x[i] in func:
			i += 1
		x = x[i:]
		if 2 <= len(x) <= 3 and not any(ch in func for ch in x):
			cnt[x] = cnt.get(x, 0) + 1

	for m in re.finditer(r"([一-鿿]{2,3})(?:%s)" % suf, material or ""):
		add(m.group(1))
	for m in re.finditer(r"([一-鿿]{2,3})(?:%s)" % "|".join(_LEAD_WORDS), material or ""):
		add(m.group(1))
	cand = {k: (material or "").count(k) for k in cnt if k not in _PRONOUNS}
	cand = {k: v for k, v in cand.items() if v >= 2}
	if not cand:
		return None, 0
	name = max(cand, key=lambda k: (cand[k], len(k)))
	return name, cand[name]


def _first_person_ratio(ans: str):
	"""(share of sentences containing the first-person pronoun U+6211, share with it in the
	first six chars, hits, sentences)."""
	sents = [s.strip().lstrip(_LEAD_STRIP) for s in _SENT_SPLIT.split(ans or "") if s.strip()]
	sents = [s for s in sents if s]
	if not sents:
		return 0.0, 0.0, 0, 0
	hit = sum(1 for s in sents if "我" in s)
	head = sum(1 for s in sents if "我" in s[:6])
	return hit / len(sents), head / len(sents), hit, len(sents)


def _check_person(ans: str, arg):
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	ratio, head, hit, n = _first_person_ratio(ans)
	if arg.get("person") == "third":
		return ratio <= 0.15, "first-person sentence ratio %.2f (%d/%d, third person needs <= 0.15)" % (ratio, hit, n)
	name, m_cnt = _protagonist(arg.get("material_text") or "")
	ok_ratio = ratio >= 0.3
	base = "first-person sentence ratio %.2f (%d/%d, needs >= 0.30)" % (ratio, hit, n)
	if name and m_cnt > 0:
		a_cnt = (ans or "").count(name)
		ok_name = a_cnt <= m_cnt / 3
		return ok_ratio and ok_name, "%s; protagonist material %d -> answer %d (needs <= %.1f)" % (base, m_cnt, a_cnt, m_cnt / 3)
	return ok_ratio, base + "; no protagonist found, ratio only"


def _check_relative_length(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("material_chars"):
		return None, "incomplete arg (no material length)"
	m = int(arg["material_chars"])
	got = _count_chars(ans)
	mode, r = arg.get("mode"), float(arg.get("ratio") or 0)
	if mode == "expand":
		return got >= r * m, "answer %d vs material %d x %.1f (expand: >=)" % (got, m, r)
	if mode == "shrink":
		return got <= r * m, "answer %d vs material %d x %.1f (shrink: <=)" % (got, m, r)
	return None, "unsupported mode: %s" % mode


def _check_copy_ratio(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("material_text"):
		return None, "incomplete arg (no material text)"
	# Both sides are folded before the bigram step (which folds again; kept as in the frozen code).
	a, m = cjk_bigrams(zh_norm(ans or "")), cjk_bigrams(zh_norm(arg["material_text"]))
	if len(a) < 10:
		return None, "answer has %d CJK bigrams, too short" % len(a)
	ov = len(a & m) / len(a)
	mx = float(arg.get("max_overlap") or 0.90)
	return ov <= mx, "bigram overlap %.3f (> %.2f means copied)" % (ov, mx)


_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*・•]|\d+[.)、．]|[（(]?\d+[）)]|[一二三四五六七八九十]+[、.])\s*(.+?)\s*$", re.M)
_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿️]")
_PUNCT_RE = re.compile(r"[，。、；：！？「」『』（）《》〈〉【】…—－,.;:!?\"'()\[\]<>~`@#$%^&*_+=|\\/]")
_EN_WORD_RE = re.compile(r"[A-Za-z]{2,}")


def _strip_sentence(s: str) -> str:
	return re.sub(r"[\s，。、；：！？「」『』（）《》〈〉【】…—,.;:!?\"'()\[\]]", "", s)


def _list_items(ans: str) -> list[str]:
	"""List items: bulleted / numbered lines; else >= 3 short lines; else a >= 5-part enumeration."""
	items = [m.group(1) for m in _LIST_ITEM_RE.finditer(ans or "")]
	if len(items) >= 2:
		return items
	lines = [l.strip() for l in (ans or "").splitlines() if l.strip()]
	if len(lines) >= 3 and all(len(l) <= 40 for l in lines):
		return lines
	parts = [p.strip(" 「」『』《》\"'") for p in re.split(r"[、，,]", ans or "") if p.strip()]
	if len(parts) >= 5 and all(len(p) <= 20 for p in parts):
		return parts
	return items


def _check_verbatim_sentence_ratio(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("material_text"):
		return None, "incomplete arg (no material)"
	mat = _strip_sentence(zh_norm(arg["material_text"]))
	sents = [_strip_sentence(zh_norm(s)) for s in _SENT_SPLIT.split(ans or "") if s.strip()]
	sents = [s for s in sents if len(s) >= 6]
	if len(sents) < 3:
		return None, "%d comparable sentences (< 3)" % len(sents)
	frac = float(arg.get("sentence_match") or 0.9)
	hit = 0
	for s in sents:
		L = len(s)
		w = max(6, int(L * frac + 0.999))
		if any(s[i:i + w] in mat for i in range(0, L - w + 1)):
			hit += 1
	ratio = hit / len(sents)
	mx = float(arg.get("max_ratio") or 0.5)
	return ratio <= mx, "verbatim sentences %d/%d = %.2f (> %.2f means copied)" % (hit, len(sents), ratio, mx)


def _check_list_unique_ratio(ans: str, arg):
	items = [_strip_sentence(x) for x in _list_items(ans)]
	items = [x for x in items if x]
	if len(items) < 3:
		return None, "%d list items (< 3)" % len(items)
	uniq = len(set(items))
	r = uniq / len(items)
	mn = float((arg or {}).get("min_unique") or 0.8)
	return r >= mn, "list items %d, unique %d, ratio %.2f (needs >= %.2f)" % (len(items), uniq, r, mn)


def _check_per_item_length(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("n"):
		return None, "incomplete arg"
	n = int(arg["n"])
	items = [_strip_sentence(x) for x in _list_items(ans)]
	items = [x for x in items if x]
	if len(items) < 2:
		return None, "%d list items (< 2)" % len(items)
	ok = sum(1 for x in items if len(x) == n)
	r = ok / len(items)
	mn = float(arg.get("min_ok") or 0.8)
	return r >= mn, "items of exactly %d chars: %d/%d = %.2f (needs >= %.2f)" % (n, ok, len(items), r, mn)


def _check_forbidden_charset(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("classes"):
		return None, "incomplete arg"
	# For list answers only the item bodies are checked (list markers removed).
	items = _list_items(ans)
	if len(items) >= 2:
		ans = "\n".join(items)
	hits = []
	for cls in arg["classes"]:
		if cls == "digits" and re.search(r"[0-9０-９]", ans):
			hits.append(cls)
		elif cls == "latin" and re.search(r"[A-Za-z]", ans):
			hits.append(cls)
		elif cls == "punct" and _PUNCT_RE.search(ans):
			hits.append(cls)
		elif cls == "emoji" and _EMOJI_RE.search(ans):
			hits.append(cls)
		elif cls == "comma" and re.search(r"[，,]", ans):
			hits.append(cls)
		elif cls == "period" and re.search(r"[。．]", ans):
			hits.append(cls)
		elif cls == "upper" and re.search(r"[A-Z]", ans):
			hits.append(cls)
	return not hits, ("forbidden classes present: %s" % "/".join(hits)) if hits else "no forbidden class present"


def _check_self_insertion(ans: str, arg):
	m = re.search(r"Qwen|通义千问|通義千問|我是[^，。]{0,8}(?:AI|人工智慧|人工智能|語言模型|语言模型|智能助手|智慧助理|助手)", ans or "")
	return (m is None), ("model self-insertion found") if m else "no self-insertion"


def _title_line(ans: str) -> str:
	for l in (ans or "").splitlines():
		s = l.strip()
		if s:
			s = s.lstrip("#*- ").strip()
			m = re.search(r"[《「『“\"]([^》」』”\"]+)[》」』”\"]", s)
			return m.group(1) if m else s
	return ""


def _check_term_required_in_title(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("term"):
		return None, "incomplete arg"
	x = arg["term"]
	title = _title_line(ans)
	ok = x in title
	return ok, "title %s the term" % ("contains" if ok else "does not contain")


def _check_role_third_person(ans: str, arg):
	"""Prompt says "you are X": X used >= min_hits times as a third-person subject or dialogue tag = violation."""
	if not isinstance(arg, dict) or not arg.get("role"):
		return None, "incomplete arg"
	x = arg["role"]
	a = ans or ""
	names = {x, x.replace("·", "").replace("・", "")}
	if not any(nm in a for nm in names):
		return True, "role not mentioned in third person"
	n_subj = n_label = 0
	for nm in names:
		e = re.escape(nm)
		n_subj += len(re.findall(r"(?:^|[。！？；：\n，、「」『』“”\[\]（）()])\s*" + e + r"(?:也|又|便|就|才|卻|却|還|还|則|则)?(?![的，,。、])[一-鿿]", a))
		n_label += len(re.findall(r"(?m)^\s*" + e + r"\s*[:：]", a))
		n_label += len(re.findall(r"[\[【][^\]】]{0,10}[:：]?\s*" + e + r"\s*[\]】]", a))
	n = n_subj + n_label
	mn = int(arg.get("min_hits") or 2)
	return n < mn, "role as third-person subject %d (subject %d, tag %d; >= %d means role reversed)" % (n, n_subj, n_label, mn)


def _check_task_echo(ans: str, arg):
	"""The answer merely repeats the request (>= 80% of its instruction part)."""
	if not isinstance(arg, dict) or not arg.get("request"):
		return None, "incomplete arg"
	raw_req = arg["request"] or ""
	# Long requests often embed the material: keep only the instruction part before the first opener.
	instr = re.split(r"[（(：:“「\"]", raw_req, maxsplit=1)[0] if len(raw_req) > 40 else raw_req
	req = _strip_sentence(zh_norm(instr))
	a = _strip_sentence(zh_norm(ans or ""))
	frac = float(arg.get("min_echo") or 0.8)
	echo, how = False, ""
	if len(req) >= 8 and a:
		w = max(8, int(len(req) * frac + 0.999))
		if any(req[i:i + w] in a for i in range(0, len(req) - w + 1)) and len(req) >= 0.5 * len(a):
			echo, how = True, "instruction"
	if not echo and a:
		n_sent = len([s for s in _SENT_SPLIT.split(ans or "") if s.strip()])
		for q in re.findall(r"[“「\"]([^”」\"]{6,})[”」\"]", raw_req):
			if "？" not in q and "?" not in q:
				continue
			qn = _strip_sentence(zh_norm(q))
			if qn and qn in a and len(qn) >= 0.9 * len(a) and n_sent <= 1:
				echo, how = True, "quoted question"
				break
	if len(req) < 8 and not echo:
		return None, "instruction part too short (%d chars)" % len(req)
	return (not echo), ("answer echoes the request (%s)" % how) if echo else "no request echo"


def _check_script_mix(ans: str, arg):
	"""CJK-dominant answer containing >= min_words distinct English words not in the material."""
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	if arg.get("wants_en"):
		return None, "request asks for English, not checked"
	a = ans or ""
	zh = len(_ZH.findall(a))
	all_words = _EN_WORD_RE.findall(a)
	if zh < 50 or zh < 2 * len(all_words):
		return None, "answer is not CJK-dominant (CJK %d, English words %d)" % (zh, len(all_words))
	words = {w.lower() for w in all_words}
	mat_words = {w.lower() for w in _EN_WORD_RE.findall(arg.get("material_text") or "")}
	novel = words - mat_words
	mn = int(arg.get("min_words") or 8)
	if len(mat_words) >= mn:
		return None, "material itself has %d English words, not checked" % len(mat_words)
	return len(novel) < mn, "English words %d (outside material %d; >= %d means mixed)" % (len(words), len(novel), mn)


def _check_format(ans: str, arg):
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	f = arg.get("format")
	if f == "json":
		s = ans.strip()
		# A ```json fence is tolerated.
		m = re.search(r"```(?:json)?\s*(.+?)```", s, re.S)
		if m:
			s = m.group(1).strip()
		try:
			json.loads(s)
			return True, "parses with json.loads"
		except Exception as ex:
			return False, "JSON parse error: %s" % str(ex)[:60]
	if f == "title":
		n = len(re.findall(r"<<[^<>\n]+>>", ans))
		need = int(arg.get("n") or 1)
		return n >= need, "<<title>> count %d (needs >= %d)" % (n, need)
	if f == "markdown":
		ok = bool(re.search(r"^#{1,6}\s|\*\*.+?\*\*|^[-*]\s|^\d+\.\s", ans, re.M))
		return ok, "markdown markup found" if ok else "no markdown markup"
	if f == "table":
		ok = bool(re.search(r"^\s*\|.*\|\s*$", ans, re.M))
		return ok, "table row found" if ok else "no table row"
	if f in ("bullets", "numbered"):
		pat = r"^\s*[-*・]\s" if f == "bullets" else r"^\s*\d+[.)、]\s"
		n = len(re.findall(pat, ans, re.M))
		return n >= 2, "matching lines %d (needs >= 2)" % n
	if f == "csv":
		lines = [l for l in ans.strip().splitlines() if l.strip()]
		ok = len(lines) >= 2 and all("," in l for l in lines[:3])
		return ok, "lines %d, first three contain commas = %s" % (len(lines), ok)
	if f in ("yaml", "html"):
		pat = r":\s" if f == "yaml" else r"<[a-zA-Z][^>]*>"
		ok = bool(re.search(pat, ans))
		return ok, "%s markers = %s" % (f, ok)
	return None, "unsupported format: %s" % f


def _check_count(ans: str, arg):
	"""Count check. Only "fewer than required" is a violation; more items is accepted (deliberate asymmetry)."""
	if not isinstance(arg, dict) or arg.get("n") is None:
		return None, "incomplete arg"
	n, unit = int(arg["n"]), arg.get("unit", "")
	bullets = len(re.findall(r"^\s*(?:[-*・]|\d+[.)、])\s", ans, re.M))
	if unit in ("段", "章", "節"):
		got = len([b for b in re.split(r"\n\s*\n", ans.strip()) if b.strip()])
		label = "paragraphs"
	elif bullets:
		got, label = bullets, "bullets"
	else:
		got = len([b for b in re.split(r"\n\s*\n", ans.strip()) if b.strip()])
		label = "paragraphs (no bullets)"
	if got == 0:
		return None, "no countable unit (%s)" % label
	return got >= n, "%s %d, required >= %d" % (label, got, n)


def _check_term_required(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("terms"):
		return None, "incomplete arg"
	k = int(arg.get("min_count") or 1)
	miss = [w for w in arg["terms"] if ans.count(w) < k]
	return not miss, ("missing %d term(s)" % len(miss)) if miss else "all required terms present"


def _check_term_forbidden(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("terms"):
		return None, "incomplete arg"
	hit = [w for w in arg["terms"] if w in ans]
	return not hit, ("%d forbidden term(s) present" % len(hit)) if hit else "no forbidden term present"


def _check_structure(ans: str, arg):
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	need = arg.get("need")
	if need == "paragraphs" and arg.get("n"):
		k = int(arg["n"])
		n = len([b for b in re.split(r"\n+", ans.strip()) if b.strip()])
		return n >= k, "paragraphs %d (needs >= %d, single newline split)" % (n, k)
	if need == "paragraphs":
		n = len([b for b in re.split(r"\n\s*\n", ans.strip()) if b.strip()])
		return n >= 2, "paragraphs %d (needs >= 2)" % n
	if need == "heading":
		ok = bool(re.search(r"^#{1,6}\s|^\S.{0,30}[:：]\s*$", ans, re.M))
		return ok, "heading line = %s" % ok
	if need in ("opening", "closing", "summary"):
		# Semantic requirements without a surface form are not decidable here.
		return None, "'%s' is semantic, not checkable by rule" % need
	return None, "unsupported structure need: %s" % need


_SENT_END110 = re.compile(r"[。！？!?．\n]|(?<![0-9])\.|\.(?![0-9])")


def count_sentences(ans: str) -> int:
	return len([x for x in _SENT_END110.split(ans or "") if re.search(r"[0-9A-Za-z一-鿿]", x)])


def _check_sentence_count(ans: str, arg):
	if not isinstance(arg, dict) or arg.get("n") is None:
		return None, "incomplete arg"
	n, op = int(arg["n"]), arg.get("op", ">=")
	got = count_sentences(ans)
	if op == "~":
		lo, hi = n * 0.8, n * 1.2
		return lo <= got <= hi, "sentences %d vs %d+-20%%" % (got, n)
	ok = got >= n if op == ">=" else got <= n
	return ok, "sentences %d %s %d" % (got, op, n)


def _check_case(ans: str, arg):
	if not isinstance(arg, dict) or arg.get("case") not in ("lower", "upper"):
		return None, "incomplete arg"
	bad = re.findall(r"[A-Z]" if arg["case"] == "lower" else r"[a-z]", ans or "")
	if not re.search(r"[A-Za-z]", ans or ""):
		return None, "no Latin letters, case not checkable"
	return not bad, ("%d letters of the wrong case" % len(bad)) if bad else "case satisfied"


V1_CHECKERS = {
	"length": _check_length,
	"language": _check_language,
	"language_forbidden": _check_language_forbidden,
	"person": _check_person,
	"relative_length": _check_relative_length,
	"copy_ratio": _check_copy_ratio,
	"verbatim_sentence_ratio": _check_verbatim_sentence_ratio,
	"list_unique_ratio": _check_list_unique_ratio,
	"per_item_length": _check_per_item_length,
	"forbidden_charset": _check_forbidden_charset,
	"self_insertion": _check_self_insertion,
	"term_required_in_title": _check_term_required_in_title,
	"role_third_person": _check_role_third_person,
	"task_echo": _check_task_echo,
	"script_mix": _check_script_mix,
	"format": _check_format,
	"count": _check_count,
	"term_required": _check_term_required,
	"term_forbidden": _check_term_forbidden,
	"structure": _check_structure,
	"sentence_count": _check_sentence_count,
	"case": _check_case,
}


# ---------------------------------------------------------------------------
# Deliverable scoping: language / length / format-like checkers judge the
# deliverable, not the whole answer (e.g. a Chinese lead-in before an English
# e-mail). Rules, in order: code fence, horizontal-rule split, lead-in phrase;
# otherwise the whole answer (scope "whole").
# ---------------------------------------------------------------------------
_DELIV_LEADIN = ("以下是", "如下：", "如下:", "下面是", "這是", "以下為",
                 "以下：", "以下:", "内容如下", "內容如下")
SCOPED_TYPES = frozenset({
	"language", "language_forbidden", "length", "format", "person", "relative_length", "copy_ratio",
	"forbidden_charset", "per_item_length", "list_unique_ratio", "verbatim_sentence_ratio",
	"term_required_in_title", "sentence_count", "case"})


def deliverable_of(answer: str) -> tuple[str, str]:
	"""Return (deliverable text, scope) with scope in {"deliverable", "whole"}."""
	if not answer or not answer.strip():
		return answer, "whole"
	fences = re.findall(r"```[a-zA-Z0-9_-]*\s*\n(.*?)```", answer, re.S)
	if fences:
		best = max(fences, key=lambda s: len(s.strip()))
		if best.strip():
			return best.strip(), "deliverable"
	parts = [p for p in re.split(r"\n\s*-{3,}\s*\n", answer) if p.strip()]
	if len(parts) >= 2:
		best = max(parts, key=lambda s: len(s.strip()))
		if best.strip():
			return best.strip(), "deliverable"
	for cue in _DELIV_LEADIN:
		i = answer.find(cue)
		if i >= 0:
			tail = answer[i + len(cue):].lstrip("：:\n 　")
			if len(tail.strip()) >= max(20, len(answer) * 0.3):
				return tail.strip(), "deliverable"
	return answer, "whole"


# ===========================================================================
# v2 revision (structural parsing). Replaces nine v1 checkers:
#   format, count, structure, term_required, term_required_in_title, person,
#   term_forbidden, language, length.
# ===========================================================================
_BUL = r"[-*・•‧][ \t]+"
_NUM = r"(?:\d{1,3}[.)、．](?!\d)|[（(]\d{1,3}[）)])"
_ZHN = r"[一二三四五六七八九十]{1,3}[、．.]"
_PRE = r"^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*)?"
_LIST = re.compile(_PRE + r"(?:%s\S|(?:%s|%s)[ \t]*(?:\S|$))" % (_BUL, _NUM, _ZHN), re.M)
_NUMONLY = re.compile(_PRE + r"(?:%s|%s)[ \t]*(?:\S|$)" % (_NUM, _ZHN), re.M)
_TABLE = re.compile(r"^\s*\|.*\|\s*$")
_TSEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)*\|?\s*$")
_INLINE = re.compile(r"(?<![\d.])(\d{1,2})[.、)．](?!\d)")


def list_lines(ans: str) -> int:
	"""Bulleted lines plus numbered lines (Arabic or Chinese ordinals, ASCII or full-width
	delimiters, parenthesised numbers), optional leading ### / **."""
	return len(_LIST.findall(ans or ""))


def table_rows(ans: str) -> int:
	"""Markdown table data rows (header and separator excluded when a separator row exists)."""
	n, block = 0, []
	for l in (ans or "").splitlines() + [""]:
		if _TABLE.match(l):
			block.append(l)
			continue
		if block:
			sep = sum(1 for b in block if _TSEP.match(b))
			n += max(0, len(block) - (sep + 1 if sep else 0))
			block = []
	return n


def _json_blobs(ans: str) -> list:
	out, s = [], ans or ""
	cands = re.findall(r"```(?:json)?\s*(.+?)```", s, re.S) + [s]
	for c in cands:
		c = c.strip()
		for a, b in (("{", "}"), ("[", "]")):
			i, j = c.find(a), c.rfind(b)
			if 0 <= i < j:
				try:
					out.append(json.loads(c[i:j + 1]))
				except Exception:
					pass
	return out


def json_items(ans: str) -> int:
	"""Length of the longest JSON array found in the answer."""
	best = 0

	def walk(v):
		nonlocal best
		if isinstance(v, list):
			best = max(best, len(v))
			for x in v:
				walk(x)
		elif isinstance(v, dict):
			for x in v.values():
				walk(x)
	for b in _json_blobs(ans):
		walk(b)
	return best


def inline_seq(ans: str) -> int:
	"""Longest in-line run numbered from 1 (1. 2. 3. on one line); only runs >= 2 count."""
	best = 0
	for l in (ans or "").splitlines():
		nums = [int(m.group(1)) for m in _INLINE.finditer(l)]
		k = 0
		for x in nums:
			if x == k + 1:
				k += 1
		if k >= 2:
			best = max(best, k)
	return best


def invisible(text: str) -> tuple[list[str], list[str]]:
	"""(non-ASCII space code points (Zs), suspicious invisible code points (Cf/Cc/Zl/Zp))."""
	ws, sus = set(), set()
	for ch in text or "":
		if ord(ch) < 128:
			continue
		cat = unicodedata.category(ch)
		if cat == "Zs":
			ws.add("U+%04X" % ord(ch))
		elif cat in ("Cf", "Cc", "Zl", "Zp"):
			sus.add("U+%04X" % ord(ch))
	return sorted(ws), sorted(sus)


def _v2_check_format(ans: str, arg):
	if isinstance(arg, dict) and arg.get("format") in ("bullets", "numbered"):
		f = arg["format"]
		n = len((_LIST if f == "bullets" else _NUMONLY).findall(ans or ""))
		return n >= 2, "v2 matching lines %d (needs >= 2)" % n
	ok, detail = _check_format(ans, arg)
	if isinstance(arg, dict) and arg.get("format") == "json" and ok is False:
		# Invisible characters: pure-space ones are normalised and retried;
		# format / control characters are not normalised and stay invalid.
		ws, sus = invisible(ans)
		if sus:
			return False, "v2 %s; suspicious characters %s" % (detail, ",".join(sus))
		if ws:
			norm = "".join(" " if unicodedata.category(c) == "Zs" else c for c in ans)
			ok2, d2 = _check_format(norm, arg)
			return ok2, "v2 after normalising %s: %s" % (",".join(ws), d2)
	return ok, detail


_OPENER = re.compile(r"以下|如下|當然|当然|好的|沒問題|没问题|這是|这是|下面|為您|为您|[:：]\s*$")
_CLOSER = re.compile(r"希望|如有|如果您|若有|若您|請告訴|请告诉|請隨時|请随时|歡迎|欢迎|祝您|祝你|有任何")


def _deliver_en(ans: str) -> str:
	"""Strip only leading / trailing Chinese courtesy lines (CJK-dominant, <= 60 chars) and separators."""
	lines = (ans or "").splitlines()
	zh_major = lambda l: len(_ZH.findall(l)) > len(re.findall(r"[A-Za-z]", l))
	sep = lambda l: not l.strip() or re.fullmatch(r"\s*[-=*_]{3,}\s*", l) is not None
	courtesy = lambda l, rx: zh_major(l) and len(l.strip()) <= 60 and rx.search(l) is not None
	i, j = 0, len(lines)
	while i < j and (sep(lines[i]) or courtesy(lines[i], _OPENER)):
		i += 1
	while j > i and (sep(lines[j - 1]) or courtesy(lines[j - 1], _CLOSER)):
		j -= 1
	return "\n".join(lines[i:j])


def _v2_check_language(ans: str, arg):
	if isinstance(arg, dict) and arg.get("lang") == "en":
		body = _deliver_en(ans)
		if body.strip() and body.strip() != (ans or "").strip():
			ok, d = _check_language(body, arg)
			return ok, "v2 after stripping courtesy lines: %s" % d
	return _check_language(ans, arg)


def _v2_check_count(ans: str, arg):
	if not isinstance(arg, dict) or arg.get("n") is None:
		return None, "incomplete arg"
	n, unit = int(arg["n"]), arg.get("unit", "")
	if unit in ("段", "章", "節"):
		return _check_count(ans, arg)
	ll, tr, js, il = list_lines(ans), table_rows(ans), json_items(ans), inline_seq(ans)
	got = max(ll + tr, js, il)
	if got == 0:
		got = len([b for b in re.split(r"\n\s*\n", (ans or "").strip()) if b.strip()])
		label = "paragraphs (no list structure)"
	else:
		label = "v2 list %d + table rows %d / JSON items %d / inline run %d, max" % (ll, tr, js, il)
	if got == 0:
		return None, "no countable unit (%s)" % label
	return got >= n, "%s %d, required >= %d" % (label, got, n)


_SENT_END = "。！？!?；;"
_HEAD_LEADIN = ("好的", "以下是", "以下為", "下面是", "如下", "這是", "这是", "當然", "当然")


def _strip_marks(s: str) -> str:
	return s.strip().lstrip("#").strip().strip("*_").strip()


def heading_found(ans: str) -> tuple[bool, str]:
	lines = [l for l in (ans or "").splitlines() if l.strip()]
	if not lines:
		return False, "empty answer"
	if re.search(r"^#{1,6}\s|^\S.{0,30}[:：]\s*$", ans, re.M):
		return True, "markdown heading or short colon line"
	for l in lines:
		s = l.strip()
		if re.match(r"^(?:\*\*)?(?:標題|标题|題目|题目|Title|TITLE)\s*[:：]", s):
			return True, "explicit title line"
		if re.fullmatch(r"【[^】]+】|《[^》]+》|\*\*[^*]+\*\*[:：]?|\*[^*]+\*|_[^_]+_", s):
			return True, "whole-line marked title"
		if re.fullmatch(r"(?:\*\*)?[一二三四五六七八九十]{1,3}[、．.].{1,30}?(?:\*\*)?", s) and not s.rstrip("*").endswith(tuple(_SENT_END)):
			return True, "Chinese ordinal section line"
	f = _strip_marks(lines[0])
	if f and len(f) <= 40 and not f.endswith(tuple(_SENT_END + "，,")) and not f.startswith(_HEAD_LEADIN + ("{", "[", "`")):
		return True, "first line is a title"
	return False, "no heading line"


def _v2_check_structure(ans: str, arg):
	if isinstance(arg, dict) and arg.get("need") == "heading":
		ok, why = heading_found(ans)
		return ok, "v2 heading = %s (%s)" % (ok, why)
	return _check_structure(ans, arg)


def _fold(s: str) -> str:
	return zh_trad(s or "")


_LATIN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9'’\- ]*$")
_UPOS = ("NOUN", "VERB")      # noun and verb inflections only; adjective comparatives are not expanded


def word_forms(term: str) -> set[str]:
	"""Dictionary inflection set of an English word (LemmInflect 0.2.3; OOV plural rule as fallback). Lower case."""
	from lemminflect import getAllInflections, getAllInflectionsOOV, getAllLemmas
	w = term.lower()
	lemmas = {w} | {l for up in _UPOS for l in getAllLemmas(w, upos=up).get(up, ())}
	forms = set(lemmas)
	for lm in lemmas:
		inf = {k: v for k, v in getAllInflections(lm).items() if k.startswith(("NN", "VB"))}
		if not inf:
			inf = getAllInflectionsOOV(lm, "NOUN")
		forms |= {x.lower() for v in inf.values() for x in v}
	return forms


def term_count(text: str, term: str) -> int:
	"""Occurrences of a term.

	CJK-containing terms: substring count after Simplified -> Traditional folding of both sides.
	Single Latin word: word-boundary match of its inflection set, case-insensitive.
	Multi-word Latin phrase: fixed expression, word-boundary match, case-insensitive, any whitespace run.
	"""
	t = (term or "").strip()
	if not t:
		return 0
	if not _LATIN.match(t):
		return _fold(text).count(_fold(t))
	if " " in t:
		pat = r"(?<![A-Za-z0-9])" + r"\s+".join(re.escape(w) for w in t.split()) + r"(?![A-Za-z0-9])"
	else:
		pat = r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])" % "|".join(re.escape(f) for f in sorted(word_forms(t), key=len, reverse=True))
	return len(re.findall(pat, text or "", re.I))


_QO, _QC = "[“「『\"'‘]", "[”」』\"'’]"
_CUE_BEFORE = r"(?:避免|不使用|未使用|沒有使用|不含|不包含|包含|含有|融入|使用了|用了|加入|提到|強調|突出|確保|涵蓋|不出現|出現|保留|符合)"
_CUE_AFTER = r"(?:一詞|這個詞|這一詞|這個關鍵詞|這一關鍵詞|關鍵詞|關鍵字|二字|兩字|這個詞彙|詞彙|一詞條|這一詞條|詞條|的使用|的出現)"


def strip_meta(ans: str, term: str) -> str:
	"""Drop sentences that talk about the constraint itself: the term is quoted and a
	constraint cue sits right next to the quote (within 8 chars before, or immediately after)."""
	t = (term or "").strip()
	if not t:
		return ans or ""
	q = _QO + r"\s*" + re.escape(_fold(t).lower()) + r"\s*" + _QC
	pat = re.compile(_CUE_BEFORE + r"[^。！？!?\n]{0,8}?" + q + "|" + q + r"\s*" + _CUE_AFTER)
	parts = re.split(r"(?<=[。！？!?；;\n])", ans or "")
	return "".join("" if pat.search(_fold(s).lower()) else s for s in parts)


def _v2_check_term_required(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("terms"):
		return None, "incomplete arg"
	k = int(arg.get("min_count") or 1)
	miss = [w for w in arg["terms"] if term_count(strip_meta(ans, w), w) < k]
	return not miss, ("v2 missing %d term(s)" % len(miss)) if miss else "v2 all required terms present"


def _v2_check_term_forbidden(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("terms"):
		return None, "incomplete arg"
	hit = [w for w in arg["terms"] if term_count(strip_meta(ans, w), w) > 0]
	return not hit, ("v2 %d forbidden term(s) present" % len(hit)) if hit else "v2 no forbidden term present"


_ALNUM_RUN = re.compile(r"[A-Za-z0-9０-９Ａ-Ｚａ-ｚ]+")


def count_text_chars(s: str) -> int:
	"""v2 character count: letters / digits of non-Latin scripts one by one, each Latin
	alphanumeric run as one unit; punctuation, symbols and whitespace are not counted."""
	rest = _ALNUM_RUN.sub("", s or "")
	return sum(1 for c in rest if unicodedata.category(c)[0] in "LN") + len(_ALNUM_RUN.findall(s or ""))


def _v2_check_length(ans: str, arg):
	if not isinstance(arg, dict) or arg.get("n") is None:
		return None, "incomplete arg"
	if arg.get("unit") in ("詞", "words"):
		return _check_length(ans, arg)
	n, op = int(arg["n"]), arg.get("op", ">=")
	got = count_text_chars(ans)
	if op == "~":
		lo, hi = n * 0.8, n * 1.2
		return lo <= got <= hi, "v2 chars (no punctuation) %d vs %d+-20%% (%.0f-%.0f)" % (got, n, lo, hi)
	ok = got >= n if op == ">=" else got <= n
	return ok, "v2 chars (no punctuation) %d %s %d" % (got, op, n)


def _v2_check_term_required_in_title(ans: str, arg):
	if not isinstance(arg, dict) or not arg.get("term"):
		return None, "incomplete arg"
	x, title = arg["term"], _title_line(ans)
	ok = term_count(title, x) > 0
	return ok, "v2 title %s the term" % ("contains" if ok else "does not contain")


_QUOTE = re.compile(r"「[^」]*」|『[^』]*』|“[^”]*”|\"[^\"\n]*\"")
_SELF_HEAD = re.compile(r"(^|[。！？!?；;：:，,、\n（(\s])(本人|吾)")


def _v2_first_person_ratio(ans: str):
	"""Quoted speech removed; the formal / literary first-person forms (U+672C U+4EBA, U+543E)
	at a clause start and U+54B1 anywhere count as first person."""
	t = _QUOTE.sub("", ans or "")
	t = _SELF_HEAD.sub(lambda m: m.group(1) + "我", t).replace("咱", "我")
	sents = [s.strip().lstrip(_LEAD_STRIP) for s in _SENT_SPLIT.split(t) if s.strip()]
	sents = [s for s in sents if s]
	if not sents:
		return 0.0, 0, 0
	hit = sum(1 for s in sents if "我" in s)
	return hit / len(sents), hit, len(sents)


def _v2_check_person(ans: str, arg):
	if not isinstance(arg, dict):
		return None, "incomplete arg"
	ratio, hit, n = _v2_first_person_ratio(ans)
	if arg.get("person") == "third":
		return ratio <= 0.15, "v2 first-person ratio %.2f (%d/%d, third person needs <= 0.15)" % (ratio, hit, n)
	short = n <= 5 and hit >= 1          # short text (<= 5 sentences) passes with one first-person sentence
	ok_ratio = ratio >= 0.3 or short
	base = "v2 first-person ratio %.2f (%d/%d, needs >= 0.30%s)" % (ratio, hit, n, "; short text" if short else "")
	name, m_cnt = _protagonist(arg.get("material_text") or "")
	if name and m_cnt > 0 and ratio < 0.5:
		a_cnt = (ans or "").count(name)
		ok_name = a_cnt <= m_cnt / 3
		return ok_ratio and ok_name, "%s; protagonist material %d -> answer %d (needs <= %.1f)" % (base, m_cnt, a_cnt, m_cnt / 3)
	return ok_ratio, base + ("; ratio >= 0.5, protagonist rule not applied" if name else "; no protagonist found, ratio only")


V2_OVERRIDES = {
	"format": _v2_check_format,
	"count": _v2_check_count,
	"structure": _v2_check_structure,
	"term_required": _v2_check_term_required,
	"term_required_in_title": _v2_check_term_required_in_title,
	"person": _v2_check_person,
	"term_forbidden": _v2_check_term_forbidden,
	"language": _v2_check_language,
	"length": _v2_check_length,
}


# ===========================================================================
# Public API
# ===========================================================================


def _checker_table(version: str, exclude) -> dict:
	if version == "v1":
		return V1_CHECKERS
	if version != "v2":
		raise ValueError("version must be 'v1' or 'v2'")
	ex = {getattr(x, "value", x) for x in (exclude or ())}
	unknown = ex - set(V2_OVERRIDES)
	if unknown:
		raise ValueError("exclude names types without a v2 revision: %s" % sorted(unknown))
	table = dict(V1_CHECKERS)
	table.update({k: f for k, f in V2_OVERRIDES.items() if k not in ex})
	return table


def check_items_detailed(items: list[dict], answer: str, version: str = "v2", exclude: tuple = ()) -> dict:
	"""{sid: (verdict, detail)} for every item whose check_type is not "other".

	Items are processed in order; a repeated sid keeps the last verdict.
	"""
	table = _checker_table(version, exclude)
	answer = answer or ""
	deliv, _scope = deliverable_of(answer)
	out: dict = {}
	for it in items:
		ct = getattr(it["check_type"], "value", it["check_type"])
		if ct == "other":
			continue
		fn = table.get(ct)
		if fn is None:
			out[it["sid"]] = (None, "no checker for type %r" % ct)
			continue
		target = deliv if ct in SCOPED_TYPES else answer
		out[it["sid"]] = fn(target, it.get("check_arg"))
	return out


def check_items(items: list[dict], answer: str, exclude: tuple = ()) -> dict:
	"""v2 verdicts {sid: True | False | None}. `exclude` keeps the v1 checker for the named types."""
	return {sid: v for sid, (v, _d) in check_items_detailed(items, answer, "v2", exclude).items()}


def check_items_v1(items: list[dict], answer: str) -> dict:
	"""v1 verdicts {sid: True | False | None} (the checker before the v2 revision)."""
	return {sid: v for sid, (v, _d) in check_items_detailed(items, answer, "v1").items()}
