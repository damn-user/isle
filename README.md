# Dynamic Island for Windows (PyQt6) 🏝️

**An interactive "Dynamic Island" styled control panel that sits at the top of your screen, providing quick access to a media player, QR code generator, and clipboard history.**

## ⚠️ Project Under Active Development

> **[📥 Download Latest Version for Windows](https://github.com/damn-user/isle/releases)**

*Note: The project is under active development. Windows Defender may show a warning on the first launch because the executable is not digitally signed yet. Click "More info" -> "Run anyway" to start. For convenience, add "isle" to your startup programs.*

**Important Notice:** This project is currently in its **early (MVP) development phase**. 
* The code presented here shows only a **fraction of the planned features** and architectural goals.
* It is not a finished product — many modules, interactions, and advanced animations are yet to be integrated or are subject to significant rewrites.
* You may encounter temporary UI constraints, bugs, or breaking changes as development progresses.

## 🚀 Current MVP Features

* **🏝️ Animated Interface:** A compact widget centered at the top of the screen that smoothly expands upon clicking.
* **🎵 Local Music Player:** Scan any local directory for tracks, switch between songs, view file names, and control playback (play/pause/stop).
* **📱 QR Code Generator:** Instantly convert any text input into a QR code, rendered directly in a separate pop-up window.
* **📋 Clipboard History:** Keep track of and easily switch between your two most recently copied text fragments.

## 🔧 Tech Stack & Dependencies

* **Language:** Python 3.10+
* **GUI Framework:** PyQt6 (`QtWidgets`, `QtCore`, `QtGui`, `QtMultimedia`)
* **Libraries:** qrcode

## 💻 Installation & Launch

### 1. Clone the repository
```bash
git clone https://github.comhttps://github.com/damn-user/isle
cd your_repository
```

### 2. Install dependencies
Install the required packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python main.py
```

*Note: Ensure your operating system has the necessary audio codecs installed for PyQt6's `QMediaPlayer` to play your local media files properly.*

