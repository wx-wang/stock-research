#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize W34 company mentions against the Tushare security master.

This is a deterministic pre-processing step before Hyper-Extract. It does not
decide whether a company is investable; it only resolves identities and adds
machine-readable context to each source post.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "cleaned" / "observer03_2026-W34_2026-08-17_2026-08-23.md"
MASTER = ROOT / "reference" / "tushare_security_master_20260824.json"
OUT_DIR = ROOT / "normalized"
OUT_MD = OUT_DIR / "observer03_2026-W34_investment.md"
OUT_JSON = OUT_DIR / "observer03_2026-W34_entity_resolution.json"
OUT_REPORT = OUT_DIR / "observer03_2026-W34_entity_resolution.md"

# These short names are also ordinary investment vocabulary. They are kept as
# unresolved candidates unless a post contains an explicit security code.
SHORT_NAME_STOPLIST = {"机器人", "农产品", "驱动力", "新产业"}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.replace("\u3000", "")
    return re.sub(r"[\s·•_\-—/（）()]+", "", value).upper()


def code_key(code: str) -> str:
    return re.sub(r"[^0-9A-Z]", "", (code or "").upper())


def split_posts(text: str) -> tuple[str, list[str]]:
    pieces = re.split(r"\n(?=<!-- topic_id: )", text)
    return pieces[0], [p for p in pieces[1:] if "<!-- topic_id:" in p]


def body_text(block: str) -> str:
    return norm(block)


def code_text(block: str) -> str:
    value = unicodedata.normalize("NFKC", block or "")
    return re.sub(r"[\s\u3000]+", "", value).upper()


def make_records(master: dict) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    alias_map: dict[str, list[dict]] = defaultdict(list)
    code_map: dict[str, dict] = {}
    for market, rows in (("A股", master.get("a_share", [])), ("港股", master.get("hk", []))):
        for row in rows:
            rec = dict(row)
            rec["market_group"] = market
            rec["canonical_id"] = rec.get("ts_code", "")
            rec["canonical_name"] = rec.get("name", "")
            code_map[code_key(rec["canonical_id"])] = rec
            # W34 is primarily Chinese-language research. Keep the resolver
            # deterministic and fast by using canonical Chinese name/fullname
            # aliases; English names and pinyin remain available in the master
            # file for a later, targeted pass.
            aliases = [rec.get("name", ""), rec.get("fullname", "")]
            for alias in aliases:
                key = norm(alias)
                if not key or len(key) < 3 or key.isascii():
                    continue
                if rec not in alias_map[key]:
                    alias_map[key].append(rec)
    return alias_map, code_map


def resolve_block(
    block: str,
    alias_map: dict[str, list[dict]],
    code_map: dict[str, dict],
    alias_pattern: re.Pattern[str],
) -> dict:
    text = body_text(block)
    title_match = re.search(r"^\*\*标题\*\*：(.+)$", block, re.M)
    title_text = norm(title_match.group(1) if title_match else "")
    by_id: dict[str, dict] = {}
    candidate_by_id: dict[str, dict] = {}
    explicit: list[str] = []
    # Accept both canonical TS codes and bare A/H numeric codes.
    code_pattern = re.compile(r"(?<![0-9A-Z])(?:\d{6}\.(?:SH|SZ|BJ)|\d{5}\.HK|\d{6}|\d{5})(?![0-9A-Z])")
    for raw in code_pattern.findall(code_text(block)):
        k = code_key(raw)
        rec = code_map.get(k)
        if rec:
            by_id[rec["canonical_id"]] = rec
            explicit.append(raw)

    # One compiled alternation is substantially faster than scanning every
    # alias separately across every post.
    matched_aliases = sorted(set(m.group(0) for m in alias_pattern.finditer(text)), key=len, reverse=True)
    for alias in matched_aliases:
        candidates = alias_map[alias]
        if len(candidates) == 1:
            rec = candidates[0]
            cname = rec.get("name", "")
            is_short_generic = cname in SHORT_NAME_STOPLIST
            title_has_company_context = bool(
                alias in title_text
                and re.search(r"(公司|股份|集团|业绩|订单|客户|产品|研报|目标价|净利|收入|利润|公告|涨|跌|推荐|关注|龙头|项目|估值|价格|产能)", title_text)
            )
            high_confidence = (len(cname) >= 4 and not is_short_generic) or title_has_company_context
            if high_confidence:
                by_id[rec["canonical_id"]] = rec
            else:
                candidate_by_id[rec["canonical_id"]] = rec

    candidate_by_id = {k: v for k, v in candidate_by_id.items() if k not in by_id}
    confirmed = sorted(by_id.values(), key=lambda r: r["canonical_id"])
    # Ambiguous aliases are recorded for review; they never create a confirmed node.
    ambiguous = []
    for alias in matched_aliases:
        candidates = alias_map[alias]
        if len(candidates) > 1:
            ambiguous.append({
                "alias": alias,
                "candidates": [c["canonical_id"] for c in candidates],
            })
    topic = re.search(r"<!-- topic_id: (\d+) -->", block)
    title = re.search(r"^\*\*标题\*\*：(.+)$", block, re.M)
    return {
        "topic_id": topic.group(1) if topic else "",
        "title": title.group(1).strip() if title else "",
        "confirmed": confirmed,
        "candidates": sorted(candidate_by_id.values(), key=lambda r: r["canonical_id"]),
        "explicit_codes": sorted(set(explicit)),
        "matched_aliases": matched_aliases[:100],
        "ambiguous": ambiguous[:100],
    }


def main() -> int:
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    source = SRC.read_text(encoding="utf-8")
    header, blocks = split_posts(source)
    alias_map, code_map = make_records(master)
    alias_pattern = re.compile("|".join(re.escape(a) for a in sorted(alias_map, key=len, reverse=True)))
    resolutions = []
    enriched = [header.rstrip(), "", "# W34 投资图谱输入（已通过 Tushare 标准化公司实体）", "", "---"]
    seen_hashes: set[str] = set()
    duplicate_count = 0
    for block in blocks:
        digest = hashlib.sha1(norm(block).encode("utf-8")).hexdigest()
        if digest in seen_hashes:
            duplicate_count += 1
            continue
        seen_hashes.add(digest)
        res = resolve_block(block, alias_map, code_map, alias_pattern)
        resolutions.append(res)
        annotations = ["\n## 机器实体标注（仅作图谱身份约束，不代表投资结论）"]
        if res["confirmed"]:
            annotations.append("已确认公司：")
            for rec in res["confirmed"]:
                annotations.append(
                    f"- {rec.get('canonical_name','')}（{rec.get('canonical_id','')}，{rec.get('market_group','')}）"
                )
        else:
            annotations.append("已确认公司：无")
        if res.get("candidates"):
            annotations.append("候选公司（未自动确认为上市公司实体）：")
            for rec in res["candidates"][:20]:
                annotations.append(f"- {rec.get('canonical_name','')}（{rec.get('canonical_id','')}）")
        if res["ambiguous"]:
            annotations.append("待确认名称：" + "；".join(a["alias"] for a in res["ambiguous"][:12]))
        enriched.append(block.rstrip() + "\n" + "\n".join(annotations))
        enriched.append("\n---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(enriched) + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps({
        "source": str(SRC),
        "security_master": str(MASTER),
        "posts": resolutions,
        "duplicate_posts_removed": duplicate_count,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    confirmed_posts = sum(bool(r["confirmed"]) for r in resolutions)
    candidate_posts = sum(bool(r.get("candidates")) for r in resolutions)
    confirmed_ids = Counter(c["canonical_id"] for r in resolutions for c in r["confirmed"])
    ambiguous_posts = sum(bool(r["ambiguous"]) for r in resolutions)
    title_hits = [r for r in resolutions if r["confirmed"] and any(r["title"] == c.get("name") for c in r["confirmed"])]
    report = [
        "# W34 公司实体标准化报告",
        "",
        f"- 源文件：`{SRC.name}`",
        f"- 证券主表：`{MASTER.name}`",
        f"- 原始清洗帖子：{len(blocks)}",
        f"- 去重剔除：{duplicate_count}",
        f"- 标准化后帖子：{len(resolutions)}",
        f"- 至少命中一家已上市公司：{confirmed_posts}",
        f"- 仅有短名/通用词候选的帖子：{candidate_posts}",
        f"- 存在名称歧义的帖子：{ambiguous_posts}",
        f"- 公司实体节点候选数：{len(confirmed_ids)}",
        "",
        "## 高频公司（按帖子提及次数）",
        "",
    ]
    for code, count in confirmed_ids.most_common(100):
        rec = code_map[code_key(code)]
        report.append(f"- {rec.get('canonical_name','')}（{code}）：{count} 帖")
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"posts={len(resolutions)} confirmed_posts={confirmed_posts} ambiguous_posts={ambiguous_posts} companies={len(confirmed_ids)}")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
