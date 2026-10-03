import tempfile
import unittest
from pathlib import Path
from analyze import summarize


class AnalyzerTests(unittest.TestCase):
    def run_csv(self, contents):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'tickets.csv'
            path.write_text(contents, encoding='utf-8')
            return summarize(path)

    def test_closed_high_priority_not_urgent(self):
        report = self.run_csv('ticket_id,status,priority,category\n1,closed,high,network\n2, OPEN ,Critical,email\n')
        self.assertEqual(report['urgent_unresolved'], 1)
        self.assertEqual(report['total_tickets'], 2)

    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.run_csv('ticket_id,status,priority,category\n1,open,low,email\n1,open,low,email\n')

    def test_missing_columns_rejected(self):
        with self.assertRaises(ValueError):
            self.run_csv('ticket_id,status\n1,open\n')

    def test_bad_status_rejected(self):
        with self.assertRaises(ValueError):
            self.run_csv('ticket_id,status,priority,category\n1,unknown,low,email\n')

    def test_empty_csv_with_headers(self):
        self.assertEqual(self.run_csv('ticket_id,status,priority,category\n')['total_tickets'], 0)

    def test_missing_value_rejected(self):
        with self.assertRaises(ValueError):
            self.run_csv('ticket_id,status,priority,category\n1,open,high,\n')
