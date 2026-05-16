#!/usr/bin/env python3
"""Fetch YouTube video metadata and print it as Markdown to stdout.

Usage: fetch_metadata.py <youtube-url>
"""
import json
import re
import subprocess
import sys


def _duration(seconds: int) -> str:
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _chapters(description: str) -> list[tuple[str, str]]:
    rows = []
    for line in description.splitlines():
        m = re.match(r"^\s*(\d+:\d{2}(?::\d{2})?)\s+(.+)", line)
        if m:
            rows.append((m.group(1), m.group(2).strip()))
    return rows


def fetch(url: str) -> str:
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-playlist", url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    d = json.loads(result.stdout)

    title = d["title"]
    channel = d["channel"]
    raw_date = d["upload_date"]
    date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    duration = _duration(int(d["duration"]))
    views = f"{d['view_count']:,}"
    url_out = d["webpage_url"]
    description = d.get("description", "")

    lines = [
        f"# {title}",
        "",
        "## Video Metadata",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Channel** | {channel} |",
        f"| **Published** | {date} |",
        f"| **Duration** | {duration} |",
        f"| **Views** | {views} |",
        f"| **URL** | {url_out} |",
        "",
        "## Description",
        "",
        description,
    ]

    chapters = _chapters(description)
    if chapters:
        lines += [
            "",
            "### Chapters",
            "",
            "| Timestamp | Topic |",
            "|-----------|-------|",
        ]
        for ts, topic in chapters:
            lines.append(f"| {ts} | {topic} |")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: fetch_metadata.py <youtube-url>", file=sys.stderr)
        sys.exit(1)
    try:
        print(fetch(sys.argv[1]))
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
