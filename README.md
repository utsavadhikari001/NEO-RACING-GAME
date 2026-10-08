# 🏎️ NEO RACING NIGHT RUN

> A neon-soaked arcade racing game built with Python and Pygame.

**NEO RACING NIGHT RUN** is a futuristic arcade racing game developed as a personal Python side project.

The game combines fast-paced racing, pseudo-3D road rendering, neon environments, AI opponents, Nitro boosting, multiple cars, and multiple tracks into a lightweight racing experience built with **Python and Pygame**.

---

## 🎮 Features

* 🏁 Pseudo-3D racing system
* 🌃 Futuristic neon night environment
* 🚗 6 playable cars
* 🛣️ 5 different racing tracks
* 🤖 AI racing opponents
* ⚡ Nitro boost system
* 🔋 Nitro pickups
* 💥 Collision system
* 🔥 Racing effects and particles
* 🎵 Race and menu music
* 🔊 Engine, boost, drift, crash and other sound effects
* 🏆 Best-time tracking
* 💾 Save system
* ⚙️ Settings system
* 🎮 Keyboard controls
* 🖥️ Built without a traditional 3D game engine

---

# 📸 Screenshots

Here are some screenshots from **NEO RACING NIGHT RUN**.

> **Add your screenshots below.**

### 🏠 Main Menu

<!-- Add your main menu screenshot here -->

<img width="993" height="646" alt="SS1" src="https://github.com/user-attachments/assets/749cc24d-59fa-43d2-ac68-e7b089698057" />


### 🏎️ Gameplay

<!-- Add your gameplay screenshot here -->

<img width="999" height="650" alt="SS2" src="https://github.com/user-attachments/assets/3c990bdc-bf3b-41c7-9e40-cfd3f31e24a1" />

<img width="1006" height="651" alt="SS5" src="https://github.com/user-attachments/assets/341bf9fa-43d1-4efa-b47e-2727deb70597" />

### 🚘 Car Selection / Garage

<!-- Add your garage screenshot here -->

<img width="1001" height="648" alt="Screenshot 2026-10-03 154159" src="https://github.com/user-attachments/assets/97f9a3e3-ed7a-4667-9895-b6660d88a1e7" />

<img width="1004" height="649" alt="SS4" src="https://github.com/user-attachments/assets/3753261e-b34d-4483-95fb-19326345f134" />


### 🏁 Race Finish

<!-- Add your finish-screen screenshot here -->

<img width="996" height="649" alt="SS3" src="https://github.com/user-attachments/assets/6a79b91f-e62c-409a-bf42-74a37ce28072" />



---

# 🚘 Cars

The game currently features **6 playable cars**, each with different performance characteristics.

| Car         | Top Speed | Acceleration | Handling |
| ----------- | --------: | -----------: | -------: |
| **Neo**     |       380 |          420 |      4.1 |
| **Volt**    |       355 |          510 |      4.0 |
| **Phantom** |       425 |          375 |      3.5 |
| **Vector**  |       370 |          410 |      5.1 |
| **Titan**   |       335 |          445 |      3.7 |
| **Apex**    |       400 |          455 |      4.4 |

Each car provides a different driving experience.

* **Neo** — Balanced
* **Volt** — Acceleration focused
* **Phantom** — High top speed
* **Vector** — Handling focused
* **Titan** — Strong acceleration
* **Apex** — Balanced performance

---

# 🌃 Tracks

NEO RACING NIGHT RUN features **5 racing environments**.

### 🌆 Neon City

A futuristic city route surrounded by neon lights.

### 🛣️ Midnight Highway

A high-speed highway designed for fast racing.

### ⚓ Cyber Port

A futuristic industrial racing environment.

### ☁️ Skyway

A high-altitude futuristic racing route.

### 🔷 Nexus

A futuristic neon racing environment designed around the game's visual style.

---

# ⚡ Nitro

Nitro is one of the main gameplay mechanics.

Use:

```text
SHIFT + W
```

to activate Nitro while accelerating.

Nitro temporarily increases your speed and acceleration.

Nitro can also be restored by collecting Nitro cells placed throughout the track.

This adds another layer of strategy to racing because players need to decide when to use their boost and where to position themselves on the track.

---

# 🏁 Racing

Each race consists of:

* **3 laps**
* **3 AI opponents**
* Multiple racing lanes
* Curved roads
* Nitro pickups
* Collision interactions
* Race timing

The goal is to complete the race as quickly as possible while managing speed, steering, Nitro and traffic.

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

### Menu Controls

| Action           | Keyboard          |
| ---------------- | ----------------- |
| Move Up          | `W` / `↑`         |
| Move Down        | `S` / `↓`         |
| Select           | `Enter` / `Space` |
| Change Selection | `←` / `→`         |
| Back             | `Esc`             |

---

# 🛠️ Built With

* **Python**
* **Pygame**
* JSON
* PNG assets
* WAV audio

The game uses a custom pseudo-3D rendering approach instead of relying on a full 3D game engine.

---

# 🧠 Technical Overview

The game is divided into several systems responsible for different parts of the experience.

### Game System

Handles:

* Game states
* Race loop
* Player movement
* AI opponents
* Nitro
* Pickups
* Collisions
* Race timing
* Menus
* Finish states

### Pseudo-3D Road System

The road is rendered using perspective calculations to create the appearance of a 3D racing environment while remaining a 2D Pygame application.

### AI System

AI opponents race alongside the player and follow the track while maintaining different speeds and positions.

### Audio System

The game includes separate sounds for:

* Engine
* Nitro
* Drift
* Collision
* Countdown
* Finish
* Menu music
* Race music

### Save System

The game can store information such as selected options and best race times.

---

# 📂 Project Structure

The project intentionally keeps its files in a simple structure.

```text
NEO-RACING-NIGHT-RUN/
│
├── README.md
├── requirements.txt
│
├── *.py
├── *.json
├── *.png
└── *.wav
```

The Python files contain the game's logic, while JSON files contain configuration/data and PNG/WAV files provide the game's visual and audio assets.

---

# 💻 Installation

## 1. Clone the repository

```bash
git clone YOUR-GITHUB-REPOSITORY-URL
```

## 2. Enter the project directory

```bash
cd NEO-RACING-NIGHT-RUN
```

## 3. Install the required package

```bash
pip install -r requirements.txt
```

## 4. Start the game

```bash
python main.py
```

---

# 📋 Requirements

* Python 3.x
* Pygame

Install the dependency with:

```bash
pip install pygame
```

Or use:

```bash
pip install -r requirements.txt
```

---

# 🚀 Future Improvements

Possible future updates include:

* 🏆 Championship mode
* 🥇 Leaderboards
* 🚘 More cars
* 🛣️ More tracks
* 🤖 Improved AI
* 🛠️ Car upgrades
* 💨 More advanced drifting
* 🌧️ Weather effects
* 🎮 Controller support
* 🖥️ Fullscreen/resolution options
* 🎨 Additional visual effects
* 🔊 More dynamic audio
* 🏅 Achievements

---

# 👨‍💻 About the Project

**NEO RACING NIGHT RUN** was created as a personal side project to experiment with game development using Python.

The project explores several areas of programming and game development, including:

* Game loops
* Player movement
* Racing physics
* AI
* Perspective rendering
* Collision detection
* UI development
* Audio systems
* Save systems
* Game-state management

The goal was to build a complete playable racing experience using **Python and Pygame**.

---

# 📜 License

If you plan to make the project open source, add your preferred license here.

For example:

```text
Copyright © 2026

All rights reserved.
```

---

# 🏎️ NEO RACING NIGHT RUN

**Race through the night. Push your limits.**

```text
NEO RACING NIGHT RUN

SPEED • NEON • NITRO
```
