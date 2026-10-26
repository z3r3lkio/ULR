import base64
import unittest
from providers import decode_input, provider_name

class ProviderTests(unittest.TestCase):
    def test_url(self):
        self.assertEqual(decode_input("https://example.com/a"),"https://example.com/a")
    def test_base64(self):
        u="https://vik1ngfile.site/f/abc"
        self.assertEqual(decode_input(base64.b64encode(u.encode()).decode()),u)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            decode_input("not-a-link")
    def test_provider(self):
        self.assertEqual(provider_name("https://gofile.io/d/abc"),"GoFile")
if __name__ == "__main__":
    unittest.main()
