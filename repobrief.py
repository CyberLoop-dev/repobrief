#!/usr/bin/env python3
"""repobrief: pack a repo into ONE clean, LLM-ready text file."""
import argparse
import fnmatch
import os
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
             "build", ".next", ".idea", ".vscode"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
            ".gz", ".tar", ".woff", ".woff2", ".ttf", ".mp4", ".mp3", ".lock",
            ".pyc", ".so", ".exe", ".bin"}


def load_ignores(root):
    path = os.path.join(root, ".gitignore")
    pats = []
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(("#", "!")):
                    pats.append(line.strip("/"))
    return pats


def ignored(rel, pats):
    parts = rel.split("/")
    return any(fnmatch.fnmatch(rel, p) or any(fnmatch.fnmatch(x, p) for x in parts)
               for p in pats)


def is_text(path):
    try:
        with open(path, "rb") as f:
            return b"\0" not in f.read(2048)
    except OSError:
        return False


def collect(root, max_bytes, exts):
    pats = load_ignores(root)
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            ext = os.path.splitext(name)[1].lower()
            if ext in SKIP_EXT or ignored(rel, pats):
                continue
            if exts and ext not in exts:
                continue
            if os.path.getsize(full) > max_bytes or not is_text(full):
                continue
            files.append((rel, full))
    return files


def main():
    ap = argparse.ArgumentParser(description="Pack a repo into one LLM-friendly file.")
    ap.add_argument("path", nargs="?", default=".", help="repo folder (default: .)")
    ap.add_argument("-o", "--out", help="write to a file instead of stdout")
    ap.add_argument("--max-bytes", type=int, default=100_000,
                    help="skip files larger than this (default: 100000)")
    ap.add_argument("--ext", nargs="*", help="only these extensions, e.g. .py .md")
    a = ap.parse_args()

    exts = {e if e.startswith(".") else "." + e for e in (a.ext or [])}
    root = os.path.abspath(a.path)
    files = collect(root, a.max_bytes, exts)

    out = [f"# Repository: {os.path.basename(root)}", "", "## Files", ""]
    out += [f"- {rel}" for rel, _ in files]
    for rel, full in files:
        with open(full, encoding="utf-8", errors="replace") as f:
            text = f.read()
        lang = os.path.splitext(rel)[1].lstrip(".")
        out += ["", f"## {rel}", "", f"```{lang}", text.rstrip("\n"), "```"]
    body = "\n".join(out) + "\n"

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(body)
    else:
        sys.stdout.write(body)
    print(f"repobrief: {len(files)} files, ~{len(body) // 4:,} tokens", file=sys.stderr)


if __name__ == "__main__":
    main()
