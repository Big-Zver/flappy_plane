import pygame as pg

from background import Background, Foreground
from settings import Settings as St, Saver
from sprites import Plane, Rock
from random import choice

from ui import UI


class Game:
    def __init__(self):
        self.running = True
        self.going = False
        self.screen = pg.display.set_mode(St.SCREEN_SIZE)
        self.rock_mode = choice(St.ROCKS_MODE)
        self.clock = pg.time.Clock()
        self.background = Background()
        self.plane = Plane()
        self.rocks = [Rock(self.rock_mode, i+2) for i in range(4)]
        self.foregrounds = [Foreground(self.rock_mode, i) for i in range(2)]
        self.ui = UI()
        self.score = 0
        self.record = Saver.read()

    def start(self):
        self.going = False
        self.rock_mode = choice(St.ROCKS_MODE)
        self.background = Background()
        self.plane = Plane()
        self.rocks = [Rock(self.rock_mode, i + 2) for i in range(4)]
        self.foregrounds = [Foreground(self.rock_mode, i) for i in range(2)]
        self.ui = UI()
        self.score = 0

    def run(self):
        pg.init()
        while self.running:
            self.event()
            if self.going:
                self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(St.FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_SPACE and not self.going:
                    if not self.plane.is_crashed:
                        self.going = True
                    else:
                        self.start()

            if event.type == pg.QUIT:
                self.running = False

            if event.type == St.PLANE_CRASH:
                self.going = False
                Saver.save(self.record)

            if event.type == St.CHANGE_MODE:
                self.rock_mode = choice(St.ROCKS_MODE)

            if event.type == St.ROCK_BACK:
                self.score += 1
                if self.score >= self.record:
                    self.record = self.score

            self.plane.event(event)
            self.ui.event(event, f"SCORE{self.score}", f"RECORD{self.record}")
        for rock in self.rocks:
            rock.event(self.plane)

    def update(self):
        self.background.update()
        self.plane.update()
        for rock in self.rocks:
            rock.update(self.rock_mode)
        for fg in self.foregrounds:
            fg.update(self.rock_mode)
        self.ui.update(self.going)


    def draw(self):
        self.background.draw(self.screen)
        self.plane.draw(self.screen)
        for rock in self.rocks:
            rock.draw(self.screen)
        for fg in self.foregrounds:
            fg.draw(self.screen)
        self.ui.draw(self.screen)



if __name__ == '__main__':
    game = Game()
    game.run()