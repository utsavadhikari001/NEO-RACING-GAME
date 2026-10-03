import math
from car import Car
from physics import angle_diff, clamp, distance

class Rival(Car):
    def drive(self, dt, track):
        closest = track.nearest_index((self.x, self.y))
        target = track.points[(closest + 5) % len(track.points)]
        desired = math.atan2(target[1] - self.y, target[0] - self.x)
        error = angle_diff(desired, self.angle)
        steering = clamp(error * 2.4, -1, 1)
        throttle = 0.50 if abs(error) < 0.6 else 0.36
        if distance((self.x, self.y), target) > 220:
            throttle = 0.65
        self.update(dt, throttle, steering, False, False, track.on_road((self.x, self.y)))
