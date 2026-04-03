from settings import Settings as St, Unit, load_image
from pygame.transform import flip
from pygame.event import post, Event
from pygame import Surface

class Background:
    def __init__(self):
        self.unit1 = Unit(St.bg_image)
        self.unit2 = Unit(St.bg_image)
        self.unit2.rect.left = self.unit1.rect.right

        self.surf = Surface(St.SCREEN_SIZE).convert_alpha()
        self.surf.fill((0, 0, 0, 25))

    def update(self):
        self.unit1.rect.x -= St.bg_speed
        self.unit2.rect.x -= St.bg_speed
        if self.unit1.rect.right <= 0:
            self.unit1.rect.left = self.unit2.rect.right
        if self.unit2.rect.right <= 0:
            self.unit2.rect.left = self.unit1.rect.right

    def draw(self, screen):
        self.unit1.draw(screen)
        self.unit2.draw(screen)
        screen.blit(self.surf, (0, 0))


class Foreground:
    def __init__(self, mode, second=False):
        self.images_top = {}
        self.images_bottom = {}
        self.get_images()

        self.image_top = self.images_top[mode]
        self.image_bottom = self.images_bottom[mode]
        self.rect_top = self.image_top.get_rect()
        self.rect_bottom = self.image_bottom.get_rect()
        self.rect_bottom.bottom = St.SCREEN_SIZE[1]

        if second:
            self.rect_top.x += St.SCREEN_SIZE[0]
            self.rect_bottom.x += St.SCREEN_SIZE[0]

    def get_images(self):
        for mode in St.ROCKS_MODE:
            image = load_image(f"images/Rocks/rock{mode}.png", St.FG_SIZE)
            self.images_bottom[mode] = image
            self.images_top[mode] = flip(image, True, True)

    def update(self, mode):
        self.rect_top.x -= St.ROCK_SPEED
        self.rect_bottom.x -= St.ROCK_SPEED
        if self.rect_top.right <= 0:
            self.start(mode)
            post(Event(St.CHANGE_MODE))

    def start(self, mode):
        self.rect_top.x = St.SCREEN_SIZE[0]
        self.rect_bottom.x = St.SCREEN_SIZE[0]
        self.image_top = self.images_top[mode]
        self.image_bottom = self.images_bottom[mode]

    def draw(self, screen):
        screen.blit(self.image_top, self.rect_top)
        screen.blit(self.image_bottom, self.rect_bottom)

