# WhatsApp Bulk Messenger - UI Guide

## Overview

A modern tkinter-based GUI for the WhatsApp Bulk Messenger tool. This provides a user-friendly interface to manage messages and phone numbers, and send bulk WhatsApp messages.

## Features

✅ **Intuitive GUI** - Clean, modern interface with color-coded sections
✅ **Message Editor** - Built-in text editor for composing/editing messages
✅ **Number Management** - Easy input and management of phone numbers
✅ **File Operations** - Load/save messages and numbers from/to files
✅ **Live Counter** - See message length and number count in real-time
✅ **Threading** - Non-blocking UI during message sending
✅ **Status Display** - Real-time status updates during the sending process

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Note: tkinter comes built-in with Python, no additional installation needed

2. **Ensure Chrome is installed** on your system

## Running the UI

Simply run:
```bash
python ui.py
```

The application window will open showing:

### Top Section - Message Editor
- Enter or paste your message here
- Click "Load from File" to load from a custom file
- Click "Clear" to empty the message
- Character count updates in real-time

### Middle Section - Phone Numbers
- Enter phone numbers (one per line)
- Supported formats: +1234567890, 1234567890, national format
- Click "Load from File" to load from a file
- Click "Clear" to empty the list
- Number count updates in real-time

### Info Bar
- Shows message length and number count
- Updates automatically as you type

### Action Buttons
- **🚀 Start Sending** - Begin the bulk messaging process
- **💾 Save to Files** - Save current message and numbers to message.txt and numbers.txt
- **❌ Exit** - Close the application

## Usage Workflow

1. **Enter your message** in the message box or click "Load from File"
2. **Enter phone numbers** in the numbers box (one per line) or click "Load from File"
3. **Review** the information displayed in the info bar
4. **(Optional) Click "Save to Files"** to save before sending
5. **Click "Start Sending"** to begin
6. A confirmation dialog will appear - click Yes to proceed
7. Chrome will open - **scan the QR code on your phone** to log into WhatsApp Web
8. Once logged in, press ENTER in the console that appears
9. Messages will be sent automatically to all numbers
10. A success message will appear when complete

## File Formats

### Message File
- Plain text file containing your message
- Supports line breaks and special characters
- File: `message.txt`

### Numbers File
- One phone number per line
- Numbers should include country code
- Examples:
  ```
  +1234567890
  +91987654321
  +441234567890
  ```
- File: `numbers.txt`

## File Operations

### Loading Files
- Click "Load from File" button in either section
- Browse and select a .txt file
- Content will be loaded into the text area
- Status bar shows which file was loaded

### Saving Files
- Click "💾 Save to Files" button
- Current message and numbers will be saved to:
  - `message.txt` - your message
  - `numbers.txt` - your phone numbers
- You'll see a success confirmation

## Important Notes

⚠️ **Before Sending Messages:**
- Make sure you have stable internet connection
- WhatsApp Web must be accessible on your device
- Your phone must be connected and WhatsApp must be running
- You'll need to scan QR code when Chrome opens

⚠️ **Phone Number Format:**
- Include country code (e.g., +1 for USA, +91 for India)
- WhatsApp will handle number validation
- Invalid numbers will fail with appropriate error messages

⚠️ **Message Limits:**
- WhatsApp has rate limits - very long lists may take time
- Recommended: 10-15 second delay between messages (built-in)
- Messages respect WhatsApp's character limits

## Keyboard Shortcuts

- `Ctrl+A` - Select all text in focused box
- `Ctrl+C` - Copy selected text
- `Ctrl+V` - Paste text
- `Ctrl+Z` - Undo changes

## Troubleshooting

### Chrome won't open
- Ensure Chrome is installed on your system
- Try restarting the application

### Can't log into WhatsApp Web
- Check your internet connection
- Make sure your phone has WhatsApp and is connected
- Try opening https://web.whatsapp.com directly in Chrome

### Messages not sending
- Verify phone numbers are in correct format with country code
- Check internet connection stability
- Ensure WhatsApp Web is fully loaded in Chrome
- Dismiss any pop-up alerts that appear

### Application freezes
- This shouldn't happen with UI threading
- If it does, restart and report the issue

## Technical Details

### Code Structure
- `ui.py` - Main GUI application (tkinter)
- `automation_core.py` - Core automation functions (Selenium)
- `automator.py` - Command-line interface (uses automation_core)

### Dependencies
- `selenium` - Web browser automation
- `webdriver-manager` - Chrome driver management
- `tkinter` - GUI (built-in with Python)

### Threading
Messages are sent in a background thread to keep UI responsive. You can monitor progress in the status bar.

## Support

For issues, feature requests, or improvements, please check the original repository:
- GitHub: www.github.com/harshgupta

---

**Made with ❤️ for WhatsApp automation**
