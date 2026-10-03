const DEFAULT_MODE = "strict";
const OWN_HANDLE = "arthurzakir";
const CONNECT_PEOPLE_PATH = /^\/i\/connect_people(?:\/|$)/;
const HANDLE_PATTERN = /^[A-Za-z0-9_]{1,15}$/;
const SYSTEM_PATHS = new Set([
  "home", "explore", "notifications", "messages", "i", "settings",
  "search", "compose", "jobs", "lists", "bookmarks", "communities",
  "premium", "grok",
]);

let mode = DEFAULT_MODE;
let lastUrl = location.href;

function parseXUrl(value = location.href) {
  try {
    const url = new URL(value, location.origin);
    return url.hostname === "x.com" ? url : null;
  } catch {
    return null;
  }
}

function profileHandle(value = location.href) {
  const url = parseXUrl(value);
  if (!url) return null;

  const parts = url.pathname.split("/").filter(Boolean);
  if (parts.length !== 1 || !HANDLE_PATTERN.test(parts[0])) return null;

  const handle = parts[0].toLowerCase();
  return SYSTEM_PATHS.has(handle) ? null : handle;
}

function isOwnProfile(value = location.href) {
  return profileHandle(value) === OWN_HANDLE;
}

function isBlockedProfile(value = location.href) {
  const handle = profileHandle(value);
  return Boolean(handle && handle !== OWN_HANDLE);
}

function isConnectPeople(value = location.href) {
  const url = parseXUrl(value);
  return Boolean(url && CONNECT_PEOPLE_PATH.test(url.pathname));
}

function isHomeUrl(value = location.href) {
  const url = parseXUrl(value);
  return Boolean(url && /^\/home\/?$/.test(url.pathname));
}

function redirectHomeToOwnProfile() {
  if (mode === "off" || !isHomeUrl()) return false;

  location.replace("https://x.com/ArthurZakir");
  return true;
}

function ensureBlocker() {
  if (!document.body) return null;

  let root = document.getElementById("xsg-root");
  if (root) return root;

  root = document.createElement("div");
  root.id = "xsg-root";
  root.innerHTML = `
    <section class="xsg-card">
      <p class="xsg-kicker">Social Media Guard</p>
      <h1>Profile hidden</h1>
      <p>This X profile is intentionally unavailable.</p>
      <button type="button">Go back</button>
    </section>
  `;
  root.querySelector("button")?.addEventListener("click", () => history.back());
  document.body.append(root);
  return root;
}

function renderProfileBlocker() {
  const active = mode !== "off" && isBlockedProfile();
  document.documentElement.toggleAttribute("data-xsg-active", active);

  const root = ensureBlocker();
  if (root) root.hidden = !active;
}

function normalizeText(value) {
  return value?.replace(/\s+/g, " ").trim().toLowerCase() ?? "";
}

function exactHeading(text) {
  return [...document.querySelectorAll('[role="heading"], h1, h2, h3, h4, span')]
    .filter((element) => normalizeText(element.textContent) === text);
}

function nearestModule(heading) {
  let node = heading.parentElement;

  while (node && node !== document.body) {
    if (node.querySelectorAll?.('[data-testid="UserCell"]').length > 0) {
      return node;
    }
    if (node.matches?.("main, [role='main']")) break;
    node = node.parentElement;
  }

  return heading.closest('[data-testid="cellInnerDiv"]') ?? heading.parentElement;
}

const HIDDEN_NAV_LABELS = new Set([
  "home",
  "notifications",
  "follow",
  "grok",
]);

function hideSidebarItems() {
  document.querySelectorAll("[data-xsg-hidden-nav]").forEach((element) => {
    element.removeAttribute("data-xsg-hidden-nav");
  });

  if (mode === "off") return;

  const primaryNav = document.querySelector('nav[aria-label="Primary"], nav[role="navigation"]');
  if (!primaryNav) return;

  for (const item of primaryNav.querySelectorAll('a, [role="link"]')) {
    const label = normalizeText(item.getAttribute("aria-label") || item.textContent);
    if (HIDDEN_NAV_LABELS.has(label)) {
      item.setAttribute("data-xsg-hidden-nav", "");
    }
  }
}

function hideRecommendationSurfaces() {
  const activePage = isConnectPeople() || isOwnProfile();

  if (mode === "off" || !activePage) {
    document.querySelectorAll("[data-xsg-hidden]").forEach((element) => {
      element.removeAttribute("data-xsg-hidden");
    });
    return;
  }

  if (isConnectPeople()) {
    for (const cell of document.querySelectorAll('[data-testid="UserCell"]')) {
      (cell.closest('[data-testid="cellInnerDiv"]') ?? cell)
        .setAttribute("data-xsg-hidden", "");
    }

    for (const text of ["who to follow", "creators for you"]) {
      for (const heading of exactHeading(text)) {
        nearestModule(heading)?.setAttribute("data-xsg-hidden", "");
      }
    }
  }

  if (isOwnProfile()) {
    for (const heading of exactHeading("who to follow")) {
      const recommendationCell = heading.closest('[data-testid="cellInnerDiv"]');
      recommendationCell?.setAttribute("data-xsg-hidden", "");
    }
  }
}

function blockProfileNavigation(event) {
  if (mode === "off") return;

  const anchor = event.target.closest?.("a[href]");
  if (!anchor || !isBlockedProfile(anchor.href)) return;

  event.preventDefault();
  event.stopImmediatePropagation();
}

function applyXFilters() {
  if (redirectHomeToOwnProfile()) return;

  renderProfileBlocker();
  hideRecommendationSurfaces();
  hideSidebarItems();
}

document.addEventListener("click", blockProfileNavigation, true);
document.addEventListener("auxclick", blockProfileNavigation, true);

if (isBlockedProfile()) {
  document.documentElement.setAttribute("data-xsg-active", "");
}

chrome.storage.sync.get({ mode: DEFAULT_MODE }).then((settings) => {
  mode = settings.mode;
  applyXFilters();
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "sync" || !changes.mode) return;
  mode = changes.mode.newValue ?? DEFAULT_MODE;
  applyXFilters();
});

new MutationObserver(() => {
  if (mode === "off") return;
  hideRecommendationSurfaces();
  hideSidebarItems();
}).observe(document.documentElement, { childList: true, subtree: true });

setInterval(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href;
  }
  applyXFilters();
}, 300);

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", applyXFilters, { once: true });
} else {
  applyXFilters();
}
