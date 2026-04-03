import pygame as pg
pg.display.set_caption("FlappyPlane")


def load_image(path, size):
    image = pg.image.load(path)
    return pg.transform.scale(image, size)


class Settings:
    SCREEN_GRADE = 110
    SCREEN_SIZE = (SCREEN_GRADE * 16, int(SCREEN_GRADE * 9.6))
    SCREEN_CENTER_POS = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
    FPS = 60

    BG_SIZE = SCREEN_SIZE
    bg_image = load_image('images/Ground/background.png', BG_SIZE)
    bg_speed = 1

    FG_SIZE = (SCREEN_SIZE[0], SCREEN_SIZE[1]//15)

    PLANE_SIZE = [i//10 for i in SCREEN_SIZE]
    PLANE_START_POS = [SCREEN_SIZE[0] // 3, SCREEN_SIZE[1] // 2]
    PLANE_COLORS = ["Blue", "Green", "Red", "Yellow"]
    ANIM_INTERVAL = 100
    GRAVITY = SCREEN_GRADE // 10
    JUMP_SPEED = int(GRAVITY * 1.5 * -1)
    PLANE_COLLIDER = SCREEN_GRADE // 2

    ROCKS_MODE = ["Rock", "Grass", "Ice", "Snow"]
    ROCK_SIZE = [SCREEN_SIZE[0] // 20, SCREEN_SIZE[1] // 2]
    ROCK_SPEED = SCREEN_GRADE // 10

    INFO_SIZE = [SCREEN_SIZE[0] // 4, SCREEN_SIZE[1] // 8]

    CHANGE_MODE = pg.USEREVENT + 1
    PLANE_CRASH = pg.USEREVENT + 2


class Unit:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)