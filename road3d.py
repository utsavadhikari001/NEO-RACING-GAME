"""Procedural, software-rendered 2.5D cyberpunk highway (no OpenGL needed)."""
import math
import random
from pathlib import Path
import pygame

W, H = 1000, 620
HORIZON = 198
VIEW = 1800


def glow(surface, position, color, radius, strength=100):
    """Small layered additive-looking glow, made with alpha surfaces."""
    radius = int(radius)
    if radius < 2:
        return
    orb = pygame.Surface((radius*2+2,radius*2+2),pygame.SRCALPHA)
    for fraction, alpha in ((1, strength//8),(.68,strength//6),(.37,strength//4),(.16,strength//2)):
        pygame.draw.circle(orb, (*color,alpha),(radius+1,radius+1),max(1,int(radius*fraction)))
    surface.blit(orb,(int(position[0])-radius-1,int(position[1])-radius-1))


class RoadRenderer:
    def __init__(self, screen):
        self.screen=screen
        self.sky=pygame.Surface((W,HORIZON))
        for y in range(HORIZON):
            k=y/HORIZON
            pygame.draw.line(self.sky,(2+int(7*k),5+int(16*k),20+int(35*k)),(0,y),(W,y))
        rng=random.Random(7721)
        self.stars=[(rng.randrange(W),rng.randrange(HORIZON-25),rng.randrange(1,3),rng.random()*5) for _ in range(95)]
        self.far=[(rng.randrange(-80,1120),rng.randrange(35,100),rng.randrange(22,65),rng.randrange(100)) for _ in range(36)]
        self.near=[(rng.randrange(-80,1120),rng.randrange(45,155),rng.randrange(24,66),rng.randrange(100)) for _ in range(38)]
        self.sky_base=self._build_sky()
        try:
            self.city=pygame.image.load(str(Path(__file__).parent/'city_sky.png')).convert()
        except (pygame.error,FileNotFoundError):
            self.city=None
        self.fog=pygame.Surface((W,120),pygame.SRCALPHA)
        for y in range(120):
            pygame.draw.line(self.fog,(11,86,157,int(22*(1-abs(y-52)/70))), (0,y),(W,y))

    def _build_sky(self):
        surface=self.sky.copy()
        # Layered halos make the moon feel luminous instead of a flat circle.
        for radius,alpha in ((115,9),(85,14),(63,22),(48,35)):
            orb=pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
            pygame.draw.circle(orb,(26,141,243,alpha),(radius,radius),radius)
            surface.blit(orb,(762-radius,89-radius))
        pygame.draw.circle(surface,(20,90,145),(762,89),40)
        pygame.draw.circle(surface,(65,186,245),(762,89),37,2)
        pygame.draw.circle(surface,(12,45,83),(762,89),33)
        for x,y,r,_ in self.stars:
            pygame.draw.circle(surface,(29,92,154),(x,y),r)
        return surface

    def project(self,z,lane,progress,curve):
        scale=190/(190+max(0,z))
        y=HORIZON+(H-HORIZON)*scale
        bend=math.sin((progress+z)/750+curve)*108+math.sin((progress+z)/1800+curve)*125
        bend-=math.sin(progress/750+curve)*108+math.sin(progress/1800+curve)*125
        center=W/2+bend*(1-scale)**.6
        return center+lane*458*scale,y,scale,center

    def _buildings(self,buildings,progress,parallax,fill,edge,window):
        s=self.screen
        pan=int(math.sin(progress/1050)*parallax)
        for x,height,width,seed in buildings:
            xx=(x+pan)%1140-75
            pygame.draw.rect(s,fill,(xx,HORIZON-height,width,height))
            pygame.draw.line(s,edge,(xx,HORIZON-height),(xx+width,HORIZON-height),1)
            for yy in range(HORIZON-height+9,HORIZON-6,12):
                for wx in range(xx+6,xx+width-3,10):
                    if (wx//3+yy+seed)%9<4:
                        pygame.draw.rect(s,window,(wx,yy,2,4))
            if seed%10==0:
                pygame.draw.line(s,(16,93,163),(xx+width//2,HORIZON-height),(xx+width//2,HORIZON-height-11),1)

    def sky_layer(self,progress,clock):
        s=self.screen
        if self.city is not None:
            shift=int(math.sin(progress/2800)*48)
            s.blit(self.city,(-52+shift,0))
        else:
            s.blit(self.sky_base,(0,0))
        for x,y,r,phase in self.stars:
            if math.sin(clock*3+phase)>0.5:
                pygame.draw.circle(s,(111,208,255),(x,y),r)
        if self.city is None:
            self._buildings(self.far,progress,13,(6,17,36),(10,45,75),(11,44,81))
            self._buildings(self.near,progress,33,(5,22,43),(11,83,129),(21,115,170))
        s.blit(self.fog,(0,HORIZON-67))
        pygame.draw.line(s,(27,146,208),(0,HORIZON),(W,HORIZON),1)
        s.fill((3,12,27),(0,HORIZON,W,H-HORIZON))

    def road(self,progress,curve,clock):
        s=self.screen
        self.sky_layer(progress,clock)
        slices=list(range(0,VIEW+24,24))
        for far,near in zip(reversed(slices[1:]),reversed(slices[:-1])):
            l0,y0,a,_=self.project(far,-1,progress,curve)
            r0,_,_,_=self.project(far,1,progress,curve)
            l1,y1,b,_=self.project(near,-1,progress,curve)
            r1,_,_,_=self.project(near,1,progress,curve)
            if y1-y0<.1:
                continue
            band=int((progress+near)/160)
            pygame.draw.polygon(s,(3,16,32) if band%2 else (4,19,36),[(0,y0),(W,y0),(W,y1),(0,y1)])
            pygame.draw.polygon(s,(17,30,52) if band%2 else (19,33,56),[(l0,y0),(r0,y0),(r1,y1),(l1,y1)])
            # Rumble strips and double edge lines.
            for side in (-1,1):
                edge0=l0 if side==-1 else r0
                edge1=l1 if side==-1 else r1
                pygame.draw.polygon(s,(8,84,139) if band%2 else (24,135,193),
                    [(edge0,y0),(edge0+side*max(1,17*a),y0),(edge1+side*max(2,17*b),y1),(edge1,y1)])
                pygame.draw.line(s,(73,200,252),(edge0,y0),(edge1,y1),max(1,int(3*b)))
                inner0,_,_,_=self.project(far,side*.91,progress,curve)
                inner1,_,_,_=self.project(near,side*.91,progress,curve)
                pygame.draw.line(s,(20,55,90),(inner0,y0),(inner1,y1),1)
            if int((progress+near)/106)%2==0:
                for lane in (-.333,.333):
                    x0,_,_,_=self.project(far,lane,progress,curve)
                    x1,_,_,_=self.project(near,lane,progress,curve)
                    pygame.draw.polygon(s,(117,191,222),[(x0-max(1,3*a),y0),(x0+max(1,3*a),y0),
                                                          (x1+max(1,4*b),y1),(x1-max(1,4*b),y1)])
            # Scrolling reflected light panels in the middle of the wet asphalt.
            if band%3==0 and near<780:
                cx0,_,_,_=self.project(far,0,progress,curve)
                cx1,_,_,_=self.project(near,0,progress,curve)
                pygame.draw.line(s,(24,53,82),(cx0,y0),(cx1,y1),max(1,int(10*b)))
        self.scenery(progress,curve,clock)

    def scenery(self,progress,curve,clock):
        s=self.screen
        first=int(progress/160)
        for marker in range(first,first+14):
            z=marker*160-progress
            if not 8<z<VIEW:
                continue
            for side in (-1,1):
                x,y,scale,_=self.project(z,side*1.28,progress,curve)
                x,y=int(x),int(y)
                height=max(4,int(155*scale))
                pygame.draw.line(s,(7,54,93),(x,y),(x,y-height),max(1,int(9*scale)))
                pygame.draw.circle(s,(19,135,204),(x,y-height),max(2,int(9*scale)))
                pygame.draw.circle(s,(156,237,255),(x,y-height),max(1,int(4*scale)))
                if scale>.3:
                    glow(s,(x,y-height),(13,135,247),int(17*scale),65)
                # Futuristic stacked window tower.
                if marker%4==0:
                    bx=x+int(side*40*scale)
                    bh=int((115+marker%3*29)*scale)
                    bw=max(3,int(42*scale))
                    pygame.draw.rect(s,(4,30,55),(bx-bw//2,y-bh,bw,bh))
                    pygame.draw.rect(s,(16,89,153),(bx-bw//2,y-bh,bw,bh),max(1,int(2*scale)))
                    for j in range(4):
                        wy=y-bh+int((14+j*26)*scale)
                        pygame.draw.line(s,(42,160,211),(bx-bw//3,wy),(bx+bw//3,wy),max(1,int(2*scale)))
            if marker%5==0 and z<1000:
                left,yy,sc,_=self.project(z,-1.15,progress,curve)
                right,_,_,_=self.project(z,1.15,progress,curve)
                roof=yy-280*sc
                width=max(1,int(9*sc))
                pygame.draw.line(s,(12,81,141),(left,yy),(left,roof),width)
                pygame.draw.line(s,(12,81,141),(right,yy),(right,roof),width)
                pygame.draw.line(s,(18,100,171),(left,roof),(right,roof),max(1,int(9*sc)))
                pygame.draw.line(s,(83,213,252),(left,roof),(right,roof),max(1,int(3*sc)))
                if sc>.28:
                    msg=pygame.font.SysFont('arial',max(10,int(30*sc)),bold=True).render('N E O  / /  R A C I N G',True,(114,216,248))
                    s.blit(msg,msg.get_rect(center=((left+right)/2,roof+13*sc)))

    def car(self,sprite,x,y,scale,clock,boosting=False,player=False,lean=0):
        if scale<.015:
            return
        width=max(3,int((180 if player else 188)*scale))
        height=max(3,int((146 if player else 150)*scale))
        if player:
            width,height=194,150
        x,y=int(x),int(y)
        pygame.draw.ellipse(self.screen,(1,5,13),(x-width//2,y-int(height*.13),width,max(3,int(height*.25))))
        if boosting:
            length=int((25+12*math.sin(clock*28))*(1 if player else scale))
            for offset in (-.22,.22):
                fx=x+int(width*offset)
                pygame.draw.polygon(self.screen,(8,107,255),[(fx-7,y-18),(fx+7,y-18),(fx,y+length)])
                pygame.draw.polygon(self.screen,(113,227,255),[(fx-3,y-15),(fx+3,y-15),(fx,y+length//2)])
        image=pygame.transform.smoothscale(sprite,(width,height))
        if player and lean:
            image=pygame.transform.rotozoom(image,-lean*3,1)
        bounce=int(math.sin(clock*18)*2) if player else int(math.sin(clock*8+x)*scale*2)
        self.screen.blit(image,image.get_rect(midbottom=(x,y+bounce)))
        if player:
            pygame.draw.arc(self.screen,(19,102,196),(x-width*.58,y-height*.9,width*1.16,height*.8),3.6,5.8,2)

    def speed_fx(self,speed,clock):
        if speed<165:
            return
        power=min(1,(speed-165)/210)
        for i in range(28):
            x=int((i*291+clock*600*(1+i%3))%W)
            y=int(HORIZON+(i*97+clock*310*(1+i%4))%(H-HORIZON))
            if abs(x-W//2)<210*(1-(y-HORIZON)/(H-HORIZON)):
                continue
            pygame.draw.line(self.screen,(15,64+int(power*70),129+int(power*110)),
                            (x,y),(x+int((8+power*24)*(1 if x<W/2 else -1)),y+int(10+power*25)),1)
