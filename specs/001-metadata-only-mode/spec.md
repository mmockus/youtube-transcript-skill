# Feature Specification: Metadata-Only Retrieval Mode

**Feature Branch**: `001-metadata-only-mode`
**Created**: 2026-05-16
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Quick Video Reference (Priority: P1)

A user provides a YouTube URL and wants only the video's metadata (title, channel, upload date, duration, view count, description, canonical URL) without waiting for the full transcript to download and process. The metadata is printed to stdout immediately.

**Why this priority**: This is the core value of the feature — faster output for users who don't need the transcript text. It's independently deliverable and demonstrates the feature completely.

**Independent Test**: Can be fully tested by invoking the skill with a YouTube URL and the metadata-only flag, then verifying the metadata fields appear in stdout without any transcript content.

**Acceptance Scenarios**:

1. **Given** a valid YouTube URL and the `--metadata-only` flag, **When** the skill runs, **Then** metadata fields (title, channel, upload date, duration, view count, description, URL) are printed to stdout in Markdown format and the skill exits without fetching or parsing any VTT transcript.
2. **Given** a valid YouTube URL and the `--metadata-only` flag, **When** the video has captions disabled, **Then** the skill still succeeds and outputs metadata (no error about captions being unavailable).
3. **Given** an invalid or inaccessible YouTube URL and the `--metadata-only` flag, **When** the skill runs, **Then** the skill relays the fetch error to the user and exits without partial output.

---

### User Story 2 - Stdout vs File Distinction (Priority: P2)

A user expects that metadata-only mode writes to stdout rather than creating a Markdown file on disk, making it composable with shell pipelines and other tools.

**Why this priority**: Consistent with user's stated preference; distinguishes metadata-only mode clearly from full transcript mode (which writes a file).

**Independent Test**: Run the skill with `--metadata-only` and verify no `.md` file is written to disk, only stdout receives content.

**Acceptance Scenarios**:

1. **Given** `--metadata-only` is passed, **When** the skill completes successfully, **Then** no file is written to the working directory.
2. **Given** `--metadata-only` is passed and the output is piped to a file by the user, **Then** that piped file contains valid Markdown metadata.

---

### Edge Cases

- What happens when `--metadata-only` is combined with `--output`? The flag should be rejected with a clear error — `--output` implies file writing, which conflicts with stdout-only mode.
- What if the video is private or deleted? The metadata fetch fails; the skill relays the yt-dlp error and exits non-zero.
- What if the description field is extremely long? Output the full description without truncation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skill MUST accept a `--metadata-only` flag that activates metadata-only retrieval mode.
- **FR-002**: When `--metadata-only` is active, the skill MUST fetch video metadata using `yt-dlp --dump-json` and print results to stdout in Markdown format.
- **FR-003**: When `--metadata-only` is active, the skill MUST NOT fetch, download, or parse any VTT transcript file.
- **FR-004**: When `--metadata-only` is active, the skill MUST NOT write any file to the working directory.
- **FR-005**: The metadata output MUST include: title, channel, upload date (YYYY-MM-DD), duration (M:SS or H:MM:SS), view count (comma-formatted), description, and canonical URL.
- **FR-006**: When `--metadata-only` and `--output` are both provided, the skill MUST exit with a clear error message explaining the conflict.
- **FR-007**: When metadata fetch fails (private video, network error, invalid URL), the skill MUST relay the yt-dlp error to the user and exit non-zero.
- **FR-008**: Metadata-only mode MUST succeed even when the video has captions disabled, since no transcript fetch is attempted.

### Key Entities

- **Video Metadata**: The set of structured fields extracted from yt-dlp JSON output — title, channel, upload_date, duration, view_count, description, webpage_url.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Metadata-only retrieval completes in under 10 seconds for a typical YouTube video (no transcript download delay).
- **SC-002**: 100% of metadata fields (title, channel, date, duration, views, description, URL) are present in the output for any publicly accessible video.
- **SC-003**: No files are written to disk when `--metadata-only` is used — verifiable by checking the working directory before and after invocation.
- **SC-004**: The skill exits successfully (exit code 0) for any publicly accessible video regardless of caption availability.

## Assumptions

- The skill is a Claude Code skill invoked in a conversational context, not a standalone CLI tool. The "flag" is a natural language instruction or a literal argument passed in the skill invocation.
- `yt-dlp` is already installed and on PATH (existing requirement of the skill).
- Python 3.11+ is available (existing requirement of the skill).
- stdout output is sufficient; no structured JSON output format is required for metadata-only mode.
- Chapters parsed from the description are included in the metadata output when present, matching the existing full-transcript behavior.
