#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拉取知识星球「观察者03」最近 N 周的主题，按 ISO 周分别存入 Markdown 文件。

用法:
    python3 pull_zsxq_weekly.py                    # 默认拉 26 周（约 6 个月）
    python3 pull_zsxq_weekly.py --weeks 4          # 只拉最近 4 周

特性:
    - 按 topic_id 去重（翻页边界会重复返回同一条）
    - 每周一个 md 文件: observer03_<年>-W<周>_<周一>_<周日>.md
    - 断点续传: 状态存 broker-news/.pull_state.json, 中断后重跑即可续拉
    - 失败自动重试; 每次调用间隔 0.35s 避免触发限流
    - 图片帖只记录占位, 音频帖记录文件名（本轮只处理文字）
    - 结束后做一次全局去重清理
输出目录: broker-news/ (脚本所在目录的上一级)
"""

import datetime
import html
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

GROUP_ID = "15525241828412"          # 观察者03
PAGE_SIZE = 30                       # zsxq-cli 单页上限
OUT_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = OUT_DIR / ".pull_state.json"
LOG_FILE = OUT_DIR / ".pull_progress.log"
CALL_INTERVAL = 0.35                 # 每页间隔(秒)
MAX_RETRY = 6
CKPT_EVERY = 30                      # 每 30 页存一次检查点
TZ8 = datetime.timezone(datetime.timedelta(hours=8))


def now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    line = f"[{now_str()}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def call_api(end_time: str | None):
    """调用 zsxq-cli 取一页, 失败重试, 返回 dict 或 None(最终失败)。"""
    cmd = [shutil.which("zsxq-cli") or "zsxq-cli", "group", "+topics",
           "--group-id", GROUP_ID, "--limit", str(PAGE_SIZE), "--json"]
    if end_time:
        cmd += ["--end-time", end_time]
    last_err = None
    for attempt in range(1, MAX_RETRY + 1):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if r.returncode == 0:
                data = json.loads(r.stdout)
                if data.get("success") is False:
                    raise RuntimeError(f"API success=false: {r.stdout[:300]}")
                return data
            last_err = f"rc={r.returncode} err={r.stderr[:200]}"
        except Exception as e:  # noqa: BLE001
            last_err = str(e)
        log(f"  第{attempt}次重试: {last_err}")
        time.sleep(5 * attempt)
    return None


def clean_text(s: str | None) -> str:
    if not s:
        return ""
    s = re.sub(r"<e[^>]*/>", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return s.strip()


def topic_section(idx_in_week: int, b: dict) -> str:
    """把一条主题格式化成 md 片段 (带 topic_id 标记便于去重)。"""
    tid = b.get("topic_id")
    ttype = b.get("type")
    ct = b.get("create_time", "")
    title = clean_text(b.get("title"))
    content = clean_text(b.get("content"))
    files = [f.get("name") for f in (b.get("files") or [])]
    imgs = b.get("images") or []

    lines = [f"<!-- topic_id: {tid} -->", f"### {idx_in_week}. [{ttype}] {ct}"]
    if title and title not in ("「文件」", "「图片」"):
        lines.append(f"**标题**：{title}")
    if content and content not in ("「文件」", "「图片」"):
        lines.append("**内容**：")
        lines.append("")
        lines.append(content)
    if files:
        lines.append("**附件（音频/文件）**：")
        lines.append("")
        lines.extend(f"- {f}" for f in files)
    if imgs and not content.strip():
        lines.append("**[图片帖]**（本轮未做图片识别，仅记录存在图片）")
    if b.get("digested"):
        lines.append("")
        lines.append("> 精华帖")
    lines.append("")
    return "\n".join(lines) + "\n"


def week_file(y: int, w: int) -> Path:
    mon = datetime.date.fromisocalendar(y, w, 1)
    sun = mon + datetime.timedelta(days=6)
    return OUT_DIR / f"observer03_{y}-W{w:02d}_{mon.strftime('%Y-%m-%d')}_{sun.strftime('%Y-%m-%d')}.md"


def ensure_header(fp: Path, y: int, w: int) -> None:
    if fp.exists():
        return
    mon = datetime.date.fromisocalendar(y, w, 1)
    sun = mon + datetime.timedelta(days=6)
    fp.write_text(
        f"# 观察者03 · 知识星球周报（{mon} ~ {sun}）\n\n"
        f"- 星球：观察者03（group_id `{GROUP_ID}`）\n"
        f"- 拉取脚本：`tools/pull_zsxq_weekly.py`\n"
        f"- 说明：图片帖仅占位，音频帖仅记录文件名\n\n---\n\n",
        encoding="utf-8",
    )


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            log("状态文件损坏，从零开始")
    return {"end_time": None, "pages": 0, "topics": 0, "last_ids": []}


def finalize_dedupe() -> None:
    """按 topic_id 标记清理每个周文件里的重复区块（断点续传边界可能引入）。"""
    cleaned_files = 0
    for fp in sorted(OUT_DIR.glob("observer03_*-W*.md")):
        text = fp.read_text(encoding="utf-8")
        blocks = re.split(r"\n(?=<!-- topic_id: )", text)
        seen: set[str] = set()
        kept = []
        dup = 0
        for blk in blocks:
            m = re.search(r"<!-- topic_id: (\d+) -->", blk)
            if not m:
                kept.append(blk)
                continue
            tid = m.group(1)
            if tid in seen:
                dup += 1
                continue
            seen.add(tid)
            kept.append(blk)
        if dup:
            fp.write_text("\n".join(kept), encoding="utf-8")
            cleaned_files += 1
            log(f"去重 {fp.name}: 移除 {dup} 条重复")
    log(f"全局去重完成（清理 {cleaned_files} 个文件）")


def main() -> int:
    weeks = 26
    if "--weeks" in sys.argv:
        weeks = int(sys.argv[sys.argv.index("--weeks") + 1])

    cutoff = datetime.datetime.now(TZ8) - datetime.timedelta(weeks=weeks)
    state = load_state()
    end_time = state.get("end_time")
    seen: set[str] = set(state.get("last_ids", []))
    pages = int(state.get("pages", 0))
    total = int(state.get("topics", 0))

    log(f"开始拉取: group={GROUP_ID}, 窗口=最近{weeks}周(截止 {cutoff.date()}), "
        f"断点={'有' if end_time else '无'}, 已累计 {total} 条")
    if end_time:
        log(f"从游标 {end_time} 继续")

    guard_streak = 0
    while True:
        data = call_api(end_time)
        if data is None:
            save_state({"end_time": end_time, "pages": pages, "topics": total,
                        "last_ids": sorted(seen)[-PAGE_SIZE:]})
            log(f"API 连续失败，已存档可续传（end_time={end_time}）。请重跑本脚本。")
            return 1

        briefs = data.get("topics_brief") or []
        if not briefs:
            log("返回空页：历史已拉完（has_more 未置位或到达尽头）")
            break

        has_more = bool(data.get("has_more"))
        new_ids = []
        for b in briefs:
            tid = str(b.get("topic_id"))
            if tid in seen:
                continue
            seen.add(tid)
            new_ids.append(b)

        if not new_ids:
            guard_streak += 1
            log(f"本页无新主题（第{guard_streak}次）")
            if guard_streak >= 3:
                log("连续 3 页无新主题，停止（可能是 API 游标循环）")
                break
        else:
            guard_streak = 0
            # 按周分组写入（序号 = 该周文件内累计条数）
            per_week: dict[tuple, list] = {}
            for b in new_ids:
                dt = datetime.datetime.strptime(b["create_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
                iso = dt.isocalendar()
                per_week.setdefault((iso[0], iso[1]), []).append(b)
            for (y, w), items in per_week.items():
                fp = week_file(y, w)
                ensure_header(fp, y, w)
                with open(fp, "r", encoding="utf-8") as f:
                    cnt = sum(1 for line in f if line.startswith("### "))
                with open(fp, "a", encoding="utf-8") as f:
                    for b in items:
                        cnt += 1
                        f.write(topic_section(cnt, b))
            total += len(new_ids)

        pages += 1
        next_end = data.get("next_end_time")
        newest = briefs[0]["create_time"]
        oldest = briefs[-1]["create_time"]
        if pages % 20 == 0 or pages <= 3:
            log(f"页{pages}: +{len(new_ids)}条, 累计{total}条, 最新{newest[:16]}, 最老{oldest[:16]}")

        # 终止条件: 达到 6 个月窗口
        t_oldest = datetime.datetime.strptime(oldest, "%Y-%m-%dT%H:%M:%S.%f%z")
        if t_oldest < cutoff:
            log(f"已到达窗口边界（{oldest} < {cutoff.strftime('%Y-%m-%d')}），拉取完成")
            break
        if not has_more or not next_end:
            log("has_more=False，历史全部拉完")
            break

        # 检查点
        if pages % CKPT_EVERY == 0:
            save_state({"end_time": next_end, "pages": pages, "topics": total,
                        "last_ids": [str(b.get("topic_id")) for b in briefs]})
        end_time = next_end
        time.sleep(CALL_INTERVAL)

    save_state({"end_time": end_time, "pages": pages, "topics": total,
                "last_ids": [], "done": True})
    finalize_dedupe()
    log(f"拉取完成: 共 {pages} 页, {total} 条主题")
    # 输出每周统计
    log("== 每周文件统计 ==")
    for fp in sorted(OUT_DIR.glob("observer03_*-W*.md")):
        n = sum(1 for line in fp.read_text(encoding="utf-8").splitlines() if line.startswith("### "))
        log(f"  {fp.name}: {n} 条, {fp.stat().st_size/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())