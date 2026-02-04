Functional Requirements:

•	The application’s user interface shall adhere to an 8-bit pixel aesthetic for all menus and in-game overlays, matching the SPARMA design.

•	The system shall process discrete keyboard input events to map specific keys to game actions input delay.

•	The system shall implement precise collision detection between the active falling block and the static block stack to handle locking mechanics and line clearing.

•	The system shall track a Sparma Currency balance that goes up in value upon successful line clears and automatically writes this data to a local file to save progress between sessions.

•	The system shall execute game state modifiers when a user activates a purchased item during the playing state.

Non-Functional Requirements:

•	The game window shall initialize at a fixed resolution with scaling enabled to preserve pixel-art integrity on modern high-resolution displays.

•	Sound effects must be pre-loaded into memory upon application launch to ensure no latency during real time playing.

•	All external assets (images, audio, etc.) must be embedded within the relative path of the executable to prevent runtime errors when the application is moved.

•	The system must process and visually reflect user input within 100 milliseconds to ensure the gameplay feels responsive.

