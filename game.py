import math
from pathlib import Path
import pygame
from audio import Audio
from garage import draw as draw_garage
from menu import OPTIONS, draw as draw_menu
from road3d import RoadRenderer, W, H, VIEW
from save import load, store
from settings import draw as draw_settings
from ui import text, panel, CYAN, MUTED, WHITE

ROOT = Path(__file__).parent
SIZE = (W,H)
LAP_LENGTH = 5200
TOTAL_LAPS = 3

class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('NEO RACING // NIGHT RUN')
        self.clock = pygame.time.Clock()
        self.cars = load('cars.json', [])
        self.tracks = load('tracks.json', [])
        if not self.cars or not self.tracks:
            raise RuntimeError('Missing car/track data. Extract the whole NEO-RACING folder.')
        self.settings = load('settings.json', {'sound': True, 'music': True})
        self.settings = self.settings if isinstance(self.settings, dict) else {}
        self.settings.setdefault('sound', True)
        self.settings.setdefault('music', True)
        self.save = load('save.json', {'selected_car':0,'selected_track':0,'best_times':{}})
        self.save = self.save if isinstance(self.save, dict) else {}
        if not isinstance(self.save.get('best_times'),dict):
            self.save['best_times']={}
        self.car_index = int(self.save.get('selected_car',0)) % len(self.cars)
        self.track_index = int(self.save.get('selected_track',0)) % len(self.tracks)
        self.sprites = {c['sprite']: pygame.image.load(str(ROOT/c['sprite'])).convert_alpha() for c in self.cars}
        self.renderer = RoadRenderer(self.screen)
        self.audio = Audio(self.settings)
        self.mode='menu'
        self.selection=0
        self.subselection=0
        self.visual_time=0.0
        self.running=True
        if self.settings['music']:
            self.audio.music('menu')

    def persist(self):
        self.save['selected_car']=self.car_index
        self.save['selected_track']=self.track_index
        store('save.json',self.save)

    def start_race(self):
        self.audio.engine(0)
        self.mode='race'
        self.distance=0.0
        self.speed=0.0
        self.lateral=0.0
        self.boost=100.0
        self.boosting=False
        self.countdown=3.5
        self.elapsed=0.0
        self.hit_cooldown=0.0
        self.boost_cooldown=0.0
        self.pickups=set()
        self.notice_time=0.0
        self.notice=''
        self.rivals=[{'distance':300+i*370, 'lane':[-.60,.47,0.07][i],
                      'pace':[225,250,270][i], 'car':self.cars[(self.car_index+i+1)%len(self.cars)]} for i in range(3)]
        self.audio.play('countdown')
        if self.settings['music']:
            self.audio.music('race')

    def back_to_menu(self):
        self.audio.engine(0)
        self.mode='menu'
        self.selection=0
        if self.settings['music']:
            self.audio.music('menu')

    def activate(self):
        if self.selection==0:
            self.start_race()
        elif self.selection==1:
            self.mode='garage'
        elif self.selection==2:
            self.track_index=(self.track_index+1)%len(self.tracks)
            self.persist()
        elif self.selection==3:
            self.mode='settings'
            self.subselection=0
        else:
            self.running=False

    def toggle_setting(self):
        if self.subselection==2:
            self.back_to_menu()
            return
        key=('sound','music')[self.subselection]
        self.settings[key]=not self.settings[key]
        store('settings.json',self.settings)
        self.audio.enabled=self.settings['sound'] and pygame.mixer.get_init() is not None
        self.audio.music_enabled=self.settings['music'] and pygame.mixer.get_init() is not None
        if key=='music':
            if self.settings['music']:
                self.audio.music('menu')
            elif pygame.mixer.get_init():
                pygame.mixer.music.stop()

    def handle_event(self,event):
        if event.type==pygame.QUIT:
            self.running=False
            return
        if event.type in (pygame.MOUSEMOTION,pygame.MOUSEBUTTONDOWN):
            x,y=event.pos
            clicked=event.type==pygame.MOUSEBUTTONDOWN and event.button==1
            if self.mode=='menu':
                for i in range(len(OPTIONS)):
                    if pygame.Rect(W//2-155,240+i*58,310,46).collidepoint(x,y):
                        self.selection=i
                        if clicked:
                            self.activate()
                        break
            elif self.mode=='settings':
                for i in range(3):
                    if pygame.Rect(W//2-170,210+i*75,340,55).collidepoint(x,y):
                        self.subselection=i
                        if clicked:
                            self.toggle_setting()
                        break
            elif clicked and self.mode=='garage':
                if y<120 or y>520:
                    self.back_to_menu()
                else:
                    self.car_index=(self.car_index+(1 if x>W//2 else -1))%len(self.cars)
                    self.persist()
            elif clicked and self.mode in ('paused','finished'):
                self.back_to_menu()
            return
        if event.type!=pygame.KEYDOWN:
            return
        k=event.key
        if self.mode=='menu':
            if k in (pygame.K_UP,pygame.K_w):
                self.selection=(self.selection-1)%len(OPTIONS)
            elif k in (pygame.K_DOWN,pygame.K_s):
                self.selection=(self.selection+1)%len(OPTIONS)
            elif k in (pygame.K_RETURN,pygame.K_SPACE):
                self.activate()
            elif k in (pygame.K_LEFT,pygame.K_RIGHT) and self.selection==2:
                self.track_index=(self.track_index+(1 if k==pygame.K_RIGHT else -1))%len(self.tracks)
                self.persist()
        elif self.mode=='garage':
            if k in (pygame.K_LEFT,pygame.K_a):
                self.car_index=(self.car_index-1)%len(self.cars)
            elif k in (pygame.K_RIGHT,pygame.K_d):
                self.car_index=(self.car_index+1)%len(self.cars)
            elif k in (pygame.K_RETURN,pygame.K_ESCAPE):
                self.back_to_menu()
            self.persist()
        elif self.mode=='settings':
            if k in (pygame.K_UP,pygame.K_w):
                self.subselection=(self.subselection-1)%3
            elif k in (pygame.K_DOWN,pygame.K_s):
                self.subselection=(self.subselection+1)%3
            elif k==pygame.K_ESCAPE:
                self.back_to_menu()
            elif k in (pygame.K_RETURN,pygame.K_SPACE):
                self.toggle_setting()
        elif self.mode=='race':
            if k==pygame.K_ESCAPE:
                self.mode='paused'
                self.audio.engine(0)
            elif k==pygame.K_r:
                self.start_race()
        elif self.mode=='paused':
            if k==pygame.K_ESCAPE:
                self.mode='race'
            elif k==pygame.K_r:
                self.start_race()
            elif k==pygame.K_m:
                self.back_to_menu()
        elif self.mode=='finished':
            if k==pygame.K_r:
                self.start_race()
            elif k in (pygame.K_RETURN,pygame.K_ESCAPE,pygame.K_m):
                self.back_to_menu()

    def update_race(self,dt):
        dt=min(dt,.05)
        if self.countdown>0:
            self.countdown-=dt
            return
        self.elapsed+=dt
        self.notice_time=max(0,self.notice_time-dt)
        keys=pygame.key.get_pressed()
        specs=self.cars[self.car_index]
        throttle=keys[pygame.K_w] or keys[pygame.K_UP]
        brake=keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_SPACE]
        steer=int(bool(keys[pygame.K_d] or keys[pygame.K_RIGHT]))-int(bool(keys[pygame.K_a] or keys[pygame.K_LEFT]))
        self.boosting=bool((keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and throttle and self.boost>0 and abs(self.lateral)<1.02)
        if self.boosting:
            self.boost=max(0,self.boost-31*dt)
        else:
            self.boost=min(100,self.boost+9*dt)
        max_speed=specs['max_speed']*(1.34 if self.boosting else 1)
        if throttle:
            self.speed+=specs['acceleration']*(1.45 if self.boosting else 1)*dt
        if brake:
            self.speed-=490*dt
        self.speed=max(0,min(max_speed,self.speed-(28+0.055*self.speed)*dt))
        self.lateral+=steer*specs['handling']*.38*dt*(.3+.7*min(1,self.speed/250))
        # Moving the lane under the car on winding parts demands continuous steering.
        bend=math.cos(self.distance/750+self.tracks[self.track_index]['variation'])*100/750
        bend+=math.cos(self.distance/1800+self.tracks[self.track_index]['variation'])*125/1800
        self.lateral-=bend*self.speed*dt/225
        self.lateral=max(-1.5,min(1.5,self.lateral))
        if abs(self.lateral)>1.04:
            self.speed*=max(.1,1-1.6*dt)
        self.audio.engine(self.speed)
        self.distance+=self.speed*dt
        # Boost-cell pickups reward taking deliberate racing lines.
        for i in range(max(0,int(self.distance//880)-1),int(self.distance//880)+2):
            marker=640+i*880
            lane=(-.50,0,.50)[i%3]
            if i not in self.pickups and abs(self.distance-marker)<29 and abs(self.lateral-lane)<.30:
                self.pickups.add(i)
                self.boost=min(100,self.boost+42)
                self.notice='NITRO +42'
                self.notice_time=1.4
        self.hit_cooldown=max(0,self.hit_cooldown-dt)
        self.boost_cooldown-=dt
        if self.boosting and self.boost_cooldown<=0:
            self.audio.play('boost')
            self.boost_cooldown=.8
        for rival in self.rivals:
            if rival['distance']<TOTAL_LAPS*LAP_LENGTH:
                rival['distance']+=rival['pace']*dt
            delta=rival['distance']-self.distance
            if self.hit_cooldown==0 and abs(delta)<40 and abs(rival['lane']-self.lateral)<.3:
                self.speed*=.46
                self.hit_cooldown=1.4
                self.audio.play('crash')
                self.notice='COLLISION  /  SPEED LOST'
                self.notice_time=1.2
        if self.distance>=TOTAL_LAPS*LAP_LENGTH:
            self.distance=TOTAL_LAPS*LAP_LENGTH
            self.mode='finished'
            self.audio.engine(0)
            self.audio.play('finish')
            key=self.tracks[self.track_index]['id']
            old=self.save['best_times'].get(key)
            if old is None or self.elapsed<old:
                self.save['best_times'][key]=round(self.elapsed,2)
                self.persist()

    def draw_race(self):
        t=self.visual_time
        track=self.tracks[self.track_index]
        curve=track['variation']
        self.renderer.road(self.distance,curve,t)
        for i in range(max(0,int(self.distance//880)-1),int(self.distance//880)+4):
            if i in self.pickups:
                continue
            z=640+i*880-self.distance
            if 35<z<VIEW:
                lane=(-.50,0,.50)[i%3]
                bx,by,scale,_=self.renderer.project(z,lane,self.distance,curve)
                radius=max(4,int(27*scale))
                bob=math.sin(t*4+i)*max(2,12*scale)
                pygame.draw.circle(self.screen,(17,78,146),(int(bx),int(by-30*scale+bob)),radius+3,3)
                pygame.draw.circle(self.screen,(114,236,255),(int(bx),int(by-30*scale+bob)),radius,2)
                pygame.draw.line(self.screen,(148,243,255),(bx-radius*.42,by-30*scale+bob),(bx+radius*.42,by-30*scale+bob),2)
        for rival in sorted(self.rivals,key=lambda r:r['distance']-self.distance,reverse=True):
            z=rival['distance']-self.distance
            if 20<z<VIEW:
                x,y,scale,_=self.renderer.project(z,rival['lane'],self.distance,curve)
                self.renderer.car(self.sprites[rival['car']['sprite']],x,y,scale,t)
        self.renderer.speed_fx(self.speed,t)
        x=W//2+int(self.lateral*305)
        self.renderer.car(self.sprites[self.cars[self.car_index]['sprite']],x,568,1,t,self.boosting,True,
                          int(bool(pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]))-
                          int(bool(pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT])))
        panel(self.screen,pygame.Rect(18,17,210,112))
        text(self.screen,f'{int(self.speed*.92):03d}',32,23,53,CYAN,bold=True)
        text(self.screen,'KM/H',144,53,15,MUTED,bold=True)
        text(self.screen,f'LAP {min(TOTAL_LAPS, int(self.distance//LAP_LENGTH)+1)} / {TOTAL_LAPS}',31,94,20,WHITE,bold=True)
        panel(self.screen,pygame.Rect(W-247,17,229,112))
        text(self.screen,track['name'].upper(),W-232,25,17,CYAN,bold=True)
        text(self.screen,f'TIME  {self.elapsed:05.1f}',W-232,59,22,WHITE)
        place=1+sum(r['distance']>self.distance for r in self.rivals)
        text(self.screen,f'POSITION  {place} / 4',W-232,93,17,MUTED)
        pygame.draw.rect(self.screen,(12,36,61),(W//2-111,29,222,16),border_radius=7)
        pygame.draw.rect(self.screen,CYAN,(W//2-111,29,int(self.boost*2.22),16),border_radius=7)
        text(self.screen,'NITRO  /  SHIFT',W//2,61,14,WHITE,True)
        # Progress timeline: the three cyan markers represent lap ends.
        pygame.draw.rect(self.screen,(5,24,46),(286,93,428,14),border_radius=6)
        pygame.draw.rect(self.screen,(30,135,199),(286,93,int(428*self.distance/(TOTAL_LAPS*LAP_LENGTH)),14),border_radius=6)
        for lapmark in (1,2):
            xx=286+round(lapmark*428/TOTAL_LAPS)
            pygame.draw.line(self.screen,(148,230,249),(xx,90),(xx,110),2)
        for rival in self.rivals:
            xx=286+round(min(1,rival['distance']/(TOTAL_LAPS*LAP_LENGTH))*428)
            pygame.draw.circle(self.screen,(242,74,129),(xx,100),4)
        text(self.screen,'START',285,115,12,MUTED)
        text(self.screen,'FINISH',660,115,12,MUTED)
        if self.notice_time>0:
            text(self.screen,self.notice,W//2,158,21,(117,230,255),True,True)
        text(self.screen,'WASD / ARROWS   DRIVE     SPACE   BRAKE     SHIFT   NITRO     ESC   PAUSE',W//2,600,14,WHITE,True)
        if self.countdown>0:
            text(self.screen,str(math.ceil(self.countdown)) if self.countdown>.65 else 'GO!',W//2,284,95,CYAN,True,True)
        if self.mode in ('paused','finished'):
            shade=pygame.Surface(SIZE,pygame.SRCALPHA)
            shade.fill((1,6,17,185))
            self.screen.blit(shade,(0,0))
            panel(self.screen,pygame.Rect(260,185,480,255))
            if self.mode=='paused':
                text(self.screen,'PAUSED',500,250,52,CYAN,True,True)
                text(self.screen,'ESC RESUME   /   R RESTART   /   M MENU',500,352,17,WHITE,True)
            else:
                text(self.screen,'FINISH LINE!',500,245,48,CYAN,True,True)
                text(self.screen,f'TIME {self.elapsed:.2f}s',500,317,29,WHITE,True)
                text(self.screen,'R RACE AGAIN    /    ENTER MENU',500,380,17,MUTED,True)

    def run(self):
        while self.running:
            dt=min(self.clock.tick(60)/1000,.05)
            self.visual_time+=dt
            for event in pygame.event.get():
                self.handle_event(event)
            if not self.running:
                break
            if self.mode=='race':
                self.update_race(dt)
            if self.mode=='menu':
                key=self.tracks[self.track_index]['id']
                best=self.save['best_times'].get(key)
                draw_menu(self.screen,self.selection,self.tracks[self.track_index]['name'],f'{best:.2f}s' if best is not None else '--:--',self.visual_time)
            elif self.mode=='garage':
                draw_garage(self.screen,self.cars,self.car_index,ROOT)
            elif self.mode=='settings':
                draw_settings(self.screen,self.settings,self.subselection)
            else:
                self.draw_race()
            pygame.display.flip()
        self.audio.engine(0)
        pygame.quit()
