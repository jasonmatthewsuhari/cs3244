# 🧠 WhatsApp Web Custom Emoji Extension

This Chrome extension replaces the default emoji reaction bar (the 6 emojis + ➕ icon) on WhatsApp Web with **model-predicted emojis**. 

It does not support actually sending the emoji as this is highly limited by WhatsApp.

---

## 🔧 Setup Instructions

1. **Clone or download** this repository (just follow the main README instructiins)

2. Inside the project directory, ensure you have the following files:
   - `manifest.json`
   - `content.js`
   - Any other required assets (e.g. icons)

3. Open **Google Chrome** and navigate to:
```
chrome://extensions/
```

4. Enable **Developer Mode** (top right toggle).

5. Click **"Load unpacked"** and select the folder containing your extension files.

6. Go to [https://web.whatsapp.com](https://web.whatsapp.com) and refresh the page.

---

## 🧪 How It Works

- The extension listens for the emoji reaction bar (the dock with 6 emojis).
- Once it appears, it replaces the default emojis with custom ones (e.g. 🧠, 🌶️, 🥵).
- Clicking one sends a **mapped real reaction** (e.g. 🧠 → 👍) that is synced to both chat participants.

> ⚠️ WhatsApp only supports a limited set of reaction emojis. Custom emojis are mapped to the nearest allowed ones.

---

