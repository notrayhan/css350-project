# QA Testing Results – Sparma Tetris

Below are the QA testing results based on the functional and non-functional requirements provided for the Sparma Tetris game. Testing was performed through active gameplay, store interaction, level progression, and system checks.

---

## Functional Requirements

### 8-Bit Pixel Aesthetic

**Status:** PASS  

**Test Performed:**  
I reviewed all menus, overlays, and gameplay screens.

**Result:**  
All UI elements follow the 8-bit SPARMA design consistently.

**Comment:**  
The design looks clean and matches the intended aesthetic.

---

### Keyboard Input Processing

**Status:** PASS  

**Test Performed:**  
I tested movement, rotation, drop, and pause multiple times.

**Result:**  
All keys responded correctly with no noticeable delay.

**Comment:**  
Controls feel smooth and responsive during gameplay.

---

### Collision Detection

**Status:** PASS  

**Test Performed:**  
I stacked blocks and tested rotation near walls and other pieces.

**Result:**  
Blocks lock properly without overlapping or clipping.

**Comment:**  
Collision detection works accurately.

---

### Sparma Currency Tracking & Saving

**Status:** PASS  

**Test Performed:**  
I cleared different colored lines and restarted the game.

**Result:**  
Currency increased correctly and saved between sessions.

**Comment:**  
No issues with saving or incorrect coin values.

---

### Game State Modifiers (Purchased Items)

**Status:** PASS  

**Test Performed:**  
I purchased an item and activated it during gameplay.

**Result:**  
The modifier applied correctly without causing errors.

**Comment:**  
Purchased items function as expected.

---

## Non-Functional Requirements

### Fixed Resolution & Pixel Scaling

**Status:** PASS  

**Test Performed:**  
I launched the game and observed resolution and scaling.

**Result:**  
The window initializes correctly and scaling keeps pixels sharp.

**Comment:**  
No distortion or blurriness observed.

---

### Sound Pre-Loading

**Status:** PASS  

**Test Performed:**  
I triggered sound effects immediately after launch.

**Result:**  
Sounds played instantly with no noticeable latency.

**Comment:**  
Audio performance is smooth.

---

### Relative Asset Paths

**Status:** PASS  

**Test Performed:**  
I moved the game folder to a new location and ran it.

**Result:**  
No missing assets or runtime errors occurred.

**Comment:**  
Asset paths are correctly configured.

---

### Input Response Under 100ms

**Status:** PASS  

**Test Performed:**  
I repeatedly tested movement and rotation inputs.

**Result:**  
Actions were reflected immediately on screen.

**Comment:**  
Gameplay feels responsive and stable.

---

## Overall QA Summary

After testing all listed requirements, the game functions properly. All core gameplay systems, UI components, store mechanics, and technical requirements operate as intended for this version of the project.