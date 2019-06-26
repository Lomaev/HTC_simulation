import pygame
import random
from board_module import Board
from entity_module import *

n = 6

board = Board(n, n, 70, 70, 100)

pygame.init()

screen = pygame.display.set_mode((700, 700))

all_sprites = pygame.sprite.Group()

for i in range(3):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(GrassFeeding(all_sprites, 1000, str(i+4), 65))
for i in range(3):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(SmallPredator(all_sprites, 1000, str(i+1), 65))
for i in range(5):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(Plant(all_sprites, 1000, 'kust', 65))

#board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(Watcher(all_sprites, 'Test', 65))

move_clock = pygame.time.Clock()
move_time = 0
while True:
    screen.fill(pygame.Color('White'))
    board.render(screen)
    all_sprites.draw(screen)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.move()

    '''move_time += move_clock.tick()
    if move_time > 100:
        move_time = 0
        board.move()'''

    pygame.display.flip()
