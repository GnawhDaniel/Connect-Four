import pygame
import sys
from singleplayer import SPGame
from multiplayer import MPGame

pygame.init()
pygame.font.init()

size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")
screen.fill((255, 255, 255))

FONT = pygame.font.Font('assets/RockSalt-Regular.ttf', 23)
FONT_TITLE = pygame.font.Font('assets/RockSalt-Regular.ttf', 50)

title = FONT_TITLE.render("Connect Four", True, (0, 0, 0))
screen.blit(title, title.get_rect(center=(screen.get_width()//2, 200)))

sp = FONT.render("Single Player", True, (0, 0, 0))
mp = FONT.render("Multiplayer",   True, (0, 0, 0))

sp_button = pygame.Rect((0, 0, 200, 100))
sp_button.center = sp_width, sp_height = (screen.get_width() // 2, HEIGHT - 400)

mp_button = pygame.Rect((0, 0, 200, 100))
mp_button.center = mp_width, mp_height = (screen.get_width() // 2, HEIGHT - 300)

while True:
    clicked = False
    x, y = pygame.mouse.get_pos()

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            sys.exit()
        if evt.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

    screen.fill("white")

    if (sp_height - 50 < y < sp_height + 50) and (sp_width - 100 < x < sp_width + 100):
        pygame.draw.rect(screen, (200, 200, 200), sp_button)
        if clicked:
            SPGame()
    elif (mp_height - 50 < y < mp_height + 50) and (mp_width - 100 < x < mp_width + 100):
        pygame.draw.rect(screen, (200, 200, 200), mp_button)
        if clicked:
            screen.fill("white")
            MPGame()

    screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 200)))
    screen.blit(sp, sp.get_rect(center=sp_button.center))
    screen.blit(mp, mp.get_rect(center=mp_button.center))

    pygame.display.update()


