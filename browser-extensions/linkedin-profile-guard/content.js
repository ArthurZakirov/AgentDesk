const DEFAULT_MODE = "strict";
const PROFILE_PATH = /^\/in\/[^/]+\/?/;

let mode = DEFAULT_MODE;
let lastUrl = location.href;

function isProfileUrl(value = location.href) {
  try {
    return new URL(value, location.origin).hostname.endsWith("linkedin.com")
      && PROFILE_PATH.test(new URL(value, location.origin).pathname);
  } catch {
    return false;
  }
}

function getProfileName() {
  const heading = document.querySelector("main h1");
  if (heading?.textContent?.trim()) return heading.textContent.trim();

  return document.title
    .replace(/\s*\|\s*LinkedIn.*$/i, "")
    .trim();
}

function getProfileImage() {
  const name = getProfileName().toLowerCase();
  const images = [...document.querySelectorAll("main img[alt]")];

  return images.find((image) => image.alt.toLowerCase().includes(name))
    || images.find((image) => image.width >= 80 && image.height >= 80)
    || null;
}

function ensureRoot() {
  if (!document.body) return null;

  let root = document.getElementById("lpg-root");
  if (root) return root;

  root = document.createElement("div");
  root.id = "lpg-root";
  document.body.append(root);
  return root;
}

function renderProfileGuard() {
  const profile = isProfileUrl();
  const active = profile && mode !== "off";

  document.documentElement.toggleAttribute("data-lpg-active", active);
  document.documentElement.dataset.lpgMode = active ? mode : "";

  const root = ensureRoot();
  if (!root) return;

  if (!active) {
    root.replaceChildren();
    return;
  }

  const card = document.createElement("section");
  card.className = "lpg-card";

  if (mode === "strict") {
    card.innerHTML = `
      <p class="lpg-kicker">LinkedIn Profile Guard</p>
      <h1>Profile hidden</h1>
      <p>This member profile is intentionally unavailable in Strict mode.</p>
      <button id="lpg-back" type="button">Go back</button>
    `;
    root.replaceChildren(card);
    root.querySelector("#lpg-back")?.addEventListener("click", () => history.back());
    return;
  }

  const name = getProfileName() || "LinkedIn member";
  const image = getProfileImage();

  card.innerHTML = `
    <p class="lpg-kicker">Minimal profile</p>
    <div class="lpg-avatar-slot"></div>
    <h1></h1>
    <p>Posts, activity, experience, education, recommendations, and the rest of the profile are hidden.</p>
  `;
  card.querySelector("h1").textContent = name;

  if (image?.src) {
    const clone = document.createElement("img");
    clone.className = "lpg-avatar";
    clone.src = image.src;
    clone.alt = "";
    card.querySelector(".lpg-avatar-slot").append(clone);
  }

  root.replaceChildren(card);
}

function showBlockedClick() {
  const toast = document.createElement("div");
  toast.className = "lpg-toast";
  toast.textContent = "Profile blocked by LinkedIn Profile Guard";
  document.body?.append(toast);
  setTimeout(() => toast.remove(), 1800);
}

function blockProfileNavigation(event) {
  if (mode !== "strict") return;

  const anchor = event.target.closest?.("a[href]");
  if (!anchor || !isProfileUrl(anchor.href)) return;

  event.preventDefault();
  event.stopImmediatePropagation();
  showBlockedClick();
}

document.addEventListener("click", blockProfileNavigation, true);
document.addEventListener("auxclick", blockProfileNavigation, true);

if (isProfileUrl()) {
  document.documentElement.setAttribute("data-lpg-active", "");
  document.documentElement.dataset.lpgMode = DEFAULT_MODE;
}

chrome.storage.sync.get({ mode: DEFAULT_MODE }).then((settings) => {
  mode = settings.mode;
  renderProfileGuard();
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "sync" || !changes.mode) return;
  mode = changes.mode.newValue ?? DEFAULT_MODE;
  renderProfileGuard();
});

const observer = new MutationObserver((mutations) => {
  if (!isProfileUrl() || mode !== "minimal") return;

  const onlyGuardChanges = mutations.every((mutation) => {
    const target = mutation.target;
    return target instanceof Element
      && (target.id === "lpg-root" || target.closest("#lpg-root"));
  });

  if (!onlyGuardChanges) renderProfileGuard();
});
observer.observe(document.documentElement, { childList: true, subtree: true });

setInterval(() => {
  if (location.href === lastUrl) return;
  lastUrl = location.href;
  renderProfileGuard();
}, 250);

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderProfileGuard, { once: true });
} else {
  renderProfileGuard();
}
