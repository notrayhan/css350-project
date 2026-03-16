# Tetris 2

## Instructions

1. Download the whole folder
2. Unzip if necessary
3. Double click "launcher.exe" to run the game
4. Enjoy!

---

## CRT (C Runtime) Toolchain

- **Python:** MSVC 
- **C++:** MSVC  
> **Note:** Development must be done using MSVC CRT.

---

## Version
- Windows
- **Python 3.12** (full installation)
- **Pygame 2.6.1**

## File Structure

> **The wrapper code uses dynamic file pathing, so the file structure must not change.**

```
GameFolder/
│
├── launcher.exe
├── python312.dll
├── vcruntime140.dll
├── vcruntime140_1.dll
├── msvcp140.dll
│
└── python/
    ├── Lib/
    │   ├── encodings/
    │   ├── site-packages/
    │   │   └── pygame/
    │   └── ...
    ├── DLLs/
    ├── python.exe
    ├── python3.dll
    ├── game.py <- tetris
    └── assets for above
```
