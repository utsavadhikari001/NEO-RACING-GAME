import math

def clamp(value, low, high):
    return max(low, min(high, value))

def angle_diff(target, current):
    return (target - current + math.pi) % (2 * math.pi) - math.pi

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
