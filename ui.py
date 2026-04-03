import pygame as pg
from settings import Settings as St, load_image

class UI:
    def __init__(self):
        self.is_on = True
        self.info = load_image("images/UI/textGetReady.png", St.INFO_SIZE)
        self.rect = self.info.get_rect()
        self.rect.center = St.SCREEN_CENTER_POS

    def event(self, event):
        if event.type == St.PLANE_CRASH:
            self.is_on = True
            self.info = load_image("images/UI/textGameOver.png", St.INFO_SIZE)
            self.rect = self.info.get_rect()
            self.rect.center = St.SCREEN_CENTER_POS

    def update(self, game_going):
        if game_going and self.is_on:
            self.is_on = False

    def draw(self, screen):
        if self.is_on:
            screen.blit(self.info, self.rect)