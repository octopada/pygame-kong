# moving sprites

import sys
import pygame
from random import randint

from globalvars import *

class movingSprite(pygame.sprite.Sprite):
    
    wall_hit_list = pygame.sprite.Group()

    def __init__(self, pos, image):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.top = pos[1]
        self.rect.left = pos[0]
        self.dx = 0
        self.dy = 0
        self.jumping = 0

    def collision(self, move_drn, walls):

        self.ret = -1
        self.wall_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for wall in self.wall_hit_list:

            if move_drn == 0:
                self.rect.top = wall.rect.bottom   

            if move_drn == 1:
                self.rect.left = wall.rect.right
                self.ret = 3                

            # gravity induced collisions
            if move_drn == 2:
                self.rect.bottom = wall.rect.top
                self.dy = 0 # gravity reset
                self.jumping = 0 # allows new jump

            if move_drn == 3:
                self.rect.right = wall.rect.left
                self.ret = 1

        return self.ret
    
    def gravity(self):

        if self.dy == 0:
            self.dy += 1
        else:
            self.dy += 0.35

        self.rect.y += self.dy

    def getPosition(self):

        return (self.rect.left, self.rect.top)


class donkey(movingSprite):

    left = 1
    right = 0
    def move(self, walls, speed):
        
        if self.rect.x == scale[0]*2:

            self.left = 0
            self.right = 1
           
        if self.rect.x > scale[0]*30:
        
            self.left = 1
            self.right = 0

        if self.left:
            self.rect.x -= speed
        if self.right:
            self.rect.x += speed
            

class fireball(movingSprite):

    state = 0
    def move(self, walls, speed):

        self.gravity()
        self.collision(2, walls)
        if self.state == 0:
            self.rect.x += speed
        if self.state == 1:
            self.rect.x -= speed
        if self.state == 0:
            self.ch_dr = self.collision(3, walls)
            if self.ch_dr == 1:
                self.state = 1
        if self.state == 1:
            self.ch_dr = self.collision(1, walls)
            if self.ch_dr == 3:
                self.state = 0 


class player(movingSprite):

    dontjump = 0
    score = 0

    def move(self, walls, ladders, coins, donkey, princess, fballs, speed):

        self.climbing = 0
        self.dontjump = 0
        self.keys = pygame.key.get_pressed()
        
        ldr_hit_list = pygame.sprite.spritecollide(self, ladders, False)
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        coin_hit_list = pygame.sprite.spritecollide(self, coins, True)
        donkey_hit_list = pygame.sprite.spritecollide(self, donkey, False)
        princess_hit_list = pygame.sprite.spritecollide(self, princess, False)
        fireball_hit_list = pygame.sprite.spritecollide(self, fballs, False)
 
        # bumping for smoother experience    
        self.ctr = 0
        for ldr in ldr_hit_list:
            self.ctr += 1
        if self.ctr == 1 and self.rect.bottom%90 == 1 or self.rect.bottom%90 == 2 or self.rect.bottom%90 == 3 or self.rect.bottom%90 == 4:
            self.rect.y -= speed-1

        # ladder climbing
        for ldr in ldr_hit_list:
            
            self.climbing = 1            

            if self.keys[pygame.K_w]:
                self.rect.y -= speed-1
                self.move_drn = 0 # top
                self.collision(self.move_drn, walls)

            if self.keys[pygame.K_s]:
                self.rect.y += speed-1
                self.move_drn = 2
                self.collision(self.move_drn, walls)

            self.dontjump = 1 # disables jumping
        
        if self.climbing == 0:
            self.gravity()
        self.move_drn = 2 # bottom
        self.collision(self.move_drn, walls)

        # horizontal movement
        if self.keys[pygame.K_a]:
            self.rect.x += -speed
            self.move_drn = 1 # left
            self.collision(self.move_drn, walls)

        if self.keys[pygame.K_d]:
            self.rect.x += speed
            self.move_drn = 3 # right
            self.collision(self.move_drn, walls)

        # jump
        if self.dontjump == 0:
            if self.keys[pygame.K_SPACE] and self.jumping == 0:
                self.jumping = 1

            if self.jumping == 1:
                self.rect.y -= 6
                self.move_drn = 0
                self.collision(self.move_drn, walls)
                
        # coin collect
        for coin in coin_hit_list:

            self.collectCoin()

        # donkey collide
        for donkey in donkey_hit_list:
            return 0

        # princess collide
        for princess in princess_hit_list:
            return 1

        # fireball collide
        for fb in fireball_hit_list:
            return 0

        return -1

    def collectCoin(self):

        self.score += 1

    def returnScore(self):

        return self.score
