# NEO RACING // NIGHT RUN

A **pseudo-3D, behind-the-car** neon highway racer in Python and Pygame. The software-rendered road curves into the distance with perspective lane markers, passing roadside pylons, a richly painted cyberpunk skyline, luminous road gantries, collectible nitro cells, a live race-progress display, depth-scaled rivals, custom rear-view cars, and animated exhaust flames. Race three opponents for three laps across five routes. Black / electric-blue visual direction. No internet or OpenGL required.

## Install and play

Requires Python 3.10+ and Pygame.

```powershell
cd H:\NEO-RACING
python -m pip install -r requirements.txt
python main.py
```

**Controls:** W / Up = accelerate; S / Down / Space = brake; A/D or Left/Right = steer; Shift = nitro; Escape = pause; R = restart. In menus, click options or use Up/Down and Enter. In the garage, Left/Right changes car; Enter or Escape returns. Clicking Track cycles routes.

## Troubleshooting

Extract the **whole** folder. If replacing an earlier release, delete/rename the old folder first: older code and newer assets are not interchangeable. Run `python test_game.py` to exercise the screens, rendering and assets without opening a window. The `pkg_resources` warning from Pygame 2.6.1 is not a crash.

`main.py` launches `game.py`; `road3d.py` builds the perspective course. JSON stores car statistics, routes, preferences and best race times. The older top-down helper modules are retained for experimentation but are not used by the pseudo-3D race. `art_cars.py` optionally regenerates the car PNGs using Pillow.
