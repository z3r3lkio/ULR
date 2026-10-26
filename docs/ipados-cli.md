# ULR CLI for iPadOS (a-Shell / Python)

`ulr_ipados.py` uses only the Python standard library. It does **not** require Chromium, Playwright or Tkinter.

## Run

In a-Shell, install/enable Python if needed, place `ulr_ipados.py` in your working directory, then:

```sh
python3 ulr_ipados.py "https://vik1ngfile.site/f/ptbYOnNq86#FINAL"
python3 ulr_ipados.py "https://pixeldrain.com/u/EXAMPLE"
python3 ulr_ipados.py "https://example.org/" --no-interactive
```

The script tries the a-Shell `open` command to launch Safari, falling back to Python `webbrowser`. If automatic launch fails, open the displayed URL manually. Complete any verification yourself. In Safari, long-press the actual download link and choose **Copy Link**, then return to the terminal and paste it into the prompt.

**Platform limitation:** iPadOS does not allow a normal Python console process to read Safari's page DOM, download events, cookies, or CAPTCHA response. A bookmarklet or Safari Web Extension would need explicit user action and still cannot generally share Safari's authenticated session with a terminal app. This release therefore uses a **manual Safari handoff**, not automatic capture. A copied download URL may be session-bound and fail in another downloader.

Pixeldrain `/u/<id>` URLs are transformed into the public API download endpoint without browser interaction. That does not bypass service access controls, quotas or rate limits. Other providers currently use manual handoff. Do not paste private cookies or access tokens into the terminal.

## Desktop CI

`python -m unittest discover -s tests -v` includes iPadOS CLI unit tests. Actual Safari behavior must be tested on an iPad.
