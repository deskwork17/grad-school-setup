---
name: sanitize-document
description: Strip hidden/leakable metadata (author info, tracked changes, hidden text, comments, embedded files, PDF XMP/annotations) from a docx/pptx/xlsx/pdf before it's shared, without Claude ever reading the document's content.
---

Use `Tools/sanitize_doc.py` at the repo root to sanitize the file. Rules:

1. Run the tool via Bash only:
   ```
   python Tools/sanitize_doc.py "<path to file>"
   ```
   It always writes a new `<name> (sanitized).<ext>` file next to the original and never overwrites it.

2. **Never `Read` the input (or output) file's content** as part of this skill - the point is that Claude doesn't need to see what's inside to strip its metadata.

3. Once the tool reports success, send the **original** file to the Recycle Bin (never a permanent delete):
   ```powershell
   Add-Type -AssemblyName Microsoft.VisualBasic
   [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('<path to original>', 'OnlyErrorHandling', 'SendToRecycleBin')
   ```

4. Report the sanitized file's path back to the user.
