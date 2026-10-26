# ULR — Universal Link Resolver

Python desktop application with URL and Base64 input, VikingFile download-link extraction after completing Turnstile, generic browser-download detection, copy/open and aria2 JSON-RPC.

## Run

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python resolver.py
python -m unittest discover -s tests -v
```

## GitHub Actions

`.github/workflows/build.yml` tests with Python 3.14 and builds unsigned PyInstaller artifacts on Windows, macOS and Linux. **Chromium is not bundled** in the generated packages; install a compatible Playwright Chromium on the target machine. This is not yet a standalone zero-dependency installer. Linux needs a GUI and Tkinter.

## Provider status

VikingFile: detects the `#download-link` URL after user verification. Other hosts: generic detection of user-initiated downloads, not a guarantee of support. No CAPTCHA bypass is provided. iPadOS is not supported by these desktop builds.
