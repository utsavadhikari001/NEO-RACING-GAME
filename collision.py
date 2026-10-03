from physics import distance

def resolve(cars):
    for i, a in enumerate(cars):
        for b in cars[i+1:]:
            d = distance((a.x, a.y), (b.x, b.y))
            if 0 < d < 34:
                nx, ny = (a.x-b.x)/d, (a.y-b.y)/d
                overlap = (34-d)/2
                a.x += nx*overlap
                a.y += ny*overlap
                b.x -= nx*overlap
                b.y -= ny*overlap
                a.speed *= 0.65
                b.speed *= 0.65
                return True
    return False
