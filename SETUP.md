# Setup: hooks, skills, commands, MCP servers, and backup/sync

`README/claude-setup-guide.md` is meant for **your own Claude** to read and act on — it interviews you first and only builds what fits. This file is the literal reference underneath that: the actual commands, in the order they were run to build the original setup. Read it yourself, or point your Claude at it once it already knows which pieces you want.

Every piece here is independent — take what's useful, skip the rest. Nothing in this repo installs itself; go through this deliberately, one step at a time, and confirm each piece works before moving to the next.

---

## 1. Standing instructions

Copy `CLAUDE.md` to `~/.claude/CLAUDE.md` (applies to every project on the machine), or into a specific project's root as `CLAUDE.md` (overrides the global file for that project only — the more specific layer wins). Read it first and edit it to actually match how *you* work; it's a starting point, not a script to run unedited.

## 2. Skills, hooks, and commands

Copy the `.claude/` folder from this repo into your own project. Piece by piece:

- **`.claude/hooks/session_start_sync.py`** — a SessionStart hook: checks GitHub, the Google Drive mirror (section 4 below), and for new PDFs since last session, every time a session starts in that project.
- **`.claude/commands/end.md`** — a `/end` slash command that reconciles a citation library + notes vault, updates setup docs, logs the session, and runs the git + Drive backups. Written for a specific citation-manager/notes-vault setup (Zotero + Obsidian) — edit the wording to match your own tools, or strip that part out if you don't have an equivalent.
- **`.claude/skills/sanitize-document/SKILL.md`** + **`Tools/sanitize_doc.py`** — strips hidden metadata from a document before sharing it, without Claude reading the file's contents. Self-contained; works as-is.
- **`.claude/skills/pdf-research-workflow/SKILL.md`** — reading a PDF via its companion Markdown transcript instead of re-opening the PDF, the "mk" subfolder convention that keeps those transcripts in sync, a source-naming convention, and OCR/PDF-to-Markdown conversion. In the source setup this one is kept **global** (`~/.claude/skills/`) rather than project-scoped, since PDF handling isn't specific to one project — copy it there for the same effect. **Don't copy the OCR/PDF→Markdown commands verbatim** — they name one specific tool stack (Tesseract + pymupdf4llm) as a working example; swap in whatever's actually installed on your machine before relying on it.
- **`.claude/settings.local.json.example`** — copy to `.claude/settings.local.json` (or merge its `hooks` block into an existing one) to actually register the SessionStart hook above. Without this file, the hook script does nothing.
- **`.claude/rclone-exclude.txt.example`** — copy to `.claude/rclone-exclude.txt` and edit; only needed if you set up the Drive mirror in section 4.

The hook and the `/end` command both reference a `DRIVE_REMOTE`/`gdrive:<folder>` name and a `Last session/` folder — see section 4 for both. If you skip the Drive mirror, delete the `drive_check()` call and the Drive step from `end.md` rather than leaving them pointing at nothing.

## 3. MCP servers (optional — set up only what you actually use)

### Zotero

```
pip install zotero-mcp-server
```

Get an API key and your numeric User ID from `zotero.org/settings/keys`, then register:

```
claude mcp add zotero -e ZOTERO_API_KEY=<key> -e ZOTERO_LIBRARY_ID=<user_id> -e ZOTERO_LIBRARY_TYPE=user -- zotero-mcp serve
```

This is **Web API mode** — it reads your real library from zotero.org rather than requiring a local Zotero install to be open and synced. If `zotero-mcp setup`'s own wizard fails (a known issue on some machines: it can't find its own executable on PATH mid-run), register directly with `claude mcp add` as above instead.

Local *write* access (adding items, attaching files) needs Zotero desktop **v10 or later** — below that, `zotero_authorize_local_writes` always fails. Upgrade via the official installer from zotero.org/download, then run the `zotero_authorize_local_writes` MCP tool once (it pops a one-time dialog in Zotero requiring a human click on "Always Allow"). Note: the write-capability self-check (`zotero_write_capabilities`) has been observed to wrongly report "no" right after a successful upgrade — don't trust a negative result from it without just trying `zotero_authorize_local_writes` directly.

### Obsidian

Install the "Local REST API with MCP" community plugin (github.com/coddingtonbear/obsidian-local-rest-api): drop its release files (`main.js`, `manifest.json`, `styles.css`) into `<vault>/.obsidian/plugins/obsidian-local-rest-api/`, and enable it in `<vault>/.obsidian/community-plugins.json`. Obsidian must be **open**, with the plugin toggled on, for the connection to work — its settings pane is where you generate the API key. Register:

```
claude mcp add --transport http obsidian https://127.0.0.1:27124/mcp/ --header "Authorization: Bearer <API_KEY>"
```

### Google Workspace (Gmail / Calendar / Drive), if you use claude.ai

Prefer the first-party connector over running a local MCP server for this — nothing to install or keep running, and it doesn't need relaunching every session the way a local server can. Only set up a local server (e.g. `workspace-mcp`) if the first-party connector turns out to be missing a capability you actually need.

## 4. Backup & sync infrastructure

### Git + GitHub

Standard setup: `git init`, create a GitHub repo (**private**, unless you deliberately mean to publish it — check what's actually in the folder first; see this repo's own README for why), `git remote add origin <url>`, push. Add a `.gitignore` that excludes `.claude/` (local runtime state — machine-specific, shouldn't sync via git and has to be rebuilt on every new machine, same as this repo), anything over GitHub's 100MB per-file limit, and anything sensitive that shouldn't leave the machine at all.

This gives you two things a plain folder doesn't: a real undo history (a bad edit or accidental overwrite can be reverted), and multi-machine continuity if you ever work the same folder from more than one computer.

### Google Drive mirror (rclone)

A second, fully independent copy of the folder, outside git entirely — useful because Drive has no 100MB-per-file limit, so it can hold things git can't, and because it's a second independent backup on different infrastructure than GitHub.

1. Install **rclone** (github.com/rclone/rclone) — `winget install Rclone.Rclone` on Windows, `brew install rclone` on macOS, or your platform's package manager.
2. Configure a remote named `gdrive` for the `drive` backend: `rclone config create gdrive drive scope=drive` (triggers a one-time browser OAuth consent). Reuse an existing Google OAuth client if you already have one set up on the machine for something else, rather than creating a redundant one.
3. Create the target folder once: `rclone mkdir "gdrive:<your folder name>"`.
4. Copy `.claude/rclone-exclude.txt.example` to `.claude/rclone-exclude.txt` and edit it for your own repo.
5. **Use `rclone copy`, never `rclone sync`, for routine updates.** `sync` mirrors the destination to exactly match the source — which means it *deletes* anything on Drive that the machine running it doesn't have a local copy of. That's not hypothetical: an earlier version of this exact setup lost a 161MB file that way, because one machine had never downloaded its own copy of a Drive-only PDF (recoverable from Drive's trash, but only by luck). `copy` only adds or updates files and never removes anything:
   ```
   rclone copy "<repo path>" "gdrive:<folder>" --exclude-from="<repo path>/.claude/rclone-exclude.txt"
   ```
   `.claude/commands/end.md` already runs this correctly — this is the manual equivalent if you're setting it up by hand or testing it the first time.
6. To find files that exist on Drive but not locally (candidates for a *manual* delete decision — never automatic):
   ```
   rclone check "<repo path>" "gdrive:<folder>" --exclude-from="<repo path>/.claude/rclone-exclude.txt" --one-way --combined -
   ```
   Lines starting `- ` are on Drive but missing locally. Decide for yourself whether each one should be deleted; don't let an assistant delete from Drive on its own judgment.

### `Last session/` log

Create a plain folder named `Last session/` at the repo root, git-tracked (not gitignored). The `/end` command writes one dated file per session (`YYYY-MM-DD.md`, appended to rather than overwritten if the day already has one). This is the continuity thread between sessions and machines: git only carries file *contents*, not an assistant's own configuration or narrative context, so reading the latest entry after a gap (or after switching machines) is what answers "what happened last, and is anything left unfinished."

---

Once all of this is in place, `.claude/` itself won't show up on a fresh `git pull` to a second machine (it's gitignored, by design — it's local runtime state, not repo content). Check for it explicitly on any new machine rather than assuming it arrived with the rest of the repo, and rebuild it there the same way.
