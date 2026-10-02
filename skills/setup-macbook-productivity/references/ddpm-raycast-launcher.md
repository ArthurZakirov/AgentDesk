# ⌨️ Open Dell DDPM from Raycast

Use **⌘ Space → DDPM Launcher → Enter** to open Dell Display and Peripheral Manager’s full settings window. The user does not need to identify or click its menu-bar icon.

## 🛠️ Fresh-Mac setup

1. Install Dell Display and Peripheral Manager from [Dell’s official setup page](https://www.dell.com/support/kbdoc/en-sg/000201067/dell-display-and-peripheral-manager-for-macos). Confirm DDPM detects the supported monitor. Install Raycast and configure its preferred launcher shortcut.
2. Ensure Apple Command Line Tools are available (`xcrun --find swiftc`). If missing, use Apple’s supported installation prompt (`xcode-select --install`) before continuing.
3. Run the [bundled installer](../scripts/setup_ddpm_raycast_launcher.py) from the installed skill directory or this repository:

   ```bash
   python3 skills/setup-macbook-productivity/scripts/setup_ddpm_raycast_launcher.py
   ```

   It builds `~/Applications/DDPM Launcher.app`, copies Dell’s icon, and verifies its local code signature. It does not launch the app or grant permissions.
4. In **System Settings → Privacy & Security → Accessibility**, add **DDPM Launcher** using **+** and enable it. The file picker’s **⌘ Shift G** accepts `~/Applications/DDPM Launcher.app`. Explain that this permission allows the helper to invoke Dell’s menu command. Follow the active runtime’s permission-confirmation rules; when authorized, use computer control to complete this setup. Let the user handle authentication if macOS requires it. Never edit the privacy database or disable protections.
5. In Raycast, search **DDPM Launcher** and press **Enter**. If it is not indexed yet, verify `open -Ra "DDPM Launcher"`; restart Raycast only if needed.

## ✅ Verify the actual behavior

Close Dell’s full settings window while leaving DDPM running. Open Raycast, select **DDPM Launcher**, and press **Enter**. Verify that the **DDPM** window shows controls such as **Brightness / Contrast**, **Input Source**, and **KVM**. Repeat once with the window already open to confirm the launcher brings it forward.

An indexed app, running process, successful compilation, or enabled permission switch alone does not establish success. Verify the resulting Dell controls with computer use or direct observation.

**Observed on 2026-10-02:** this workflow opened DDPM’s full controls from Raycast after the window had been closed. Re-run the procedure above on each new Mac; Dell’s menu structure and macOS behavior may change.

## 🔍 Why this mechanism works

The [launcher source](../scripts/ddpm_launcher.swift) locates DDPM by its bundle identifier. If its full controls already exist, it raises that window. Otherwise it locates Dell’s own status item through Accessibility, opens its context menu, and invokes the exact **Open Dell Display and Peripheral Manager** item. It restores the pointer position afterward. It starts DDPM if necessary and uses bounded waits for the menu and window.

A regular app reopen request did not reopen the controls in the observed setup. Dell’s status item exposed only `AXPress`; that basic action opened an empty popup in automation. A context-menu event exposed the named **Open** action. The helper therefore automates that specific action rather than making the user find the icon.

## 🧩 Troubleshooting without repeating failed attempts

| Symptom | Check / action |
| --- | --- |
| Accessibility switch is on but the helper still reports denied access. | Quit the helper. Remove only its stale Accessibility entry, add the current app again, and enable it. This resolved the stale identity observed during development. |
| Rebuilding changes the permission identity. | Use the installer’s stable designated requirement and bundle identifier. Do not rename the identifier or replace signing requirements casually. This is a locally built, ad-hoc-signed helper, not a notarized vendor app. |
| Computer use times out when selecting DDPM Launcher. | The helper normally exits and has no persistent window. Inspect **DDPM** after running it; a helper-window timeout is not proof that its action failed. |
| Computer use reports no windows for DDPM before launch. | DDPM may be running with its controls closed. Start through Raycast, then inspect DDPM again. System Settings and Raycast remain usable computer-control surfaces. |
| An empty popup appears. | Do not substitute the basic `AXPress` action for the tested context-menu mechanism. |
| The named Open command or status item is unavailable. | Inspect Dell’s current menu once, confirm DDPM is running and detects the monitor, and adapt only after observing the changed UI. Do not cycle through unrelated menu-bar icons, reinstall blindly, or edit Raycast databases. |

The installer can build to an isolated destination with `--output /tmp/DDPM-test.app` for compilation/signature checks. Do not run an isolated test copy when validating the installed app’s permission identity.
