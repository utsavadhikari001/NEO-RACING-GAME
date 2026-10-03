import math
from pathlib import Path
import pygame
from road3d import RoadRenderer
from ui import text, button, panel, CYAN, MUTED, WHITE

OPTIONS=['START RACE','GARAGE','TRACK','SETTINGS','QUIT']
_renderer=None
_city=None

def background(screen,tick):
    global _renderer, _city
    if _renderer is None or _renderer.screen is not screen:
        _renderer=RoadRenderer(screen)
    if _city is None:
        try:
            image=pygame.image.load(str(Path(__file__).parent/'city_backdrop.png')).convert()
            _city=pygame.transform.smoothscale(image,screen.get_size())
        except (FileNotFoundError,pygame.error):
            _city=False
    if _city is not False:
        screen.blit(_city,(0,0))
    else:
        _renderer.road(tick*265,.35,tick)
    # A deep veil behind interactive controls keeps text readable over motion.
    shade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
    shade.fill((0,4,15,149))
    screen.blit(shade,(0,0))
    for i in range(4):
        y=int((tick*115+i*165)%700)-70
        pygame.draw.line(screen,(12,55,98),(0,y),(200,y-75),1)
        pygame.draw.line(screen,(12,55,98),(1000,y),(800,y-75),1)

def draw(screen,selected,track_name,best,tick=0):
    w,h=screen.get_size()
    background(screen,tick)
    panel(screen,pygame.Rect(w//2-190,32,380,559),color=(3,12,29),border=(14,100,169))
    pulse=.5+.5*math.sin(tick*3)
    text(screen,'N E O',w//2,88,66,(46,169+int(54*pulse),255),True,True)
    pygame.draw.line(screen,(12,111,185),(w//2-104,142),(w//2+104,142),2)
    text(screen,'R A C I N G',w//2,171,35,WHITE,True,True)
    text(screen,'NIGHT RUN  //  2.5D',w//2,214,13,MUTED,True,True)
    for i,option in enumerate(OPTIONS):
        rect=pygame.Rect(w//2-155,240+i*58,310,46)
        button(screen,option,rect,i==selected)
        if i==selected:
            pygame.draw.polygon(screen,CYAN,[(w//2-176,254+i*58),(w//2-164,263+i*58),(w//2-176,272+i*58)])
    text(screen,f'{track_name.upper()}   /   BEST {best}',w//2,h-55,14,CYAN,True,True)
    text(screen,'CLICK OR USE ARROW KEYS + ENTER',w//2,h-21,12,MUTED,True)
