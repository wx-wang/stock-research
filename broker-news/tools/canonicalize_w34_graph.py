#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonicalize a Hyper-Extract graph with the Tushare security master.

The raw extraction remains untouched. This pass only merges duplicate company
nodes, normalizes company names/codes, drops malformed edges, and produces a
small audit report.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "kb_W34_investment_v1"
OUT = ROOT / "kb_W34_investment_v1_canonical"
MASTER = ROOT / "reference" / "tushare_security_master_20260824.json"

ALLOWED_TYPES = {
    "公司", "行业", "产业链环节", "产品技术", "事件催化剂", "宏观变量",
    "市场叙事", "机构人物", "地点", "其他",
}


def compact(value: str) -> str:
    return re.sub(r"[\s\u3000·•_\-—/（）()]+", "", (value or "")).upper()


def main() -> int:
    raw = json.loads((RAW / "data.json").read_text(encoding="utf-8"))
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    by_code = {r["ts_code"].upper(): r for r in master.get("a_share", []) + master.get("hk", [])}
    by_name = defaultdict(list)
    for r in by_code.values():
        for name in (r.get("name"), r.get("fullname")):
            if name:
                by_name[compact(name)].append(r)

    merged: dict[str, dict] = {}
    original_to_key: dict[str, str] = {}
    name_to_keys: defaultdict[str, set[str]] = defaultdict(set)
    invalid_codes = []
    company_without_code = []

    for node in raw.get("nodes", []):
        original_name = str(node.get("name") or "").strip()
        ntype = str(node.get("type") or "其他").strip()
        if ntype not in ALLOWED_TYPES:
            ntype = "其他"
        code = str(node.get("canonical_id") or "").upper().strip()
        record = by_code.get(code)
        if record is None and ntype == "公司":
            candidates = by_name.get(compact(original_name), [])
            if len(candidates) == 1 and len(candidates[0].get("name", "")) >= 4:
                record = candidates[0]
                code = record["ts_code"]
        if code and code not in by_code:
            invalid_codes.append({"name": original_name, "code": code})
            code = ""
        if ntype == "公司" and not code:
            company_without_code.append(original_name)

        canonical_name = record.get("name") if record else original_name
        key = f"公司|{code}" if ntype == "公司" and code else f"{ntype}|{compact(canonical_name)}"
        out = merged.setdefault(key, {
            "name": canonical_name,
            "type": ntype,
            "canonical_id": code or None,
            "description": node.get("description"),
            "aliases": [],
        })
        for alias in [original_name, *(node.get("aliases") or [])]:
            if alias and alias != out["name"] and alias not in out["aliases"]:
                out["aliases"].append(alias)
        if node.get("description") and node["description"] not in (out.get("description") or ""):
            old = out.get("description") or ""
            out["description"] = (old + "；" + node["description"]).strip("；")[:1000]
        original_to_key[original_name] = key
        name_to_keys[original_name].add(key)

    edges = []
    dropped_edges = []
    edge_seen = set()
    for edge in raw.get("edges", []):
        source = str(edge.get("source") or "").strip()
        target = str(edge.get("target") or "").strip()
        etype = str(edge.get("type") or "提及").strip() or "提及"
        skey = original_to_key.get(source)
        tkey = original_to_key.get(target)
        if not skey or not tkey or skey == tkey:
            dropped_edges.append({"source": source, "target": target, "type": etype})
            continue
        sname = merged[skey]["name"]
        tname = merged[tkey]["name"]
        dedup = (sname, tname, etype)
        if dedup in edge_seen:
            continue
        edge_seen.add(dedup)
        edges.append({
            "source": sname,
            "target": tname,
            "type": etype,
            "description": edge.get("description"),
            "evidence": edge.get("evidence"),
        })

    data = {"nodes": list(merged.values()), "edges": edges}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "template": "investment/w34_graph",
        "source_graph": str(RAW),
        "security_master": str(MASTER),
        "type": "graph",
        "canonicalized": True,
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    report = [
        "# W34 投资图谱质量审计",
        "",
        f"- 原始节点：{len(raw.get('nodes', []))}",
        f"- 规范化节点：{len(data['nodes'])}",
        f"- 原始边：{len(raw.get('edges', []))}",
        f"- 规范化边：{len(edges)}",
        f"- 丢弃边（缺少端点或自环）：{len(dropped_edges)}",
        f"- 公司节点缺少有效代码：{len(company_without_code)}",
        f"- 无效代码：{len(invalid_codes)}",
        "",
        "## 节点类型",
        "",
    ]
    for key, count in Counter(n["type"] for n in data["nodes"]).most_common():
        report.append(f"- {key}：{count}")
    report.extend(["", "## 关系类型", ""])
    for key, count in Counter(e["type"] for e in edges).most_common():
        report.append(f"- {key}：{count}")
    report.extend(["", "## 需要人工复核的公司节点（前100）", ""])
    for name in sorted(set(company_without_code))[:100]:
        report.append(f"- {name}")
    (OUT / "audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"raw_nodes={len(raw.get('nodes', []))} canonical_nodes={len(data['nodes'])} raw_edges={len(raw.get('edges', []))} canonical_edges={len(edges)}")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
