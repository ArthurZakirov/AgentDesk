# LinkedIn Profile Guard

A local Chrome extension that removes the reward surface from LinkedIn member profiles.

## Behavior

| Mode | Result |
| --- | --- |
| **Strict** | Default. Prevents normal clicks to `/in/...` profiles and fully covers profiles opened directly or in a new tab. Arthur's own `/in/arthurzakirov/` profile is always allowed. |
| **Minimal** | Covers other member profiles but retains only the person's name and, when LinkedIn exposes it in the loaded DOM, their profile image. Arthur's own profile remains fully accessible. |
| **Off** | Leaves LinkedIn unchanged. |

In both Strict and Minimal modes, `/mynetwork` and every subpath below it (for example `/mynetwork/...`) are blocked and fully covered when opened directly.

The extension also hides selected recommendation/distraction cards wherever LinkedIn renders them, including **Today’s puzzles**, **Add to your feed**, **People you may know**, and **You might like**. This also applies on Arthur's own allowed profile without hiding the profile itself.

The extension intentionally avoids selectors for Experience, Activity, Education, and similar sections. Hiding the whole profile surface is simpler and less sensitive to LinkedIn DOM changes.

## Install locally

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Choose **Load unpacked**.
4. Select this directory:
   `browser-extensions/linkedin-profile-guard`
5. Keep **Strict** mode selected in the extension popup.

No build step or third-party dependency is required.

## Implementation

- Manifest V3 extension.
- Runs only on `https://www.linkedin.com/*`.
- Treats `/in/<slug>` as a member-profile route.
- Uses a capture-phase click handler to stop profile navigation in Strict mode.
- Uses a fixed, extension-owned overlay for direct profile URLs.
- Watches URL changes so LinkedIn's single-page navigation is covered as well.
- Stores the selected mode in `chrome.storage.sync`.

## Limitations

LinkedIn can change its markup at any time. Strict mode depends only on the stable profile URL shape and is therefore intentionally more robust than Minimal mode.

Minimal mode's name and image extraction is best-effort. If LinkedIn changes the relevant DOM, the guard still covers the underlying profile, but it may show only the fallback member label or no image.

Chrome extensions cannot prevent the user from disabling or removing the extension. This is a friction mechanism, not a security boundary.
