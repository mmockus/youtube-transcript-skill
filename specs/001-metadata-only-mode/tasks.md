# Tasks: Metadata-Only Retrieval Mode

**Input**: Design documents from `specs/001-metadata-only-mode/`
**Branch**: `001-metadata-only-mode`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other [P] tasks (different files, no dependencies)
- **[Story]**: User story this task belongs to (US1, US2)

---

## Phase 1: Setup

**Purpose**: Understand the existing skill structure before making changes.

- [x] T001 Read `youtube-transcript/SKILL.md` in full to understand existing flag handling (`--output`, `--no-date`) and the 5-step workflow

**Checkpoint**: You understand how the existing skill parses flags and branches on them.

---

## Phase 2: User Story 1 — Quick Video Reference (Priority: P1) 🎯 MVP

**Goal**: Add `--metadata-only` flag that prints metadata to stdout and exits, skipping transcript steps.

**Independent Test**: Invoke the skill with a public YouTube URL and `--metadata-only`; confirm all metadata fields appear in stdout and no `.md` file is created in the working directory.

- [x] T002 [US1] In `youtube-transcript/SKILL.md`, add an `## Optional Flags` (or equivalent) section documenting `--metadata-only` with description, behavior, and output format — place it before the existing `## Workflow` section
- [x] T003 [US1] In `youtube-transcript/SKILL.md`, add flag detection logic at the top of the workflow: if `--metadata-only` is present, skip to the metadata-only path (Steps 2–3 of the normal workflow are skipped)
- [x] T004 [US1] In `youtube-transcript/SKILL.md`, add the metadata-only output instructions: run `yt-dlp --dump-json`, extract all metadata fields, render using the metadata section of `transcript-template.md` (title heading + Video Metadata table + Description + Chapters if present), print to stdout, exit — no file written
- [x] T005 [US1] In `youtube-transcript/SKILL.md`, add the captions-disabled edge case note under metadata-only mode: since no VTT fetch occurs, captions-disabled videos succeed normally

**Checkpoint**: Skill correctly handles `--metadata-only` — metadata prints to stdout, no file written, works even when captions are disabled.

---

## Phase 3: User Story 2 — Stdout vs File Distinction (Priority: P2)

**Goal**: Enforce that `--metadata-only` and `--output` cannot be combined; make the no-file behavior explicit.

**Independent Test**: Invoke the skill with `--metadata-only --output my-notes`; confirm an error message is printed and no file is written, and exit is non-zero.

- [x] T006 [US2] In `youtube-transcript/SKILL.md`, add flag conflict check immediately after flag detection (before any yt-dlp calls): if both `--metadata-only` and `--output` are present, print `"--metadata-only and --output cannot be combined: metadata-only mode writes to stdout only."` and stop
- [x] T007 [US2] In `youtube-transcript/SKILL.md`, add a note that `--no-date` is silently ignored when `--metadata-only` is active (no file is written regardless, so date prefix is irrelevant)

**Checkpoint**: Conflicting flags produce a clear error; `--no-date` is handled gracefully.

---

## Phase 4: Polish & Documentation

**Purpose**: Update user-facing documentation to reflect the new flag.

- [x] T008 [P] Update `README.md` to document the `--metadata-only` flag: add it to the usage/flags table with description "Print video metadata to stdout; skip transcript download. No file written."
- [x] T009 [P] Update `youtube-transcript/README.md` (skill-level readme) with the same flag documentation if a flags/usage section exists there

**Checkpoint**: Run `quickstart.md` verification steps to confirm the feature works end-to-end.

---

## Dependencies & Execution Order

- **Phase 1**: No dependencies — start immediately
- **Phase 2**: Depends on Phase 1 (T001 must be read before editing)
- **Phase 3**: Depends on Phase 2 (flag detection must exist before adding conflict check)
- **Phase 4**: T008 and T009 are independent of each other [P] — both depend on Phase 3 completion

### Parallel Opportunities

```
T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008
                                                    T009  (parallel with T008)
```

---

## Implementation Strategy

### MVP (User Story 1 only)

1. Complete Phase 1: Read SKILL.md
2. Complete Phase 2: Add `--metadata-only` to SKILL.md
3. **Stop and validate**: Test with a real YouTube URL using `--metadata-only`
4. Proceed to Phase 3 and 4 once P1 is confirmed working

### Full delivery

1. Complete all phases in order
2. Run smoke-test.md verification steps
3. Commit and open PR from `001-metadata-only-mode`
