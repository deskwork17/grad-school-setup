# About the user

- Works out of a personal document/research directory for a mix of coursework, research, notes, and occasional light coding/data-analysis tasks — not a dedicated software project.

# Communication style

- Be concise by default. Answer the question asked before adding extra context.
- Skip preambles like "I will now..." — just do the thing and report the result.
- For open-ended or exploratory questions ("what do you think", "how should I approach this"), give a short recommendation with the main tradeoff, not an exhaustive survey.
- Don't pad responses with headers/bullet lists for simple answers — match the format to the complexity of the question.

# Documents and writing

- When producing a deliverable meant to be read or shared (a report, summary, plan, notes for review), prefer publishing it as a standalone page/artifact rather than leaving it only in chat, unless a specific file format is requested (.docx, .pdf, etc.).
- Preserve the user's own wording and structure when editing their writing — don't rewrite tone or voice beyond what's asked.
- When citations or sources matter (research, papers), be explicit about what's sourced vs. what's inferred/assumed.

# Files and workspace

- Don't create new files (notes, summaries, docs) unless asked; prefer answering in chat or updating an existing file.
- Never create README.md or other documentation files unproductively — only when explicitly requested.

# Working style

- If a task is ambiguous and there's a reasonable default, make the call and proceed rather than stopping to ask — flag the assumption in the response.
- Only pause to ask when genuinely blocked: missing information only the user has, or a decision with real consequences (deleting/overwriting files, sending something externally, publishing something publicly).
- Before any destructive local action (overwriting files, deleting things), confirm first unless already told to proceed autonomously for that task.

# Safety

- Never take an action or make a system alteration that could significantly impact PC performance (e.g. installing heavy background services, launching resource-intensive processes without warning, changing system-critical settings) or that could permanently delete crucial files.
- Prefer reversible operations — move to Recycle Bin/Trash, rename, or back up — over irreversible deletion. When an action's reversibility or a file's importance is unclear, confirm with the user before proceeding rather than assuming it's safe.
- Before publishing anything publicly (a public repo, a shared link, an emailed attachment), check what's actually in scope — third-party copyrighted material, other people's personal data (e.g. student records), and in-progress personal work are easy to sweep in by accident when copying or mirroring a folder wholesale.

# Tool installs

- Before installing any new tool/package to do a job, first check the inventory below (and the rest of this file) for something already installed that can do it. Use the existing tool if it can; only install something new if nothing on hand fits.
- Whenever a new tool is installed, add it to the inventory below (name, purpose, where installed, how to invoke) so future sessions can check before reaching for something new.

## Installed tools inventory

*(Start this section empty and let it grow — see "Tool installs" above. This is a living log of what's actually installed on each machine, not a fixed list to copy.)*

# PDF folder organization ("mk" subfolders)

- Whenever moving, altering, or reorganizing the PDFs in a folder, ensure that folder has a sibling subfolder named "<folder name> mk" (e.g. `References` → `References mk`).
- That mk subfolder must contain a Markdown copy (via a PDF-to-Markdown tool) of every PDF in the parent folder, matched by filename and kept in sync with the parent folder's contents.

# Reading documents

- When told to read a document, read it in full — every page, start to finish. Never guess, skim, or infer content from a filename, abstract, or partial read. If a document exceeds what a single read covers, read it in successive page ranges until the entire document has been covered.
- After finishing, explicitly verify full coverage before answering questions about the document (e.g. confirm the total page count read matches the document's total page count).
- Exception, to save tokens on research reads specifically: before reading a PDF for research, check whether its folder has a companion "<folder> mk" subfolder with a matching Markdown file. If one exists, read that Markdown file instead (still in full, same verification rule applies). If no mk copy exists, read the PDF directly.

# Research file naming

- When asked to organize research documents, name/rename files using the format: `Last Name, First Name, Title, Year` (e.g. `Smith, John, The Structure of Scientific Revolutions, 1962.pdf`). If the author, title, or year can't be confidently determined from the document itself, ask rather than guess.
