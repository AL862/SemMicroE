#!/usr/bin/env python3
"""Proofread course text with a local LanguageTool server. Never modify inputs."""
import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


class VisibleHTML(HTMLParser):
    skip_tags = {"script", "style", "head", "template", "textarea"}
    blocks = {"p", "div", "h1", "h2", "h3", "h4", "li", "tr", "section",
              "article", "summary", "br", "hr", "td", "th"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = []
        self.inline_handlers = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in self.skip_tags:
            self.skip.append(tag)
            return
        if self.skip:
            return
        for name in attrs:
            if name.lower().startswith("on"):
                self.inline_handlers.append(name)
        if tag in self.blocks:
            self.parts.append("\n")
        if tag == "input" and attrs.get("type", "text") not in {"hidden", "password"}:
            if attrs.get("value"):
                self.parts.append(attrs["value"] + "\n")
        if tag == "img" and attrs.get("alt"):
            self.parts.append(attrs["alt"] + "\n")

    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip[-1]:
                self.skip.pop()
            return
        if tag in self.blocks:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def text(self):
        return normalize_text("".join(self.parts))


def normalize_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def extract_text(path):
    suffix = path.suffix.lower()
    metadata = {}
    if suffix in {".html", ".htm"}:
        parser = VisibleHTML()
        parser.feed(path.read_text(encoding="utf-8-sig"))
        text = parser.text()
        metadata["inline_handlers"] = sorted(set(parser.inline_handlers))
        metadata["coverage"] = "Static HTML text; excludes script/style/head/template/textarea. Dynamic text and image text require separate review."
    elif suffix in {".txt", ".md"}:
        text = normalize_text(path.read_text(encoding="utf-8-sig"))
    elif suffix in {".docx", ".pptx"}:
        with zipfile.ZipFile(path) as archive:
            if suffix == ".docx":
                names = ["word/document.xml"]
            else:
                names = sorted(
                    (name for name in archive.namelist()
                     if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
                    key=lambda name: int(re.search(r"slide(\d+)", name).group(1)))
            paragraphs = []
            for name in names:
                root = ElementTree.fromstring(archive.read(name))
                for paragraph in root.iter():
                    if paragraph.tag.rsplit("}", 1)[-1] == "p":
                        paragraphs.append("".join(
                            node.text or "" for node in paragraph.iter()
                            if node.tag.rsplit("}", 1)[-1] == "t"))
            text = normalize_text("\n".join(paragraphs))
        metadata["coverage"] = "Native document/slide text only. Images, charts, formulas and slide pictures require separate visual or OCR review."
    elif suffix == ".pdf":
        result = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(path), "-"],
            check=True, capture_output=True, text=True, encoding="utf-8")
        text = normalize_text(result.stdout)
        metadata["coverage"] = "PDF text layer only. Scanned pages require OCR and visual verification."
    else:
        raise ValueError("Supported inputs: HTML, TXT, MD, DOCX, PPTX and text PDFs.")
    if not text.strip():
        raise ValueError(f"No extractable text in {path}; scanned pages and image-only slides require OCR.")
    return text, metadata


def course_findings(text, metadata):
    rules = [
        ("COURSE_NO_COMMAS", ",", "README 0.21: rewrite visible teaching text without commas."),
        ("COURSE_ROMANIAN_DIACRITICS", "[şţŞŢ]", "Use Romanian comma-below letters ș/ț rather than cedilla letters."),
        ("COURSE_CHELTUIALA", r"\bcheltuial[ăa]\b", "README 0.9: rephrase without this word."),
        ("COURSE_ROMANIAN_PHRASE", r"\bceteris\s+paribus\b", "README 6.1: use ceilalți factori rămân neschimbați."),
        ("COURSE_PSEUDO_SUBSCRIPT", r"\b(?:Q|P|E|MU|TU|TP|AP|MP|CO)_[A-Za-z]", "README 0.17: use real subscript/superscript notation.")
    ]
    issues = []
    for rule_id, pattern, message in rules:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            issues.append({
                "rule": rule_id, "message": message, "count": len(matches),
                "examples": [
                    {"offset_codepoints": m.start(),
                     "context": text[max(0, m.start()-45):m.end()+45]}
                    for m in matches[:10]]
            })
    if metadata.get("inline_handlers"):
        issues.append({"rule": "COURSE_INLINE_HANDLER",
                       "message": "Review inline JavaScript event handlers against README 0.6.",
                       "attributes": metadata["inline_handlers"]})
    return issues


def chunks(text, limit=6000):
    start = 0
    while start < len(text):
        end = min(start + limit, len(text))
        if end < len(text):
            boundary = max(text.rfind("\n", start+limit//2, end),
                           text.rfind(". ", start+limit//2, end))
            if boundary < 0:
                boundary = text.rfind(" ", start+limit//2, end)
            if boundary > start:
                end = boundary + 1
        yield start, text[start:end]
        start = end


def check_text(text, language, server, timeout):
    parsed = urllib.parse.urlsplit(server)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("--server must be an HTTP(S) LanguageTool base URL.")
    if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    else:
        opener = urllib.request.build_opener()
    responses = []
    software = None
    for index, (start, chunk) in enumerate(chunks(text), 1):
        data = urllib.parse.urlencode({"text": chunk, "language": language}).encode()
        request = urllib.request.Request(
            server.rstrip("/") + "/v2/check", data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        with opener.open(request, timeout=timeout) as response:
            result = json.load(response)
        if "matches" not in result:
            raise ValueError("LanguageTool returned a response without matches.")
        software = result.get("software", software)
        responses.append({
            "chunk": index,
            "chunk_start_codepoints": start,
            "matches": result["matches"]
        })
    return software, responses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--language", default="ro")
    parser.add_argument("--server", default="http://127.0.0.1:8081")
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skip-course-rules", action="store_true")
    args = parser.parse_args()
    reports = []
    try:
        for path in args.files:
            text, metadata = extract_text(path)
            software, responses = check_text(text, args.language, args.server, args.timeout)
            reports.append({
                "file": str(path), "language": args.language,
                "characters": len(text), "extraction": metadata,
                "software": software,
                "course_findings": [] if args.skip_course_rules else course_findings(text, metadata),
                "languagetool_chunks": responses,
                "languagetool_match_count": sum(len(r["matches"]) for r in responses)
            })
    except (OSError, ValueError, KeyError, zipfile.BadZipFile,
            ElementTree.ParseError, subprocess.CalledProcessError,
            urllib.error.URLError) as error:
        print(f"Check failed: {error}", file=sys.stderr)
        return 2
    payload = json.dumps({"files": reports}, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 1 if any(r["course_findings"] or r["languagetool_match_count"] for r in reports) else 0


if __name__ == "__main__":
    raise SystemExit(main())
