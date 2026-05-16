# youtube-transcript skill

Downloads a YouTube video transcript as a formatted Markdown file with metadata, chapters, and timestamped transcript.

## What it produces

```
YYYY-MM-DD-{title-slug}.md
```

Each file contains:
- Metadata table (channel, date, duration, views, URL)
- Description with chapters table
- Full timestamped transcript

## Requirements

- `yt-dlp` on PATH
- Python 3.11+

## Installation

```bash
# Clone the repo
git clone https://github.com/mmockus/youtube-transcript-skill.git ~/Development/youtube-transcript-skill

# Symlink into the global skills directory
ln -sf ~/Development/youtube-transcript-skill/skills/youtube-transcript \
       ~/.claude/skills/youtube-transcript
```

## Usage

Invoke via any Claude Code-compatible agent:

```
/youtube-transcript https://www.youtube.com/watch?v=VIDEO_ID
```

Or just paste a YouTube URL and the skill will trigger automatically.

### Flags

| Flag | Description |
|------|-------------|
| `--metadata-only` | Print video metadata to stdout only; skip transcript download. No file is written. |
| `--output <name>` | Custom filename base (full mode only). |
| `--no-date` | Suppress date prefix on output filename (full mode only). |

**Example — metadata only**:

```
https://www.youtube.com/watch?v=VIDEO_ID --metadata-only
```

## Supported agents

Claude Code, Copilot CLI, Codex, Gemini CLI, Hermes. See `references/tool-map.md` for per-platform tool name differences.

## Directory layout

```
youtube-transcript/
├── SKILL.md                     ← skill definition + title/filename rules
├── README.md                    ← this file
├── assets/
│   └── transcript-template.md  ← Markdown output template
├── references/
│   └── tool-map.md              ← cross-agent tool name mapping
└── scripts/
    └── vtt_to_md.py             ← VTT parser (stdlib only, no extra deps)
```
