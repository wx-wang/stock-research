#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建 A股 + 港股通 股票词典(名称/代码), 缓存到 stock_dict.json。
A股: akshare stock_info_a_code_name (官方交易所源, 稳定)
港股通: akshare stock_hk_ggt_components_em (eastmoney, 网络抖动时自动重试)
"""
import json
import os
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

OUT = Path(__file__).resolve().parent / "stock_dict.json"


def norm(s: str) -> str:
    s = (s or "").replace(" ", "").replace("\u3000", "")
    out = []
    for c in s:
        o = ord(c)
        out.append(chr(o - 0xFEE0) if 0xFF01 <= o <= 0xFF5E else c)
    return "".join(out).upper()


def fetch_with_retry(fn, tries=4, delay=3):
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            print(f"  第{i+1}次失败: {str(e)[:100]}", flush=True)
            time.sleep(delay)
    return None


def main() -> int:
    # A股
    a = fetch_with_retry(lambda: __import__("akshare").stock_info_a_code_name())
    if a is None:
        print("A股列表获取失败"); return 1

    # 港股通(成分股, 与沪深交易所公布一致)
    hk = fetch_with_retry(lambda: __import__("akshare").stock_hk_ggt_components_em())

    stocks = {"A股": [], "港股通": []}
    for _, r in a.iterrows():
        name = norm(str(r["name"]))
        if name:
            stocks["A股"].append({"code": str(r["code"]).zfill(6), "name": name, "norm": name})
    if hk is not None:
        for _, r in hk.iterrows():
            name = norm(str(r["名称"]))
            if name:
                stocks["港股通"].append({"code": str(r["代码"]).zfill(5), "name": name, "norm": name})

    OUT.write_text(json.dumps(stocks, ensure_ascii=False), encoding="utf-8")
    print(f"词典已保存 {OUT}: A股 {len(stocks['A股'])} 只, 港股通 {len(stocks['港股通'])} 只")
    return 0


if __name__ == "__main__":
    sys.exit(main())