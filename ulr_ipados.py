#!/usr/bin/env python3
"""ULR iPadOS CLI: stdlib-only resolver with manual Safari handoff.

Safari and Python terminals on iPadOS do not share DOM/session state. This
tool never attempts to bypass CAPTCHA or access Safari cookies.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import webbrowser

USER_AGENT = "ULR-iPadOS/0.1"
KNOWN = ("vik1ngfile.site", "vikingfile.com", "mediafire.com", "gofile.io", "pixeldrain.com", "1fichier.com")

def normalize(value):
    value = value.strip()
    if not value.startswith(("http://", "https://")):
        try:
            value = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode("utf-8").strip()
        except (ValueError, UnicodeError) as exc:
            raise ValueError("Not an HTTP(S) URL or Base64-encoded URL") from exc
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Invalid HTTP(S) URL")
    return value

def provider(url):
    host = urllib.parse.urlsplit(url).hostname.lower()
    for domain in KNOWN:
        if host == domain or host.endswith("." + domain):
            return domain
    return "generic"

def direct_pixeldrain(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname not in ("pixeldrain.com", "www.pixeldrain.com"):
        return None
    match = re.fullmatch(r"/u/([a-zA-Z0-9_-]+)", parsed.path)
    if not match:
        return None
    return "https://pixeldrain.com/api/file/" + match.group(1)

def open_safari(url):
    # a-Shell provides an 'open' command on iPadOS.
    try:
        result = subprocess.run(["open", url], check=False, capture_output=True, timeout=8)
        if result.returncode == 0:
            return True
    except (OSError, subprocess.TimeoutExpired):
        pass
    try:
        return bool(webbrowser.open(url))
    except Exception:
        return False

def safari_handoff(url, interactive=True):
    print("\n[Safari] Open this URL and complete any required verification:")
    print(url)
    opened = open_safari(url)
    if not opened:
        print("[Safari] Could not open automatically. Copy the URL into Safari.")
    print("[Safari] When a download link is visible, copy its URL using a long press.")
    print("[Safari] Return to the terminal and paste the copied URL.")
    if not interactive:
        return None
    while True:
        try:
            candidate = input("Direct download URL (blank to cancel): ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if not candidate:
            return None
        try:
            return normalize(candidate)
        except ValueError as exc:
            print("[!] " + str(exc))

def resolve(url, interactive=True):
    # This endpoint is documented by Pixeldrain. Download may be rate-limited.
    direct = direct_pixeldrain(url)
    if direct:
        return direct, "pixeldrain-api"
    # Other services require a verified provider adapter or a manual Safari handoff.
    return safari_handoff(url, interactive), "safari-manual"

def main(argv=None):
    parser = argparse.ArgumentParser(description="ULR CLI for iPadOS (Python stdlib)")
    parser.add_argument("url", help="HTTP(S) URL or URL-safe Base64 URL")
    parser.add_argument("--no-interactive", action="store_true", help="Print instructions without prompting")
    parser.add_argument("--json", action="store_true", help="Print result as JSON")
    args = parser.parse_args(argv)
    try:
        url = normalize(args.url)
        if not args.json:
            print("[+] Provider:", provider(url))
        result, method = resolve(url, interactive=not args.no_interactive)
        if args.json:
            print(json.dumps({"input": url, "provider": provider(url), "method": method, "url": result}))
        elif result:
            print("\n[+] Download URL (may require the same Safari session):\n" + result)
        else:
            print("\n[!] No link supplied.")
        return 0 if result else 1
    except ValueError as exc:
        print("[ERROR] " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
