import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from organizer import category_for, organize


class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def test_preview_does_not_create_directories(self):
        (self.folder / 'notes.txt').write_text('keep')
        self.assertEqual(organize(self.folder)[0]['status'], 'planned')
        self.assertFalse((self.folder / 'Documents').exists())
        self.assertTrue((self.folder / 'notes.txt').exists())

    def test_move_preserves_bytes(self):
        (self.folder / 'notes.txt').write_bytes(b'hello\x00world')
        self.assertEqual(organize(self.folder, True)[0]['status'], 'moved')
        self.assertEqual((self.folder / 'Documents/notes.txt').read_bytes(), b'hello\x00world')
        self.assertFalse((self.folder / 'notes.txt').exists())

    def test_conflict_keeps_both_files(self):
        (self.folder / 'Documents').mkdir()
        (self.folder / 'Documents/notes.txt').write_text('existing')
        (self.folder / 'notes.txt').write_text('new')
        self.assertEqual(organize(self.folder, True)[0]['status'], 'conflict')
        self.assertEqual((self.folder / 'Documents/notes.txt').read_text(), 'existing')
        self.assertEqual((self.folder / 'notes.txt').read_text(), 'new')

    def test_category_file_blocks_move(self):
        (self.folder / 'Images').write_text('not a directory')
        (self.folder / 'pic.png').write_text('demo')
        rows = organize(self.folder, True)
        self.assertEqual(next(r for r in rows if r['file'] == 'pic.png')['status'], 'blocked')
        self.assertTrue((self.folder / 'pic.png').exists())

    def test_hidden_and_nested_files_ignored(self):
        (self.folder / '.env').write_text('demo')
        (self.folder / 'nested').mkdir()
        (self.folder / 'nested/a.txt').write_text('demo')
        self.assertEqual(organize(self.folder, True), [])

    def test_extension_case_and_fallback(self):
        self.assertEqual(category_for(Path('PHOTO.PNG')), 'Images')
        self.assertEqual(category_for(Path('unknown.xyz')), 'Other')

    @patch('organizer.os.link', side_effect=OSError('unsupported'))
    def test_failed_move_preserves_source(self, mock):
        (self.folder / 'a.txt').write_text('preserve')
        self.assertEqual(organize(self.folder, True)[0]['status'], 'error')
        self.assertEqual((self.folder / 'a.txt').read_text(), 'preserve')

    def test_second_run_has_no_work(self):
        (self.folder / 'a.txt').write_text('demo')
        organize(self.folder, True)
        self.assertEqual(organize(self.folder, True), [])

    def test_unlink_failure_reports_partial_and_keeps_data(self):
        (self.folder / 'a.txt').write_text('preserve')
        with patch.object(Path, 'unlink', side_effect=PermissionError('locked')):
            self.assertEqual(organize(self.folder, True)[0]['status'], 'partial')
        self.assertEqual((self.folder / 'a.txt').read_text(), 'preserve')
        self.assertEqual((self.folder / 'Documents/a.txt').read_text(), 'preserve')
