import unittest
from pathlib import Path
from subprocess import check_output
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
class BookmarkletTests(unittest.TestCase):
    def test_generated_url(self):
        out=check_output(["python3",str(ROOT/"bookmarklet/make_bookmarklet.py")],text=True).strip()
        self.assertTrue(out.startswith("javascript:"))
        decoded=unquote(out[len("javascript:"):])
        self.assertIn("#download-link[href]",decoded)
        self.assertIn("vik1ngfile.site",decoded)
        self.assertNotIn("fetch(",decoded)
