"""
Strip hidden/leakable metadata from a document without displaying its content.

Supported types:
  .docx/.docm/.dotx/.dotm  - Word: properties, comments, tracked changes, hidden (vanish) text
  .pptx/.pptm/.potx/.potm  - PowerPoint: properties, comments
  .xlsx/.xlsm/.xltx/.xltm  - Excel: properties, comments/notes, legacy shared-workbook revisions
  .pdf                     - PDF: Info dict + XMP metadata, annotations, embedded files, JS/OpenAction

Always writes a NEW file (default: "<name> (sanitized).<ext>" next to the input) and
never overwrites the original. Only reports counts/categories of what was removed -
never prints the actual field values or document content.

Usage:
    python sanitize_doc.py <input> [-o output_path]
"""

import argparse
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# OOXML (docx/pptx/xlsx) namespaces
# ---------------------------------------------------------------------------

NS = {
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

_COMMON_PREFIXES = {
    "w": NS["w"],
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "v": "urn:schemas-microsoft-com:vml",
    "o": "urn:schemas-microsoft-com:office:office",
}
for _prefix, _uri in _COMMON_PREFIXES.items():
    ET.register_namespace(_prefix, _uri)


def _q(ns_key, local):
    return f"{{{NS[ns_key]}}}{local}"


def _local(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _write_xml(root, default_ns_uri=None):
    if default_ns_uri is not None:
        ET.register_namespace("", default_ns_uri)
    body = ET.tostring(root, encoding="unicode")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n' + body).encode("utf-8")


# ---------------------------------------------------------------------------
# Core/extended properties (docProps/core.xml, docProps/app.xml)
# ---------------------------------------------------------------------------

_CORE_FIELDS_TO_CLEAR = {"creator", "lastModifiedBy", "description", "keywords", "subject", "title", "category", "contentStatus"}
_APP_FIELDS_TO_CLEAR_EMPTY = {"Company", "Manager", "HyperlinkBase"}
_APP_FIELDS_TO_ZERO = {"TotalTime"}


def _sanitize_core_props(xml_bytes, counts):
    root = ET.fromstring(xml_bytes)
    changed = False
    for el in root.iter():
        local = _local(el.tag)
        if local in _CORE_FIELDS_TO_CLEAR and el.text:
            el.text = ""
            changed = True
            counts["properties_cleared"] += 1
        elif local == "revision" and el.text and el.text != "1":
            el.text = "1"
            changed = True
    return _write_xml(root, NS["cp"]) if changed else xml_bytes


def _sanitize_app_props(xml_bytes, counts):
    root = ET.fromstring(xml_bytes)
    changed = False
    for el in root.iter():
        local = _local(el.tag)
        if local in _APP_FIELDS_TO_CLEAR_EMPTY and el.text:
            el.text = ""
            changed = True
            counts["properties_cleared"] += 1
        elif local in _APP_FIELDS_TO_ZERO and el.text and el.text != "0":
            el.text = "0"
            changed = True
    return _write_xml(root, NS["ep"]) if changed else xml_bytes


# ---------------------------------------------------------------------------
# Word: tracked changes, hidden text, comment markers
# ---------------------------------------------------------------------------

_FULL_REMOVE_TAGS = {
    "del", "moveFrom",
    "rPrChange", "pPrChange", "sectPrChange", "tblPrChange", "tcPrChange", "trPrChange", "tblGridChange",
    "commentRangeStart", "commentRangeEnd", "commentReference",
}
_UNWRAP_TAGS = {"ins", "moveTo"}


def _sanitize_word_part(xml_bytes, counts):
    root = ET.fromstring(xml_bytes)

    parent_of = {}
    for parent in root.iter():
        for child in parent:
            parent_of[child] = parent

    to_remove = []
    to_unwrap = []
    for el in root.iter():
        local = _local(el.tag)
        if local in _FULL_REMOVE_TAGS:
            to_remove.append(el)
        elif local in _UNWRAP_TAGS:
            to_unwrap.append(el)

    for r in root.iter(_q("w", "r")):
        rpr = r.find(_q("w", "rPr"))
        if rpr is not None and rpr.find(_q("w", "vanish")) is not None:
            to_remove.append(r)

    removed = 0
    for el in to_remove:
        parent = parent_of.get(el)
        if parent is None:
            continue
        try:
            parent.remove(el)
            removed += 1
        except ValueError:
            pass  # already removed as a descendant of another removed element

    unwrapped = 0
    for el in to_unwrap:
        parent = parent_of.get(el)
        if parent is None:
            continue
        try:
            idx = list(parent).index(el)
        except ValueError:
            continue
        for i, child in enumerate(list(el)):
            parent.insert(idx + i, child)
            parent_of[child] = parent
        parent.remove(el)
        unwrapped += 1

    counts["tracked_changes_removed"] += removed
    counts["tracked_changes_removed"] += unwrapped
    return _write_xml(root) if (removed or unwrapped) else xml_bytes


# ---------------------------------------------------------------------------
# Content types / relationship cleanup after dropping parts
# ---------------------------------------------------------------------------

def _resolve_rels_target(rels_zip_path, target, mode):
    if mode == "External":
        return None
    base_dir = posixpath.dirname(posixpath.dirname(rels_zip_path))  # "<dir>/_rels/<part>.rels" -> "<dir>"
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(base_dir, target)).replace("\\", "/")


def _scrub_content_types(xml_bytes, removed_parts):
    root = ET.fromstring(xml_bytes)
    removed_set = {"/" + p for p in removed_parts}
    changed = False
    for override in list(root):
        if _local(override.tag) == "Override" and override.get("PartName") in removed_set:
            root.remove(override)
            changed = True
    return _write_xml(root, NS["ct"]) if changed else xml_bytes


def _scrub_rels(zip_path, xml_bytes, removed_parts):
    root = ET.fromstring(xml_bytes)
    changed = False
    for rel in list(root):
        if _local(rel.tag) != "Relationship":
            continue
        target = rel.get("Target", "")
        mode = rel.get("TargetMode", "")
        resolved = _resolve_rels_target(zip_path, target, mode)
        if resolved is not None and resolved in removed_parts:
            root.remove(rel)
            changed = True
    return _write_xml(root, NS["pkgrel"]) if changed else xml_bytes


# ---------------------------------------------------------------------------
# OOXML driver (docx / pptx / xlsx)
# ---------------------------------------------------------------------------

_WORD_CONTENT_PARTS = re.compile(r"^word/(document\.xml|header\d*\.xml|footer\d*\.xml|footnotes\.xml|endnotes\.xml)$")
_WORD_COMMENT_PARTS = re.compile(r"^word/(comments.*\.xml|people\.xml)$")
_PPT_COMMENT_PARTS = re.compile(r"^ppt/comments/.*\.xml$")
_XL_COMMENT_PARTS = re.compile(r"^xl/(comments\d*\.xml|threadedComments/.*\.xml|persons/.*\.xml|revisions/.*\.xml)$")
_THUMBNAIL_PART = re.compile(r"^docProps/thumbnail\.(jpeg|jpg|png|emf|wmf)$", re.IGNORECASE)


def sanitize_ooxml(input_path, output_path):
    counts = {"properties_cleared": 0, "comments_removed_parts": 0, "tracked_changes_removed": 0, "other_parts_removed": 0}

    with zipfile.ZipFile(input_path, "r") as zin:
        names = zin.namelist()
        contents = {name: zin.read(name) for name in names}
        infos = {info.filename: info for info in zin.infolist()}

    removed_parts = set()
    for name in names:
        if name == "docProps/custom.xml":
            removed_parts.add(name)
        elif _THUMBNAIL_PART.match(name):
            removed_parts.add(name)
        elif _WORD_COMMENT_PARTS.match(name):
            removed_parts.add(name)
        elif _PPT_COMMENT_PARTS.match(name):
            removed_parts.add(name)
        elif _XL_COMMENT_PARTS.match(name):
            removed_parts.add(name)

    # drop each removed part's own dedicated .rels file too, if it has one
    for part in list(removed_parts):
        d, f = posixpath.split(part)
        rels_path = posixpath.join(d, "_rels", f + ".rels") if d else posixpath.join("_rels", f + ".rels")
        if rels_path in contents:
            removed_parts.add(rels_path)

    counts["comments_removed_parts"] = sum(1 for p in removed_parts if _WORD_COMMENT_PARTS.match(p) or _PPT_COMMENT_PARTS.match(p) or _XL_COMMENT_PARTS.match(p))
    counts["other_parts_removed"] = len(removed_parts) - counts["comments_removed_parts"]

    edited = {}
    if "docProps/core.xml" in contents:
        edited["docProps/core.xml"] = _sanitize_core_props(contents["docProps/core.xml"], counts)
    if "docProps/app.xml" in contents:
        edited["docProps/app.xml"] = _sanitize_app_props(contents["docProps/app.xml"], counts)

    for name in names:
        if name in removed_parts:
            continue
        if _WORD_CONTENT_PARTS.match(name):
            edited[name] = _sanitize_word_part(contents[name], counts)

    if "[Content_Types].xml" in contents and removed_parts:
        edited["[Content_Types].xml"] = _scrub_content_types(contents["[Content_Types].xml"], removed_parts)

    if removed_parts:
        for name in names:
            if name.endswith(".rels") and name not in removed_parts:
                edited[name] = _scrub_rels(name, contents.get(name, edited.get(name)), removed_parts)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            if name in removed_parts:
                continue
            data = edited.get(name, contents[name])
            info = infos[name]
            new_info = zipfile.ZipInfo(name, date_time=info.date_time)
            new_info.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(new_info, data)

    return counts


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def sanitize_pdf(input_path, output_path):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    counts = {"had_metadata": False, "had_xmp": False, "embedded_files_removed": 0, "annotations_removed": 0, "js_or_openaction_removed": 0}

    doc = fitz.open(str(input_path))

    meta = doc.metadata or {}
    if any(v for k, v in meta.items() if k != "format" and v):
        counts["had_metadata"] = True
    doc.set_metadata({})

    try:
        xmp = doc.get_xml_metadata()
        if xmp:
            counts["had_xmp"] = True
        doc.set_xml_metadata("")
    except Exception:
        pass

    try:
        for name in list(doc.embfile_names()):
            doc.embfile_del(name)
            counts["embedded_files_removed"] += 1
    except Exception:
        pass

    try:
        catalog_xref = doc.pdf_catalog()
        if doc.xref_get_key(catalog_xref, "OpenAction")[0] != "null":
            doc.xref_set_key(catalog_xref, "OpenAction", "null")
            counts["js_or_openaction_removed"] += 1
        names_type, names_val = doc.xref_get_key(catalog_xref, "Names")
        if names_type == "xref":
            names_xref = int(names_val.strip().split()[0])
            if doc.xref_get_key(names_xref, "JavaScript")[0] != "null":
                doc.xref_set_key(names_xref, "JavaScript", "null")
                counts["js_or_openaction_removed"] += 1
    except Exception:
        pass

    for page in doc:
        for annot in list(page.annots() or []):
            if annot.type[1] == "Widget":
                continue
            page.delete_annot(annot)
            counts["annotations_removed"] += 1

    doc.save(str(output_path), garbage=4, deflate=True, clean=True)
    doc.close()
    return counts


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_OOXML_EXTS = {".docx", ".docm", ".dotx", ".dotm", ".pptx", ".pptm", ".potx", ".potm", ".xlsx", ".xlsm", ".xltx", ".xltm"}


def default_output_path(input_path):
    return input_path.with_name(f"{input_path.stem} (sanitized){input_path.suffix}")


def sanitize(input_path, output_path=None):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(str(input_path))
    ext = input_path.suffix.lower()
    output_path = Path(output_path) if output_path else default_output_path(input_path)
    if output_path.resolve() == input_path.resolve():
        raise ValueError("output path must differ from input path (sanitize never overwrites the original)")

    if ext == ".pdf":
        counts = sanitize_pdf(input_path, output_path)
    elif ext in _OOXML_EXTS:
        counts = sanitize_ooxml(input_path, output_path)
    else:
        raise ValueError(f"unsupported file type: {ext}")

    return output_path, counts


def main():
    parser = argparse.ArgumentParser(description="Strip hidden metadata/comments/tracked-changes from a document without displaying its content.")
    parser.add_argument("input", help="path to the document")
    parser.add_argument("-o", "--output", help="output path (default: '<name> (sanitized).<ext>' next to the input)")
    args = parser.parse_args()

    try:
        output_path, counts = sanitize(args.input, args.output)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Sanitized copy written to: {output_path}")
    for key, val in counts.items():
        label = key.replace("_", " ")
        if isinstance(val, bool):
            print(f"  - {label}: {'yes' if val else 'no'}")
        else:
            print(f"  - {label}: {val}")


if __name__ == "__main__":
    main()
