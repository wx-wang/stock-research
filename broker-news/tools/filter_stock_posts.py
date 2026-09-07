#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帖子级清洗: 只保留与 A股 / 港股 相关的帖子(命中股票名称或代码), 其余剔除。

理由: 观察者03 内容含大量美股/海外宏观/无关内容, 而投资者聚焦 A股为主港股为辅。
输出: broker-news/filtered/  + broker-news/filtered/过滤统计.md

用法: python3 filter_stock_posts.py [--dir broker-news/cleaned]
"""
import json
import re
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = OUT_DIR / "cleaned"
DST_DIR = OUT_DIR / "filtered"
DICT = json.loads((Path(__file__).resolve().parent / "stock_dict.json").read_text(encoding="utf-8"))

# 构建匹配器
def norm(s: str) -> str:
    s = (s or "").replace(" ", "").replace("\u3000", "")
    return "".join(chr(ord(c) - 0xFEE0) if 0xFF01 <= ord(c) <= 0xFF5E else c for c in s).upper()

A_NAMES = sorted({s["norm"] for s in DICT["A股"]}, key=len, reverse=True)
HK_NAMES = sorted({s["norm"] for s in DICT["港股通"]}, key=len, reverse=True)
A_CODE_RE = re.compile(r"(?<!\d)(?:60|00|30|68|80|83|43|87)\d{4}(?!\d)")
HK_CODE_RE = re.compile(r"(?<!\d)0\d{4}(?!\d)")


def _is_chinese(c: str) -> bool:
    return "\u4e00" <= c <= "\u9fff"


# 两段式匹配: 长名(>=4字)纯字面交替; 3字名也放宽为子串(避免"新雷能定增"式误删,
# 过滤场景下误留的成本远低于误删); 2字名太歧义跳过。
_LONG_NAMES = sorted({n for n in set(A_NAMES) | set(HK_NAMES) if len(n) >= 4}, key=len, reverse=True)
_SHORT_NAMES = sorted({n for n in set(A_NAMES) | set(HK_NAMES) if len(n) == 3})
LONG_NAME_RE = re.compile("|".join(re.escape(n) for n in _LONG_NAMES))
SHORT_NAME_RE = re.compile("|".join(re.escape(n) for n in _SHORT_NAMES))


def match_names(text: str) -> list[str]:
    """返回命中的股票名(长名正则 + 短名边界正则)。"""
    return LONG_NAME_RE.findall(text) + SHORT_NAME_RE.findall(text)

def post_text(blk: str) -> str:
    """提取帖子可匹配文本(标题+内容+附件名)。"""
    m = re.search(r"^\*\*标题\*\*：(.+)$", blk, re.M)
    c = re.search(r"^\*\*内容\*\*：(.*)$", blk, re.M | re.S)
    parts = []
    if m:
        parts.append(m.group(1))
    if c:
        parts.append(c.group(1))
    parts.extend(re.findall(r"^- (.+)$", blk, re.M))
    return norm("\n".join(parts))

def filter_one(fp: Path) -> tuple[int, int, list[str]]:
    text = fp.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=<!-- topic_id: )", text)
    header = blocks[0]
    kept, dropped, dropped_samples = [], 0, []
    for blk in blocks[1:]:
        if not re.search(r"<!-- topic_id: (\d+) -->", blk):
            header += blk
            continue
        txt = post_text(blk)
        code_hits = A_CODE_RE.findall(txt) + HK_CODE_RE.findall(txt)
        name_hits = match_names(txt)
        if code_hits or name_hits:
            kept.append(blk)
        else:
            dropped += 1
            if len(dropped_samples) < 5:
                t = re.search(r"^\*\*标题\*\*：(.+)$", blk, re.M)
                dropped_samples.append(t.group(1)[:40] if t else "(无标题)")
    renumbered = []
    for i, blk in enumerate(kept, 1):
        renumbered.append(re.sub(r"^### \d+\. ", f"### {i}. ", blk, count=1, flags=re.M))
    header = re.sub(r"- 共 .*? 条.*", f"- 共 {len(kept)} 条（A股/港股相关过滤后）", header)
    header = re.sub(r"- 说明：.*", "- 说明：仅保留命中A股/港股名称或代码的帖子", header)
    (DST_DIR / fp.name).write_text(header + "\n".join(renumbered) + "\n", encoding="utf-8")
    return len(kept) + dropped, dropped, dropped_samples

def main() -> int:
    DST_DIR.mkdir(exist_ok=True)
    total_o = total_d = 0
    stats = []
    for fp in sorted(SRC_DIR.glob("observer03_*-W*.md")):
        orig, dropped, samples = filter_one(fp)
        total_o += orig
        total_d += dropped
        pct = 100 * dropped / orig if orig else 0
        stats.append((fp.name, orig, orig - dropped, dropped, pct))
        print(f"{fp.name}: {orig}条 → 保留{orig-dropped}, 剔除{dropped} ({pct:.0f}%)", flush=True)
        for s in samples:
            print(f"    [剔除示例] {s}", flush=True)

    print(f"\n总计: {total_o} → 保留 {total_o-total_d} ({100*(total_o-total_d)/total_o:.0f}%), 剔除 {total_d}")
    # 统计报告
    lines = ["# 帖子过滤统计（A股/港股相关）\n",
             f"- 源: {SRC_DIR}",
             f"- 过滤规则: 帖子命中 A股/港股 名称或代码 即保留",
             f"- 总帖子 {total_o} → 保留 {total_o-total_d} ({100*(total_o-total_d)/total_o:.1f}%), 剔除 {total_d}\n"]
    for name, orig, keep, drop, pct in stats:
        lines.append(f"- {name}: {orig} → {keep} (剔除 {drop}, {pct:.0f}%)")
    (DST_DIR / "过滤统计.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())