# C++ Wrapper / Launcher

## Brief

Downloading the entire project folder and running launcher.exe allows the user to run tetris without installing Python, C++, or any other dependencies.

---

## CRT (C Runtime) Toolchain

- **Python:** MSVC 
- **C++:** MSVC  
> **Note:** Development must be done using MSVC CRT.

---

## Python version
- **Python 3.12** (full installation)

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

---

## Complete

- Dynamic filepathing to all bundled Python dependencies (Lib, DLLs, etc.).
- Bundle all C++ dependencies.  
- Filepathing to all bundled C++ dependencies.  
- Create executable.
- All dependencies needed for Python are bundled. (pygame installed)

---

## To-Do

- Integrate game into the `python` folder.  
- Integrate assets into the `python` folder.  