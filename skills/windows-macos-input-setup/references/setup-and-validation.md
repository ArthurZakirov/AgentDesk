# Windows 11 macOS-like input setup

## Known-good layout

This profile was validated on Windows 11 with a Logitech MX Keys S in Windows mode and Microsoft PowerToys `0.101.2362.0`.

Logitech key identity in Windows mode:

| Physical legend | Windows key | VK |
| --- | --- | --- |
| `control` | Left Ctrl | 162 |
| `option | start` | Left Win | 91 |
| `cmd | alt` immediately left of Space | Left Alt | 164 |

In Logi Options+, enable **Always keep the keyboard in Windows layout**. Do not rely on `Fn+P`: this keyboard provides no useful onscreen confirmation, and forcing Windows layout in Logi Options+ is inspectable and persistent.

## Components

Use current stable Microsoft PowerToys with Keyboard Manager enabled and PowerToys startup enabled. Do not run another keyboard hook for this setup. In particular, disable startup links and running processes for Kinto, `mac-keyboard-behavior-in-windows`, and custom `.ahk` profiles; rename startup links to `.lnk.disabled` instead of deleting them.

PowerToys configuration paths:

```text
%LOCALAPPDATA%\Microsoft\PowerToys\settings.json
%LOCALAPPDATA%\Microsoft\PowerToys\Keyboard Manager\settings.json
%LOCALAPPDATA%\Microsoft\PowerToys\Keyboard Manager\default.json
```

Before editing, create timestamped backups. Parse and write JSON structurally where practical.

Keep the classic Keyboard Manager editor selected in the module settings. Preserve existing properties and set:

```json
"useNewEditor": false
```

PowerToys issue #48498 documents a current regression where merely opening the new Keyboard Manager editor breaks Alt-based shortcut remaps. This setup avoids those remaps entirely, but keeping the classic editor prevents stale `editorSettings.json` state from reintroducing confusion.

## Exact PowerToys profile

Write the following as `default.json`:

```json
{
  "remapKeys": {
    "inProcess": [
      {
        "originalKeys": "164",
        "newRemapKeys": "162"
      }
    ]
  },
  "remapKeysToText": {
    "inProcess": []
  },
  "remapShortcuts": {
    "global": [
      { "originalKeys": "91;9", "newRemapKeys": "164;9", "operationType": 0, "secondKeyOfChord": 0 },
      { "originalKeys": "162;37", "newRemapKeys": "91;163;37", "operationType": 0, "secondKeyOfChord": 0 },
      { "originalKeys": "162;38", "newRemapKeys": "91;9", "operationType": 0, "secondKeyOfChord": 0 },
      { "originalKeys": "162;39", "newRemapKeys": "91;163;39", "operationType": 0, "secondKeyOfChord": 0 },
      { "originalKeys": "91;37", "newRemapKeys": "162;37", "operationType": 0, "secondKeyOfChord": 0 },
      { "originalKeys": "162;91;37", "newRemapKeys": "91;160;37", "operationType": 0, "secondKeyOfChord": 0 },
      { "originalKeys": "162;91;39", "newRemapKeys": "91;160;39", "operationType": 0, "secondKeyOfChord": 0 }
    ],
    "appSpecific": []
  },
  "remapShortcutsToText": {
    "global": [],
    "appSpecific": []
  }
}
```

Resulting behavior:

| Physical shortcut | Windows action |
| --- | --- |
| `cmd | alt` + `C/V/X/Z/A/S/F/W/T/...` | Corresponding `Ctrl` shortcut |
| `option | start` + `Tab` | `Alt+Tab` app switcher |
| `option | start` + `Left` | Move one word left (`Ctrl+Left`) |
| `Control+Up` | Open Task View with all windows and virtual desktops (`Win+Tab`) |
| `Control+Left/Right` | Previous/next virtual desktop (target uses Right Ctrl) |
| `Control+Option+Left/Right` | Move focused window to adjacent monitor |
| `Option+Up` | Native Windows maximize (`Win+Up`), no remap needed |

## Text navigation

The user validated `Option+Left -> Control+Left` directly in PowerToys. It moves
the caret one word left while physical `Control+Left` continues to switch virtual
desktops. In this configuration, PowerToys does not feed the generated
`Control+Left` target back through the separate physical `Control+Left` desktop
rule. The earlier assumption that these rules necessarily conflict was wrong.

The captured profile currently contains:

```text
91;37 -> 162;37
```

This is physical `option | start` (`Left Win`) plus Left mapped to Windows
`Left Ctrl+Left`. The symmetric right-word rule is `91;39 -> 162;39`; add and
validate it when rightward word navigation is requested.

As a fallback, `Control+Shift+Left/Right` selects one word at a time and a plain
arrow collapses the selection. Do not install Kinto or another keyboard hook for
this behavior.

## Task View versus app switching

Preserve these as separate actions:

```text
physical Control+Up  -> Win+Tab  -> Task View / virtual desktops
physical Option+Tab -> Alt+Tab  -> app switching
```

Keep only this Task View source rule:

```text
162;38 -> 91;9
```

Physical Left Control is intentionally not globally remapped. Therefore native
`Control+Tab` continues to switch browser or editor tabs. The separate
`91;9 -> 164;9` rule keeps physical `Option+Tab` as the Windows `Alt+Tab`
application switcher. Never add `162 -> 164` as a key remap; doing so collapses
these distinct behaviors into duplicate `Alt+Tab` actions.

## Maximizing without Narrator

On this Logitech Windows layout, physical `Control+Option+Enter` reaches Windows
as `Win+Control+Enter`. Windows reserves that chord to start or stop Narrator.
On this machine, Narrator still intercepted the real hardware chord even while
`WinEnterLaunchEnabled` was `0`, so do not configure or recommend this mapping.

Disable only the Narrator launch shortcut for the current user:

```powershell
$path = 'HKCU:\Software\Microsoft\Narrator\NoRoam'
New-ItemProperty -Path $path -Name WinEnterLaunchEnabled -PropertyType DWord -Value 0 -Force
```

Keep both of these values disabled:

```text
RunningState = 0
WinEnterLaunchEnabled = 0
```

Use native physical `Option+Up` instead. The Logitech Option key sends Left Win,
so this is already Windows `Win+Up` and requires no PowerToys rule. Do not invent
`Control+Option+Up` as a third shortcut scheme: keep either a platform-native
shortcut or an exact macOS/Rectangle shortcut.

The global Command remap intentionally does not emulate every macOS shortcut. For example, `Command+Q` becomes `Ctrl+Q`, not `Alt+F4`. Do not add Alt-only shortcut rules to compensate while PowerToys issue #48498 remains unresolved.

## Restart correctly

After changing the profile, restart the full PowerToys runner, not only a manually launched Keyboard Manager executable. The engine should be launched by and have the PowerToys runner as its parent.

PowerShell inspection targets:

```powershell
Get-Process PowerToys,PowerToys.KeyboardManagerEngine
Get-CimInstance Win32_Process |
  Where-Object Name -eq 'PowerToys.KeyboardManagerEngine.exe' |
  Select-Object ProcessId,ParentProcessId,CommandLine
```

When starting PowerToys from automation, use its installed `PowerToys.exe` with `--dont-elevate` and a hidden window. Confirm:

- the installed binary version is the intended stable version;
- `%LOCALAPPDATA%\Microsoft\PowerToys\settings.json` has `startup: true`;
- `enabled."Keyboard Manager"` is `true`;
- `PowerToys.KeyboardManagerEngine.exe` is running under `PowerToys.exe`;
- no `AutoHotkey64.exe` or conflicting startup link is active.

## Automatic verification

Configuration validity is necessary but not sufficient. Verify behavior after the final clean restart.

### Command copy/paste

Use native Windows Computer Use against Notepad:

1. Focus the editor and insert a unique sentinel such as `FINAL_GLOBAL_REMAP_PROOF`.
2. Select it with native `Ctrl+A`.
3. send physical-source `Alt_L+C` (`cmd | alt` + `C`).
4. Delete the selected source text.
5. send physical-source `Alt_L+V`.
6. Read Notepad accessibility text and require an exact sentinel match.

Capture state after every input. If a failed Alt-shortcut experiment leaves Notepad menu mnemonics visible, press and release `Alt_L` once, refresh focus, and restart the test from a new sentinel. This is test-environment cleanup, not part of normal setup.

Repeat the copy/paste test after restarting PowerToys. A success before restart can be a stale in-memory remap and is not final proof.

### Virtual desktops

Require at least two desktops. Read these registry values before and after the source shortcut:

```powershell
$v = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops'
[Convert]::ToHexString([byte[]]$v.CurrentVirtualDesktop)
[Convert]::ToHexString([byte[]]$v.VirtualDesktopIDs)
```

From a window on the current desktop, send `Control_L+Left` or `Control_L+Right` through native Computer Use, then require `CurrentVirtualDesktop` to equal the adjacent ID. Test the two directions independently from a clean Keyboard Manager hook. A target-window-bound synthetic chord can lose its key-up when the window disappears during a desktop switch; do not interpret an immediate opposite-direction failure from that same synthetic session as a physical-keyboard failure.

Computer Use must not send a Windows-key shortcut directly. It may send the user-facing source `Control+Left/Right`; PowerToys generates the Windows-key target.

### Monitor movement

Validate that the final profile contains:

```text
162;91;37 -> 91;160;37
162;91;39 -> 91;160;39
```

These are physical `Control+Option+Left/Right` to native `Win+Shift+Left/Right`. End-to-end automation requires an allowed input path capable of the source Windows key and a multi-monitor geometry check. Do not claim end-to-end proof when the automation policy forbids Windows-key injection.

### Option+Tab

Validate `91;9 -> 164;9`. This maps the Logitech `option | start` key plus Tab to native Windows `Alt+Tab`, while physical Control remains available for browser tab switching and desktop shortcuts.

## Natural scrolling

On current Windows 11, use:

```text
Settings > Bluetooth & devices > Mouse > Scrolling > Scrolling direction
```

Choose **Down motion scrolls up** (German: **Abwärtsbewegung nach oben**). This is system-wide and independent of PowerToys. If the setting is absent, use Logi Options+ for that mouse; only use the `FlipFlopWheel` registry fallback after identifying the correct HID device instance and backing up its value.

## Direct monitor selection

Do not reproduce the approximate Hammerspoon `Control+Option+J/K/L` mapping on this Windows layout. `Option` is Left Win, so `Control+Option+L` includes protected `Win+L` and may lock the workstation before a remapper can intercept it. A safer future design is `Control+Option+1/2/3`, implemented with an established monitor-window utility and verified against actual monitor bounds. It is optional and not part of the known-good profile above.

## Sources

- Microsoft PowerToys Keyboard Manager: https://learn.microsoft.com/windows/powertoys/keyboard-manager
- PowerToys profile format: https://github.com/microsoft/PowerToys/blob/main/doc/devdocs/modules/keyboardmanager/keyboardmanager.md
- Current Alt-remap editor regression: https://github.com/microsoft/PowerToys/issues/48498
- Microsoft mouse settings: https://support.microsoft.com/windows/hardware/input-devices/change-mouse-settings
