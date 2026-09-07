#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 Hyper-Extract Python API 抽取一个 Markdown 到知识库,
显式控制 LLM 并发(max_workers, 默认 10)。

用法(用 uv tool 环境里的 python 运行):
    /Users/bella/.local/share/uv/tools/hyperextract/bin/python parse_week.py \
        <input.md> <output_dir> [max_workers]
"""
import sys
import time
from pathlib import Path

from hyperextract import Template, get_client
from hyperextract.utils.logging import configure_logging
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main() -> int:
    md = Path(sys.argv[1])
    out = Path(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    # 打开阶段级进度日志(DEBUG 级会输出 stage=two_stage_chunks / node_extraction /
    # edge_extraction / merge_start 等标记), 让全量跑时能实时看到进行到哪一步
    configure_logging("DEBUG")

    llm, emb = get_client()  # 读取 ~/.he/config.toml
    ka = Template.create("general/graph", "zh", llm, emb, max_workers=workers)
    text = md.read_text(encoding="utf-8")

    # 预估文本块数(与 graph 模板默认参数一致: chunk_size=2048, overlap=256)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2048, chunk_overlap=256,
        separators=["\n\n", "\n", "。", "！", "？", ". ", "! ", "? ", " ", ""]
    )
    n_chunks = len(splitter.split_text(text)) if len(text) > 2048 else 1
    print(f"输入: {md.name} | {len(text)} 字符 | 预计 {n_chunks} 块 | "
          f"并发 max_workers={workers} | 两阶段≈{2*n_chunks}次LLM调用", flush=True)
    t0 = time.time()
    ka.feed_text(text)
    print(f"抽取完成, 耗时 {time.time()-t0:.0f}s", flush=True)
    ka.dump(out)
    print("数据已保存", flush=True)
    t1 = time.time()
    ka.build_index()
    print(f"索引构建完成, 耗时 {time.time()-t1:.0f}s", flush=True)
    ka.dump(out)
    print(f"全部完成, 共耗时 {time.time()-t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())