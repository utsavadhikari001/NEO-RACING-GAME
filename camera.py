from physics import clamp

class Camera:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.offset = (0, 0)

    def follow(self, target, world_width, world_height, dt):
        wanted_x = clamp(target.x - self.width / 2, 0, world_width - self.width)
        wanted_y = clamp(target.y - self.height / 2, 0, world_height - self.height)
        blend = min(1, dt * 5)
        self.offset = (self.offset[0] + (wanted_x-self.offset[0])*blend,
                       self.offset[1] + (wanted_y-self.offset[1])*blend)

    def world_to_screen(self, point):
        return (int(point[0]-self.offset[0]), int(point[1]-self.offset[1]))
