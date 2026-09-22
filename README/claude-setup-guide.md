# Setting up Claude for your own research workflow

## What this file is

This is not documentation to read — it's a script for **your own Claude** (Claude Code, or another Claude with file and shell access on your machine) to read and act on. It was adapted from a working setup built for a sociology graduate student's thesis and coursework directory, documented in a companion handout ("Using Claude Code in the Social Sciences").

The point isn't to copy that setup wholesale. Everyone's research workflow is different — different file types, different comfort with the command line, different backup needs, different sensitivity around data. This file instead has your Claude **interview you** about your own workflow, then build only the pieces that actually fit. Most of the questions below are general (section A–F); section G asks about the specific named pieces of the source setup — Zotero, Obsidian, a document sanitizer, OCR'd PDFs, a Google Drive mirror — by name, since it's easier to say "yes, I use Zotero too" than to recognize your own tools inside an abstract category.

**Prerequisite:** this requires Claude Code (or an equivalent Claude environment with file/terminal access) already installed on your machine. If you don't have that yet, get it set up first — this file can't install itself.

---

## Instructions to the Claude reading this file

Follow these steps in order. Do not skip ahead to building anything.

1. Read this entire file before doing or saying anything else.
2. Do **not** install any software, create any accounts, initialize any git repository, or modify any files yet.
3. Ask the person the questions in "Interview questions" below. Group them by section and go section by section rather than dumping all of them at once — wait for real answers, don't assume.
4. Based on their answers, put together a short, concrete plan using "Build menu" below — state plainly which pieces you'd set up and which you'd skip, and why, given what they told you.
5. Show them that plan and get explicit approval before creating or changing anything.
6. Once approved, execute it — but pause and confirm again before any step that installs software, creates an account/API key, sets up a git remote, or configures cloud sync. Those are exactly the steps worth a heads-up first.
7. When finished, tell them plainly what you set up, where the relevant files live, and how to undo or adjust any of it later.

If at any point their answers suggest none of this is a good fit for how they work, say so — a plain preferences file with no automation at all is a completely valid outcome here.

---

## Interview questions

### A. The work itself
- What kind of work is this for — coursework, a thesis/dissertation, ongoing research, something else?
- What file types make up most of it? (PDFs, scanned or handwritten notes, interview transcripts, survey/spreadsheet data, code or statistical scripts, something else)
- Is it already organized in one main folder, or scattered across several?

### B. Working style
- Any strong preferences for how you want Claude to communicate — concise vs. detailed, ask-first vs. just-proceed?
- When Claude produces something meant to be read or shared (a summary, a write-up, notes), do you want it saved as a file, or is chat fine?

### C. Repeatable tasks
- Is there anything you do the same way more than once or twice — converting file formats, a citation/naming convention, cleaning up transcripts, anonymizing data, anything else? These are candidates for a **skill** (a written, reusable procedure Claude follows automatically when it recognizes the task).

### D. Automation appetite
- Do you want automatic checks running in the background (for example, a check that Claude actually read a source document in full rather than skimming it), or would that feel like unnecessary overhead for how you work?
- Would a single command that wraps up a work session (update notes, log what happened, back everything up) be useful, or is that more structure than you want?

### E. Backup and multi-machine work
- Do you already use git/GitHub, or version control of any kind?
- Do you want this folder backed up with real version history (not just a copy, but the ability to step back through changes)?
- Do you work from more than one computer? If so, which ones, and do you switch between them often?
- Do you want a second, independent backup (e.g., a cloud drive mirror) in addition to git, and do you already have a cloud storage account you'd want to use?

### F. Platform
- What operating system(s) are you on? (This matters — install commands and file paths differ between Windows, macOS, and Linux, and a setup built for one won't directly copy to another.)
- How comfortable are you installing and running command-line tools?

### G. Specific pieces of the source setup — ask about each by name
The source setup (see `SETUP.md` in this repo for the literal commands behind each of these) has several named integrations. Ask about each rather than assuming section C already covered it — someone won't necessarily think to mention "Zotero" in answer to an abstract question about repeatable tasks.

- **Reference manager.** Do you use Zotero, or another reference/citation manager? If Zotero: would it help to have Claude search, read, and cite directly from your library instead of copy-pasting? (`SETUP.md` section 3 has the MCP setup — it works in "Web API mode," reading your real library from zotero.org, so it doesn't need a local Zotero install running and synced.)
- **Notes app.** Do you keep research or thesis notes in Obsidian, or a similar notes app? Want Claude to read and write notes there directly, rather than notes living only in chat? (Also `SETUP.md` section 3 — needs the notes app open with a plugin enabled, not just installed.)
- **Sharing documents externally.** Do you ever send documents outside your research group — drafts, grant materials, reviewer copies — where hidden metadata, tracked changes, or leftover comments could be a problem if they went out unnoticed? The source setup has a ready-to-copy skill for this (`.claude/skills/sanitize-document/`) that strips that information via a script, without Claude ever reading the document's actual content.
- **Scanned or image-only PDFs, and citation naming.** Do you work with scanned/handwritten sources that need OCR before they're searchable? Want a consistent renaming convention for sources (e.g. `Last Name, First Name, Title, Year`), and a parallel folder of Markdown transcripts so a document can be read as text without reopening the PDF each time? This one's a packaged skill in this repo (`.claude/skills/pdf-research-workflow/`) — the mk-folder convention and naming rule are ready to copy, but its OCR/PDF-to-Markdown commands name one example tool stack (Tesseract + pymupdf4llm) that needs swapping for whatever's actually installed on their machine.
- **A read-integrity check.** Would it help to have Claude periodically forced to stop and confirm it actually read the last few source documents in full, rather than skimming or guessing at their content? Useful specifically for research, where getting a source's content wrong is a bigger problem than in casual use. Flag this as a "would this help" question, not a guaranteed build — it depends on what's available in your own Claude environment.
- **Backup specifics.** If section E said yes to a cloud mirror: do you specifically want the rclone-to-Google-Drive approach this setup uses? If so, `SETUP.md` section 4 has the exact commands — including a real incident where an earlier `rclone sync` deleted a file, and why the fix was switching to `rclone copy` everywhere. Worth reading before setting this part up even if you already know rclone.

### H. Sensitive data — ask this explicitly, don't skip it
- Does any of this work involve data that must never leave your machine or be backed up anywhere outside it — IRB-protected human-subjects data, identifiable interview material, anything under a data use agreement, or anything else confidential? If yes, get specific about which files or folders, so they can be explicitly excluded from *any* backup or sync step set up below, before any backup is configured.

---

## Build menu

Offer these conditionally, matched to what was actually said above — don't set up something nobody asked for.

1. **A standing preferences file** (a `CLAUDE.md`-equivalent). Always worth offering — lowest effort, biggest payoff, just a text file capturing how they want Claude to work so it doesn't need to be re-explained every session.
2. **Skills** for any recurring task named in section C. One skill per distinct task; don't invent one that wasn't asked for.
3. **The document-sanitizer skill** — only if section G said yes to sharing documents externally. Copy `.claude/skills/sanitize-document/` and `Tools/sanitize_doc.py` from this repo as-is; it doesn't need adapting.
4. **Zotero MCP integration** — only if section G named Zotero. `SETUP.md` section 3 has the install and registration commands.
5. **Obsidian MCP integration** — only if section G named Obsidian (or offer to look up the equivalent for whatever notes app they actually use, if it has one). `SETUP.md` section 3, same as above.
6. **The `pdf-research-workflow` skill** — only if section G indicated PDFs, especially scanned ones, are a real part of the work. Copy `.claude/skills/pdf-research-workflow/` as a starting point (the mk-folder convention and naming rule need no changes), but rebuild its OCR and PDF→Markdown sections around whatever's actually installed on their machine — those two parts are a worked example, not something to copy verbatim.
7. **Automatic checks (hooks)** — only if section D indicated they want this. Explain plainly that this is optional machinery, not something everyone needs.
8. **A session wrap-up command** — only if section D indicated they want a routine, repeatable end-of-session step. `.claude/commands/end.md` in this repo is a working example to adapt — it's written around Zotero + Obsidian specifically, so strip or replace the parts that don't apply.
9. **Git-based version control** — only if section E indicated they want it. If section H flagged sensitive files, make sure those are excluded (`.gitignore` or equivalent) from the very first commit, not added after the fact.
10. **A cloud backup mirror** — only if section E indicated wanting a second backup. If section G said they specifically want the rclone/Google-Drive approach, `SETUP.md` section 4 has the exact commands and the reasoning behind `copy` vs. `sync`; otherwise use whichever service they already have. Same sensitive-data exclusions as above apply here too.
11. **Cross-machine sync** (a startup check that pulls updates, a log of what happened each session) — only if section E indicated they actually work across multiple machines. Skip entirely for a single-machine setup; it solves a problem they don't have.

---

## Safety rules to carry over, not optional

- Never install software, create an account, generate an API key, or set up a git remote/cloud connection without telling the person first and getting a clear yes.
- Never include a file flagged in section H in any backup, sync, or cloud step, under any circumstance.
- Prefer reversible actions over destructive ones (e.g., send a file to the recycle bin/trash rather than deleting it permanently) when cleaning anything up.
- Don't assume a specific operating system's paths or install commands — confirm the OS from section F before writing anything platform-specific.

---

## When done

Give a plain-language summary: what got built, where the files live, and — for anything automated (skills, hooks, commands) — a one-line reminder of what it does and how to turn it off if it turns out not to be useful.
