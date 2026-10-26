import os
import sys
from pathlib import Path

def configure_browser():
    root = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    bundled = root / "pw-browsers"
    if bundled.is_dir():
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(bundled)
    return bundled

if __name__ == "__main__":
    browser_dir = configure_browser()
    if "--self-test" in sys.argv:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            executable = Path(playwright.chromium.executable_path)
            if not executable.is_file():
                raise SystemExit(f"Chromium executable missing: {executable}")
            print(f"ULR packaged browser OK: {executable}")
        raise SystemExit(0)
    from resolver import gui
    gui()
