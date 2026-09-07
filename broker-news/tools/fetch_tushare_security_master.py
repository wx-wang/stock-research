#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch a read-only A-share/HK security master through the Tushare MCP.

The output is a reference file for deterministic entity resolution. It is not
an investment database and contains no claims extracted from the source text.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reference"


def call_tool(url: str, name: str, arguments: dict) -> list[dict]:
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8", "replace")
    messages = [json.loads(line[6:]) for line in raw.splitlines() if line.startswith("data: ")]
    if not messages:
        raise RuntimeError(f"MCP returned no message for {name}")
    message = messages[-1]
    if "error" in message:
        raise RuntimeError(json.dumps(message["error"], ensure_ascii=False))
    result = message.get("result", {})
    if result.get("isError"):
        text = " ".join(c.get("text", "") for c in result.get("content", []))
        raise RuntimeError(text or f"Tushare tool error: {name}")
    texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
    if not texts:
        return []
    payload = texts[-1]
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Unexpected {name} payload: {payload[:200]}") from exc
    if isinstance(data, dict):
        return [data]
    return data


def main() -> int:
    url = os.environ.get("TUSHARE_MCP_URL")
    if not url:
        print("TUSHARE_MCP_URL is required", file=sys.stderr)
        return 2
    common_a = [
        "ts_code", "symbol", "name", "fullname", "enname", "cnspell",
        "market", "exchange", "list_status", "industry", "list_date",
        "delist_date", "is_hs",
    ]
    common_hk = [
        "ts_code", "name", "fullname", "enname", "cn_spell", "market",
        "list_status", "list_date", "delist_date",
    ]
    a = call_tool(url, "stock_basic", {"list_status": "L", "fields": common_a})
    hk = call_tool(url, "hk_basic", {"list_status": "L", "fields": common_hk})
    payload = {
        "as_of": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "Tushare MCP",
        "a_share": a,
        "hk": hk,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "tushare_security_master_20260824.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved {out}")
    print(f"A股 {len(a)} 条；港股 {len(hk)} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
