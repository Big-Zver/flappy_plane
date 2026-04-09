import math
from random import choice
import pygame as pg
from settings import Settings as St, Unit, load_image


class Triangle:
    def __init__(self, rock):
        if rock.is_up:
            self.left = rock.rect.topleft
            self.right = rock.rect.topright
            self.top = rock.rect.midbottom
        else:
            self.top = rock.rect.midtop
            self.left = rock.rect.bottomleft
            self.right = rock.rect.bottomright

    def update(self, rock):
        if rock.is_up:
            self.left = rock.rect.topleft
            self.right = rock.rect.topright
            self.top = rock.rect.midbottom
        else:
            self.top = rock.rect.midtop
            self.left = rock.rect.bottomleft
            self.right = rock.rect.bottomright

    def collide(self, plane):
        return self.collide_circle_segment(plane, self.top, self.left) or \
            self.collide_circle_segment(plane, self.top, self.right) or \
            self.collide_circle_segment(plane, self.right, self.left)

    def collide_circle_segment(self, plane, p1, p2):
        circle_pos, circle_radius = plane.rect.center, plane.collider
        cx, cy = circle_pos
        x1, y1 = p1
        x2, y2 = p2

        # Вектор отрезка
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:  # Отрезок нулевой длины (точка)
            return math.hypot(cx - x1, cy - y1) <= circle_radius

        # Находим параметр t проекции точки на прямую: t = [(C-P1) * (P2-P1)] / |P2-P1|^2
        t = ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)

        # Ограничиваем t интервалом [0, 1], чтобы остаться на ОТРЕЗКЕ
        t = max(0, min(1, t))

        # Координаты ближайшей точки на отрезке
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        # Расстояние от центра до ближайшей точки
        distance = math.hypot(cx - closest_x, cy - closest_y)

        return distance <= circle_radius


class Plane:
    def __init__(self):
        self.images = self.get_plane_images()
        self.num_image = 0
        self.image = self.images[0]
        self.timer = pg.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = St.PLANE_START_POS
        self.gravity = St.GRAVITY
        self.collider = St.PLANE_COLLIDER
        self.is_crashed = False
        self.sound_jump = pg.mixer.Sound('sounds/impactMetal_004.ogg')
        self.sound_crash = pg.mixer.Sound('sounds/lowFrequency_explosion_001.ogg')

    def get_plane_images(self):
        color = choice(St.PLANE_COLORS)
        return [load_image(f"images/Planes/plane{color}{n}.png", St.PLANE_SIZE) for n in range(1, 4)]

    def event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.gravity = St.JUMP_SPEED
                self.sound_jump.play()
        if event.type == St.PLANE_CRASH and not self.is_crashed:
            self.is_crashed = True
            self.sound_crash.play()

    def update(self):
        self.handle_animation()
        self.is_crash()
        self.rect.y += self.gravity
        if self.gravity < St.GRAVITY:
            self.gravity += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_crash(self):
        if self.rect.bottom >=St.SCREEN_SIZE[1] or self.rect.top <= 0:
            pg.event.post(pg.event.Event(St.PLANE_CRASH))

    def handle_animation(self):
        if pg.time.get_ticks() - self.timer >= St.ANIM_INTERVAL:
            self.timer = pg.time.get_ticks()
            self.num_image += 1
            if self.num_image >= len(self.images):
                self.num_image = 0
            self.image = self.images[self.num_image]


class Rock(Unit):
    def __init__(self, mode, position):
        self.is_up = choice([True, False])
        Unit.__init__(self, self.get_image(mode))
        self.start(mode)
        self.rect.x = St.SCREEN_SIZE[0]//2 * position
        self.collider = Triangle(self)
        self.back = False

    def event(self, plane):
        self.is_back(plane)
        if self.collider.collide(plane):
            pg.event.post(pg.event.Event(St.PLANE_CRASH))

    def is_back(self, plane):
        if not self.back and self.collider.right[0] <= plane.rect.centerx - plane.collider:
            self.back = True
            pg.event.post(pg.event.Event(St.ROCK_BACK))


    def get_image(self, mode):
        path = f"images/Rocks/rock{mode}"
        if self.is_up:
            path = path + "Down"
        return load_image(path+'.png', St.ROCK_SIZE)

    def start(self, mode):
        self.is_up = choice([True, False])
        self.image = self.get_image(mode)
        self.rect.left = St.SCREEN_SIZE[0] * 2
        self.back = False
        if self.is_up:
            self.rect.top = 0
        else:
            self.rect.bottom = St.SCREEN_SIZE[1]

    def update(self, mode):
        self.rect.x -= St.ROCK_SPEED
        if self.rect.right <= 0:
            self.start(mode)
        self.collider.update(self)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
