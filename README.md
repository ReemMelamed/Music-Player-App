# Music-Player-App 🎵

A modern, simple desktop music player built with Python, PyQt6, and VLC.  
Play your local MP3 files with a responsive interface, Hebrew support, search, shuffle, repeat, and keyboard shortcuts.

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
- **Mac/Linux:**
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
- Use the control buttons for play/pause, next, previous, repeat, and shuffle.
- Click or drag on the seek bar to jump to any point in the song.
- Use the search bar to filter songs by name.
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

## License

This project is for personal use only.

---

## Contributing

Ideas, suggestions, and pull requests are welcome!