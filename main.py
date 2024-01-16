# import pygame
#
# if __name__ == '__main__':
#     pygame.init()
#     pygame.display.set_caption('Движущийся круг 2')
#     size = width, height = 800, 400
#     screen = pygame.display.set_mode(size)
#
#     running = True
#     x_pos = 0
#     v = 20  # пикселей в секунду
#     fps = 60
#     clock = pygame.time.Clock()
#     while running:
#         screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEMOTION:
#                 pygame.draw.circle(screen, (0, 0, 255), event.pos, 20)
#         pygame.display.flip()
#         clock.tick(50)
#     pygame.quit()


import sys

import pygame

from button import Button


def myFunction():
    print('Button Pressed')




pygame.init()

width = 1440
height = 780

boyut = (width, height)
screen = pygame.display.set_mode(boyut)

background = pygame.image.load("Group 53.png")
background = pygame.transform.scale(background, (boyut))

font = pygame.font.Font('assets/fonts/Kodchasan-SemiBold.ttf', 55)
objects = []

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

Button(194, 352, 888, 77, font, objects, screen, 'Fast reaction', myFunction)
Button(194, 450, 888, 77, font, objects, screen, 'Collect order', myFunction)
Button(194, 548, 888, 77, font, objects, screen, 'Choose right', myFunction)
Button(194, 646, 888, 77, font, objects, screen, 'Settings', myFunction)


class Parca(pygame.sprite.Sprite):
    def __init__(self, x=width / 2, y=height / 2):
        super().__init__()

        self.image = pygame.image.load("ball.png").convert()

        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, *args):
        up, down, right, left = args

        if self.rect.x > width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = width
        if self.rect.y > height:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = height

        if right:
            self.rect.x += 10
        if left:
            self.rect.x -= 10
        if up:
            self.rect.y -= 10
        if down:
            self.rect.y += 10


parca1 = Parca()
all_sprites.add(parca1)

while True:
    keys = pygame.key.get_pressed()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        up, down, right, left = keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_LEFT]
        all_sprites.update(up, down, right, left)

    screen.blit(background, (0, 0))
    # all_sprites.draw(screen)

    for object in objects:
        object.process()

    pygame.display.update()
