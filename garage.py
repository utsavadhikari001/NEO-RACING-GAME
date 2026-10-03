import pygame
import math
from ui import text, panel, CYAN, MUTED
from menu import background

_images = {}

def draw(screen, cars, selected, root):
    w, h = screen.get_size()
    background(screen, pygame.time.get_ticks()*.001)
    text(screen, 'THE GARAGE', 40, 32, 45, CYAN, bold=True)
    text(screen, 'LEFT / RIGHT  SELECT CAR    •    ENTER  EQUIP    •    ESC  BACK', 42, 90, 16, MUTED)
    car = cars[selected]
    panel(screen, pygame.Rect(140, 143, w-280, 355))
    if car['sprite'] not in _images:
        _images[car['sprite']] = pygame.transform.smoothscale(
            pygame.image.load(str(root / car['sprite'])).convert_alpha(), (370, 277))
    image = _images[car['sprite']]
    phase = pygame.time.get_ticks()*.003
    image = pygame.transform.rotozoom(image, math.sin(phase)*3, 1+math.sin(phase*2)*.025)
    pygame.draw.ellipse(screen, (7, 73, 117), (w//2-180, 319, 360, 38), 2)
    screen.blit(image, image.get_rect(center=(w//2, 254+int(math.sin(phase)*7))))
    text(screen, car['name'].upper(), w//2, 347, 34, CYAN, True, True)
    for i, field in enumerate(('max_speed', 'acceleration', 'handling')):
        value = car[field]
        fraction = value / {'max_speed': 450, 'acceleration': 530, 'handling': 5.5}[field]
        x, y = w//2-210, 391+i*30
        text(screen, field.replace('_', ' ').upper(), x, y, 15, MUTED)
        pygame.draw.rect(screen, (34, 49, 68), (x+175, y+2, 190, 12), border_radius=6)
        pygame.draw.rect(screen, CYAN, (x+175, y+2, min(190, int(190*fraction)), 12), border_radius=6)
    text(screen, f'◀     {selected+1} / {len(cars)}     ▶', w//2, h-42, 19, MUTED, True)
