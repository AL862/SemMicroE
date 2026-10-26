import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
import zipfile
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "check_course_text.py"
spec = importlib.util.spec_from_file_location("course_checker", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class CourseCheckerTests(unittest.TestCase):
    def test_html_preserves_romanian_text_and_excludes_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "seminar.html"
            path.write_text(
                '<head><style>.a{color:red}</style></head>'
                '<p>Text corect șț. Q<sub>d</sub> este cantitatea cerută.</p>'
                '<script>const text="cheltuiala, ceteris paribus";</script>',
                encoding="utf-8")
            original = path.read_bytes()
            text, metadata = checker.extract_text(path)
            self.assertIn("Text corect șț.", text)
            self.assertIn("Qd este cantitatea cerută.", text)
            self.assertNotIn("const", text)
            self.assertNotIn("color:red", text)
            self.assertEqual(checker.course_findings(text, metadata), [])
            self.assertEqual(path.read_bytes(), original)

    def test_course_rules_detect_punctuation_and_wrong_diacritics(self):
        findings = checker.course_findings(
            "Cheltuială, ceteris paribus. ştiinţă Q_d", {})
        identifiers = {finding["rule"] for finding in findings}
        self.assertEqual(identifiers, {
            "COURSE_NO_COMMAS", "COURSE_CHELTUIALA",
            "COURSE_ROMANIAN_PHRASE", "COURSE_ROMANIAN_DIACRITICS",
            "COURSE_PSEUDO_SUBSCRIPT"})

    def test_chunking_keeps_all_unicode_text_in_order(self):
        text = ("Explicație despre școală și producție. 🧮\n" * 700) + "Final."
        parts = list(checker.chunks(text))
        self.assertEqual("".join(part for _, part in parts), text)
        self.assertTrue(all(len(part) <= 6000 for _, part in parts))
        for offset, part in parts:
            self.assertEqual(text[offset:offset+len(part)], part)

    def test_docx_joins_runs_inside_paragraphs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "conspect.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml",
                    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                    '<w:body><w:p><w:r><w:t>Produc</w:t></w:r>'
                    '<w:r><w:t>ție corectă.</w:t></w:r></w:p></w:body></w:document>')
            text, _ = checker.extract_text(path)
            self.assertEqual(text, "Producție corectă.")

    def test_image_only_pptx_requires_ocr(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "slides.pptx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("ppt/slides/slide1.xml",
                    '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
                    '<p:pic/></p:sld>')
            with self.assertRaisesRegex(ValueError, "require OCR"):
                checker.extract_text(path)

    def test_unavailable_server_does_not_report_success_or_change_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "material.txt"
            report = Path(directory) / "report.json"
            source.write_text("Text corect.", encoding="utf-8")
            original = source.read_bytes()
            args = ["checker", str(source), "--output", str(report)]
            with patch.object(checker.sys, "argv", args), \
                 patch.object(checker, "check_text",
                              side_effect=urllib.error.URLError("unavailable")), \
                 contextlib.redirect_stderr(io.StringIO()):
                status = checker.main()
            self.assertEqual(status, 2)
            self.assertFalse(report.exists())
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
