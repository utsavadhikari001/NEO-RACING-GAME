from ui import text, button, CYAN, MUTED
import pygame
from menu import background

def draw(screen, settings, selected):
    w, h = screen.get_size()
    background(screen, pygame.time.get_ticks()*.001)
    text(screen, 'SETTINGS', 40, 35, 46, CYAN, bold=True)
    labels = [f'SOUND     {"ON" if settings["sound"] else "OFF"}',
              f'MUSIC     {"ON" if settings["music"] else "OFF"}', 'BACK']
    for i, label in enumerate(labels):
        button(screen, label, pygame.Rect(w//2-170, 210+i*75, 340, 55), i == selected)
    text(screen, 'UP / DOWN TO SELECT    •    ENTER TO TOGGLE', w//2, h-65, 17, MUTED, True)
