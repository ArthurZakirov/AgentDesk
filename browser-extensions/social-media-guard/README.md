# Social Media Guard

A local Chrome extension that removes people-discovery and recommendation surfaces from LinkedIn and X.

## LinkedIn

- Arthur's own profile, `/in/arthurzakirov/`, remains fully accessible.
- Other member profiles are blocked in Strict mode or reduced to name/profile image in Minimal mode.
- `/mynetwork` and all subpaths below it are blocked in Strict and Minimal modes.
- Hides **Today’s puzzles**, **Add to your feed**, **People you may know**, and **You might like**.
- On Arthur's own profile, the right-hand recommendation sidebar is hidden while the main profile remains visible.

## X

- Arthur's own profile, `x.com/ArthurZakir`, remains accessible.
- Other single-handle profile pages such as `x.com/ArminNassehi` are blocked whenever the guard is enabled.
- On `/i/connect_people...`, **Who to follow** and **Creators for you** are hidden.
- On Arthur's own X profile, **Who to follow** sections are hidden.
- Common application routes such as `/home`, `/explore`, `/notifications`, `/messages`, `/i/...`, and `/settings` are not treated as profiles.

## Modes

| Mode | LinkedIn | X |
| --- | --- | --- |
| **Strict** | Blocks other profiles and My Network. | Blocks other profiles and hides recommendation surfaces. |
| **Minimal** | Shows only name/profile image on other profiles; My Network stays blocked. | Blocks other profiles and hides recommendation surfaces. |
| **Off** | Leaves LinkedIn unchanged. | Leaves X unchanged. |

## Install locally

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Choose **Load unpacked**.
4. Select `browser-extensions/social-media-guard`.
5. Leave **Strict** selected unless you explicitly want LinkedIn Minimal mode.

No build step or third-party dependency is required.

## Implementation notes

- Manifest V3.
- One extension, with separate LinkedIn and X content scripts.
- The selected mode is stored in `chrome.storage.sync`.
- Profile blocking is route-based rather than dependent on brittle CSS class names.
- Recommendation removal uses exact visible labels plus nearby structural containers.
- Both sites are single-page applications, so DOM and URL changes are re-checked after navigation.

Chrome extensions can always be disabled or removed by the user. This is a friction mechanism, not a security boundary.
