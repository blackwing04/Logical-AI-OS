# Public copy of the internal `scripts/canon_v3/lexicon.py` (unchanged since before the v4.5 seal, 2026-10-06).
# Name-redacted (internal handle -> PI, 4 places); corpus-redacted (2 examples); one internal order reference rewritten; one comment word changed. Code unchanged. Record: PUBLIC_NOTES.md section 7.
from __future__ import annotations

import re


def compile_lexicon_pattern(terms: tuple[str, ...]) -> re.Pattern[str]:
	return re.compile("|".join(re.escape(term) for term in sorted(terms, key=len, reverse=True)))


# Source: linguistic closed class, complete zh-TW interrogative syntax forms; not derived from evaluation rows.
L2_QUESTION_CUE_TERMS = (
	"怎麼", "怎樣", "如何", "哪", "哪裡", "哪邊", "什麼", "甚麼", "幾", "多少", "多久", "何時", "為什麼", "為何",
	"嗎", "呢",
	"能不能", "可不可以", "可以嗎", "該不該", "要不要", "是不是", "有沒有", "能否", "是否", "會不會", "行不行", "好不好", "好嗎",
	"還是",
	"請問", "想問", "想請教", "想知道", "想了解", "求",
)


L2_QUESTION_CUE_PATTERN = re.compile(r"[？?]|" + compile_lexicon_pattern(L2_QUESTION_CUE_TERMS).pattern)


# Source: linguistic closed class, zh-TW demonstrative pronouns.
DEICTIC_TERMS = ("這個", "這樣", "這種", "這件", "這狀況", "這情況", "那個", "那樣", "那種", "上面說的", "剛才說的", "剛剛說的")


DEICTIC_PATTERN = compile_lexicon_pattern(DEICTIC_TERMS)


# Source: seven theoretical question-type head verb classes; semi-open, changes require PI review.
QUESTION_TYPE_VERB_GROUPS = {
	"recommendation_selection": ("推薦", "建議", "選", "挑", "適合", "哪個", "哪一個"),
	"planning_arrangement": ("安排", "規劃", "排", "準備", "計畫"),
	"diagnosis_troubleshooting": ("查", "排查", "檢查", "找原因", "除錯", "解決", "分析"),
	"writing_output": ("怎麼寫", "如何寫", "撰寫"),
	"judgement_evaluation": ("判斷", "評估", "算不算", "能不能算"),
	"operation_procedure": ("處理", "辦", "申請", "辦理"),
	"review_inspection": ("看看", "看一下", "幫我看", "檢查一下"),
}


QUESTION_TYPE_VERB_PATTERNS = {group: compile_lexicon_pattern(terms) for group, terms in QUESTION_TYPE_VERB_GROUPS.items()}


# Source: measurement and time units. Table 5a keeps sole responsibility for these; a term
# appearing here is mechanically removed from the measure-word set below.
TABLE5_UNIT_TERMS = ("元", "塊", "小時", "分鐘", "天", "夜", "週", "月", "年", "萬", "GB", "G", "吋", "歲")


# Source: 專用量詞閉集, signed by PI as lexicon rev2 on 2026-08-07 (internal order,
# not published). Drawn from the 名量詞/動量詞 classification of
# standard grammars, cross-checked across several term lists. A single academic count may
# differ by a few entries; completeness is backstopped by the OOD incorporation loop.
#
# Boundary set by the same order, and it matters more than the list itself:
#   - 專用量詞 are a closed class and are enumerated here in full.
#   - 借用量詞 are半-open and productive, so they are deliberately NOT enumerated. Nouns
#     borrowed on the spot (一身汗, 一桌菜, 一地水, 一臉倦容) and body-part verbal measures
#     (踢一腳, 打一拳, 看一眼) would always leak from any list. They are carried by the
#     three-layer net instead: bare-numeric second chance, guard ASK, OOD incorporation.
#   - Measurement and time units stay in TABLE5_UNIT_TERMS above.
#
# The two layers below are a review structure only. They are merged into one flat closed set
# at runtime and nothing distinguishes them there.

# 常用層: high frequency in everyday requests, scanned term by term by PI.
_MEASURE_WORDS_COMMON = (
	# 人/稱謂
	"個", "位", "名", "員", "戶", "口",
	# 動物
	"隻", "匹", "頭", "條", "尾", "峰",
	# 一般個體
	"張", "支", "枝", "件", "顆", "粒", "枚", "塊", "片", "根", "面", "扇", "頂", "座",
	"棟", "幢", "間", "層", "台", "部", "輛", "架", "艘", "輪", "棵", "朵", "把", "桿",
	"管", "盞",
	# 書文/知識
	"本", "冊", "卷", "篇", "章", "句", "段", "頁", "行", "欄", "封", "則", "首", "幅",
	"題", "課", "門", "堂", "節",
	# 事務
	"項", "款", "筆", "宗", "樁", "起", "例", "案", "招",
	# 集合
	"組", "對", "雙", "套", "副", "批", "群", "幫", "串", "束", "捆", "疊", "堆", "排",
	"隊", "列", "打", "窩",
	# 容器, 專用化
	"杯", "碗", "盤", "碟", "瓶", "罐", "桶", "盒", "包", "袋", "箱", "籃", "鍋", "壺",
	"盆", "籠", "勺", "滴",
	# 餐飲/商用
	"客", "份",
	# 藥/服飾
	"劑", "帖", "服", "丸", "錠", "襲",
	# 段落/場次
	"屆", "期", "檔", "集", "幕", "級", "站", "處", "所",
	# 動量詞
	"次", "回", "趟", "遍", "場", "頓", "番", "圈", "遭", "通", "覺", "跤", "聲", "發", "響",
)

# 罕用/文言層: carried by the grammars, low frequency and low risk since a cue only fires
# when the term sits next to a digit.
_MEASURE_WORDS_RARE = (
	"縷", "彎", "葉", "闋", "尊", "幀", "軸", "泓", "抹", "沓", "摞", "垛", "貫", "令",
	"刀", "羅", "撮", "窠", "腔", "丘", "鉤", "曲", "板", "貼", "挑", "擔", "味",
)

# Kept out by the same order, in two sub-classes. Reversing an exclusion needs OOD evidence
# against the reason it was excluded, judged case by case. Recorded here so a later session
# does not quietly add them back.
#
# 高頻語用填充: these would fire constantly on 等一下, 快一點, 一些, 一會, 一陣.
_EXCLUDED_PRAGMATIC_FILLERS = ("下", "點", "些", "會", "陣")
#
# 動詞同形優勢, added by PI on 2026-08-07 after the R12 pre-flight: 打 as a measure word
# (一打 = a dozen) is close to fossilised, while the verb readings 打開, 打算 dominate real
# text. The pre-flight caught 一打開 converting to 1打開, destroying the word.
_EXCLUDED_VERB_HOMOGRAPH_DOMINANT = ("打",)

MEASURE_WORD_EXCLUSIONS = (*_EXCLUDED_PRAGMATIC_FILLERS, *_EXCLUDED_VERB_HOMOGRAPH_DOMINANT)

TABLE5_MEASURE_WORD_TERMS = tuple(
	term
	for term in dict.fromkeys((*_MEASURE_WORDS_COMMON, *_MEASURE_WORDS_RARE))
	if term not in TABLE5_UNIT_TERMS and term not in MEASURE_WORD_EXCLUSIONS
)


_MEASURE_ALTERNATION = "|".join(map(re.escape, TABLE5_MEASURE_WORD_TERMS))
_UNIT_ALTERNATION = "|".join(map(re.escape, TABLE5_UNIT_TERMS))

# R12 terminal spec: a digit followed by a measure word is a valid quantity cue on its own, so
# a numeral plus a measure word fires without a unit ever appearing (example corpus-redacted). The unit-terminal branch is tried first so that
# 5個月 still yields the longer cue 5個月 rather than stopping at 5個.
TABLE5_NUMERIC_UNIT_PATTERN = re.compile(
	r"\d+(?:\.\d+)?\s*(?:" + _MEASURE_ALTERNATION + r")?\s*(?:" + _UNIT_ALTERNATION + r")"
	r"|\d+(?:\.\d+)?\s*(?:" + _MEASURE_ALTERNATION + r")"
)


# The last three are the postpositive cap family, signed 2026-08-25. Semantics, closed and not
# to be widened: placed after a quantity or a specification, meaning "this is the ceiling" or
# "this is enough". 就可以 and 便可 are deliberately not included -- in the test bank 就可以
# occurs as a modal and not as a cap at all (the sentence is corpus-redacted).
TABLE5_LIMITING_HEAD_TERMS = ("只有", "只剩", "只能", "不想", "不喜歡", "不要", "不求", "不可能", "最多", "至少", "內", "以內", "之內", "以下", "以上", "為止", "封頂", "頂多", "至多", "上下", "左右", "就好", "就行", "即可")


TABLE5_LIMITING_HEAD_PATTERN = compile_lexicon_pattern(TABLE5_LIMITING_HEAD_TERMS)


A3_MATERIAL_STATE_REASON_CODES = ("material_state", "material_technical_state", "material_admin_status", "material_event")


ZH_TW_DIGITS = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "兩": 2, "半": 0.5}


ZH_TW_SMALL_UNITS = {"十": 10, "百": 100, "千": 1000}


ZH_TW_LARGE_UNITS = {"萬": 10000, "億": 100000000}


# Kept verbatim from before R12 so unit behavior is unchanged. 萬 is deliberately absent: it is
# a magnitude handled by the second alternative below, and admitting it here would make 兩萬
# convert to 2萬 instead of 20000.
_NUMBER_LOOKAHEAD_UNITS = ("元", "塊", "小時", "分鐘", "天", "夜", "週", "月", "年", "G", "GB", "吋", "歲")

# R12: the conversion condition widens from "numeral immediately followed by a unit" to
# "numeral immediately followed by a unit or a measure word", so 一組 becomes 1組 and 一個小時
# becomes 1個小時. The exclusions are not measure words, so 等一下, 快一點, 一些 and 一打開 are
# untouched by construction rather than by a special case.
#
# 零 is admitted before a unit but not before a measure word. 零 plus a measure word is not
# how anyone says a quantity, while 零 plus almost anything else is word formation: 零件,
# 零錢, 零食. The pre-flight caught 零件 converting to 0件.
_NUMERALS_WITH_ZERO = "零一二三四五六七八九兩半十百千萬億"
_NUMERALS_WITHOUT_ZERO = "一二三四五六七八九兩半十百千萬億"

# Determiners that make a following numeral part of a determiner phrase rather than a count:
# 哪一個, 這一次, 每一天, 第一次. Guarding the class rather than patching each case.
_NUMBER_LEFT_GUARD = "哪這那每某任第"

# 半 needs its own left guard, kept separate on purpose. 上半年, 下半年, 多半 and 大半 are
# lexicalised time and degree words, and splitting them is the same input contamination the
# other guards prevent. 下 must not join the general guard above: 剩下一個小時 is a real
# quantity and the general guard would kill it. So this one only applies when the match itself
# begins with 半.
_HALF_LEFT_GUARD = "上下多大"

ZH_TW_NUMBER_PATTERN = re.compile(
	r"(?<![" + _NUMBER_LEFT_GUARD + r"])"
	r"(?!(?<=[" + _HALF_LEFT_GUARD + r"])半)(?:"
	r"[" + _NUMERALS_WITH_ZERO + r"]+(?=(?:" + "|".join(map(re.escape, _NUMBER_LOOKAHEAD_UNITS)) + r"))"
	r"|[" + _NUMERALS_WITHOUT_ZERO + r"]+(?=(?:" + "|".join(map(re.escape, TABLE5_MEASURE_WORD_TERMS)) + r"))"
	r"|[零一二三四五六七八九兩半]*[十百千萬億][" + _NUMERALS_WITH_ZERO + r"]*"
	r")"
)


ZH_TW_AMBIGUOUS_NUMBER_PATTERN = re.compile(r"^[一二三四五六七八九兩]{2,}(?:十|百|千|萬|億)?$")
