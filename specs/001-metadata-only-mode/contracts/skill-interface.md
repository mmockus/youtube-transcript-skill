# Contract: youtube-transcript Skill Interface

**Type**: Claude Code Skill (natural language invocation)
**Version**: post-feature (includes --metadata-only)

---

## Invocation Patterns

### Full transcript (existing — unchanged)

```
[youtube URL]
[youtube URL] --output my-notes
[youtube URL] --output my-notes --no-date
```

**Output**: `.md` file written to working directory containing metadata + transcript.

---

### Metadata only (new)

```
[youtube URL] --metadata-only
```

**Output**: Metadata printed to stdout in Markdown format. No file written.

---

## Flag Reference

| Flag | Argument | Default | Description |
|------|----------|---------|-------------|
| *(none)* | — | — | Full transcript mode |
| `--metadata-only` | — | false | Metadata-only stdout mode |
| `--output <name>` | string | auto-generated slug | Custom output filename base |
| `--no-date` | — | false | Suppress `YYYY-MM-DD-` prefix on filename |

## Conflict Rules

| Combination | Result |
|-------------|--------|
| `--metadata-only` + `--output` | Error: flags conflict; exit non-zero |
| `--metadata-only` + `--no-date` | `--no-date` is silently ignored (no file written regardless) |

## Exit Behavior

| Condition | Exit |
|-----------|------|
| Success | 0 |
| `--metadata-only` + `--output` conflict | non-zero |
| `yt-dlp` metadata fetch fails | non-zero |

## Stdout Format (metadata-only mode)

Valid CommonMark Markdown containing:
- `# {title}` heading
- `## Video Metadata` table with Channel, Published, Duration, Views, URL
- `## Description` section with full description text
- `### Chapters` table (omitted if no chapters in description)
