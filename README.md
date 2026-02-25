# C++ Wrapper / Launcher

## Brief

Ultimately, this will be an executable, bundled with the game and all other necessary dependencies, that when run will allow the user to run the game without installing Python, C++, or any other dependencies.

---

## CRT (C Runtime) Toolchain

- **Python:** MSVC 
- **C++:** MSVC  
> **Note:** Development must be done using MSVC CRT.

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

- Dynamic filepathing to all bundled Python dependencies (Lib, DLLs, etc.).
- Bundle all C++ dependencies.  
- Filepathing to all bundled C++ dependencies.  
- Create executable.

---

## To-Do

- Integrate game into the `scripts` folder.  
- Integrate assets into the `scripts` folder.  
- All dependencies needed for Python are bundled.  

