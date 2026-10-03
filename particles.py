import random
import pygame

class Particles:
    def __init__(self):
        self.items = []

    def emit(self, x, y, color, count=3):
        for _ in range(count):
            self.items.append([x, y, random.uniform(-60,60), random.uniform(-60,60), random.uniform(.2,.5), color])

    def update(self, dt):
        for p in self.items:
            p[0] += p[2]*dt
            p[1] += p[3]*dt
            p[4] -= dt
        self.items = [p for p in self.items if p[4] > 0]

    def draw(self, screen, camera):
        for x, y, _, _, life, color in self.items:
            pygame.draw.circle(screen, color, camera.world_to_screen((x,y)), max(1, int(life*9)))
