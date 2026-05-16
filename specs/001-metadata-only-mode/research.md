# Research: Metadata-Only Retrieval Mode

**Branch**: `001-metadata-only-mode` | **Date**: 2026-05-16
**Spec**: [spec.md](spec.md)

---

## Decision 1: Where does the flag live?

**Decision**: `--metadata-only` is documented in `SKILL.md` as an optional invocation flag. Claude recognizes it in the user's message or skill arguments.

**Rationale**: The youtube-transcript skill is a Claude Code skill — its logic is encoded in `SKILL.md` as instructions to Claude. There is no CLI entry point to add an argument parser to. The flag convention is already established in the existing skill (`--output`, `--no-date`), so `--metadata-only` follows that same pattern.

**Alternatives considered**:
- A separate `youtube-metadata` skill — rejected because the metadata fetch is already Step 1 of the existing skill; duplicating it creates maintenance overhead.
- A Python script that handles the metadata-only path — rejected because the skill already delegates yt-dlp calls inline; a standalone script adds complexity without benefit.

---

## Decision 2: Output destination — stdout vs file

**Decision**: Metadata-only mode prints to stdout. No file is written.

**Rationale**: The user explicitly confirmed stdout is acceptable. Stdout output keeps the feature lightweight, composable (pipe-friendly), and distinguishable from the full-transcript mode (which always writes a `.md` file). The `--output` flag already signals "write a file" in the existing skill, so metadata-only naturally belongs to the stateless stdout path.

**Alternatives considered**:
- Write a file by default with an opt-out — rejected because user confirmed stdout is fine and the feature is specifically for "quick reference without saving."
- Support both stdout and file depending on `--output` — not needed; `--output` conflicts with `--metadata-only` by design (FR-006).

---

## Decision 3: Output format

**Decision**: Reuse the metadata portion of `transcript-template.md` as the stdout format — the existing `## Video Metadata` table plus `## Description` section and `### Chapters` table (if present). Omit the `---` divider and the `## Transcript` section entirely.

**Rationale**: Reusing the existing template structure means the output is immediately familiar to users of the full transcript mode. No new template file is needed; the SKILL.md instructions describe which sections to include.

**Alternatives considered**:
- A new `assets/metadata-template.md` — adds a file but no functional difference; the template is short enough to specify inline in SKILL.md.
- JSON output — rejected; the existing skill outputs Markdown, and the user did not request JSON.

---

## Decision 4: Flag conflict handling (`--metadata-only` + `--output`)

**Decision**: If both flags are present, exit with a clear error: `"--metadata-only and --output cannot be combined: metadata-only mode writes to stdout only."` Do not proceed.

**Rationale**: `--output` implies writing a named file; `--metadata-only` implies stdout only. Silently ignoring one would be surprising. Failing fast with an informative message is the right behavior.

---

## Decision 5: File changes required

**Decision**: Only `SKILL.md` needs to be modified. No new files are required.

**Rationale**:
- The metadata output format is described inline in `SKILL.md` (Step 4a) using the existing template's structure — no new template asset needed.
- `vtt_to_md.py` is unchanged — it is skipped entirely in metadata-only mode.
- `transcript-template.md` is unchanged — it is skipped entirely in metadata-only mode.
- `README.md` should be updated to document the new flag.

---

## Summary of Changes

| File | Change |
|------|--------|
| `youtube-transcript/SKILL.md` | Add `--metadata-only` flag section: conflict check, skip Steps 2–3, stdout output instructions |
| `README.md` | Document `--metadata-only` flag in usage section |
