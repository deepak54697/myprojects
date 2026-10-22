import tempfile
import unittest
from pathlib import Path
from stock_alert import analyze_inventory, render_html

HEADER = 'sku,name,quantity,reorder_point,target_stock\n'


class StockTests(unittest.TestCase):
    def analyze(self, rows, header=HEADER):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'input.csv'
            path.write_text(header + rows, encoding='utf-8')
            return analyze_inventory(path)

    def test_boundary_triggers_and_order_calculated(self):
        alert = self.analyze('A,Coffee,5,5,15\n')['alerts'][0]
        self.assertEqual(alert['suggested_order'], 10)

    def test_healthy_stock_excluded(self):
        self.assertEqual(self.analyze('A,Coffee,6,5,15\n')['alert_count'], 0)

    def test_out_of_stock_first(self):
        alerts = self.analyze('A,Coffee,2,5,15\nB,Cups,0,3,10\n')['alerts']
        self.assertEqual(alerts[0]['sku'], 'B')
        self.assertEqual(alerts[0]['status'], 'out_of_stock')

    def test_duplicate_sku_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.analyze('A,Coffee,2,5,15\na,Cups,3,5,15\n')

    def test_negative_and_fractional_rejected(self):
        for value in ['-1', '2.5', 'NaN', 'inf']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.analyze(f'A,Coffee,{value},5,15\n')

    def test_invalid_target_rejected(self):
        with self.assertRaisesRegex(ValueError, 'target_stock'):
            self.analyze('A,Coffee,2,5,4\n')

    def test_missing_headers_rejected(self):
        with self.assertRaises(ValueError):
            self.analyze('A,Coffee\n', 'sku,name\n')

    def test_duplicate_headers_rejected(self):
        with self.assertRaises(ValueError):
            self.analyze('', HEADER.strip() + ',sku\n')

    def test_empty_valid_input(self):
        self.assertEqual(self.analyze('')['products_checked'], 0)

    def test_html_escapes_product_name(self):
        report = self.analyze('A,<script>alert(1)</script>,0,5,15\n')
        self.assertNotIn('<script>', render_html(report))
        self.assertIn('&lt;script&gt;', render_html(report))
