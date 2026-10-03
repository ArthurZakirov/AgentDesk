const DEFAULT_MODE = "strict";

async function loadMode() {
  const { mode = DEFAULT_MODE } = await chrome.storage.sync.get("mode");
  const input = document.querySelector(`input[value="${mode}"]`);
  if (input) input.checked = true;
}

async function saveMode(mode) {
  await chrome.storage.sync.set({ mode });
  const status = document.getElementById("status");
  status.textContent = "Saved";
  setTimeout(() => {
    status.textContent = "";
  }, 900);
}

document.addEventListener("change", (event) => {
  if (event.target.matches('input[name="mode"]')) {
    saveMode(event.target.value);
  }
});

loadMode();
