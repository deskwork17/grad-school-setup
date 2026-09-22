Upload a local file to the Google Drive mirror and share a link to it — optionally emailing that link to someone — without ever reproducing the file's content as base64 inside a tool call. Use this whenever the user asks to email, send, or share a file, instead of attaching it directly through the Gmail/Drive MCP tools (which require the whole file inline and get token-expensive or risk corruption past trivial sizes).

Arguments: `$ARGUMENTS` — a file path, optionally followed by a recipient email address, e.g. `/send-file "path/to/deck.pptx" someone@example.com`. Quote the path if it has spaces.

1. **Parse the arguments.** The last whitespace-separated token is a recipient email only if it looks like one (contains `@` and a `.` after it); everything before that is the file path. No such trailing token → no recipient, the path is everything given.

2. **Resolve and check the file.** If it doesn't exist, say so and stop — don't guess at a similar filename.

3. **Sensitivity check — don't skip this.** If the path falls under anything your `.gitignore`/Drive-exclude list treats as sensitive, stop and confirm with the user before doing anything — the result of this command is a publicly link-shareable file (see step 6), which is a meaningfully bigger exposure than a normal git/Drive-mirror sync.

4. **Find rclone.** Try `rclone` on PATH first. If that fails on Windows, a fresh shell often hasn't picked up a winget install's PATH entry yet — search the winget packages folder (`%LOCALAPPDATA%\Microsoft\WinGet\Packages\Rclone.Rclone_*\rclone-*\rclone.exe`) and use the full path instead of failing outright.

5. **Pick the Drive target path.** If the file lives inside your project, mirror its path exactly onto your Drive remote (matching however your own backup sync organizes things — see `SETUP.md` section 4). If it's outside the project, use a dedicated folder (e.g. `<remote>:<folder>/_sent/<filename>`) instead.

6. **Upload directly from disk — never read the file into a tool call:**
   ```
   rclone copyto "<local path>" "<remote>:<folder>/<target path>"
   ```

7. **Generate the link:**
   ```
   rclone link "<remote>:<folder>/<target path>"
   ```
   On Google Drive remotes this also sets the file's permission to "anyone with the link can view" as a side effect — that's what lets a recipient open it even from an account other than the one the Drive mirror lives in. Mention this plainly when reporting back; don't bury it. (Confirm this is actually the behavior on your own remote/backend before relying on it — it's confirmed on a `drive` remote specifically, not verified against other rclone backends.)

8. **Deliver it:**
   - Recipient given → send a short email via your Gmail/email connector: a plain one-line subject, and a body containing just the link (no attachment, no markdown formatting in a plain-text body). Do not attach the file itself.
   - No recipient → just give the user the link in chat.

9. **Report back:** what was uploaded, the target path it landed at, the link, and — if emailed — who it went to. If the upload or email step failed, say so plainly rather than claiming success.

**Never fall back to reproducing the file as base64 in a Gmail/Drive tool call if rclone fails for some reason** — that defeats the entire point of this command. If rclone isn't working, say so and ask the user how they want to proceed instead of silently paying the token cost this command exists to avoid.
