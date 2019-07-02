# import pygame
import random
from entity_module import *
from log_module import print_to_log


class Board:
    def __init__(self, cols, rows, grassfeeding_count):
        self._cols = cols
        self._rows = rows
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
                            Plant(random.randint(0, 40), random.randint(100, 200)))
                    else:
                        if type(entity) == GrassFeeding:
                            self.grassfeeding_count -= 1

        self.board = new_board

    def to_json_model(self):  # TODO normal view model.
        new_board = [[[] for __ in range(self._cols)] for _ in range(self._rows)]
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                for entity in elem:
                    new_board[i][j].append(entity.__class__.__name__)

        return new_board

    def check_grassfeeding(self):
        return self.grassfeeding_count
