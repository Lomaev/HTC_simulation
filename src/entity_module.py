import pygame
import os


def load_image(name, colorkey=None):
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


class BaseAnimal(pygame.sprite.Sprite):
    def __init__(self, group, kind, power, size):  # kind - grass-feeding or predator, size - size of sprite rect.
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('cat.jpg', colorkey=-1), (size, size))
        self.rect = self.image.get_rect()
        self.kind = kind
        self.power = power
