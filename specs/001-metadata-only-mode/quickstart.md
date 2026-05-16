# Quickstart: Metadata-Only Retrieval Mode

**Branch**: `001-metadata-only-mode` | **Date**: 2026-05-16

---

## Overview

The `--metadata-only` flag lets you fetch a YouTube video's metadata (title, channel, date, duration, views, description, chapters) and print it to stdout — without downloading or processing any transcript. Useful for quick lookups and pipeline composition.

## Prerequisites

- `yt-dlp` on PATH
- Python 3.11+
- Claude Code with the `youtube-transcript` skill installed

## Usage

```
[YouTube URL] --metadata-only
```

**Example**:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ --metadata-only
```

**Example output** (stdout):

```markdown
# Rick Astley - Never Gonna Give You Up (Official Music Video)

## Video Metadata

| Field | Value |
|-------|-------|
| **Channel** | Rick Astley |
| **Published** | 2009-10-25 |
| **Duration** | 3:33 |
| **Views** | 1,500,000,000 |
| **URL** | https://www.youtube.com/watch?v=dQw4w9WgXcQ |

## Description

The official video for "Never Gonna Give You Up" by Rick Astley...
```

## Saving to a file

Pipe stdout to a file yourself:

```bash
# Ask Claude: "[URL] --metadata-only" then copy the output
# Or pipe via terminal:
claude -p "youtube-transcript: [URL] --metadata-only" > my-notes.md
```

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `--metadata-only and --output cannot be combined` | Both flags used together | Remove `--output` when using `--metadata-only` |
| yt-dlp error about private/deleted video | Video is inaccessible | Use a different URL |

## Verification

After implementation, confirm:

```bash
# 1. No file created in working directory
ls *.md   # should show no new file

# 2. Metadata fields present in output
# Output contains: title heading, Video Metadata table, Description section
```
