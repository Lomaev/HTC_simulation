import pygame
import random
from entity_module import *


class Board:
    def __init__(self, cols, rows, cell_size, top, left, grassfeeding_count, sprite_group):
        self._cols = cols
        self._rows = rows
        self._cell_size = cell_size
        self._top = top
        self._left = left
        self.sprite_group = sprite_group
        self.grassfeeding_count = grassfeeding_count
        self.board = [[[] for __ in range(cols)] for _ in range(rows)]

    def move(
            self):  # Only moves animals and watchers on board. Doesnt move them on screen and doesnt check interactions.
        new_board = [[[] for __ in range(self._cols)] for _ in range(self._rows)]
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                for entity in elem:
                    new_i, new_j = entity.move(i, j, self._rows, self._cols)
                    new_board[new_i][new_j].append(entity)

        self.board = new_board

    def interact(self):
        new_board = [[[] for __ in range(self._cols)] for _ in range(self._rows)]
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                for entity in elem:  # Checking interactions.
                    for target in elem:
                        if entity is not target and entity.check_interaction(target):
                            break
                for entity in elem:  # Deleting dead.
                    if entity.alive:
                        new_board[i][j].append(entity)
                    elif type(entity) == Plant:
                        new_board[random.randint(0, self._rows - 1)][random.randint(0, self._cols - 1)].append(
                            Plant(self.sprite_group, random.randint(0, 40), random.randint(100, 200),
                                  self._cell_size - 5))
                        entity.kill()
                    else:
                        if type(entity) == GrassFeeding:
                            self.grassfeeding_count -= 1
                        entity.kill()

        self.board = new_board

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('Black'),
                         ((self._left, self._top),
                          (self._cell_size * self._cols, self._cell_size * self._rows)), 2)
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                self.render_cell(screen, elem, (i, j))

    def render_cell(self, screen, cell, pos):
        pygame.draw.rect(screen, pygame.Color('Black'),
                         ((self._left + self._cell_size * pos[1], self._top + self._cell_size * pos[0]),
                          (self._cell_size, self._cell_size)), 1)

        for sprite in cell:
            sprite.rect.x = self._left + self._cell_size * pos[1] + 2
            sprite.rect.y = self._top + self._cell_size * pos[0] + 2

    def check_grassfeeding(self):
        return self.grassfeeding_count

    def get_cell(self, left, top):
        top_cell = (top - self._top) // self._cell_size
        left_cell = (left - self._left) // self._cell_size
        if 0 <= top_cell < self._cols and 0 <= left_cell < self._rows:
            return top_cell, left_cell
        else:
            return None

    def get_item(self, row, col):
        if 0 < row < self._rows and 0 < col < self._cols:
            return self.board[row][col]
        else:
            return None

    def set_item(self, col, row, item):
        self.board[row][col] = item

    def click(self, left, top):
        pos = self.get_cell(left, top)

