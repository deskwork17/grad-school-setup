# Setting up Claude for your own research workflow

## What this file is

This is not documentation to read — it's a script for **your own Claude** (Claude Code, or another Claude with file and shell access on your machine) to read and act on. It was adapted from a working setup built for a sociology graduate student's thesis and coursework directory, documented in a companion handout ("Using Claude Code in the Social Sciences").

The point isn't to copy that setup wholesale. Everyone's research workflow is different — different file types, different comfort with the command line, different backup needs, different sensitivity around data. This file instead has your Claude **interview you** about your own workflow, then build only the pieces that actually fit.

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

### G. Sensitive data — ask this explicitly, don't skip it
- Does any of this work involve data that must never leave your machine or be backed up anywhere outside it — IRB-protected human-subjects data, identifiable interview material, anything under a data use agreement, or anything else confidential? If yes, get specific about which files or folders, so they can be explicitly excluded from *any* backup or sync step set up below, before any backup is configured.

---

## Build menu

Offer these conditionally, matched to what was actually said above — don't set up something nobody asked for.

1. **A standing preferences file** (a `CLAUDE.md`-equivalent). Always worth offering — lowest effort, biggest payoff, just a text file capturing how they want Claude to work so it doesn't need to be re-explained every session.
2. **Skills** for any recurring task named in section C. One skill per distinct task; don't invent one that wasn't asked for.
3. **Automatic checks (hooks)** — only if section D indicated they want this. Explain plainly that this is optional machinery, not something everyone needs.
4. **A session wrap-up command** — only if section D indicated they want a routine, repeatable end-of-session step.
5. **Git-based version control** — only if section E indicated they want it. If section G flagged sensitive files, make sure those are excluded (`.gitignore` or equivalent) from the very first commit, not added after the fact.
6. **A cloud backup mirror** — only if section E indicated wanting a second backup, using whichever service they already have rather than pushing a new one on them. Same sensitive-data exclusions as above apply here too.
7. **Cross-machine sync** (a startup check that pulls updates, a log of what happened each session) — only if section E indicated they actually work across multiple machines. Skip entirely for a single-machine setup; it solves a problem they don't have.

---

## Safety rules to carry over, not optional

- Never install software, create an account, generate an API key, or set up a git remote/cloud connection without telling the person first and getting a clear yes.
- Never include a file flagged in section G in any backup, sync, or cloud step, under any circumstance.
- Prefer reversible actions over destructive ones (e.g., send a file to the recycle bin/trash rather than deleting it permanently) when cleaning anything up.
- Don't assume a specific operating system's paths or install commands — confirm the OS from section F before writing anything platform-specific.

---

## When done

Give a plain-language summary: what got built, where the files live, and — for anything automated (skills, hooks, commands) — a one-line reminder of what it does and how to turn it off if it turns out not to be useful.
