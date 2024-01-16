import os.path
import sys
import time

import pygame

from button import Button
from const import WIDTH, HEIGHT

MUSIC = {
    1: "8-bit",
    2: "Ukulele",
    3: "Mexico",
    4: "Cubism",
    5: "Morning",
    6: "High tech"
}


def myFunction():
    print('Button Pressed')


def show_menu():
    global background, buttons, texts
    background = pygame.image.load("assets/menu_screen.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    buttons = []
    texts = []
    Button(194, 352, 888, 77, font, buttons, screen, 'Fast reaction', myFunction)
    Button(194, 450, 888, 77, font, buttons, screen, 'Collect order', show_collect_order)
    Button(194, 548, 888, 77, font, buttons, screen, 'Choose right', myFunction)
    Button(194, 647, 888, 77, font, buttons, screen, 'Settings', show_settings)


def show_collect_order():
    global background, buttons, texts
    background = pygame.image.load("assets/collect_order_screen.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    buttons = []
    texts = []

    black = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    black.fill((131, 205, 235, 150))
        # black.convert_alpha()
        # black = pygame.Rect(0, 0, WIDTH, HEIGHT)
    texts.append((black, (0, 0)))
    Button(0, 0, 967, 91, font, buttons, screen, 'Menu', show_menu)


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

    background = pygame.image.load("assets/settings_screen.png")
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

background = pygame.image.load("assets/menu_screen.png")
buttons = []
texts = []

sound1 = pygame.mixer.Sound('assets/audio/sounds/MenuButtons.mp3')
font = pygame.font.Font('assets/fonts/Kodchasan-SemiBold.ttf', 55)

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


    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    for text in texts:
        screen.blit(text[0], text[1])

    for object in buttons:
        object.process()

    pygame.display.update()
