
# Prompt Security Chrome Extension

This project consists of a **Chrome extension** and a **Python backend server** that inspects PDF uploads on ChatGPT only for secrets using Prompt Security's API.

## Project Structure
- **chrome-extension/** – Chrome extension code (manifest, background script, content script, popup).
- **server/** – Python backend server for handling PDF inspection.
- **server/app/** – Contains routes, services, configuration, and PDF inspection logic.

## Setup & Installation

### 1. Server Setup
1. Navigate to the `server` folder:
   ```bash
   cd server
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python run.py
   ```
   The server will start locally (default: `http://127.0.0.1:5001`).

### 2. Chrome Extension Setup
1. Open **Google Chrome** and go to `chrome://extensions/`.
2. Enable **Developer Mode** (toggle on top-right).
3. Click **Load unpacked** and select the `chrome-extension` folder.
4. The extension will now appear in your browser.

### 3. Usage
- Drag & drop or upload a **PDF** in a supported AI chat interface.
- The extension captures the file and sends it to the server for inspection.
- If secrets are detected, an **alert** will be displayed.

## Logging
- Logs are handled by `server/app/logger.py`. Check log files for detailed runtime information.

## Notes
- This project is for internal use and testing.
- Ensure the backend server is running before using the extension.
- This Extension suits ChatGPT only but can be used for all AI chats with proper adaption.
---
