Wrap up this session on the `grad-school` repo. Do these steps in order:

1. **Reconcile Zotero ↔ the repo's `Zotero/thesis` mirror ↔ the Obsidian Thesis Wiki vault** for anything that changed this session:
   - Any new or re-attached Zotero item should have a matching, properly-named PDF copy in the repo, filed under the subfolder matching its Zotero collection.
   - That PDF should have a matching `mk` Markdown copy (via `pymupdf4llm`) in the sibling `<folder> mk` subfolder.
   - Check for a correspondingly-formatted Obsidian note in the Thesis Wiki vault for any thesis-relevant new source. If the Obsidian MCP server isn't connected (common if Obsidian wasn't already open when the session started), say so explicitly rather than skipping silently.

2. **Update `claudereadme.md`** at the repo root to reflect anything that changed this session (new tools, new MCP servers, new conventions, fixed bugs in the sync layer itself).

3. **Write a dated session file** in the `Last session` folder: `Last session/YYYY-MM-DD.md`. If today's file already exists, append a new dated section to it rather than overwriting.

4. **Commit and push** to GitHub (`origin/main`). Review `git status`/`git diff` before staging - don't blindly `git add -A`.

5. **Update the Google Drive mirror**, if rclone is configured on this machine. **Never auto-delete from Drive** - use `copy`, not `sync`, so new/changed files go up but nothing on Drive is ever removed without the user's say-so:
   ```
   rclone copy "<repo path>" "gdrive:Grad School" --exclude-from="<repo path>/.claude/rclone-exclude.txt"
   ```
   Then separately check for files that exist on Drive but not locally:
   ```
   rclone check "<repo path>" "gdrive:Grad School" --exclude-from="<repo path>/.claude/rclone-exclude.txt" --one-way --combined -
   ```
   Look for lines starting `- ` (present on Drive, missing locally). If there are any, list them for the user and ask before removing anything (`rclone delete`/`rclone deletefile`) - do not delete on your own judgment. This mirrors the rule in `claudereadme.md`: updating an existing file with a newer version is fine to do automatically; deleting is not, ever, without asking first.

6. **Report back** to the user: what was reconciled, what was committed/pushed, whether the Drive copy ran clean, any Drive-only files flagged for a deletion decision, and anything left unfinished for next session.
