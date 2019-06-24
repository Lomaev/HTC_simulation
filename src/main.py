import pygame
import random
from board_module import Board
from entity_module import *

n = 5

board = Board(n, n, 70, 70, 100)

pygame.init()

screen = pygame.display.set_mode((700, 700))

all_sprites = pygame.sprite.Group()

for i in range(4):
    board.board[random.randint(0, 4)][random.randint(0, 4)].append(BaseAnimal(all_sprites, 'cat', 1000, 65))


while True:
    screen.fill(pygame.Color('White'))
    board.render(screen)
    all_sprites.draw(screen)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit(0)

    pygame.display.flip()
