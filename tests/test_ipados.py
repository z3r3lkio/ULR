import unittest
from ulr_ipados import normalize, provider, direct_pixeldrain, resolve

class IPadCliTests(unittest.TestCase):
    def test_url(self):
        self.assertEqual(normalize("https://example.org/a"), "https://example.org/a")
    def test_base64(self):
        self.assertEqual(normalize("aHR0cHM6Ly9leGFtcGxlLm9yZy9h"), "https://example.org/a")
    def test_reject_bad(self):
        for value in ("file:///tmp/x", "javascript:alert(1)", "http://user:pass@example.org"):
            with self.assertRaises(ValueError):
                normalize(value)
    def test_provider(self):
        self.assertEqual(provider("https://pixeldrain.com/u/abc"), "pixeldrain.com")
        self.assertEqual(provider("https://fakepixeldrain.com/u/abc"), "generic")
    def test_pixeldrain(self):
        self.assertEqual(direct_pixeldrain("https://pixeldrain.com/u/abc123"), "https://pixeldrain.com/api/file/abc123")
        self.assertIsNone(direct_pixeldrain("https://evilpixeldrain.com/u/abc123"))
    def test_noninteractive(self):
        result, method = resolve("https://example.org", interactive=False)
        self.assertIsNone(result)
        self.assertEqual(method, "safari-manual")
