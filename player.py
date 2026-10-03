from car import Car

class Player(Car):
    def drive(self, dt, keys, on_road):
        import pygame
        throttle = int(keys[pygame.K_w] or keys[pygame.K_UP]) - int(keys[pygame.K_s] or keys[pygame.K_DOWN])
        steering = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        braking = keys[pygame.K_SPACE]
        boost = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        return self.update(dt, throttle, steering, braking, boost, on_road)
