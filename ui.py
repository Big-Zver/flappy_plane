from settings import Settings as St, load_image

class UI:
    def __init__(self):
        self.is_on = True
        self.info = load_image("images/UI/textGetReady.png", St.INFO_SIZE)
        self.rect = self.info.get_rect()
        self.rect.center = St.SCREEN_CENTER_POS
        self.score_writer = TextWriter()
        self.record_writer = TextWriter(True)

    def event(self, event, score_text, record_text):
        self.score_writer.event(event, score_text)
        self.record_writer.event(event, record_text)
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
        else:
            self.score_writer.draw(screen)
            self.record_writer.draw(screen)


class TextWriter:
    def __init__(self, is_right = False):
        self.symbols = {}
        self.get_letters()
        self.get_numbers()
        self.text = ''
        self.images = []
        self.rects = []
        self.is_right = is_right
        self.start_x = 0 if not self.is_right else St.SCREEN_SIZE[0]
        self.start_y = 0

    def get_letters(self):
        for letter in "QWERTYUIOPASDFGHJKLZXCVBNM":
            self.symbols[letter] = load_image(f"images/Letters/letter{letter}.png", St.SYMBOL_SIZE)

    def get_numbers(self):
        for num in "1234567890":
            self.symbols[num] = load_image(f"images/Numbers/number{num}.png", St.SYMBOL_SIZE)

    def event(self, event, text):
        if event.type == St.ROCK_BACK:
            self.images, self.rects = self.set_images(text)

    def set_images(self, text):
        images = []
        rects = []
        x = self.start_x
        y = self.start_y
        if self.is_right:
            text = text[::-1]
            x -= St.SYMBOL_SIZE[0]
        for symbol in text.upper():
            image = self.symbols[symbol]
            rect = image.get_rect(x=x, y=y)
            images.append(image)
            rects.append(rect)
            x += St.SYMBOL_SIZE[0] if not self.is_right else -St.SYMBOL_SIZE[0]
        return images, rects

    def draw(self, screen):
        for i in range(len(self.images)):
            screen.blit(self.images[i], self.rects[i])