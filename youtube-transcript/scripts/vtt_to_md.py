#!/usr/bin/env python3
"""Parse a YouTube VTT subtitle file into timestamped Markdown lines.

Usage: vtt_to_md.py [<path-to-vtt-file>|-]
       Reads from stdin when path is "-" or omitted.
Output: [MM:SS] line per unique segment, written to stdout.
"""
import re
import sys

_TS_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> ")
_TAG_RE = re.compile(r"<[^>]+>")


def parse_content(vtt: str) -> str:
    lines = []
    last_text: str | None = None

    for block in re.split(r"\n\s*\n", vtt.strip()):
        block_lines = block.strip().splitlines()
        ts_line = next((l for l in block_lines if _TS_RE.match(l)), None)
        if not ts_line:
            continue

        m = _TS_RE.match(ts_line)
        assert m is not None
        h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
        start = h * 3600 + mi * 60 + s

        idx = block_lines.index(ts_line)
        clean = [
            _TAG_RE.sub("", l).strip()
            for l in block_lines[idx + 1:]
            if l.strip() and "<" not in l
        ]
        if not clean:
            continue

        text = clean[-1]
        if text == last_text:
            continue
        last_text = text

        mins, secs = start // 60, start % 60
        lines.append(f"[{mins:02d}:{secs:02d}] {text}")

    return "\n".join(lines)


def parse(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return parse_content(f.read())


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "-":
        print(parse_content(sys.stdin.read()))
    elif len(sys.argv) == 2:
        print(parse(sys.argv[1]))
    else:
        print("Usage: vtt_to_md.py [<vtt-file>|-]", file=sys.stderr)
        sys.exit(1)
