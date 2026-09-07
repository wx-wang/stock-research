#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并行拉取知识星球「观察者03」最近 N 周: 按时间切成多段, 每段一个独立进程,
段间留重叠, 合并时按 topic_id 去重。

用法:
    python3 pull_zsxq_parallel.py                 # 默认 5 段 × 26 周
    python3 pull_zsxq_parallel.py --segs 5 --weeks 26
    python3 pull_zsxq_parallel.py --worker --seg 0 --low ... --high ...   # 内部 worker 模式

分段说明:
    6 个月时间线均分成 K 段, 每段从段上界往回翻页到 (名义下界 - 2 天) 为止,
    与相邻段有 2 天重叠, 重叠区的重复主题在合并阶段按 topic_id 去掉。
    worker 独立存 state.json, 中断后重跑父进程会断点续传。
"""

import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pull_zsxq_weekly as w  # noqa: E402  复用 call_api / clean_text / topic_section

PARALLEL_SCRIPT = Path(__file__).resolve()
OUT_DIR = w.OUT_DIR
TMP_DIR = OUT_DIR / ".tmp_segs"
SEGS_DEFAULT = 5
OVERLAP_DAYS = 2
WORKER_INTERVAL = 0.9


# ---------- worker ----------

def worker_main(seg: int, low: datetime.datetime, high: datetime.datetime) -> int:
    segdir = TMP_DIR / f"seg{seg}"
    segdir.mkdir(parents=True, exist_ok=True)
    statefile = segdir / "state.json"
    logfile = segdir / "worker.log"

    def slog(msg: str) -> None:
        line = f"[{w.now_str()}] [seg{seg}] {msg}"
        print(line, flush=True)
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    state = {"end_time": None, "pages": 0, "topics": 0, "last_ids": [], "done": False}
    if statefile.exists():
        try:
            state.update(json.loads(statefile.read_text(encoding="utf-8")))
        except Exception:  # noqa: BLE001
            pass
    if state.get("done"):
        slog("该段已完成, 跳过")
        return 0
    end_time = state.get("end_time") or ts_ms(high)
    seen: set[str] = set(state.get("last_ids", []))
    pages = int(state.get("pages", 0))
    total = int(state.get("topics", 0))

    def save_state(next_end=None, done=False) -> None:
        # 原子写: 先写临时文件再 rename, 防止写一半崩溃损坏 state
        tmp = statefile.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(
            {"end_time": next_end, "pages": pages, "topics": total,
             "last_ids": sorted(seen)[-w.PAGE_SIZE:], "done": done},
            ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, statefile)

    slog(f"启动: 窗口 [{low.strftime('%Y-%m-%d')} ~ {high.strftime('%Y-%m-%d')}], "
         f"游标 {end_time[:10]}, 已累计 {total} 条")

    guard = 0
    while True:
        data = w.call_api(end_time)
        if data is None:
            save_state(end_time)
            slog("连续失败, 已存档可续传")
            return 1

        briefs = data.get("topics_brief") or []
        if not briefs:
            slog("空页, 到历史尽头")
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
            guard += 1
            if guard >= 3:
                slog("连续 3 页无新主题, 停止(疑似游标循环)")
                break
        else:
            guard = 0
            per_week: dict[tuple, list] = {}
            for b in new_ids:
                dt = datetime.datetime.strptime(b["create_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
                iso = dt.isocalendar()
                per_week.setdefault((iso[0], iso[1]), []).append(b)
            for (y, wk), items in per_week.items():
                fp = week_file_in(segdir, y, wk)
                ensure_header_in(fp, y, wk)
                with open(fp, "r", encoding="utf-8") as f:
                    cnt = sum(1 for line in f if line.startswith("### "))
                with open(fp, "a", encoding="utf-8") as f:
                    for b in items:
                        cnt += 1
                        f.write(w.topic_section(cnt, b))

            total += len(new_ids)
            # 检查是否越过本段下界: 但注意 weekly 文件要按实际时间写,
            # 边界外多抓的几条也写入(合并去重), 不影响。
            if total % 500 == 0:
                slog(f"累计 {total} 条, 最新 {briefs[0]['create_time'][:16]}, "
                     f"最老 {briefs[-1]['create_time'][:16]}")

        pages += 1
        next_end = data.get("next_end_time")
        oldest = briefs[-1]["create_time"]
        if pages % 20 == 0:
            slog(f"页{pages}, +{len(new_ids)}条, 累计{total}条, 最老{oldest[:16]}")

        t_oldest = datetime.datetime.strptime(oldest, "%Y-%m-%dT%H:%M:%S.%f%z")
        if t_oldest < low:
            slog(f"到达段下界 {low.strftime('%Y-%m-%d')} (最老 {oldest[:10]}), 完成")
            break
        if not has_more or not next_end:
            slog("has_more=False, 历史尽头")
            break

        if pages % 10 == 0:
            save_state(next_end)
        end_time = next_end
        time.sleep(WORKER_INTERVAL)

    save_state(end_time, done=True)
    return 0


def week_file_in(segdir: Path, y: int, wk: int) -> Path:
    mon = datetime.date.fromisocalendar(y, wk, 1)
    sun = mon + datetime.timedelta(days=6)
    return segdir / f"observer03_{y}-W{wk:02d}_{mon.strftime('%Y-%m-%d')}_{sun.strftime('%Y-%m-%d')}.md"


def ensure_header_in(fp: Path, y: int, wk: int) -> None:
    if fp.exists():
        return
    mon = datetime.date.fromisocalendar(y, wk, 1)
    sun = mon + datetime.timedelta(days=6)
    fp.write_text(
        f"# 观察者03 · 知识星球周报（{mon} ~ {sun}）\n\n"
        "- 星球：观察者03（group_id `15525241828412`）\n"
        "- 拉取脚本：`tools/pull_zsxq_parallel.py`\n"
        "- 说明：图片帖仅占位，音频帖仅记录文件名\n\n---\n\n",
        encoding="utf-8",
    )


def ts_ms(dt: datetime.datetime) -> str:
    """格式化为 zsxq API 认可的毫秒时间戳(微秒格式会被拒绝)。"""
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{dt.microsecond // 1000:03d}+0800"


# ---------- 父进程 ----------

def segment_windows(weeks: int, segs: int):
    """把 [now-6mo, now] 均匀切成 segs 段(新→旧), 每段向下多挖 OVERLAP_DAYS 天。"""
    now = datetime.datetime.now(w.TZ8)
    start = now - datetime.timedelta(weeks=weeks)
    step = (now - start) / segs
    windows = []
    for i in range(segs):
        high = now - i * step
        low = start + (segs - 1 - i) * step - datetime.timedelta(days=OVERLAP_DAYS)
        if i == segs - 1:   # 最旧段
            low = start - datetime.timedelta(days=OVERLAP_DAYS)
        windows.append((low, high))
    return windows


def merge_and_finalize() -> int:
    """把各段临时周文件合并成最终周文件: 按 topic_id 去重, 按时间升序重排。"""
    final_files: dict[tuple, Path] = {}
    blobs: dict[tuple, list[tuple[str, str, str, str]]] = {}  # (y,w) -> [(topic_id, ts, block, seg)]

    for segdir in sorted(TMP_DIR.glob("seg*")):
        for fp in sorted(segdir.glob("observer03_*-W*.md")):
            m = re.match(r"observer03_(\d+)-W(\d+)_", fp.name)
            if not m:
                continue
            key = (int(m.group(1)), int(m.group(2)))
            final_files.setdefault(key, w.week_file(*key))
            text = fp.read_text(encoding="utf-8")
            for blk in re.split(r"\n(?=<!-- topic_id: )", text):
                tm = re.search(r"<!-- topic_id: (\d+) -->", blk)
                hm = re.search(r"^### \d+\. \[\w+\] (\S+)", blk, re.M)
                if not tm:
                    continue  # header 等内容块跳过
                blobs.setdefault(key, []).append(
                    (tm.group(1), hm.group(1) if hm else "", blk, segdir.name))

    total_topics = 0
    for key, final_fp in sorted(final_files.items()):
        items = blobs.get(key, [])
        uniq = {}
        for tid, ts, blk, seg in items:
            uniq.setdefault(tid, (ts, blk))   # 保留首个
        ordered = sorted(uniq.values(), key=lambda x: x[0])
        y, wk = key
        mon = datetime.date.fromisocalendar(y, wk, 1)
        sun = mon + datetime.timedelta(days=6)
        lines = [
            f"# 观察者03 · 知识星球周报（{mon} ~ {sun}）\n",
            f"- 星球：观察者03（group_id `15525241828412`）",
            f"- 拉取脚本：`tools/pull_zsxq_parallel.py`",
            f"- 共 {len(ordered)} 条 / 按 topic_id 去重",
            f"- 说明：图片帖仅占位，音频帖仅记录文件名\n",
            "---\n",
        ]
        for i, (ts, blk) in enumerate(ordered, 1):
            blk = re.sub(r"^### \d+\. ", f"### {i}. ", blk, count=1, flags=re.M)
            lines.append(blk)
        final_fp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        total_topics += len(ordered)
        w.log(f"合并 {final_fp.name}: {len(ordered)} 条")

    # 安全清理: 只有所有最终文件都成功写出且非空后才删除临时段目录,
    # 否则保留现场供重跑恢复(重跑 merge 会用临时数据覆盖重建最终文件)。
    import shutil
    finals_ok = all(fp.exists() and fp.stat().st_size > 0 for fp in final_files.values())
    if finals_ok:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
        w.log("临时段目录已清理")
    else:
        w.log("[警告] 部分最终文件未写完整, 保留临时段目录供恢复")
    w.log(f"=== 全部完成: {len(final_files)} 个周文件, {total_topics} 条主题 ===")
    for fp in sorted(OUT_DIR.glob("observer03_*-W*.md")):
        w.log(f"  {fp.name}: {fp.stat().st_size/1024:.0f} KB")
    return 0


def parent_main(weeks: int, segs: int) -> int:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    windows = segment_windows(weeks, segs)

    # 续传模式: 不删任何段文件, worker 从各自 state.json 游标继续追加
    for segdir in TMP_DIR.glob("seg*"):
        if (segdir / "state.json").exists():
            w.log(f"检测到 {segdir.name} 有断点, 将续传")

    # 防重复 worker: 若上次运行遗留的 worker 进程还在(孤儿), 先收掉再启动新的,
    # 避免同一段两个进程同时写 md/state 造成数据混乱。
    import signal
    stale = []
    for segdir in TMP_DIR.glob("seg*"):
        pidf = segdir / "worker.pid"
        if pidf.exists():
            try:
                pid = int(pidf.read_text().strip())
                os.kill(pid, 0)  # 探测是否存活
                stale.append(pid)
            except (ValueError, ProcessLookupError):
                pass
    for pid in stale:
        w.log(f"清理遗留 worker pid={pid}")
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    time.sleep(2)

    procs = []
    for i, (low, high) in enumerate(windows):
        cmd = [sys.executable, str(PARALLEL_SCRIPT), "--worker", "--seg", str(i),
               "--low", low.strftime("%Y-%m-%d"), "--high", high.strftime("%Y-%m-%d")]
        w.log(f"启动段{i}: [{low.strftime('%Y-%m-%d')} ~ {high.strftime('%Y-%m-%d')}]")
        segdir = TMP_DIR / f"seg{i}"
        segdir.mkdir(parents=True, exist_ok=True)
        logf = open(segdir / "proc.log", "ab")
        p = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT)
        (segdir / "worker.pid").write_text(str(p.pid))
        procs.append((i, p))
        time.sleep(1)  # 错峰启动, 降低限流风险

    failed = []
    for i, p in procs:
        rc = p.wait()
        if rc != 0:
            failed.append(i)
    if failed:
        w.log(f"段 {failed} 未完成, 中间状态已存档, 重跑本脚本即可续传")
        return 1
    return merge_and_finalize()


if __name__ == "__main__":
    if "--worker" in sys.argv:
        seg = int(sys.argv[sys.argv.index("--seg") + 1])
        low = datetime.datetime.strptime(sys.argv[sys.argv.index("--low") + 1], "%Y-%m-%d").replace(tzinfo=w.TZ8)
        high = datetime.datetime.strptime(sys.argv[sys.argv.index("--high") + 1], "%Y-%m-%d").replace(tzinfo=w.TZ8)
        sys.exit(worker_main(seg, low, high))

    weeks = 26
    segs = SEGS_DEFAULT
    if "--weeks" in sys.argv:
        weeks = int(sys.argv[sys.argv.index("--weeks") + 1])
    if "--segs" in sys.argv:
        segs = int(sys.argv[sys.argv.index("--segs") + 1])
    sys.exit(parent_main(weeks, segs))