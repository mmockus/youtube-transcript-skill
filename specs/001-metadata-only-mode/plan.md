# Implementation Plan: Metadata-Only Retrieval Mode

**Branch**: `001-metadata-only-mode` | **Date**: 2026-05-16 | **Spec**: [spec.md](spec.md)

## Summary

Add a `--metadata-only` flag to the youtube-transcript Claude Code skill. When active, the skill fetches video metadata via `yt-dlp --dump-json`, renders it as Markdown, prints to stdout, and exits — skipping all VTT transcript steps. Only `SKILL.md` and `README.md` require changes.

## Technical Context

**Language/Version**: Python 3.14 (vtt_to_md.py helper script); Claude Code skill instructions (Markdown)
**Primary Dependencies**: yt-dlp (external CLI, already required); Python stdlib only
**Storage**: N/A — skill writes files to working directory in full mode; stdout only in metadata-only mode
**Testing**: Manual invocation via Claude Code
**Target Platform**: macOS (darwin), wherever Claude Code runs
**Project Type**: Claude Code skill (Markdown prompt + Python helper script)
**Performance Goals**: Metadata-only fetch completes in under 10 seconds (no transcript download)
**Constraints**: No new dependencies; no new Python packages; changes confined to SKILL.md and README.md
**Scale/Scope**: Single-user skill invocation

## Constitution Check

Constitution is an unfilled template — no project-specific gates apply. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/001-metadata-only-mode/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── skill-interface.md
└── tasks.md             # Phase 2 output (speckit-tasks)
```

### Source Code (repository root)

```text
youtube-transcript/
├── SKILL.md                    # Primary change — add --metadata-only section
├── assets/
│   └── transcript-template.md  # Unchanged
├── scripts/
│   └── vtt_to_md.py            # Unchanged
└── references/
    └── tool-map.md             # Unchanged

README.md                       # Update to document --metadata-only flag
```

**Structure Decision**: This is a Claude Code skill (not a traditional source tree). The entire implementation is in `SKILL.md` — adding a new workflow branch for `--metadata-only`. The Python helper script is only used in full-transcript mode and is untouched.
