#!/usr/bin/env python3
"""Minimal guardrails for PRs on the macOS maintainer line.

Checks only documentation presence and coarse Apple-header guards.
Does not build native code or touch donor trees.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "docs/macos.md",
    "docs/macos-baseline.md",
    "docs/macos-gaps.md",
    "docs/maintainers/grok-bot-duty.md",
    ".cursor/BUGBOT.md",
    ".cursor/config/bugbot.yaml",
    "AGENTS.md",
    "tools/bootstrap_macos_helper.py",
    "tools/build.py",
)

APPLE_INCLUDE = re.compile(
    r'^\s*#\s*include\s*[<"](?:CoreText|ImageIO|CoreGraphics|CoreFoundation|Security)/'
)

IFDEF_WIN32 = re.compile(r"^\s*#\s*if(?:n)?def\s+_WIN32\b")
IFNDEF_WIN32 = re.compile(r"^\s*#\s*ifndef\s+_WIN32\b")
ELSE = re.compile(r"^\s*#\s*else\b")
ENDIF = re.compile(r"^\s*#\s*endif\b")


def iter_flat_src_cpp() -> list[Path]:
    src = ROOT / "src"
    if not src.is_dir():
        return []
    files: list[Path] = []
    for domain in sorted(p for p in src.iterdir() if p.is_dir()):
        for cpp in sorted(domain.glob("*.cpp")):
            # Nested paths under a domain are rejected by product_sources; skip deeper.
            if cpp.parent == domain:
                files.append(cpp)
    return files


def unguarded_apple_includes(path: Path) -> list[int]:
    """Return 1-based line numbers of Apple includes outside a non-Windows region."""
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # Stack of regions: True = currently in a non-Windows-only compile region.
    # Start: compiling on Windows, so Apple includes are not allowed.
    stack: list[bool] = [False]
    bad: list[int] = []

    for i, line in enumerate(text, start=1):
        if IFNDEF_WIN32.match(line):
            # Non-Windows region begins.
            stack.append(True)
            continue
        if IFDEF_WIN32.match(line):
            # Windows region begins (Apple includes not allowed here).
            stack.append(False)
            continue
        if ELSE.match(line) and stack:
            stack[-1] = not stack[-1]
            continue
        if ENDIF.match(line):
            if len(stack) > 1:
                stack.pop()
            continue
        if APPLE_INCLUDE.match(line) and not stack[-1]:
            bad.append(i)
    return bad


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_PATHS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing required path: {rel}")

    for cpp in iter_flat_src_cpp():
        for line_no in unguarded_apple_includes(cpp):
            rel = cpp.relative_to(ROOT).as_posix()
            errors.append(f"unguarded Apple include: {rel}:{line_no}")

    if errors:
        print("mac_pr_guard: FAILED")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("mac_pr_guard: ok")
    print(f"  checked {len(REQUIRED_PATHS)} required paths")
    print(f"  scanned {len(iter_flat_src_cpp())} flat src/*.cpp files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
