import pygame

BG = (3, 8, 20)
WHITE = (234, 243, 255)
MUTED = (142, 160, 186)
CYAN = (39, 201, 255)

def font(size, bold=False):
    return pygame.font.SysFont('arial', size, bold=bold)

def text(screen, message, x, y, size=24, color=WHITE, center=False, bold=False):
    image = font(size, bold).render(str(message), True, color)
    screen.blit(image, image.get_rect(center=(x, y)) if center else (x, y))

def panel(screen, rect, color=(5, 16, 35), border=(23, 94, 155)):
    pygame.draw.rect(screen, color, rect, border_radius=14)
    pygame.draw.rect(screen, border, rect, 2, border_radius=14)

def button(screen, label, rect, active=False):
    panel(screen, rect, (8, 71, 117) if active else (8, 22, 46), CYAN if active else (28, 76, 120))
    text(screen, label, rect.centerx, rect.centery, 22, WHITE, True, True)

def hud(screen, car, track, elapsed, remaining):
    panel(screen, pygame.Rect(16, 16, 246, 101))
    text(screen, f'{int(max(0, car.speed) * .37):03d}', 28, 22, 48, CYAN, bold=True)
    text(screen, 'KM/H', 145, 51, 15, MUTED, bold=True)
    text(screen, f'LAP {min(car.lap+1, 3)} / 3', 28, 83, 18, WHITE, bold=True)
    panel(screen, pygame.Rect(screen.get_width()-242, 16, 226, 101))
    text(screen, track.name.upper(), screen.get_width()-226, 25, 17, CYAN, bold=True)
    text(screen, f'TIME {elapsed:05.1f}', screen.get_width()-226, 58, 22)
    text(screen, f'RIVALS {remaining}', screen.get_width()-226, 87, 17, MUTED)
    pygame.draw.rect(screen, (39, 54, 78), (screen.get_width()//2-110, 27, 220, 14), border_radius=7)
    pygame.draw.rect(screen, CYAN, (screen.get_width()//2-110, 27, int(220*car.boost/100), 14), border_radius=7)
    text(screen, 'BOOST  /  SHIFT', screen.get_width()//2, 53, 13, WHITE, True)
