import math
import pygame
from physics import clamp

class Car:
    def __init__(self, x, y, angle, specs, image, color=(0, 240, 255)):
        self.x, self.y, self.angle = float(x), float(y), angle
        self.speed = 0.0
        self.specs = specs
        self.image = pygame.image.load(image).convert_alpha()
        self.color = color
        self.boost = 100.0
        self.boosting = False
        self.lap = 0
        self.checkpoint = 0
        self.finished = False
        self.drift_time = 0

    def update(self, dt, throttle, steering, braking, boost, on_road):
        dt = min(dt, 0.05)
        accelerating = throttle * self.specs['acceleration']
        boosting = boost and self.boost > 0 and throttle > 0 and on_road
        self.boosting = bool(boosting)
        if boosting:
            accelerating *= 1.8
            self.boost = max(0, self.boost - 36 * dt)
        else:
            self.boost = min(100, self.boost + (8 if on_road else 3) * dt)
        if braking:
            accelerating -= 440 if self.speed > 0 else 160
        drag = (0.985 if on_road else 0.91) ** (dt * 60)
        self.speed = clamp((self.speed + accelerating * dt) * drag,
                           -self.specs['max_speed'] * 0.35,
                           self.specs['max_speed'] * (1.42 if boosting else 1) * (1 if on_road else 0.48))
        self.angle += self.specs['handling'] * steering * dt * clamp(abs(self.speed) / 145, 0, 1.25) * (1 if self.speed >= 0 else -1)
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        self.drift_time = max(0, self.drift_time - dt)
        if abs(steering) > 0.7 and abs(self.speed) > 205:
            self.drift_time = 0.1
        return boosting

    def draw(self, screen, camera, glow=True):
        p = camera.world_to_screen((self.x, self.y))
        ticks = pygame.time.get_ticks()
        pulse = .5+.5*math.sin(ticks*.015)
        if glow:
            for radius, width in ((27, 1), (23, 2)):
                pygame.draw.circle(screen, self.color, p, radius+int(pulse*3), width)
        # Exhaust flames and engine light animate independently of car direction.
        direction = (math.cos(self.angle), math.sin(self.angle))
        normal = (-direction[1], direction[0])
        if self.speed > 20:
            flame = 8 + int(pulse*7) + (17 if self.boosting else 0)
            for side in (-1, 1):
                bx = p[0] - direction[0]*31 + normal[0]*side*10
                by = p[1] - direction[1]*31 + normal[1]*side*10
                tip = (int(bx-direction[0]*flame), int(by-direction[1]*flame))
                pygame.draw.line(screen, (13, 91, 240), (int(bx),int(by)), tip, 6 if self.boosting else 3)
                pygame.draw.circle(screen, (128, 236, 255), (int(bx),int(by)), 3)
        sprite = pygame.transform.rotozoom(self.image, -math.degrees(self.angle), 1.12)
        screen.blit(sprite, sprite.get_rect(center=p))
        if self.boosting:
            pygame.draw.circle(screen, (68, 192, 255), p, 38+int(pulse*7), 1)
