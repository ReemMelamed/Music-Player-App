# Music-Player-App

A modern, simple desktop music player built with Python, PyQt6, and VLC.  
Play your local MP3 files with a responsive interface, Hebrew support, search, shuffle, repeat, favorites, and keyboard shortcuts.

---

## Features

- 🎵 Play all your local `.mp3` files from the `songs` folder
- 🖥️ Modern, responsive interface with dark theme
- 🔎 Search bar for instant filtering of songs
- 🔂 Repeat modes: none, repeat one, repeat all
- 🔀 Shuffle mode
- ⭐ Mark and view favorite songs
- ⏩ Seek bar: click or drag to jump to any point in the song
- ⌨️ Rich keyboard shortcuts (see below)
- 🏷️ Hebrew and English support
- 🗂️ Remembers your favorites between sessions
- 🖱️ Double-click to play, click buttons for controls

---

## Requirements

- Python 3.8 or newer
- [VLC Media Player](https://www.videolan.org/vlc/) (must be installed on your system)
- Python packages: `PyQt6`, `python-vlc`

---

## Quick Start Guide

### 1. Download or Clone the Project

```sh
git clone https://github.com/yourusername/Music-Player-App-1.git
cd Music-Player-App-1
```

### 2. (Recommended) Create a Virtual Environment

```sh
python -m venv venv
```
Activate the environment:
- **Windows:**
  ```sh
  .\venv\Scripts\activate
  ```
- **Linux:**
  ```sh
  source venv/bin/activate
  ```

### 3. Install Python Dependencies

```sh
pip install PyQt6 python-vlc
```

### 4. Install VLC Media Player

- Download and install from [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/)
- Make sure VLC is accessible from your system (usually automatic).

### 5. Add Your Music

- Place your `.mp3` files in the `songs` folder inside the project directory.
- If the folder does not exist, create it manually.

### 6. Run the Music Player

```sh
python main.py
```

---

## How to Use

- All `.mp3` files in the `songs` folder will appear in the song list.
- Double-click a song to play it.
- Use the control buttons for play/pause, next, previous, repeat, shuffle, and theme.
- Click or drag on the seek bar to jump to any point in the song.
- Use the search bar to filter songs by name.
- Mark songs as favorites with the ⭐ button and view only your favorites.
- The interface supports both Hebrew and English.

---

## Keyboard Shortcuts

| Action                | Shortcut         |
|-----------------------|-----------------|
| Play/Pause            | Space / S       |
| Next Song             | → / D           |
| Previous Song         | ← / A           |
| Repeat Mode           | ↑ / W           |
| Shuffle Mode          | ↓               |
| Focus Search Bar      | F               |
| Show Shortcuts Help   | H               |

---

## Project Structure

```
Music-Player-App-1/
├── main.py         # Main application file
├── songs/          # Place your MP3 files here
│   └── (your mp3 files)
├── README.md
```

---

## Troubleshooting

- **No songs appear:**  
  Make sure your `.mp3` files are in the `songs` folder and have the correct extension.

- **VLC not found:**  
  Ensure VLC is installed and accessible. On Windows, the installer usually adds VLC to your PATH automatically.

- **Other issues:**  
  Make sure all dependencies are installed and you are using a supported Python version.

---

## Running on Linux

1. **Install Python 3 and pip** (if not already installed):
   ```sh
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install VLC:**
   ```sh
   sudo apt install vlc
   ```

3. **Install Python dependencies:**
   ```sh
   pip3 install PyQt6 python-vlc
   ```

4. **Run the app:**
   ```sh
   python3 main.py
   ```

### Creating a Desktop Icon (Linux)

To create a desktop shortcut (icon) for the app:

1. Create a file named `MusicPlayer.desktop` on your desktop:
   ```sh
   nano ~/Desktop/MusicPlayer.desktop
   ```
2. Paste the following content (update the paths if needed):
   ```
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=Music Player
   Exec=python3 /home/youruser/Music/Music-Player-App-1/main.py
   Icon=audio-x-generic
   Terminal=false
   ```
3. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
4. Make it executable:
   ```sh
   chmod +x ~/Desktop/MusicPlayer.desktop
   ```
5. Double-click the icon to launch the app.

---

## Creating a Desktop Shortcut (Windows)

To create a desktop shortcut (icon) that launches the app:

1. Install the required package:
   ```sh
   pip install pywin32
   ```
2. Save the following script as `create_shortcut.py` in your project folder:
   ```python
   import os
   import sys
   from win32com.client import Dispatch

   def create_shortcut():
       desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
       shortcut_path = os.path.join(desktop, "Music Player.lnk")
       python_path = sys.executable
       script_path = r"c:\ . . . \Music-Player-App-1\main.py"

       shell = Dispatch('WScript.Shell')
       shortcut = shell.CreateShortCut(shortcut_path)
       shortcut.Targetpath = python_path
       shortcut.Arguments = f'"{script_path}"'
       shortcut.WorkingDirectory = os.path.dirname(script_path)
       shortcut.IconLocation = python_path
       shortcut.save()
       print("Shortcut created on Desktop!")

   if __name__ == "__main__":
       create_shortcut()
   ```
3. Run the script:
   ```sh
   python create_shortcut.py
   ```
4. A "Music Player" icon will appear on your desktop. Double-click to launch the app.

---

## License

This project is for personal use only.

---

## Contributing

Ideas, suggestions, and pull requests are welcome!