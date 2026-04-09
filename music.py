import pygame as pg


class MusicMaker:
    def __init__(self):
        self.sound1 = pg.mixer.Sound(f'sounds/samplefocus com/techno-kick-with-bass_130bpm_C#.wav')
        # self.sound2 = pg.mixer.Sound(f'sounds/samplefocus com/bassy-phonk-bouncy-lead_130bpm_C#_minor.wav')
        self.timer = pg.time.get_ticks()
        self.sound1.play()
        # self.secondplay = False

    def play(self):
        if self.sound1.get_length() <= (pg.time.get_ticks() - self.timer) / 1000:
            self.sound1.play()
            self.timer = pg.time.get_ticks()
            # self.secondplay = False
        # if self.sound2.get_length() <= (pg.time.get_ticks() - self.timer) / 1000 and not self.secondplay:
        #     self.secondplay = True
        #     self.sound2.play()

