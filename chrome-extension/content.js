console.log('content.js loaded');

function handleFile(file) {
  if (!file || file.type !== 'application/pdf') return;
  console.log('PDF selected:', file.name);

  const reader = new FileReader();
  reader.onload = () => {
    const dataUrl = reader.result;
    const base64 = dataUrl.split(',')[1];

    chrome.runtime.sendMessage(
      { type: 'pdf-uploaded', filename: file.name, base64 },
      response => {
        if (chrome.runtime.lastError) {
          console.error('sendMessage error:', chrome.runtime.lastError.message);
        } else {
          console.log('Background response:', response);
        }
      }
    );
  };
  reader.onerror = () => console.error('FileReader error for', file.name);
  reader.readAsDataURL(file);
}

function bindChatArea() {
  const container = document.querySelector('main') || document.body;
  if (!container) return;

  container.addEventListener('drop', e => {
    e.preventDefault();
    if (e.dataTransfer?.files.length) {
      Array.from(e.dataTransfer.files).forEach(handleFile);
    }
  }, true);

  container.addEventListener('change', e => {
    const input = e.target;
    if (input.type === 'file' && input.files.length) {
      Array.from(input.files).forEach(handleFile);
    }
  }, true);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bindChatArea);
} else {
  bindChatArea();
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "show-popup") {
    showPopup(msg.filename);
  }
});

function showPopup(filename) {
  fetch(chrome.runtime.getURL("popup/popup.html"))
    .then(r => r.text())
    .then(html => {
      const container = document.createElement("div");
      container.innerHTML = html.trim();
      document.body.appendChild(container);

      const textEl = container.querySelector("#popup-text");
      if (textEl) {
        textEl.textContent = `The file "${filename}" contains sensitive data.`;
      }

      const closeBtn = container.querySelector("#popup-close");
      if (closeBtn) {
        closeBtn.addEventListener("click", () => container.remove());
      }
    })
    .catch(err => console.error("Failed to load popup:", err));
}

