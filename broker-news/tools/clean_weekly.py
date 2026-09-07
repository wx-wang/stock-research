#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清洗每周 Markdown: 剔除"纯音频帖/纯图片帖"(没有正文文字、只有附件或图片占位的帖子),
避免污染知识库。保留有正文的帖子(即使带附件)。

输出到 broker-news/cleaned/, 原文件不动。
用法: python3 clean_weekly.py [--dir broker-news]
"""
import re
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = OUT_DIR / "cleaned"
PLACEHOLDER = {"「文件」", "「图片」", ""}


def clean_one(fp: Path) -> tuple[int, int]:
    text = fp.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=<!-- topic_id: )", text)
    header = blocks[0] if not blocks[0].startswith("<!--") else ""
    kept = []
    orig = 0
    dropped = 0
    for blk in blocks[1:]:
        if not re.search(r"<!-- topic_id: (\d+) -->", blk):
            header += blk
            continue
        orig += 1
        title_m = re.search(r"^\*\*标题\*\*：(.+)$", blk, re.M)
        title = title_m.group(1).strip() if title_m else ""
        has_content = bool(re.search(r"^\*\*内容\*\*：", blk, re.M))
        # 判断是否纯音频/图片帖: 无正文内容, 且标题为占位(或缺失)
        if not has_content and title in PLACEHOLDER:
            dropped += 1
            continue
        kept.append(blk)
    # 重新编号
    renumbered = []
    for i, blk in enumerate(kept, 1):
        renumbered.append(re.sub(r"^### \d+\. ", f"### {i}. ", blk, count=1, flags=re.M))
    body = "\n".join(renumbered)
    # 更新头部统计
    header = re.sub(r"- 共 .*? 条.*", f"- 共 {len(kept)} 条（清洗后）", header)
    header = re.sub(r"- 说明：.*", "- 说明：已剔除纯音频/图片帖（清洗于 2026-08-23）", header)
    out = CLEAN_DIR / fp.name
    out.write_text(header + body + "\n", encoding="utf-8")
    return orig, dropped


def main() -> int:
    CLEAN_DIR.mkdir(exist_ok=True)
    total_o = total_d = 0
    for fp in sorted(OUT_DIR.glob("observer03_*-W*.md")):
        orig, dropped = clean_one(fp)
        total_o += orig
        total_d += dropped
        pct = 100 * dropped / orig if orig else 0
        print(f"{fp.name}: {orig} 条 → 保留 {orig - dropped}, 剔除 {dropped} ({pct:.0f}%)")
    print(f"\n总计: {total_o} 条 → 剔除 {total_d} ({100*total_d/total_o:.0f}%)")
    print(f"清洗结果输出到: {CLEAN_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())