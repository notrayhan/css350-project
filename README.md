# C++ Wrapper / Launcher

## Brief

Ultimately, this will be an executable, bundled with the game and all other necessary dependencies, that when run will allow the user to run the game without installing Python, C++, or any other dependencies.

---

## CRT (C Runtime) Toolchain

- **Python:** UTRVC  
- **C++:** UTRVC  
> **Note:** Development must be done using UTRVC CRT.

---

## File Structure

> **The wrapper code uses dynamic file pathing, so the file structure must not change.**

```
GameFolder/
│
├── launcher.exe
├── python314.dll
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
    └── your_game.py
```

---

## Complete

- All dependencies needed for Python are bundled.  
- Dynamic filepathing to all bundled Python dependencies (Lib, DLLs, etc.).

---

## To-Do

- Bundle all C++ dependencies.  
- Filepathing to all bundled C++ dependencies.  
- Integrate game into the `scripts` folder.  
- Integrate assets into the `scripts` folder.  
- Create executable.
