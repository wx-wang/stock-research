"""Register the repository's sole skill copies in the current user's Codex.

Never overwrite an existing installation. Use --check for a read-only check.
"""

import argparse
from pathlib import Path


SKILLS = (
    "industry-understanding",
    "investment-financial-statement-analysis",
    "narrative-valuation",
)
PROJECT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--skills-dir", type=Path, default=Path.home() / ".agents" / "skills"
    )
    args = parser.parse_args()
    destination = args.skills_dir.expanduser().absolute()
    pending = []
    conflicts = []
    for name in SKILLS:
        source = PROJECT / "Skills" / name
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"Missing skill source: {source}")
        link = destination / name
        if link.is_symlink() and link.resolve() == source.resolve():
            print(f"OK: {name}")
        elif link.exists() or link.is_symlink():
            conflicts.append(str(link))
        else:
            pending.append((link, source))
    # Check all conflicts before any changes, including legacy global copies.
    legacy = Path.home() / ".codex" / "skills"
    if destination == (Path.home() / ".agents" / "skills").absolute():
        for name in SKILLS:
            old = legacy / name
            if old.exists() or old.is_symlink():
                conflicts.append(str(old))
    if conflicts:
        raise SystemExit(
            "Existing or duplicate installations found; compare and archive them first.\n"
            + "\n".join(conflicts)
        )
    if args.check:
        for link, _ in pending:
            print(f"NOT REGISTERED: {link.name}")
        raise SystemExit(1 if pending else 0)
    created = []
    try:
        if pending:
            destination.mkdir(parents=True, exist_ok=True)
        for link, source in pending:
            link.symlink_to(source, target_is_directory=True)
            created.append(link)
            if not (link / "SKILL.md").samefile(source / "SKILL.md"):
                raise RuntimeError(f"Link verification failed: {link}")
            print(f"REGISTERED: {link.name}")
    except Exception:
        for link in reversed(created):
            if link.is_symlink():
                link.unlink()
        raise


if __name__ == "__main__":
    main()
