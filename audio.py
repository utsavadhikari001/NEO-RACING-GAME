from pathlib import Path
import pygame

class Audio:
    def __init__(self, settings):
        self.enabled = settings.get('sound', True) and pygame.mixer.get_init() is not None
        self.music_enabled = settings.get('music', True) and pygame.mixer.get_init() is not None
        self.sounds = {}
        self.engine_channel = None
        if pygame.mixer.get_init() is not None:
            for name in ('boost', 'drift', 'crash', 'countdown', 'finish', 'engine'):
                try:
                    self.sounds[name] = pygame.mixer.Sound(str(Path(__file__).parent / (name + '.wav')))
                except pygame.error:
                    pass

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def engine(self, speed=0):
        if not self.enabled or speed <= 0:
            if self.engine_channel is not None:
                self.engine_channel.stop()
                self.engine_channel = None
            return
        if 'engine' not in self.sounds:
            return
        if self.engine_channel is None or not self.engine_channel.get_busy():
            self.engine_channel = self.sounds['engine'].play(loops=-1)
        if self.engine_channel is not None:
            self.engine_channel.set_volume(min(.16, .025+speed/3500))

    def music(self, name):
        if not self.music_enabled:
            return
        try:
            pygame.mixer.music.load(str(Path(__file__).parent / (name + '_music.ogg')))
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
