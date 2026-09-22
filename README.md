# Grad school + Claude Code: a research workflow setup

A working example of configuring [Claude Code](https://claude.com/claude-code) to run inside a real graduate research workflow — coursework, a thesis project, and a citation library — rather than as a standalone chat window. This repo is the **infrastructure only**: standing instructions, automation, and tooling. It does not include the actual coursework, thesis notes, or citation-library PDFs from the setup it was extracted from — those are personal and, in the case of the citation library and assigned readings, other people's copyrighted work.

## Start here

Two ways into this, depending on how hands-on you want to be:

- **Let your own Claude drive:** hand it **[`README/claude-setup-guide.md`](README/claude-setup-guide.md)**. It interviews you about your own workflow first and builds only the pieces that fit, rather than replicating this setup wholesale.
- **Do it yourself, or follow along with the literal steps:** **[`SETUP.md`](SETUP.md)** is the actual reference — real commands, in order, for the hooks/skills/commands, the Zotero and Obsidian MCP servers, and the Git + Google Drive backup layer.
- **See it explained first:** **[`README/Using Claude Code in the Social Sciences.pptx`](README/Using%20Claude%20Code%20in%20the%20Social%20Sciences.pptx)** is a slide-deck walkthrough of the whole setup, including the "lesson learned" incident that shaped the backup rules in `SETUP.md`.

## What's in this repo

| Path | What it is |
|---|---|
| `CLAUDE.md` | Portable standing instructions — drop into `~/.claude/CLAUDE.md` (or adapt into a project-level `CLAUDE.md`) to replicate the behavioral rules this setup runs on. |
| `SETUP.md` | Step-by-step reference for everything below: hooks, skills, commands, MCP servers, and the backup/sync layer. |
| `.claude/hooks/session_start_sync.py` | A SessionStart hook: checks GitHub, a Google Drive mirror, and for new PDFs at the start of every session, and reports all three every time. |
| `.claude/commands/end.md` | A `/end` slash command that reconciles a citation library, updates setup docs, logs the session, and pushes/backs up — one command instead of six manual steps. |
| `.claude/skills/sanitize-document/SKILL.md` | A skill that strips hidden metadata from a document before it's shared, without Claude ever reading the file's contents. |
| `.claude/settings.local.json.example` | Shows how the hook above gets registered — copy to `.claude/settings.local.json` and adjust. |
| `.claude/rclone-exclude.txt.example` | Template exclude list for the Google Drive mirror — copy to `.claude/rclone-exclude.txt` and edit. |
| `Tools/sanitize_doc.py` | The script the sanitize-document skill runs. |

MCP servers (Zotero, Obsidian) aren't files you copy — they're covered in `SETUP.md` section 3 as install + registration commands.

## The folder-structure convention this setup assumes

The hook and slash command above assume a directory shaped roughly like this (none of it is created for you — it's documentation, not scaffolding):

| Folder | Holds |
|---|---|
| `<Term>/` (e.g. `Fall 2026/`) | Coursework, one folder per term |
| `<Term>/<Topic> mk/` | Markdown transcripts of that topic's PDFs, kept in sync — see the PDF-research workflow described in the slide deck |
| `<Notes vault>/` | An Obsidian (or similar) vault of research notes, optionally linked to Claude via a local MCP connection |
| `<Citation mirror>/` | A repo-tracked mirror of a citation manager's PDFs, organized by collection |
| `Tools/` | Small custom scripts |
| `Last session/` | Dated session logs — the continuity thread between sessions and machines |

## Why no content, only infrastructure

The setup this was extracted from lives in a private repository that also holds actual coursework readings, a citation-library PDF mirror, and in-progress thesis notes — most of that is either someone else's copyrighted work (assigned readings, journal articles) or personal academic work not meant for public redistribution. This repo exists so the *mechanism* — the instructions, hooks, skills, and commands — can be reused without any of that content coming along for the ride.

---

*Companion project: [soc-methods-handout](https://github.com/deskwork17/soc-methods-handout) — a narrative handout covering the same setup, written for a methods-seminar audience.*
