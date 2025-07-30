console.log("background.js loaded");

chrome.runtime.onInstalled.addListener(() => {
  console.log("PDF Inspector installed");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || message.type !== 'pdf-uploaded') {
    sendResponse({ success: false, error: "Invalid message type" });
    return false;
  }

  console.log("Received PDF for:", message.filename);

  const handleUpload = async () => {
    if (!message.base64) throw new Error("No file data provided");

    const binary = atob(message.base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    const fileBlob = new Blob([bytes], { type: 'application/pdf' });

    const form = new FormData();
    form.append('file', fileBlob, message.filename || 'upload.pdf');

    const res = await fetch('http://localhost:5001/inspect', {
      method: 'POST',
      body: form,
      keepalive: true
    });

    if (!res.ok) throw new Error(`Server responded ${res.status} ${res.statusText}`);
    const data = await res.json();
    console.log("✅ Server response:", data);

    if (data.found_secrets) {
        chrome.tabs.sendMessage(sender.tab.id, {
    type: "show-popup",
    filename: message.filename,
    secrets: data.found_secrets
  });
    }

    return { success: true, data };
  };

  handleUpload()
    .then(result => sendResponse(result))
    .catch(err => {
      console.error("Inspection error:", err.message);
      sendResponse({ success: false, error: err.message });
    });

  return true;
});
