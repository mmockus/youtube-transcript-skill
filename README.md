# youtube-transcript-skill

A Claude Code skill that fetches YouTube video transcripts and metadata. Supports two modes:

- **Full transcript** — writes a Markdown file with metadata, chapters, and timestamped transcript
- **Metadata only** — prints title, channel, date, duration, views, description, and chapters to stdout without downloading a transcript

Also ships two standalone Python scripts usable outside of Claude Code.

## Installation

```bash
git clone https://github.com/mmockus/youtube-transcript-skill.git ~/Development/youtube-transcript-skill

ln -sf ~/Development/youtube-transcript-skill/youtube-transcript \
       ~/.claude/skills/youtube-transcript
```

## Requirements

- `yt-dlp` on PATH (`brew install yt-dlp`)
- Python 3.11+

## Usage

Paste a YouTube URL into any Claude Code session — the skill triggers automatically. Or invoke it explicitly:

```
https://www.youtube.com/watch?v=VIDEO_ID
```

Optional flags:

| Flag | Description |
|------|-------------|
| `--metadata-only` | Print video metadata to stdout only; skip transcript download. No file is written. |
| `--output <name>` | Custom filename base (date still prepended: `2026-05-12-my-notes.md`). |
| `--output <name> --no-date` | Custom filename without date prefix. |

> **Note**: `--metadata-only` and `--output` cannot be combined.

## Output

**Full mode** (default) — writes a Markdown file to the current working directory:

```
2026-05-12-video-title-slug.md
```

Containing:
- Metadata table (channel, date, duration, views, URL)
- Description with chapters table (if present)
- Full timestamped transcript

**Metadata-only mode** (`--metadata-only`) — prints to stdout, no file written:

```markdown
# Video Title

## Video Metadata
| Field | Value |
...

## Description
...

### Chapters (if present)
...
```

## Standalone Scripts

These scripts work independently of Claude Code — useful for pipelines, automation, or quick lookups.

### `fetch_metadata.py` — fetch video metadata

Accepts a URL, prints Markdown metadata to stdout. No files written.

```bash
uv run python youtube-transcript/scripts/fetch_metadata.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Output includes: title heading, metadata table (channel, date, duration, views, URL), full description, and chapters table if present.

### `vtt_to_md.py` — parse a VTT subtitle file

Converts a VTT file (or stdin stream) into timestamped Markdown lines.

```bash
# From a local file
uv run python youtube-transcript/scripts/vtt_to_md.py /path/to/file.vtt

# From stdin (pipe from curl or yt-dlp)
curl -sL "https://example.com/captions.vtt" | uv run python youtube-transcript/scripts/vtt_to_md.py -
```

---

## Running Tests

No automated test suite. Run the smoke tests manually:

```bash
# See specs/001-metadata-only-mode/smoke-test.md for full steps

# Fetch metadata for a video (prints Markdown to stdout)
uv run python youtube-transcript/scripts/fetch_metadata.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Verify the VTT parser works standalone (pipe mode)
curl -sL "https://example.com/some.vtt" | uv run python youtube-transcript/scripts/vtt_to_md.py -

# Verify the VTT parser works with a local file
uv run python youtube-transcript/scripts/vtt_to_md.py /path/to/file.vtt
```

Skill invocation tests are run through Claude Code — see [`specs/001-metadata-only-mode/smoke-test.md`](specs/001-metadata-only-mode/smoke-test.md).

## Sample Calls

**Fetch metadata via standalone script (no Claude required)**
```bash
uv run python youtube-transcript/scripts/fetch_metadata.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Get a full transcript (default)**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Metadata only — prints to stdout, no file written**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ --metadata-only
```

**Custom output filename**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ --output my-notes
```
→ writes `2026-05-12-my-notes.md`

**Custom filename without date prefix**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ --output my-notes --no-date
```
→ writes `my-notes.md`

**Short URL form works too**
```
https://youtu.be/dQw4w9WgXcQ
```

## Supported agents

Claude Code, Copilot CLI, Codex, Gemini CLI, Hermes. See [`youtube-transcript/references/tool-map.md`](youtube-transcript/references/tool-map.md) for per-platform tool name differences.
