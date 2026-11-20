# LuxShare

Offline local-network file sharing app built with Python and Kivy.

## Features
- Device discovery using UDP broadcast on the same Wi-Fi/hotspot network.
- TCP streaming transfers (does not load the entire file into memory).
- Maximum file size: 5 GB.
- SHA-256 verification and duplicate filename protection.
- Android APK build using GitHub Actions.

## Build APK
1. Open the repository's **Actions** tab.
2. Select **Build LuxShare APK**.
3. Press **Run workflow** on the main branch.
4. When the run finishes, open it and download the **LuxShare-APK** artifact.

Received files are saved inside the app's private storage under the `Received` folder. Local network discovery can be blocked by some hotspot/router client-isolation settings; both devices must be on the same reachable LAN.
