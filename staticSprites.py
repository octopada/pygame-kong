# static sprites

import sys
import pygame
from random import randint

from globalvars import *

class board:

    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(white)

class staticSprite(pygame.sprite.Sprite):

    def __init__(self, pos, image):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.top = pos[1]
        self.rect.left = pos[0]

class coin(staticSprite):
    
    pass

class wall(staticSprite):

    pass

class ladder(staticSprite):
    
    pass

class princess(staticSprite):

    pass
