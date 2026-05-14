---
name: youtube-transcript
description: Download a YouTube video transcript as a formatted Markdown file with metadata header, timestamped transcript, and chapter table. Use whenever a user provides a YouTube URL and wants the transcript saved, downloaded, or exported as Markdown. Also triggers on "get the transcript for", "save this video as markdown", "download transcript", "transcript with timestamps", "export YouTube transcript". If the user pastes a YouTube URL with no further instruction, this skill likely applies.
---

# YouTube Transcript

Fetch a YouTube video's metadata and transcript, then write a formatted Markdown file to the current working directory.

## Requirements

- `yt-dlp` on PATH
- Python 3.11+

## Workflow

### 1. Fetch metadata

```bash
yt-dlp --dump-json --no-playlist "VIDEO_URL"
```

Extract from the JSON output:
- `title` — video title (used verbatim as the `# Heading`)
- `channel` — channel name
- `upload_date` — `YYYYMMDD`, convert to `YYYY-MM-DD`
- `duration` — seconds, convert to `M:SS` or `H:MM:SS`
- `view_count` — format with commas
- `description` — full text (parse chapters from here)
- `webpage_url` — canonical URL

### 2. Fetch transcript VTT

```bash
yt-dlp \
  --write-auto-sub \
  --sub-lang en \
  --sub-format vtt \
  --skip-download \
  --ignore-no-formats-error \
  -o /tmp/yt-transcript \
  "VIDEO_URL"
```

If no English sub is found, retry without `--sub-lang en` to accept any language. Glob `/tmp/yt-transcript*.vtt` to find the output file.

### 3. Parse the VTT into timestamped lines

```bash
python3 ~/.claude/skills/youtube-transcript/scripts/vtt_to_md.py /tmp/yt-transcript.en.vtt
```

Adjust the filename to match whatever the glob found.

### 4. Read the output template

Read `~/.claude/skills/youtube-transcript/assets/transcript-template.md` and replace every `{{PLACEHOLDER}}` with the fetched values.

### 5. Write the output file

Determine the filename using the rules below, then write to the **current working directory**.

---

## Filename Rules

Default pattern: `{upload_date}-{slug}.md`

`slug` derivation from the video title:
1. Lowercase the full title
2. Replace runs of non-alphanumeric characters with `-`
3. Strip leading/trailing dashes
4. Truncate to 60 characters — never cut mid-word, break at the last `-` before the limit

Examples:
- `"ChatGPT Has 900M Weekly Users. Almost None Can Buy In It."` → `2026-05-12-chatgpt-has-900m-weekly-users-almost-none-can-buy.md`
- `"10 Things I Wish I Knew Before Learning React"` → `2026-03-01-10-things-i-wish-i-knew-before-learning-react.md`

### Optional: custom output name

If the user passes `--output <name>`, use that as the base filename instead of the auto-generated slug. The upload date is still prepended by default.

| Invocation | Result |
|---|---|
| `--output my-notes` | `2026-05-12-my-notes.md` |
| `--output my-notes --no-date` | `my-notes.md` |
| `--output 2026-05-12-my-notes` | `2026-05-12-my-notes.md` (date already present, don't double-prefix) |

Rules:
- Always append `.md` if the name doesn't already end in `.md`
- Prepend `{upload_date}-` unless `--no-date` is passed or the name already starts with a date pattern (`YYYY-MM-DD-`)
- Apply the same slug normalization (lowercase, non-alphanumeric → `-`) to the passed name

## Title Rules

The Markdown `# Heading` uses the **original YouTube title verbatim** — no casing transforms, no truncation. The filename slug is always lowercase regardless.

## Chapters

Look for a chapters/timestamps section in the `description` field — lines matching `H:MM` or `M:SS` followed by label text. Render them as a Markdown table (see template).

If no chapters are present, omit the chapters section entirely rather than leaving an empty table.

## Error Handling

- VTT unavailable (captions disabled): write the file with the transcript section replaced by `> Transcript unavailable — captions are disabled for this video.`
- Metadata fetch fails: relay the yt-dlp error to the user and stop.

---

*Non-Claude Code agents: see `references/tool-map.md` for tool name equivalents on Copilot CLI, Codex, Gemini, and Hermes.*
