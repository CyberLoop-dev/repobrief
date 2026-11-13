<p align="center">
  <img src="assets/banner.svg" alt="repobrief banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-38bdf8?style=for-the-badge" alt="python">
  <img src="https://img.shields.io/badge/dependencies-zero-818cf8?style=for-the-badge" alt="zero deps">
  <img src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge" alt="MIT">
</p>

**repobrief** packs a whole repository into a single, clean Markdown file you can paste straight into an LLM. One file, one command, no setup.

## Why

Chatting with an AI about your codebase usually means copy-pasting file after file. repobrief does it in one go: a file list, then every text file in its own fenced block, plus a token estimate so you know if it fits.

## Features

- Respects your `.gitignore`
- Skips binaries, lockfiles, images and huge files
- Skips `node_modules`, `.git`, `venv`, `dist` and friends
- Filter by extension, set a size limit
- Prints an approximate token count
- Pure Python, zero dependencies

## Usage

```bash
python repobrief.py .                       # print to stdout
python repobrief.py . -o brief.md           # write to a file
python repobrief.py ~/proj --ext .py .md    # only Python and Markdown
python repobrief.py . --max-bytes 20000     # skip files over 20 KB
```

Example stderr summary:

```
repobrief: 42 files, ~18,350 tokens
```

## Output shape

```markdown
# Repository: myproject

## Files

- main.py
- utils/helpers.py

## main.py

```py
print("hello")
```
```

## Notes

- Token count is a rough estimate (characters / 4), not exact.
- `.gitignore` support covers common patterns, not the full gitignore spec.

## License

MIT
