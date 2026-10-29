# -*- coding: utf-8 -*-
"""Map ComplexBench rule strings to this project's constraint types, and match recorded reads against them.

Used for two things:
  * the "mappable subset" column of the scores: a rule is mappable when it maps to one of our types and
    is not a punctuation *allow-list* (we have no "only these may appear" form);
  * reading coverage: given what the architecture read for a question (a list of typed items with
    parameters), decide per rule: hit / right type wrong parameters / missed / no matching type.

This module only reads the benchmark's rule strings and recorded reads. It contains none of the
architecture's reading patterns.

Mapping:
  length:[lo,hi]          -> length {ge lo (when lo > 1), le hi (when hi < 10000)}, unit = character ("字")
  length_word:[lo,hi]     -> same, unit = word ("詞")
  keyword / modek_keyword -> term_required {terms}
  forbidden_word          -> term_forbidden {terms}
  Json:[keys]             -> format {json}  (keys are not compared)
  constraint_punc:[]      -> forbidden_charset {punct};  constraint_punc:[allowed...] -> allow-list, never matches
  startswith / endswith   -> no matching type (counted as missed, listed separately)

A recorded read item looks like {"idx": int, "type": str, "arg": dict}; for length the arg carries
{"op": ">=" | "<=" | "~", "n": int, "unit": "字" | "詞"}, for terms {"terms": [...]} (or {"term": ...}),
for format {"format": "json" | ...}, for forbidden_charset {"classes": [...]}.
"""
from __future__ import annotations

import json


def _list(s: str) -> list[str]:
	return [x.strip() for x in s.strip().strip("[]").split(",") if x.strip()]


def gold_of(rule: str) -> dict:
	kind, _, arg = rule.partition(":")
	if kind in ("length", "length_word"):
		lo, hi = json.loads(arg)
		b = {}
		if lo > 1:
			b["ge"] = lo
		if hi < 10000:
			b["le"] = hi
		return {"type": "length", "bounds": b, "unit": "詞" if kind == "length_word" else "字"}
	if kind in ("keyword", "modek_keyword"):
		return {"type": "term_required", "terms": sorted(t.lower() for t in _list(arg))}
	if kind == "forbidden_word":
		return {"type": "term_forbidden", "terms": sorted(t.lower() for t in _list(arg))}
	if kind == "Json":
		return {"type": "format", "fmt": "json"}
	if kind == "constraint_punc":
		return {"type": "forbidden_charset", "allow": _list(arg)}
	return {"type": None, "kind": kind}          # startswith / endswith: no matching type


def mappable(rule: str) -> bool:
	g = gold_of(rule)
	if g["type"] is None:
		return False
	return not (g["type"] == "forbidden_charset" and g.get("allow"))


def norm_terms(arg) -> list[str]:
	ts = (arg or {}).get("terms") or ([arg["term"]] if (arg or {}).get("term") else [])
	return sorted(str(t).strip("「」『』“”\"' ").lower() for t in ts if str(t).strip())


def match(g: dict, cand: list[dict], used: set[int]) -> tuple[list[int], bool, str]:
	"""Return (indices of reads consumed, matched?, reason). `cand` = all reads for the question."""
	t = g["type"]
	pool = [c for c in cand if c["idx"] not in used and c["type"] == t]
	if not pool:
		return [], False, "no read of this type"
	if t == "length":
		got = {}
		for c in pool:
			a = c["arg"]
			op, n = a.get("op"), a.get("n")
			if op == "~" and n:
				got.setdefault("~", (c["idx"], n, a.get("unit")))
			elif op in (">=", "<="):
				got.setdefault("ge" if op == ">=" else "le", (c["idx"], n, a.get("unit")))
		need = g["bounds"]
		ok_idx, diff = [], []
		for d, n in need.items():
			if d in got and got[d][1] == n:
				ok_idx.append(got[d][0])
				if (got[d][2] == "詞") != (g["unit"] == "詞"):
					diff.append("unit %s != %s" % (g["unit"], got[d][2]))
			else:
				diff.append("%s %s != %s" % (d, n, got[d][1] if d in got else "none"))
		if ok_idx and not diff and len(ok_idx) == len(need):
			return ok_idx, True, "match"
		first = [v[0] for v in got.values()][:1] or [pool[0]["idx"]]
		return (ok_idx or first), False, "; ".join(diff) or "bounds incomplete"
	if t in ("term_required", "term_forbidden"):
		gs = set(g["terms"])
		best = max(pool, key=lambda c: len(gs & set(norm_terms(c["arg"]))))
		ps = set(norm_terms(best["arg"]))
		if gs == ps:
			return [best["idx"]], True, "match"
		return [best["idx"]], False, ("partial overlap" if gs & ps else "no overlap") + " gold %s / read %s" % (sorted(gs), sorted(ps))
	if t == "format":
		hit = next((c for c in pool if (c["arg"] or {}).get("format") == "json"), None)
		return ([hit["idx"]], True, "match") if hit else ([pool[0]["idx"]], False, "fmt %s" % (pool[0]["arg"] or {}).get("format"))
	if t == "forbidden_charset":
		c = pool[0]
		cls = (c["arg"] or {}).get("classes") or []
		if not g["allow"] and "punct" in cls:
			return [c["idx"]], True, "match"
		return [c["idx"]], False, "gold allows only %s / read forbids %s" % (g["allow"] or "(no punctuation)", cls)
	return [], False, "no comparison rule for this type"
