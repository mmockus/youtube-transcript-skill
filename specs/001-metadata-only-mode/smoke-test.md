# Smoke Test: Metadata-Only Retrieval Mode

**Purpose**: Verify that `--metadata-only` prints video metadata to stdout and skips transcript download/file writing.
**Branch**: `001-metadata-only-mode`
**After implementing**: tasks.md Phases 1–3 must be complete before running these steps.

## Prerequisites

- `yt-dlp` installed and on PATH (`yt-dlp --version` exits 0)
- Claude Code with the `youtube-transcript` skill active
- A public YouTube URL handy (any popular video works)

---

## Test 1: Happy path — metadata prints to stdout, no file written

**What this checks**: FR-001 through FR-005, SC-001, SC-002, SC-003 — the primary acceptance scenario.

1. Note the files currently in your working directory: `ls *.md`
2. Invoke the skill: provide a public YouTube URL with `--metadata-only`
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ --metadata-only
   ```
3. Observe Claude's response.

**Expected result**:
- Response contains a `# <title>` heading
- Response contains a `## Video Metadata` table with Channel, Published, Duration, Views, URL fields populated
- Response contains a `## Description` section with text
- Running `ls *.md` again shows **no new file** compared to step 1
- Total response time under 15 seconds

---

## Test 2: Captions-disabled video succeeds

**What this checks**: FR-008, SC-004 — metadata-only succeeds even when transcripts are unavailable.

1. Use a video known to have captions disabled, or any video URL — in metadata-only mode, captions are irrelevant.
2. Invoke the skill with `--metadata-only`.

**Expected result**:
- Metadata fields appear in stdout with no error about captions or transcripts.
- No mention of "captions are disabled" in the output.

---

## Test 3: Conflict detection — `--metadata-only` + `--output`

**What this checks**: FR-006 — conflicting flags produce a clear error.

1. Invoke the skill with both flags:
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ --metadata-only --output my-notes
   ```

**Expected result**:
- Claude outputs an error message containing `--metadata-only and --output cannot be combined`
- No metadata is fetched or printed
- No file is written to disk

---

## Test 4: Invalid URL fails gracefully

**What this checks**: FR-007 — metadata fetch errors are relayed to the user.

1. Invoke the skill with a bad URL:
   ```
   https://www.youtube.com/watch?v=INVALID_ID_HERE --metadata-only
   ```

**Expected result**:
- Claude relays the yt-dlp error (e.g., "Video unavailable" or similar)
- No partial metadata is output
- No file is written

---

## Cleanup (optional)

- Remove any accidental `.md` files created during testing: `rm -f <unexpected-file>.md`
