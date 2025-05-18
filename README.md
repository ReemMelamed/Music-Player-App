# Music-Player-App

Welcome to your new favorite desktop music player!  
This app was built with Python, PyQt6, and VLC to give you a simple, beautiful, and modern way to play your local MP3 files.  
Enjoy features like shuffle, repeat (once or always), and a responsive interface.

---

## Features

- Play, pause, skip, and go back with easy controls
- Shuffle and repeat modes (none, once, always)
- Click or drag anywhere on the seek bar to jump in the song
- Clean, modern interface (supports Hebrew and English)
- Automatically loads all your songs from a folder
- 100% offline


---

## Requirements

- Python 3.8+
- [VLC Media Player](https://www.videolan.org/vlc/) (must be installed on your system)
- Python packages: `PyQt6`, `python-vlc`

---

## Installation

1. **Download or clone this repository**

2. **(Recommended) Create a virtual environment:**
   ```sh
   python -m venv venv
   ```
   Activate it:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Install the required Python packages:**
   ```sh
   pip install PyQt6 python-vlc
   ```

4. **Install VLC media player:**
   - Download and install from [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/)
   - Make sure VLC is in your system PATH, or that `libvlc` is accessible.

---


## How to use

1. **Add your MP3 files** to the `songs` folder in the project directory.  
   (Create the folder if it doesn't exist.)

2. **Run the application:**
   ```sh
   python main.py
   ```

3. **How to use:**
   - The app will display all MP3 files from the `songs` folder.
   - Double-click a song to play it.
   - Use the control buttons for play/pause, next, previous, shuffle, and repeat.
   - Click or drag on the seek bar to jump to any point in the song.
   - Shuffle and repeat buttons change color and icon to indicate their state.

---

## Project structure

```
music-player-app/
├── main.py         # Main application file
├── songs/          # Folder for your MP3 files
│   └── (your mp3 files)
├── README.md
```

---

## Notes and tips

- The app only plays `.mp3` files from the `songs` folder.
- You can add or remove songs at any time (restart the app to refresh the list).
- The interface is fully responsive and supports both Hebrew and English song names.
- Requires VLC to be installed for audio playback.

---

## Troubleshooting

- **VLC not found:**  
  Make sure VLC is installed and accessible. On Windows, the installer usually adds VLC to your PATH. If not, add the VLC installation directory (e.g., `C:\Program Files\VideoLAN\VLC`) to your PATH environment variable.
- **No songs appear:**  
  Make sure your MP3 files are in the `songs` folder and have the `.mp3` extension.
- **Other issues:**  
  Make sure all dependencies are installed and you are using a supported version of Python.

---

## License

This project is provided for personal use only.

---

## Contributing

Ideas, suggestions, and pull requests are always welcome!
