import math
import pygame
from physics import distance

class Track:
    def __init__(self, data):
        self.data = data
        self.name = data['name']
        self.width = 1640
        self.height = 1100
        self.road_width = data.get('road_width', 152)
        self.points = []
        for i in range(160):
            t = 2 * math.pi * i / 160
            # Clockwise in screen space, with subtle bends between the long straights.
            x = 820 + 600 * math.cos(t) + 32 * math.cos(3 * t + data['variation'])
            y = 550 + 365 * math.sin(t) + 28 * math.sin(4 * t + data['variation'])
            self.points.append((x, y))
        self.palette = tuple(data['accent'])

    def nearest_index(self, p):
        return min(range(len(self.points)), key=lambda i: (self.points[i][0]-p[0])**2 + (self.points[i][1]-p[1])**2)

    def on_road(self, p):
        i = self.nearest_index(p)
        return distance(p, self.points[i]) < self.road_width / 2 + 8

    def update_lap(self, car):
        idx = self.nearest_index((car.x, car.y))
        n = len(self.points)
        # Require progress through each quarter before a full lap can be registered.
        if car.checkpoint == 0 and n//4 <= idx < n//2:
            car.checkpoint = 1
        elif car.checkpoint == 1 and n//2 <= idx < 3*n//4:
            car.checkpoint = 2
        elif car.checkpoint == 2 and idx >= 3*n//4:
            car.checkpoint = 3
        elif car.checkpoint == 3 and idx < 8 and car.speed > 0:
            car.checkpoint = 0
            car.lap += 1

    def draw(self, screen, camera, tick):
        screen.fill(tuple(self.data['ground']))
        tick *= .001
        ox, oy = camera.offset
        # City grid / runway tiles.
        for x in range(0, self.width + 1, 80):
            pygame.draw.line(screen, (19, 28, 44), (int(x-ox), -int(oy)), (int(x-ox), int(self.height-oy)), 1)
        for y in range(0, self.height + 1, 80):
            pygame.draw.line(screen, (19, 28, 44), (-int(ox), int(y-oy)), (int(self.width-ox), int(y-oy)), 1)
        path = [camera.world_to_screen(p) for p in self.points]
        pygame.draw.lines(screen, (8, 45, 91), True, path, self.road_width + 31)
        pygame.draw.lines(screen, self.palette, True, path, self.road_width + 17)
        pygame.draw.lines(screen, (10, 13, 28), True, path, self.road_width + 7)
        pygame.draw.lines(screen, (46, 53, 72), True, path, self.road_width - 5)
        pygame.draw.lines(screen, (34, 40, 58), True, path, self.road_width - 33)
        for i in range(0, len(path), 5):
            pygame.draw.line(screen, (150, 166, 197), path[i], path[(i+2) % len(path)], 2)
        # Start line perpendicular to the track tangent.
        x, y = self.points[0]
        a = math.atan2(self.points[1][1]-y, self.points[1][0]-x) + math.pi/2
        dx, dy = math.cos(a), math.sin(a)
        for j in range(-5, 5):
            start = camera.world_to_screen((x + dx*j*13, y + dy*j*13))
            end = camera.world_to_screen((x + dx*(j+1)*13, y + dy*(j+1)*13))
            pygame.draw.line(screen, (235, 242, 255) if j%2 else (11, 18, 30), start, end, 12)
        for i in range(0, len(path), 5):
            p = path[i]
            phase = .5+.5*math.sin(tick*4-i*.36)
            pygame.draw.circle(screen, self.palette, p, 3+int(phase*3))
        # Light packets chase each other around the circuit.
        for offset in (0, 40, 80, 120):
            p = path[(int(tick*23)+offset) % len(path)]
            pygame.draw.circle(screen, (105, 225, 255), p, 10, 2)
            pygame.draw.circle(screen, (210, 249, 255), p, 3)
