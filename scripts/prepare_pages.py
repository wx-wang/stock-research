#!/usr/bin/env python3
"""从研究输出生成 MkDocs 的临时内容树。"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "研究输出"
CONTENT_ROOT = ROOT / "site_content"
BUILD_ROOT = ROOT / ".site-src"
IGNORED_NAMES = {".DS_Store"}
DATE_PATTERN = re.compile(r"^(\d{8})[_-]")


@dataclass(frozen=True)
class Report:
    source: Path
    relative: Path
    title: str
    date: str
    category: str


def title_from_markdown(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("# "):
                return line[2:].strip()
    return path.stem


def date_from_name(path: Path) -> str:
    match = DATE_PATTERN.match(path.name)
    if not match:
        return "未标注日期"
    raw = match.group(1)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"


def collect_reports() -> list[Report]:
    reports: list[Report] = []
    if not OUTPUT_ROOT.exists():
        return reports
    for path in sorted(OUTPUT_ROOT.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(OUTPUT_ROOT).parts):
            continue
        relative = path.relative_to(OUTPUT_ROOT)
        category = relative.parts[0] if len(relative.parts) > 1 else "其他"
        reports.append(
            Report(
                source=path,
                relative=relative,
                title=title_from_markdown(path),
                date=date_from_name(path),
                category=category,
            )
        )
    return reports


def copy_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        if any(part.startswith(".") for part in relative.parts):
            continue
        if path.name in IGNORED_NAMES:
            continue
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def markdown_link(path: Path) -> str:
    return "/".join(quote(part) for part in path.parts)


def build_homepage(reports: list[Report]) -> str:
    categories: dict[str, list[Report]] = {}
    for report in reports:
        categories.setdefault(report.category, []).append(report)

    publication_reports = [report for report in reports if report.category != "方法论"]
    recent_pool = publication_reports or reports
    recent = sorted(recent_pool, key=lambda item: (item.date, item.title), reverse=True)[:6]
    lines = [
        "---",
        "hide:",
        "  - navigation",
        "  - toc",
        "---",
        "",
        '<section class="archive-hero">',
        '  <p class="archive-kicker">可追溯的产业与公司研究</p>',
        "  <h1>从变化出发，<br>回到股东现金</h1>",
        "  <p>这里保存行业、财务与估值研究。每项判断都尽量标明证据日期、成立条件、主要缺口与证伪方式。</p>",
        '  <a class="archive-cta" href="#最新研究">阅读最新研究 <span aria-hidden="true">↓</span></a>',
        "</section>",
        "",
        '<div class="archive-statline">',
        f'  <span><strong>{len(reports)}</strong> 篇研究记录</span>',
        f'  <span><strong>{len(categories)}</strong> 个研究分类</span>',
        '  <span><strong>动态</strong> 随 main 分支更新</span>',
        "</div>",
        "",
        "## 最新研究",
        "",
    ]

    if recent:
        lines.append('<div class="report-list" markdown>')
        for report in recent:
            link = markdown_link(Path("研究输出") / report.relative)
            lines.extend(
                [
                    f'- <span class="report-date">{report.date}</span> '
                    f'<span class="report-type">{report.category}</span>  ',
                    f'  [**{report.title}**]({link})',
                ]
            )
        lines.extend(["</div>", ""])
    else:
        lines.extend(["> 尚无研究输出。新报告加入 `研究输出/` 后会自动出现在这里。", ""])

    lines.extend(["## 按研究类型浏览", "", '<div class="grid cards" markdown>', ""])
    for category, items in sorted(categories.items()):
        target = markdown_link(Path("研究输出") / category / "index.md")
        lines.extend(
            [
                f'-   **{category}**',
                "",
                f'    {len(items)} 篇记录，按日期与主题归档。',
                "",
                f'    [打开档案 →]({target})',
                "",
            ]
        )
    lines.extend(["</div>", "", "---", "", "*站内内容不构成证券推荐或交易建议。*", ""])
    return "\n".join(lines)


def write_directory_indexes(reports: list[Report]) -> None:
    grouped: dict[Path, list[Report]] = {}
    for report in reports:
        parent = report.relative.parent
        while parent != Path("."):
            grouped.setdefault(parent, []).append(report)
            parent = parent.parent

    root_index = BUILD_ROOT / "研究输出" / "index.md"
    root_index.parent.mkdir(parents=True, exist_ok=True)
    root_index.write_text(
        "# 研究输出\n\n按研究类型和主题浏览所有已归档成果。\n",
        encoding="utf-8",
    )

    for directory, items in grouped.items():
        index_path = BUILD_ROOT / "研究输出" / directory / "index.md"
        if index_path.exists():
            continue
        title = directory.name
        direct_children = [item for item in items if item.relative.parent == directory]
        lines = [f"# {title}", "", f"共 {len(items)} 篇相关记录。", ""]
        for report in sorted(direct_children, key=lambda item: (item.date, item.title), reverse=True):
            link = markdown_link(Path(report.relative.name))
            lines.append(f"- `{report.date}` [{report.title}]({link})")
        index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if BUILD_ROOT.exists():
        shutil.rmtree(BUILD_ROOT)
    BUILD_ROOT.mkdir(parents=True)

    copy_tree(CONTENT_ROOT, BUILD_ROOT)
    copy_tree(OUTPUT_ROOT, BUILD_ROOT / "研究输出")
    reports = collect_reports()
    (BUILD_ROOT / "index.md").write_text(build_homepage(reports), encoding="utf-8")
    write_directory_indexes(reports)
    print(f"Prepared {len(reports)} research documents in {BUILD_ROOT}")


if __name__ == "__main__":
    main()
