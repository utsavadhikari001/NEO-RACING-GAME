# 🏎️ NEO RACING  NIGHT RUN

> **A neon-soaked pseudo-3D racing game built entirely in Python and Pygame.**

**NEO RACING // NIGHT RUN** is a fast-paced arcade racing game inspired by futuristic night highways, cyberpunk cities, and classic pseudo-3D racing games.

Race through neon-lit environments, manage your speed around winding roads, collect Nitro cells, use boost, avoid rival cars, and chase your best lap times across multiple futuristic routes.

The game uses a **software-rendered pseudo-3D road system** rather than OpenGL or an external 3D engine.

---

## ✨ Features

* 🏁 **Pseudo-3D racing**
* 🌃 Neon/cyberpunk night aesthetic
* 🛣️ Curving perspective-based roads
* 🚗 **6 selectable cars**
* 🌆 **5 different racing routes**
* 🤖 **3 AI rivals**
* ⚡ Nitro boost system
* 🔋 Collectible Nitro cells
* 💥 Rival collision system
* 🔥 Animated exhaust effects
* 🎵 Menu and race music
* 🔊 Engine, boost, drift, crash, countdown and finish sounds
* 🏆 Best-time saving
* 💾 Persistent car and track selection
* ⚙️ Sound and music settings
* 🎮 Keyboard and mouse menu controls
* 🖥️ Runs without OpenGL
* 🌐 No internet connection required

---

# 🚘 Cars

Choose between six different cars, each with its own performance characteristics.

| Car         | Top Speed | Acceleration | Handling |
| ----------- | --------: | -----------: | -------: |
| **Neo**     |       380 |          420 |      4.1 |
| **Volt**    |       355 |          510 |      4.0 |
| **Phantom** |       425 |          375 |      3.5 |
| **Vector**  |       370 |          410 |      5.1 |
| **Titan**   |       335 |          445 |      3.7 |
| **Apex**    |       400 |          455 |      4.4 |

Different cars are designed around different driving characteristics:

* **Neo** — balanced
* **Volt** — acceleration focused
* **Phantom** — high top speed
* **Vector** — high handling
* **Titan** — acceleration-oriented heavier car
* **Apex** — balanced performance with strong acceleration

---

# 🌃 Tracks

Race across five futuristic routes:

### 🌆 Neon City

A neon-lit urban route surrounded by a cyberpunk skyline.

### 🛣️ Midnight Highway

A high-speed highway built for long, fast runs.

### ⚓ Cyber Port

A futuristic industrial route with a cyberpunk port atmosphere.

### ☁️ Skyway

A high-altitude futuristic racing route.

### 🔷 Nexus

A mysterious neon route designed around the game's futuristic aesthetic.

Each track has its own road width, visual environment, and curve variation.

---

# ⚡ Nitro System

Nitro is one of the main gameplay mechanics.

Hold:

**Shift + W**

to activate Nitro while accelerating.

Nitro:

* Increases maximum speed
* Increases acceleration
* Consumes the boost meter
* Automatically regenerates when not being used

You can also collect **Nitro cells** placed along the road.

Collecting one restores:

**+42 Nitro**

This encourages players to choose racing lines instead of simply staying in the center of the road.

---

# 🏁 Racing System

Each race consists of:

**3 laps**

with a total race distance of approximately:

**15,600 distance units**

The player races against three AI opponents.

The rivals have different:

* Starting positions
* Lanes
* Racing speeds
* Cars

Colliding with a rival temporarily reduces the player's speed.

---

# 🎮 Controls

| Action      | Keyboard            |
| ----------- | ------------------- |
| Accelerate  | `W` / `↑`           |
| Brake       | `S` / `↓` / `Space` |
| Steer Left  | `A` / `←`           |
| Steer Right | `D` / `→`           |
| Nitro       | `Shift`             |
| Pause       | `Esc`               |
| Restart     | `R`                 |

### Menu

* `W` / `↑` — Move up
* `S` / `↓` — Move down
* `Enter` / `Space` — Select
* `←` / `→` — Change track/car where applicable
* `Esc` — Return

Mouse controls are also supported in the menus and garage.

---

# 🖥️ Requirements

* **Python 3.10+**
* **Pygame 2.5+**
* Windows, Linux, or another Python-compatible desktop environment

The game does **not** require:

* OpenGL
* Internet access
* A game engine
* External servers

---

# 📦 Installation

Clone or download the project and enter the game directory:

```bash
cd NEO-RACING
```

Install the required dependency:

```bash
python -m pip install -r requirements.txt
```

Start the game:

```bash
python main.py
```

---

# 🗂️ Project Structure

```text
NEO-RACING/
│
├── main.py
├── game.py
│
├── physics.py
├── car.py
├── player.py
├── ai.py
├── track.py
├── camera.py
├── collision.py
├── particles.py
├── road3d.py
│
├── audio.py
├── ui.py
├── menu.py
├── garage.py
├── settings.py
├── save.py
│
├── cars.json
├── tracks.json
├── settings.json
├── save.json
├── requirements.txt
│
├── test_game.py
├── art_cars.py
│
├── car_neo.png
├── car_volt.png
├── car_phantom.png
├── car_vector.png
├── car_titan.png
├── car_apex.png
│
├── track_neon_city.png
├── track_highway.png
├── track_cyber_port.png
├── track_skyway.png
├── track_nexus.png
│
├── logo.png
├── icon.png
├── city_backdrop.png
├── city_sky.png
│
├── engine.wav
├── boost.wav
├── drift.wav
├── crash.wav
├── countdown.wav
├── finish.wav
├── menu_music.ogg
└── race_music.ogg
```

---

# 🧠 How It Works

The main game loop is handled by `game.py`.

The pseudo-3D road is generated by:

```text
road3d.py
```

Rather than using a traditional 3D engine, the game projects road positions onto the screen using perspective calculations.

The basic gameplay flow is:

```text
Input
  ↓
Player acceleration / braking
  ↓
Steering + road curvature
  ↓
Speed calculation
  ↓
Rival movement
  ↓
Collision / Nitro detection
  ↓
Distance progression
  ↓
Perspective rendering
  ↓
HUD + effects
```

---

# 🏗️ Main Systems

### `game.py`

Controls the main game state and race loop.

Handles:

* Menus
* Garage
* Settings
* Race state
* Pause state
* Finish state
* Player movement
* Nitro
* Rivals
* Pickups
* Collision
* Race timing
* Saving best times

### `road3d.py`

Responsible for the pseudo-3D racing environment.

It handles:

* Perspective projection
* Road rendering
* Curves
* Lane positioning
* Roadside objects
* Depth scaling

### `audio.py`

Handles the game's sound system:

* Engine audio
* Boost
* Drift
* Crash
* Countdown
* Finish
* Menu music
* Race music

### `save.py`

Handles persistent game data such as:

* Selected car
* Selected track
* Best race times

### `cars.json`

Contains the performance statistics for all playable cars.

### `tracks.json`

Contains track configuration and visual information.

---

# 💾 Save System

The game automatically stores player preferences and best times in:

```text
save.json
```

Settings are stored separately in:

```text
settings.json
```

This means your selected car, selected track, and best times can persist between sessions.

---

# 🧪 Testing

A testing utility is included:

```bash
python test_game.py
```

It can be used to exercise parts of the game without launching the normal gameplay window.

---

# 🎨 Visual Style

NEO RACING follows a dark futuristic visual direction built around:

* Deep black backgrounds
* Electric blue lighting
* Cyan neon elements
* Futuristic cars
* Glowing road elements
* Cyberpunk city scenery
* High-speed night racing

The overall goal is to make the game feel like a futuristic arcade racer while keeping the implementation lightweight.

---

# 🔧 Development

This project was created as a **Python side project** using Pygame.

The project also contains several modular systems and experimental/legacy modules, including:

```text
physics.py
car.py
player.py
ai.py
track.py
camera.py
collision.py
particles.py
```

The current pseudo-3D racing experience primarily uses the newer road-rendering architecture centered around:

```text
game.py
road3d.py
```

Some older helper modules are retained for experimentation and future development.

---

# 🚀 Possible Future Improvements

Potential future additions include:

* 🏆 Championship mode
* 🏁 More tracks
* 🚘 More cars
* 🤖 More advanced AI racing lines
* 🥇 Leaderboards
* 🛠️ Car upgrades
* 💨 More advanced drifting
* 🌧️ Weather effects
* 🌙 Different time-of-night environments
* 🎨 More visual effects
* 💥 More detailed collision effects
* 🎮 Controller support
* 🖥️ Resolution/fullscreen options
* 🔊 More dynamic audio
* 🏅 Achievements

---

# 📸 Screenshots

Add screenshots of the game here:

```text
screenshots/
├── menu.png
├── garage.png
├── neon_city.png
├── race.png
└── finish.png
```

Example:

```markdown
![Main Menu](screenshots/menu.png)

![Race](screenshots/race.png)
```

---

# 👨‍💻 Project

**NEO RACING // NIGHT RUN**

A personal Python/Pygame side project focused on experimenting with:

* Game loops
* Arcade racing physics
* Perspective rendering
* AI opponents
* UI systems
* Audio systems
* Persistent saves
* Procedural road curvature
* 2D asset rendering

---

## 📜 License

Add your preferred license here before publishing the project publicly.

For example:

```text
Copyright © 2026

All rights reserved.
```

---

# 🌌 NEO RACING // NIGHT RUN

**Accelerate. Drift. Boost. Survive the night.**

```text
        N E O   R A C I N G

          // NIGHT RUN //

       SPEED • NEON • NITRO
```
