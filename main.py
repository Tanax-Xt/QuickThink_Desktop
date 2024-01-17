import os.path
import sys
import time
from random import shuffle, sample

import pygame

from button import Button
from const import WIDTH, HEIGHT
from database import DataBase

MUSIC = {
    1: "8-bit",
    2: "Ukulele",
    3: "Mexico",
    4: "Cubism",
    5: "Morning",
    6: "High tech"
}

FAST_REACTION = 0
COLLECT_ORDER = 0
CHOOSE_RIGHT = 0


class Card(pygame.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.im = pygame.image.load(f'assets/collect_order_cards/image{num}.png')
        self.coords = (WIDTH / 2 - self.im.get_rect().width / 2, HEIGHT / 2 - self.im.get_rect().height / 2)
        self.show = False
        self.pressed = False

    def update(self, coords=None):
        buttonRect = pygame.Rect(*self.coords, 228, 228)
        mousePos = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mousePos) and self.show:
            if pygame.mouse.get_pressed(num_buttons=3)[0] and not self.pressed:
                check_collect_order(self.num)
                self.pressed = True

        if not self.pressed:
            screen.blit(self.im, self.coords if coords is None else coords)


def myFunction():
    print('Button Pressed')


def show_menu():
    global background, buttons, texts, FAST_REACTION, COLLECT_ORDER, CHOOSE_RIGHT
    FAST_REACTION = 0
    COLLECT_ORDER = 0
    CHOOSE_RIGHT = 0
    background = pygame.image.load("assets/screens/menu_screen.png")
    buttons = []
    texts = []
    Button(194, 352, 888, 77, font, buttons, screen, 'Fast reaction', myFunction)
    Button(194, 450, 888, 77, font, buttons, screen, 'Collect order', show_collect_order)
    Button(194, 548, 888, 77, font, buttons, screen, 'Choose right', myFunction)
    Button(194, 647, 888, 77, font, buttons, screen, 'Settings', show_settings)


def start_screen(text):
    black = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    black.fill((131, 205, 235, 150))
    texts.append((black, (0, 0)))

    screen_text = ru_font.render(text, True, '#ffffff')
    texts.append(
        (screen_text, (WIDTH / 2 - screen_text.get_rect().width / 2, HEIGHT / 2 - screen_text.get_rect().height / 2)))
    instruction = ru_font.render('Нажми ПРОБЕЛ, чтобы начать!', True, '#ffffff')
    texts.append((instruction, (WIDTH / 2 - instruction.get_rect().width / 2, 550)))


def finish_screen(game, score):
    black = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    black.fill((131, 205, 235, 150))
    texts.append((black, (0, 0)))
    print(database.get_result(game))
    database.add_result(game, score)

    instruction = font.render('Game over!', True, '#ffffff')
    texts.append((instruction, (WIDTH / 2 - instruction.get_rect().width / 2, 120)))

    results = ru_font.render('Предыдущие результаты:', True, '#ffffff')
    texts.append((results, (WIDTH / 2 - results.get_rect().width / 2, 250)))
    for j, i in enumerate(database.get_result(game)):
        results_i = ru_font.render(f'{j + 1}. {i[2]} – {i[1]} очков', True, '#ffffff')
        texts.append((results_i, (WIDTH / 2 - results_i.get_rect().width / 2, 320 + 70 * j)))


def show_collect_order():
    global background, buttons, texts, COLLECT_ORDER
    background = pygame.image.load("assets/screens/collect_order_screen.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    buttons = []
    texts = []
    COLLECT_ORDER = -1
    start_screen('Запомни 6 карточек и отметь их в правильном порядке')


def game_collect_order():
    global texts, order, cards
    texts = []
    Button(0, 0, 967, 91, font, buttons, screen, 'Menu', show_menu)
    order.clear()
    order = [i for i in range(6)]
    shuffle(order)
    cards = pygame.sprite.Group()
    for i in range(6):
        cards.add(Card(order[i]))
    show = 0
    screen.blit(background, (0, 0))
    pygame.display.update()
    while COLLECT_ORDER not in [0, 2]:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        if show < 6:
            screen.blit(background, (0, 0))
            cards.sprites()[show].update()
            cards.sprites()[show].show = True
            show += 1
            if show > 0:
                # pygame.display.update()
                time.sleep(0.8)
        elif show == 6:
            screen.blit(background, (0, 0))
            show += 1
            for object in buttons:
                object.update()
            for i, j in enumerate(sample(range(6), 6)):
                cards.sprites()[i].coords = (140 + 478.5 * (j % 3), 108 + 240 * (j // 3))
            cards.update()
            # pygame.display.update()
        else:
            screen.blit(background, (0, 0))
            cards.update()

        for object in buttons:
            object.update()

        pygame.display.update()

    if COLLECT_ORDER == 2:
        finish_screen('collect_order', 60 - 10 * len(order))
    # im = pygame.image.load("ball.png").convert()
    # screen.blit(im, (500, 500))
    # screen.blit(background, (0, 0))
    # pygame.time.wait(3000)


def check_collect_order(num):
    global COLLECT_ORDER, cards, order
    if num == order[0]:
        print(1)
        order.pop(0)
        cards.remove(cards.sprites()[0])
        if len(order) == 0:
            COLLECT_ORDER = 2
    else:
        COLLECT_ORDER = 2



def show_settings():
    def turn_mode():
        with open('data/sounds.txt', 'r') as f:
            mode = f.read()

        if mode == 'on':
            mode = 'off'
        else:
            mode = 'on'

        with open('data/sounds.txt', 'w') as f:
            f.write(mode)

        load_music()
        buttons.pop()
        Button(460, 428, 495, 90, font, buttons, screen, f'Turn {mode}', turn_mode, True)
        time.sleep(0.15)

    def music_down():
        with open('data/music.txt', 'r') as f:
            music_num = int(f.read())

        music_num = music_num - 1 if music_num > 1 else 6

        with open('data/music.txt', 'w') as f:
            f.write(str(music_num))

        texts[0] = (font.render(MUSIC[music_num], True, '#00BFFF'), (590, 590))
        load_music()

    def music_up():
        with open('data/music.txt', 'r') as f:
            music_num = int(f.read())

        music_num = music_num + 1 if music_num < 6 else 1

        with open('data/music.txt', 'w') as f:
            f.write(str(music_num))

        texts[0] = (font.render(MUSIC[music_num], True, '#00BFFF'), (590, 590))
        load_music()

    global background, buttons, texts

    with open('data/sounds.txt', 'r') as f:
        mode = f.read()
    if mode == 'on':
        sound1.play()

    background = pygame.image.load("assets/screens/settings_screen.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    buttons = []
    texts = []

    with open('data/music.txt', 'r') as f:
        music_num = int(f.read())

    music_name_text = font.render(MUSIC[music_num], True, '#00BFFF')
    # screen.blit(music_name_text, (530, 590))
    texts.append((music_name_text, (590, 590)))

    Button(0, 0, 967, 91, font, buttons, screen, 'Menu', show_menu)
    Button(430, 580, 135, 90, font, buttons, screen, '<', music_down)
    Button(930, 580, 135, 90, font, buttons, screen, '>', music_up)
    with open('data/sounds.txt', 'r') as f:
        mode = f.read()
        Button(460, 428, 495, 90, font, buttons, screen, f'Turn {mode}', turn_mode, True)


def check_sounds_data():
    if not os.path.exists('data/sounds.txt'):
        with open('data/sounds.txt', 'w', encoding='utf-8') as f:
            f.write('on')
    if not os.path.exists('data/music.txt'):
        with open('data/music.txt', 'w', encoding='utf-8') as f:
            f.write('1')


def load_music():
    with open('data/sounds.txt', 'r') as f:
        mode = f.read()
        if mode == 'on':
            with open('data/music.txt') as f1:
                n = f1.read()
                pygame.mixer.music.load(f'assets/audio/music{n}.mp3')
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("assets/screens/menu_screen.png")
buttons = []
texts = []

order = []
cards = pygame.sprite.Group()

sound1 = pygame.mixer.Sound('assets/audio/sounds/MenuButtons.mp3')
font = pygame.font.Font('assets/fonts/Kodchasan-SemiBold.ttf', 55)
ru_font = pygame.font.Font('assets/fonts/ISOCPEUR.ttf', 55)
database = DataBase('data/data.sqlite3')

show_menu()
check_sounds_data()
load_music()

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# class Parca(pygame.sprite.Sprite):
#     def __init__(self, x=WIDTH / 2, y=HEIGHT / 2):
#         super().__init__()
#
#         self.image = pygame.image.load("ball.png").convert()
#
#         self.image.set_colorkey((0, 0, 0))
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)
#
#     def update(self, *args):
#         up, down, right, left = args
#
#         if self.rect.x > WIDTH:
#             self.rect.x = 0
#         if self.rect.x < 0:
#             self.rect.x = WIDTH
#         if self.rect.y > HEIGHT:
#             self.rect.y = 0
#         if self.rect.y < 0:
#             self.rect.y = HEIGHT
#
#         if right:
#             self.rect.x += 10
#         if left:
#             self.rect.x -= 10
#         if up:
#             self.rect.y -= 10
#         if down:
#             self.rect.y += 10
#
#
# parca1 = Parca()
# all_sprites.add(parca1)

while True:
    keys = pygame.key.get_pressed()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
    #     up, down, right, left = keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_LEFT]
    #     all_sprites.update(up, down, right, left)
    # print(FAST_REACTION, COLLECT_ORDER, CHOOSE_RIGHT)

    # Start screen
    if -1 in [FAST_REACTION, COLLECT_ORDER, CHOOSE_RIGHT]:
        while not keys[pygame.K_SPACE]:
            keys = pygame.key.get_pressed()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            screen.blit(background, (0, 0))
            # all_sprites.draw(screen)

            for text in texts:
                screen.blit(text[0], text[1])
            pygame.display.update()
        # print(-1)
        FAST_REACTION = 1 if FAST_REACTION == -1 else 0
        COLLECT_ORDER = 1 if COLLECT_ORDER == -1 else 0
        CHOOSE_RIGHT = 1 if CHOOSE_RIGHT == -1 else 0
        texts = []

    screen.blit(background, (0, 0))
    # all_sprites.draw(screen)

    for text in texts:
        screen.blit(text[0], text[1])

    for object in buttons:
        object.update()

    if COLLECT_ORDER == 1:
        game_collect_order()

    pygame.display.update()

database.close()
