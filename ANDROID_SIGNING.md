# Android Release Signing

These workflows support one shared Android release signing identity across the Lux apps.

## One-time setup (keep the key private)

1. On your own trusted computer, open PowerShell in a private folder (not inside a public Git repository).
2. Generate the keystore. Choose a strong password when prompted and keep it in a password manager:

```powershell
keytool -genkeypair -v -keystore lux-apps-release.jks -alias lux-apps-release -keyalg RSA -keysize 4096 -validity 10000 -dname "CN=king0878artin-byte, OU=Apps, O=king0878artin-byte, C=US"
```

3. Convert the keystore to one Base64 line:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$PWD\lux-apps-release.jks")) | Set-Clipboard
```

4. In each of the five GitHub repositories, open Settings → Secrets and variables → Actions → New repository secret and add:

| Secret name | Value |
|---|---|
| ANDROID_KEYSTORE_BASE64 | Base64 value copied in step 3 |
| ANDROID_KEYSTORE_PASSWORD | Keystore password |
| ANDROID_KEY_ALIAS | lux-apps-release |
| ANDROID_KEY_PASSWORD | Key password |

Use the exact same keystore, alias, and passwords in all five repositories. Never upload the .jks file, paste passwords into chat, or commit them to Git.

5. Run the repository workflow from Actions. The workflow signs the APK with Android apksigner and verifies the signature before uploading. If secrets are missing, it warns that the APK remains debug-signed.

## Critical backup warning

Keep at least two secure offline backups of lux-apps-release.jks and its passwords. If this key is lost, future updates signed with a new key will not install as updates over existing installations signed with the old key. Do not rotate or replace this key casually.

## What signing does and does not mean

A valid signature identifies the signing key and detects changes made after signing. It does not prove an app is harmless, grant Google Play trust, or guarantee antivirus products will never show a warning. Keep dependencies and source code clean, publish transparent releases, and investigate security detections rather than attempting to bypass them.