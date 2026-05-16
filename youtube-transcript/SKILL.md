---
name: youtube-transcript
description: Download a YouTube video transcript as a formatted Markdown file with metadata header, timestamped transcript, and chapter table. Use whenever a user provides a YouTube URL and wants the transcript saved, downloaded, or exported as Markdown. Also triggers on "get the transcript for", "save this video as markdown", "download transcript", "transcript with timestamps", "export YouTube transcript". If the user pastes a YouTube URL with no further instruction, this skill likely applies. Also triggers on "--metadata-only", "metadata only", "just the metadata", "video info only".
---

# YouTube Transcript

Fetch a YouTube video's metadata and transcript, then write a formatted Markdown file to the current working directory. Pass `--metadata-only` to print only the video metadata to stdout without downloading a transcript.

## Requirements

- `yt-dlp` on PATH
- Python 3.11+

## Flags

| Flag | Description |
|------|-------------|
| `--metadata-only` | Print video metadata to stdout only; skip transcript download. No file is written. |
| `--output <name>` | Use `<name>` as the output filename base (full mode only). |
| `--no-date` | Suppress the `YYYY-MM-DD-` date prefix on the output filename (full mode only). |

**Flag conflict**: If both `--metadata-only` and `--output` are present, stop immediately and output:
> `--metadata-only and --output cannot be combined: metadata-only mode writes to stdout only.`

**`--no-date` with `--metadata-only`**: `--no-date` is silently ignored — no file is written regardless.

---

**Before starting the workflow**: Check for `--metadata-only`. If present, skip to **Metadata-Only Mode** below.

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

### 2. Extract VTT URL and parse transcript in memory

From the JSON fetched in step 1, extract the VTT URL:
- Check `automatic_captions.en` first; use the entry whose `ext` is `vtt`
- If no English entry, fall back to the first available language in `automatic_captions`
- If `automatic_captions` is empty, captions are disabled — see Error Handling

Fetch and parse in a single pipeline (no file written to disk):

```bash
curl -sL "VTT_URL" | uv run python ~/.claude/skills/youtube-transcript/scripts/vtt_to_md.py -
```

### 3. Read the output template

Read `~/.claude/skills/youtube-transcript/assets/transcript-template.md` and replace every `{{PLACEHOLDER}}` with the fetched values.

### 4. Write the output file

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

## Metadata-Only Mode

Activated when `--metadata-only` is passed. Skips transcript download and file writing entirely.

### 1. Fetch metadata

Same command as the full workflow:

```bash
yt-dlp --dump-json --no-playlist "VIDEO_URL"
```

If this fails, relay the yt-dlp error to the user and stop. (Captions-disabled videos are fine — no VTT fetch is attempted.)

### 2. Print to stdout

Render and print the following Markdown to stdout — do **not** write a file:

```
# {title}

## Video Metadata

| Field | Value |
|-------|-------|
| **Channel** | {channel} |
| **Published** | {upload_date} |
| **Duration** | {duration} |
| **Views** | {view_count} |
| **URL** | {webpage_url} |

## Description

{description}
```

If chapters are found in `description` (lines matching `H:MM` or `M:SS` followed by label text), append:

```
### Chapters

| Timestamp | Topic |
|-----------|-------|
| {ts}      | {label} |
```

Omit the Chapters section entirely if no chapters are present.

---

*Non-Claude Code agents: see `references/tool-map.md` for tool name equivalents on Copilot CLI, Codex, Gemini, and Hermes.*
