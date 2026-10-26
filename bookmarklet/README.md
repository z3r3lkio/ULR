# ULR Safari bookmarklet — iPadOS (no installation)

This is a manual, on-page alternative while the native Safari extension is being tested. It reads the **current page's visible link elements only**, after any required user verification. It never solves CAPTCHAs, reads cookies, or sends URLs to an external server.

## Add on an iPad

1. Open Safari and save **any** page as a bookmark named `ULR Resolver`.
2. Run `python3 bookmarklet/make_bookmarklet.py` on a computer/terminal (or copy the generated URL from a trusted source); copy the entire output starting with `javascript:`.
3. In Safari, edit the `ULR Resolver` bookmark, replacing its address with that complete `javascript:` URL.
4. Open a supported download page. Complete verification manually.
5. Tap the bookmark. If a link is present, ULR shows it in a copyable prompt. If no link is present, retry after the page exposes the final link.

**Important:** JavaScript bookmarklets are subject to Safari/iPadOS version-specific restrictions and are not guaranteed to work on all pages. A page may require interaction that does not expose a normal anchor link. Bookmarklets do not transfer Safari's authenticated session to another app. The prompt UI may require manual selection and copying.

Supported host allowlist: VikingFile, MediaFire, GoFile, Pixeldrain, 1fichier. Other providers require a specific adapter; generic anchor scanning is not guaranteed to yield the final download URL.
