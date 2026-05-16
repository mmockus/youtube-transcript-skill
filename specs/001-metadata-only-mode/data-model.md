# Data Model: Metadata-Only Retrieval Mode

**Branch**: `001-metadata-only-mode` | **Date**: 2026-05-16

---

## Entities

### VideoMetadata

Extracted from `yt-dlp --dump-json` output. Already used in full-transcript mode; unchanged for metadata-only mode.

| Field | Source JSON key | Transform | Required |
|-------|----------------|-----------|----------|
| `title` | `title` | Verbatim | Yes |
| `channel` | `channel` | Verbatim | Yes |
| `upload_date` | `upload_date` | `YYYYMMDD` → `YYYY-MM-DD` | Yes |
| `duration` | `duration` | seconds → `M:SS` or `H:MM:SS` | Yes |
| `view_count` | `view_count` | integer → comma-formatted string | Yes |
| `description` | `description` | Verbatim; chapters parsed from this | Yes |
| `webpage_url` | `webpage_url` | Verbatim | Yes |

### InvocationFlags

The set of flags parsed from the user's skill invocation message.

| Flag | Type | Conflict | Description |
|------|------|----------|-------------|
| `--metadata-only` | boolean | conflicts with `--output` | Activates metadata-only mode |
| `--output <name>` | string | conflicts with `--metadata-only` | Target filename (existing flag) |
| `--no-date` | boolean | — | Suppress date prefix on filename (existing flag) |

### MetadataOutput

The stdout artifact produced in metadata-only mode. A Markdown string composed of the metadata fields.

**Format** (subset of `transcript-template.md`):

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

### Chapters          ← omit entire section if no chapters found

| Timestamp | Topic |
|-----------|-------|
| {ts}      | {label} |
```

---

## State Transitions

```
Invocation received
       │
       ▼
Parse flags
       │
       ├── --metadata-only AND --output → ERROR (exit non-zero)
       │
       ├── --metadata-only → MetadataOnlyPath
       │       │
       │       ▼
       │   Fetch VideoMetadata (yt-dlp --dump-json)
       │       │
       │       ├── fetch fails → relay error, exit non-zero
       │       │
       │       └── fetch succeeds → render MetadataOutput → print to stdout → exit 0
       │
       └── (no flag) → FullTranscriptPath (existing behavior, unchanged)
```
