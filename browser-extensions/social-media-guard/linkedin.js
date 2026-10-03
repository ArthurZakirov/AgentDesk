const DEFAULT_MODE = "strict";
const PROFILE_PATH = /^\/in\/[^/]+\/?/;
const MY_NETWORK_PATH = /^\/mynetwork(?:\/|$)/;
const ALLOWED_PROFILE_PATHS = new Set(["/in/arthurzakirov"]);

let mode = DEFAULT_MODE;
let lastUrl = location.href;

function parseLinkedInUrl(value = location.href) {
  try {
    const url = new URL(value, location.origin);
    return url.hostname.endsWith("linkedin.com") ? url : null;
  } catch {
    return null;
  }
}

function normalizeProfilePath(pathname) {
  return pathname.replace(/\/+$/, "").toLowerCase();
}

function isAllowedProfileUrl(value = location.href) {
  const url = parseLinkedInUrl(value);
  return url ? ALLOWED_PROFILE_PATHS.has(normalizeProfilePath(url.pathname)) : false;
}

function isProfileUrl(value = location.href) {
  const url = parseLinkedInUrl(value);
  return Boolean(url && PROFILE_PATH.test(url.pathname));
}

function isMyNetworkUrl(value = location.href) {
  const url = parseLinkedInUrl(value);
  return Boolean(url && MY_NETWORK_PATH.test(url.pathname));
}

function isFeedUrl(value = location.href) {
  const url = parseLinkedInUrl(value);
  return Boolean(url && (/^\/feed\/?$/.test(url.pathname) || url.pathname === "/"));
}

function redirectFeedToOwnProfile() {
  if (mode === "off" || !isFeedUrl()) return false;

  location.replace("https://www.linkedin.com/in/arthurzakirov/");
  return true;
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

const HIDDEN_CARD_TITLES = new Set([
  "today’s puzzles",
  "today's puzzles",
  "add to your feed",
]);

function nearestSidebarCard(element, sidebar) {
  let node = element;

  while (node && node !== sidebar) {
    if (node.classList?.contains("artdeco-card")) return node;
    if (node.parentElement === sidebar) return node;
    node = node.parentElement;
  }

  return null;
}

function hideDistractingCards() {
  if (!parseLinkedInUrl() || mode === "off") {
    document.querySelectorAll("[data-lpg-hidden-card]").forEach((element) => {
      element.removeAttribute("data-lpg-hidden-card");
    });
    return;
  }

  const sidebars = document.querySelectorAll("aside, .scaffold-layout__aside");
  for (const sidebar of sidebars) {
    for (const candidate of sidebar.querySelectorAll("*")) {
      const title = candidate.textContent?.trim().toLowerCase();
      if (!HIDDEN_CARD_TITLES.has(title)) continue;

      nearestSidebarCard(candidate, sidebar)
        ?.setAttribute("data-lpg-hidden-card", "");
    }
  }
}

function hideOwnProfileSidebar() {
  if (mode === "off" || !isAllowedProfileUrl()) {
    document.querySelectorAll("[data-lpg-hidden-sidebar]").forEach((element) => {
      element.removeAttribute("data-lpg-hidden-sidebar");
    });
    return;
  }

  const sidebar = document.querySelector("aside, .scaffold-layout__aside");
  sidebar?.setAttribute("data-lpg-hidden-sidebar", "");
}

const HIDDEN_NAV_PATHS = [
  /^\/$/,
  /^\/feed\/?$/,
  /^\/mynetwork(?:\/|$)/,
  /^\/jobs(?:\/|$)/,
  /^\/messaging(?:\/|$)/,
  /^\/notifications(?:\/|$)/,
];

const HIDDEN_NAV_LABELS = new Set([
  "home",
  "my network",
  "jobs",
  "messaging",
  "notifications",
]);

function hidePrimaryNavigationItems() {
  document.querySelectorAll("[data-lpg-hidden-nav]").forEach((element) => {
    element.removeAttribute("data-lpg-hidden-nav");
  });

  if (mode === "off") return;

  for (const candidate of document.querySelectorAll('header a, header button, nav a, nav button')) {
    const label = candidate.textContent?.trim().toLowerCase()
      || candidate.getAttribute("aria-label")?.trim().toLowerCase()
      || "";
    const url = candidate.href ? parseLinkedInUrl(candidate.href) : null;
    const hiddenByPath = Boolean(
      url && HIDDEN_NAV_PATHS.some((pattern) => pattern.test(url.pathname))
    );
    const hiddenByLabel = HIDDEN_NAV_LABELS.has(label);

    if (!hiddenByPath && !hiddenByLabel) continue;

    const navItem = candidate.closest("li") || candidate;
    navItem.setAttribute("data-lpg-hidden-nav", "");
  }
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
  const myNetwork = isMyNetworkUrl();
  const active = mode !== "off"
    && ((profile && !isAllowedProfileUrl()) || myNetwork);

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

  if (myNetwork || mode === "strict") {
    card.innerHTML = `
      <p class="lpg-kicker">LinkedIn Profile Guard</p>
      <h1>${myNetwork ? "My Network hidden" : "Profile hidden"}</h1>
      <p>${myNetwork
        ? "LinkedIn My Network is intentionally unavailable."
        : "This member profile is intentionally unavailable in Strict mode."}</p>
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

function blockRestrictedNavigation(event) {
  if (mode === "off") return;

  const anchor = event.target.closest?.("a[href]");
  if (!anchor) return;

  if (isFeedUrl(anchor.href)) {
    event.preventDefault();
    event.stopImmediatePropagation();
    location.assign("https://www.linkedin.com/in/arthurzakirov/");
    return;
  }

  const blockedProfile = mode === "strict"
    && isProfileUrl(anchor.href)
    && !isAllowedProfileUrl(anchor.href);
  const blockedNetwork = isMyNetworkUrl(anchor.href);

  if (!blockedProfile && !blockedNetwork) return;

  event.preventDefault();
  event.stopImmediatePropagation();
  showBlockedClick();
}

document.addEventListener("click", blockRestrictedNavigation, true);
document.addEventListener("auxclick", blockRestrictedNavigation, true);

if ((isProfileUrl() && !isAllowedProfileUrl()) || isMyNetworkUrl()) {
  document.documentElement.setAttribute("data-lpg-active", "");
  document.documentElement.dataset.lpgMode = DEFAULT_MODE;
}

chrome.storage.sync.get({ mode: DEFAULT_MODE }).then((settings) => {
  mode = settings.mode;
  applyPageFilters();
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "sync" || !changes.mode) return;
  mode = changes.mode.newValue ?? DEFAULT_MODE;
  applyPageFilters();
});

const observer = new MutationObserver((mutations) => {
  if (mode !== "off") {
    hideDistractingCards();
    hideOwnProfileSidebar();
    hidePrimaryNavigationItems();
  }

  if ((!isProfileUrl() && !isMyNetworkUrl()) || mode === "off") return;

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
  applyPageFilters();
}, 250);

function applyPageFilters() {
  if (redirectFeedToOwnProfile()) return;

  renderProfileGuard();
  hideDistractingCards();
  hideOwnProfileSidebar();
  hidePrimaryNavigationItems();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", applyPageFilters, { once: true });
} else {
  applyPageFilters();
}
