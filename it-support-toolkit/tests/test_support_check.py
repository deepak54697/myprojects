import unittest
from unittest.mock import patch
import socket
from support_check import disk_status, dns_check, render_html


class DiagnosticsTests(unittest.TestCase):
    def test_low_space_warns(self):
        self.assertEqual(disk_status(10, 100)['status'], 'warning')

    def test_threshold_boundary_passes(self):
        self.assertEqual(disk_status(15, 100)['status'], 'pass')

    def test_invalid_disk_total(self):
        with self.assertRaises(ValueError):
            disk_status(0, 0)

    @patch('support_check.socket.getaddrinfo', side_effect=socket.gaierror())
    def test_dns_failure_reported(self, mock):
        self.assertEqual(dns_check('missing.invalid')['status'], 'warning')

    @patch('support_check.socket.getaddrinfo', return_value=[object()])
    def test_dns_success_reported(self, mock):
        self.assertEqual(dns_check('example.test')['status'], 'pass')

    def test_html_escapes_content(self):
        output = render_html({'created_utc': 'demo', 'system': {'os': '<script>'},
                              'checks': {'disk': {'message': '<img onerror=alert(1)>'}}})
        self.assertNotIn('<script>', output)
        self.assertIn('&lt;img', output)


if __name__ == '__main__':
    unittest.main()
