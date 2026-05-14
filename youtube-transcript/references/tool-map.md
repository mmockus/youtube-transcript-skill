# Cross-Agent Tool Map

This skill is written using Claude Code tool names. Use the equivalents below for your platform.

| Claude Code | Copilot CLI | Codex | Gemini CLI | Hermes |
|-------------|-------------|-------|------------|--------|
| `Bash` | `bash` | native shell | `run_shell_command` | `bash` |
| `Read` | `view` | native file tools | `read_file` | `read_file` |
| `Write` | `create` | native file tools | `create_file` | `write_file` |
| `Glob` | `glob` | native file tools | `list_directory` | `list_files` |

## Notes by platform

**Copilot CLI** — `bash` with `async: true` for long yt-dlp downloads if needed. No `WebSearch` equivalent; use `web_fetch` with a direct URL.

**Codex** — All file and shell tools are native. No mapping needed beyond the table above.

**Gemini CLI** — Tool mapping is loaded automatically via GEMINI.md. Use `run_shell_command` in place of `Bash`.

**Hermes (local/Ollama)** — Tool availability varies by server config. Confirm `bash` and file tools are enabled before running. If shell execution is unavailable, run the yt-dlp commands manually and paste the output back.
