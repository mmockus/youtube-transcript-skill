# youtube-transcript-skill

A Claude Code skill that downloads a YouTube video transcript as a formatted Markdown file with metadata, chapters, and timestamped transcript.

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
- `--output my-notes` — custom filename (date still prepended: `2026-05-12-my-notes.md`)
- `--output my-notes --no-date` — custom filename without date prefix

## Output

Each run writes a Markdown file to the current working directory:

```
2026-05-12-video-title-slug.md
```

Containing:
- Metadata table (channel, date, duration, views, URL)
- Description with chapters table (if present)
- Full timestamped transcript

## Supported agents

Claude Code, Copilot CLI, Codex, Gemini CLI, Hermes. See [`youtube-transcript/references/tool-map.md`](youtube-transcript/references/tool-map.md) for per-platform tool name differences.
