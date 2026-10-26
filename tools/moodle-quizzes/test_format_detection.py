"""Regression tests for Moodle's literal XML declaration requirement."""
import unittest
import xml.etree.ElementTree as E
from build import xmlbytes
from validate import detect_moodle2_metadata

class FormatDetection(unittest.TestCase):
    def metadata(self):
        root=E.Element('moodle_backup');E.SubElement(root,'information');return root
    def test_generated_metadata(self):
        # Use a populated information element as in a real Moodle backup.
        root=self.metadata();E.SubElement(root.find('information'),'name').text='Test.mbz'
        self.assertTrue(detect_moodle2_metadata(xmlbytes(root)))
    def test_previous_default_is_well_formed_but_not_detected(self):
        root=self.metadata();E.SubElement(root.find('information'),'name').text='Test.mbz'
        old=E.tostring(root,encoding='utf-8',xml_declaration=True)
        E.fromstring(old)
        self.assertFalse(detect_moodle2_metadata(old))
    def test_provided_template_style(self):
        raw=b'<?xml version="1.0" encoding="UTF-8"?>\n<moodle_backup>\n<information>\n</information>\n</moodle_backup>'
        self.assertTrue(detect_moodle2_metadata(raw))
    def test_standard_question_xml_is_not_activity_backup(self):
        self.assertFalse(detect_moodle2_metadata(xmlbytes(E.Element('quiz'))))
    def test_detector_reads_only_first_200_bytes(self):
        raw=b' '*201+b'<?xml version="1.0" encoding="UTF-8"?><moodle_backup><information>'
        self.assertFalse(detect_moodle2_metadata(raw))
if __name__=='__main__':unittest.main()
