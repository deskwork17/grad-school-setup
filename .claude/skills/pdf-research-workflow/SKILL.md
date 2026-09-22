---
name: pdf-research-workflow
description: Read, organize, rename, and convert PDF research documents — checks for and reads a companion Markdown transcript instead of re-opening the PDF, keeps a folder's sibling "<folder> mk" transcript subfolder in sync, renames sources to "Last Name, First Name, Title, Year", and runs OCR + PDF-to-Markdown conversion for scanned/text PDFs. Use whenever reading, organizing, moving, or naming a PDF (or similar) research source.
---

In the source setup this is a **global** skill (`~/.claude/skills/pdf-research-workflow/`), not project-scoped — PDF handling isn't specific to one project, so it's set up to apply everywhere. Copy it to your own `~/.claude/skills/` for the same effect, or into a project's `.claude/skills/` if you'd rather scope it narrower.

**Before using this as-is:** the OCR and PDF→Markdown sections below name specific tools (Tesseract + pymupdf4llm) as a working example — swap them for whatever's actually installed on your machine. See `SETUP.md` in this repo for more on why nothing here should be copied blindly.

## Reading a PDF for research

Before reading a PDF for research, check whether its folder has a companion "<folder> mk" subfolder with a matching Markdown file. If one exists, read that Markdown file instead — still in full, with the same coverage-verification standard as any document read. If no mk copy exists, read the PDF directly.

## Keeping the "mk" subfolder in sync

Whenever moving, altering, or reorganizing the PDFs in a folder, ensure that folder has a sibling subfolder named "<folder name> mk" (e.g. `References` → `References mk`). That mk subfolder must contain a Markdown copy (via the PDF-to-Markdown tool below) of every PDF in the parent folder, matched by filename and kept in sync with the parent folder's contents.

## Naming research files

When asked to organize research documents, name/rename files using the format `Last Name, First Name, Title, Year` (e.g. `Smith, John, The Structure of Scientific Revolutions, 1962.pdf`). If the author, title, or year can't be confidently determined from the document itself, ask rather than guess.

## OCR (scanned/image PDF → searchable text) — example: Tesseract

- Engine: Tesseract OCR — free, works fully offline, no Ghostscript dependency needed if paired with a PyMuPDF-based wrapper (renders each page to an image, OCRs each page with Tesseract's own `pdf` output mode, merges pages with `pypdf`).
- A heavier alternative some setups prefer: OCRmyPDF + Ghostscript, or Marker (adds ML-based layout detection at the cost of a much larger install).
- Whichever you use, confirm it actually works against a real scanned file in your own folder before relying on it — a working example only proves the *pattern* works, not that your install of it does.

## PDF → Markdown — example: pymupdf4llm

- Tool: `pymupdf4llm` (`pip install pymupdf4llm`) — pure text/layout extraction, no ML model weights, small footprint.
- Usage: `pymupdf4llm.to_markdown(path)` from Python, or `python -c "import pymupdf4llm; open('out.md','w',encoding='utf-8').write(pymupdf4llm.to_markdown('input.pdf'))"`.
- Only extracts existing text — does not OCR. Run an OCR step first on scanned/image-only PDFs.
- Tables and equations come out less richly than a heavier tool (e.g. Marker) would produce — the tradeoff for a much smaller footprint. If a specific document's tables/equations matter and come out garbled, that's a sign to reach for something heavier for that one file rather than switching your whole stack.
