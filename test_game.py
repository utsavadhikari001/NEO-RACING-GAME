"""Headless integration tests. Run: python test_game.py"""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
from pathlib import Path
from unittest.mock import patch
import pygame
import game as module
from game import Game, LAP_LENGTH, TOTAL_LAPS
from garage import draw as draw_garage
from settings import draw as draw_settings

ROOT=Path(__file__).parent

class GameTests(unittest.TestCase):
    def setUp(self):
        self.patch=patch.object(module,'store')
        self.patch.start()
        self.g=Game()

    def tearDown(self):
        self.patch.stop()
        pygame.quit()

    def key(self,k):
        self.g.handle_event(pygame.event.Event(pygame.KEYDOWN,key=k))

    def click(self,x,y):
        self.g.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=(x,y)))

    def test_assets(self):
        self.assertEqual((len(self.g.cars),len(self.g.tracks)),(6,5))
        for c in self.g.cars:
            self.assertGreater(self.g.sprites[c['sprite']].get_width(),100)
        for t in self.g.tracks:
            pygame.image.load(str(ROOT/t['image']))
        for name in ('engine','boost','drift','crash','countdown','finish'):
            pygame.mixer.Sound(str(ROOT/(name+'.wav')))
        for name in ('menu','race'):
            pygame.mixer.music.load(str(ROOT/(name+'_music.ogg')))

    def test_all_tracks_and_car_rendering(self):
        for i in range(5):
            self.g.track_index=i
            self.g.car_index=i
            self.g.start_race()
            self.g.countdown=0
            self.g.speed=280
            self.g.distance=1230
            self.g.draw_race()
            self.g.update_race(.016)
            self.g.draw_race()

    def test_menu_keyboard_and_mouse(self):
        self.key(pygame.K_DOWN)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.g.mode,'garage')
        draw_garage(self.g.screen,self.g.cars,0,ROOT)
        self.key(pygame.K_RIGHT)
        self.assertEqual(self.g.car_index,1)
        self.key(pygame.K_ESCAPE)
        self.g.selection=2
        self.key(pygame.K_RETURN)
        self.assertEqual(self.g.track_index,1)
        self.click(500,437)
        self.assertEqual(self.g.mode,'settings')
        draw_settings(self.g.screen,self.g.settings,0)
        self.click(500,237)
        self.assertFalse(self.g.settings['sound'])
        self.click(500,311)
        self.assertFalse(self.g.settings['music'])
        self.click(500,388)
        self.assertEqual(self.g.mode,'menu')
        self.click(500,263)
        self.assertEqual(self.g.mode,'race')

    def test_progress_pause_restarts_and_finish(self):
        self.g.start_race()
        self.g.countdown=0
        self.g.speed=240
        initial=self.g.distance
        self.g.update_race(.05)
        self.assertGreater(self.g.distance,initial)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.g.mode,'paused')
        self.g.draw_race()
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.g.mode,'race')
        self.g.distance=TOTAL_LAPS*LAP_LENGTH-2
        self.g.speed=300
        self.g.update_race(.05)
        self.assertEqual(self.g.mode,'finished')
        self.g.draw_race()
        self.key(pygame.K_RETURN)
        self.assertEqual(self.g.mode,'menu')

    def test_drive_pickups_and_full_race(self):
        class Keys:
            def __init__(self):
                self.values={}
            def __getitem__(self,key):
                return self.values.get(key,False)
        controls=Keys()
        controls.values[pygame.K_w]=True
        self.g.start_race()
        self.g.countdown=0
        with patch.object(pygame.key,'get_pressed',return_value=controls):
            for _ in range(60*85):
                controls.values[pygame.K_d]=self.g.lateral<-.04
                controls.values[pygame.K_a]=self.g.lateral>.04
                controls.values[pygame.K_LSHIFT]=self.g.boost>55
                self.g.update_race(1/60)
                if self.g.mode=='finished':
                    break
        self.assertEqual(self.g.mode,'finished')
        self.assertLess(self.g.elapsed,85)
        self.assertTrue(self.g.pickups)

    def test_startup_main_loop(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.g.run()

if __name__=='__main__':
    unittest.main(verbosity=2)
