import pygame
import random
from board_module import Board
from entity_module import *

n = 20

pygame.init()

screen = pygame.display.set_mode((700, 700))

all_sprites = pygame.sprite.Group()

board = Board(n, n, 35, 0, 0, 3, all_sprites)

for i in range(3):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(GrassFeeding(all_sprites, random.randint(0, 20), str(i+4), 35))
for i in range(3):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(SmallPredator(all_sprites, random.randint(50, 200), str(i+1), 35))
for i in range(2):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(BigPredator(all_sprites, random.randint(200, 300), str(i+7), 35))
for i in range(5):
    board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(Plant(all_sprites, random.randint(0, 40), 'kust', 35))
board.board[random.randint(0, n-1)][random.randint(0, n-1)].append(Watcher(all_sprites, 'Man', 35))

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
            board.interact()

    move_time += move_clock.tick()
    if move_time > 100 and board.check_grassfeeding():
        move_time = 0
        board.move()
        board.interact()

    pygame.display.flip()
