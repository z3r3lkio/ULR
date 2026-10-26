# ULR Safari Web Extension — iOS / iPadOS

This folder contains a SwiftUI container app, native Safari extension handler, Safari Web Extension JavaScript resources, and an **XcodeGen project specification** (`project.yml`).

## Generate and build on macOS

Install Xcode and XcodeGen, then:

```bash
cd ios
xcodegen generate --spec project.yml
xcodebuild -project ULR.xcodeproj -scheme ULR -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build
```

GitHub Actions performs an unsigned iOS Simulator build and checks for the embedded Safari extension. **A simulator .app is not an IPA and cannot be installed on a physical iPad.**

## Install on an iPad

Open the generated project in Xcode, choose your Apple Development team for **both** targets, replace bundle identifiers if needed, connect the iPad and build/run. Enable ULR in iPadOS Settings → Apps → Safari → Extensions and grant access to the supported website.

The app observes VikingFile's `#download-link` after **manual** verification and displays candidate links in a popup. Other sites use generic anchor detection. It does not bypass CAPTCHA or read private Safari cookies. A detected link can be session-bound.

## Limitations

The code has not been tested on a physical iPad. Safari API behavior, extension permissions and popup clipboard operations must be validated on-device. This is a development build, not a signed distribution IPA. GitHub Actions cannot generate an installable device IPA without Apple signing credentials and appropriate provisioning.
