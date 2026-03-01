<div align="center">

<img src="logo.png" width="80" />

# WhatsApp Bulk Messenger

**Automate sending WhatsApp messages to hundreds of contacts in minutes.**

Made by **Harsh Gupta**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?style=flat-square&logo=selenium)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

</div>

---

## What It Does

WhatsApp Bulk Messenger opens WhatsApp Web in Chrome and automatically sends a pre-written message to every phone number in your list. It includes a modern dark-themed GUI for easy use.

---

## Prerequisites

- **Google Chrome** installed on your machine
- **Python 3.12+** (only needed if running from source)
- An active WhatsApp account on your phone

> ChromeDriver is downloaded **automatically** — you do not need to install it manually.

---

## Option A — Run the EXE (Recommended, No Python needed)

1. Go to the `dist/` folder and copy **`WA Bulk Messenger.exe`** anywhere on your PC.
2. Place `message.txt` and `numbers.txt` in the **same folder** as the exe.
3. Double-click the exe to launch.
4. Follow the [Usage Steps](#usage-steps) below.

---

## Option B — Run from Source

### 1. Install Python

Download and install Python 3.12+ from https://python.org  
Make sure to check **"Add Python to PATH"** during installation.

### 2. Clone / Download the project

```bash
git clone https://github.com/harshgupta/whatsapp-bulk-messenger.git
cd whatsapp-bulk-messenger
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the GUI

```bash
python ui.py
```

---

## Usage Steps

1. **Enter your message**  
   Type directly in the **Message** panel, or click **📂 Load** to load from a `.txt` file.

2. **Enter phone numbers**  
   Paste numbers in the **Phone Numbers** panel — one per line.  
   Always include the country code:
   ```
   +919821185590
   +14155552671
   +447911123456
   ```

3. **Save (optional)**  
   Click **💾 Save** to write your message and numbers to `message.txt` / `numbers.txt` so they auto-load next time.

4. **Click 🚀 Send Messages**  
   Confirm the prompt — Chrome will open and navigate to WhatsApp Web.

5. **Scan the QR code**  
   Open WhatsApp on your phone → **Linked Devices** → **Link a Device** → scan the QR code shown in Chrome.

6. **Click ✅ I'm Logged In – Go!**  
   Once your chats are visible in Chrome, click this button in the app.

7. **Sit back and relax!**  
   Messages are sent automatically. Progress is shown in the status bar.

---

## File Structure

```
WA Bulk Messenger.exe   ← main app (or run ui.py from source)
message.txt             ← your message (auto-loaded on startup)
numbers.txt             ← phone numbers, one per line (auto-loaded on startup)
```

---

## Building the EXE yourself

```bash
pip install pyinstaller pillow
python build.py
```

Output will be in the `dist/` folder.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Chrome doesn't open | Make sure Google Chrome is installed |
| QR code not showing | Check your internet connection |
| Message not sending | Dismiss any WhatsApp pop-ups in Chrome manually |
| Number fails | Ensure country code is included (e.g. `+91`, `+1`) |
| App slow to start (exe) | Normal — exe unpacks itself on first run |
| ChromeDriver error | Ensure Chrome is up to date; driver is auto-matched |

---

## Notes

- WhatsApp may rate-limit bulk sending — a short delay is built in between messages.
- This tool uses **WhatsApp Web** and requires your phone to stay connected.
- Do not close your phone's WhatsApp while messages are being sent.

---

<div align="center">
Made with ❤️ by <strong>Harsh Gupta</strong>
</div>
