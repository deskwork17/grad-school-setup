#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CLAUDE_DIR = REPO / ".claude"
KNOWN_PDFS_PATH = CLAUDE_DIR / "known_pdfs.json"
RCLONE_EXCLUDE = CLAUDE_DIR / "rclone-exclude.txt"
DRIVE_REMOTE = "gdrive:Grad School"
NEW_PDF_IGNORE_PREFIXES = ("Zotero_backup_", "grant stuff/")


def run(cmd, cwd=REPO):
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )


def github_check():
    run(["git", "fetch", "origin"])
    local = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    remote = run(["git", "rev-parse", "origin/main"]).stdout.strip()
    if local == remote:
        return "GitHub: up to date", None
    behind = run(["git", "rev-list", "--count", "HEAD..origin/main"]).stdout.strip()
    ahead = run(["git", "rev-list", "--count", "origin/main..HEAD"]).stdout.strip()
    if ahead != "0":
        return f"GitHub: diverged from origin/main ({behind} behind, {ahead} ahead) - not auto-pulling", None
    pull = run(["git", "pull", "--ff-only", "origin", "main"])
    if pull.returncode != 0:
        return f"GitHub: pull failed ({pull.stderr.strip()[:200]})", None
    context = (
        "This session just pulled new commits from origin/main. Before doing anything else: "
        "read claudereadme.md in full, then read the most recent file in the 'Last session' "
        "folder, to catch up on what changed and what's outstanding."
    )
    return f"GitHub: pulled {behind} new commit(s)", context


def drive_check():
    if not RCLONE_EXCLUDE.exists():
        return "Drive: skipped (no rclone-exclude.txt yet)"
    check = run([
        "rclone", "check", str(REPO), DRIVE_REMOTE,
        f"--exclude-from={RCLONE_EXCLUDE}",
    ])
    if check.returncode == 0:
        return "Drive: in sync"
    combined = (check.stdout + check.stderr)
    diff_lines = [l for l in combined.splitlines() if l.strip()]
    return f"Drive: {len(diff_lines)} path(s) differ (normal between /end runs)"


def new_pdf_check():
    current = set()
    for p in REPO.rglob("*.pdf"):
        rel = p.relative_to(REPO).as_posix()
        if rel.startswith(".claude/"):
            continue
        if any(rel.startswith(prefix) for prefix in NEW_PDF_IGNORE_PREFIXES):
            continue
        current.add(rel)

    if KNOWN_PDFS_PATH.exists():
        known = set(json.loads(KNOWN_PDFS_PATH.read_text(encoding="utf-8")))
    else:
        known = set()

    new = sorted(current - known)
    KNOWN_PDFS_PATH.write_text(json.dumps(sorted(current), indent=2), encoding="utf-8")

    if not new:
        return "New PDFs: none", None

    listing = "\n".join(f"- {p}" for p in new)
    context = (
        f"New PDF(s) detected since last session start:\n{listing}\n\n"
        "For each one, check: (1) does its folder have a sibling '<folder> mk' subfolder "
        "with a matching Markdown copy - create one if not; (2) is it in Zotero with a "
        "proper citation - add/fix if not; (3) does it have a corresponding Thesis Wiki "
        "Obsidian note, if it's a thesis-relevant source."
    )
    return f"New PDFs: {len(new)} found", context


def main():
    gh_msg, gh_context = github_check()
    drive_msg = drive_check()
    pdf_msg, pdf_context = new_pdf_check()

    system_message = f"{gh_msg} | {drive_msg} | {pdf_msg}"
    out = {"systemMessage": system_message}

    contexts = [c for c in (gh_context, pdf_context) if c]
    if contexts:
        out["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": "\n\n".join(contexts),
        }

    print(json.dumps(out))


if __name__ == "__main__":
    main()
