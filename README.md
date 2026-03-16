# Tetris 2

## Instructions

1. Download full project folder
2. Run "launcher"
3. Enjoy the game!

---

## Version
- **Python 3.12.7** (full installation)
- **Pygame 2.6.1**

## File Structure

> **The launcher code uses dynamic file pathing, so the file structure must not change.**

```
GameFolder/
│
├── launcher  <--- Run this file to start the game
├── main.cpp 
│
└── python/
    ├── Lib/
    │   ├── encodings/
    │   ├── site-packages/
    │   │   └── pygame/
    │   └── ...
    ├── game.py <--- tetris
    ├── ...     <--- other game files *.py
    └── assets
```
## Warnings

- executable launcher is an "unsigned binary" meaning it can trigger "unsafe developer" flags / permission checks
- launcher may need "chmod permissions", in terminal: chmod +x launcher
