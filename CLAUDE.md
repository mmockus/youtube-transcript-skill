# youtube-transcript-skill Development Guidelines

Auto-generated from feature plans. Last updated: 2026-05-16

## Project Type

Claude Code skill — logic lives in `youtube-transcript/SKILL.md` (Markdown prompt instructions).
The only code file is `youtube-transcript/scripts/vtt_to_md.py` (Python 3.14, stdlib only).

## Active Technologies

- yt-dlp (external CLI, must be on PATH)
- Python 3.14 (for vtt_to_md.py)
- Markdown (skill instructions)

## Project Structure

```text
youtube-transcript/
├── SKILL.md                    # Skill instructions for Claude
├── assets/transcript-template.md
├── scripts/vtt_to_md.py
└── references/tool-map.md

specs/                          # speckit feature specs
README.md
```

## Commands

```bash
# Run VTT parser directly
uv run python youtube-transcript/scripts/vtt_to_md.py <path-to-vtt>
```

## Active Features

- 001-metadata-only-mode: Add `--metadata-only` flag to print video metadata to stdout without transcript

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
