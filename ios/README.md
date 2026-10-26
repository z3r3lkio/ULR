# ULR Safari Web Extension — prototype

The source for a Safari Web Extension for iPhone and iPad lives in this folder. It observes page links and detects VikingFile's #download-link after the user completes any verification. The popup offers Copy and Open. No cookies are extracted and no CAPTCHA is bypassed.

## Build setup

On macOS, use Xcode's **Safari Web Extension App** template for iOS, name the app ULR, then replace the generated SwiftUI app sources with those under ULR/ and the extension's web resources with the contents of ULRSafariExtension/. Configure unique app/extension bundle IDs and your Apple signing team. Enable the extension in iPad Settings → Apps → Safari → Extensions and grant permission to the supported site.

**Not yet an Xcode project or IPA.** The repository includes source files only, not a ready-to-build Xcode project. Actual iPadOS execution, Safari MV3 support and clipboard behavior still require device validation. A generated template may require adjusting the manifest/background script for the target Safari version. The extension retains detected URLs in extension-local storage and does not upload them.
