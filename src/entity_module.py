import pygame
import os
import random


def load_image(name, colorkey=None):
    print(name, 'loaded.')
    if type(name) != str:
        fullname = os.path.join('data', *name)
    else:
        fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
            image = image.convert_alpha()
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class ImageLoader:
    img = None

    @classmethod
    def get_class_image(cls, image_name):
        if not cls.img:
            cls.img = load_image(image_name, colorkey=-1)

        return cls.img


class BaseAnimal(pygame.sprite.Sprite, ImageLoader):
    def __init__(self, group, power, name):
        super().__init__(group)
        self.alive = True
        self.power = power
        self.name = name

    def move(self, i, j, rows, cols):
        print('Animal', self.name, 'moved from', i, j, 'to', end=' ')
        off_i, off_j = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        i += off_i
        j += off_j
        if i < 0:
            i = rows + i
        elif i == rows:
            i = 0
        if j < 0:
            j = cols + j
        elif j == cols:
            j = 0
        print(i, j)

        return i, j


class SmallPredator(BaseAnimal):
    def __init__(self, group, power, name, size):
        super().__init__(group, power, name)
        self.image = pygame.transform.scale(self.get_class_image('cat.jpg'), (size, size))
        self.rect = self.image.get_rect()

    def check_interaction(self, target):
        if type(target) == GrassFeeding and target.alive and target.power < self.power:
            print('Small predator', self.name, 'eat', target.name)
            if self.power + target.power // 2 < 200:
                self.power += target.power // 2
            else:
                self.power = 200
            target.alive = False
            return True
        else:
            return False


class GrassFeeding(BaseAnimal):
    def __init__(self, group, power, name, size):
        super().__init__(group, power, name)
        self.image = pygame.transform.scale(self.get_class_image('grass-feeding.jpg'), (size, size))
        self.rect = self.image.get_rect()

    def check_interaction(self, target):
        if type(target) == Plant and target.alive:
            print('Grass feeding', self.name, 'eat plant', target.name)
            if self.power + target.food_value < 400:
                self.power += target.food_value
            else:
                self.power = 400
            target.alive = False
            return True
        else:
            return False


class BigPredator(BaseAnimal):
    def __init__(self, group, power, name, size):
        super().__init__(group, power, name)
        self.image = pygame.transform.scale(self.get_class_image('lion.jpg'), (size, size))
        self.rect = self.image.get_rect()

    def check_interaction(self, target):
        if target is self:
            return False
        if (type(target) == GrassFeeding or type(
                target) == SmallPredator) and target.alive and target.power < self.power:
            print('Big predator', self.name, 'eat', type(target), 'with power', target.power)
            if self.power + target.power // 2 < 300:
                self.power += target.power // 2
            else:
                self.power = 300
            target.alive = False
            return True
        elif type(target) == BigPredator and random.randint(0, 1):
            print('Big predator', self.name, 'hit', target.name, 'decreasing his power by', self.power // 2)
            target.power -= self.power // 2
            if target.power <= 0:
                target.alive = False
            return True
        else:
            return False


class Plant(pygame.sprite.Sprite, ImageLoader):
    def __init__(self, group, food_value, name, size):
        super().__init__(group)
        self.alive = True
        self.image = pygame.transform.scale(self.get_class_image('plant.jpg'), (size, size))
        self.rect = self.image.get_rect()
        self.food_value = food_value
        self.name = name

    def move(self, i, j, rows, cols):
        return i, j

    def check_interaction(self, target):
        return True


class Watcher(pygame.sprite.Sprite, ImageLoader):
    def __init__(self, group, name, size):
        super().__init__(group)
        self.image = pygame.transform.scale(self.get_class_image('man.jpg'), (size, size))
        self.rect = self.image.get_rect()
        self.name = name

    def move(self, i, j, rows, cols):
        new_i, new_j = random.randint(0, rows - 1), random.randint(0, cols - 1)
        print('Watcher', self.name, 'moved from', i, j, 'to', new_i, new_j)
        return new_i, new_j

    def check_interaction(self, target):
        if target is not self and target.alive:
            print('Watcher', self.name, 'see', type(target), 'and name it', target.name)
        if type(target) == Plant:
            target.alive = False
        return False
