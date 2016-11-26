# main game class

import sys
import pygame
from random import randint

from globalvars import *
from staticSprites import *
from movingSprites import *

class game:

    walls = pygame.sprite.Group()
    ladders = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    donkey = pygame.sprite.Group()
    princess = pygame.sprite.Group()
    fballs = pygame.sprite.Group()
    all_muh_sprites = pygame.sprite.Group()

    fb_spwn_ctr = 0
    skip = 0

    def __init__(self):

        # horizontal walls
        for i in range(0, 1200, scale[0]):

            self.wall = wall((i, 0), wImage)
            self.walls.add(self.wall)
            self.all_muh_sprites.add(self.wall)
            self.wall = wall((i, size[1]-scale[0]), wImage)
            self.walls.add(self.wall)
            self.all_muh_sprites.add(self.wall)

        # vertical walls
        for i in range(0, 450, scale[0]):

            self.wall = wall((0, scale[0]+i), wImage)
            self.walls.add(self.wall)
            self.all_muh_sprites.add(self.wall)
            self.wall = wall((size[0]-scale[0], scale[0]+i), wImage)
            self.walls.add(self.wall)
            self.all_muh_sprites.add(self.wall)
       
        # coins
        for i in range(scale[0]*5, scale[0]*36, scale[0]*6):

            for j in range(scale[0], width-scale[0]*1, scale[0]):

                if randint(0, 20) == False:

                    self.coin = coin((j, i), cImage)
                    self.coins.add(self.coin)
                    self.all_muh_sprites.add(self.coin)

        # princess chamber
        for i in range(scale[0]*1, scale[0]*15, scale[0]):

            self.wall = wall((i, scale[0]*3), wImage)
            self.walls.add(self.wall)
            self.all_muh_sprites.add(self.wall)

        
        self.ldr = ladder((i+scale[0], scale[0]*3), lImage)
        self.ladders.add(self.ldr)
        self.all_muh_sprites.add(self.ldr)

        # random level
        for i in range(scale[0]*6, scale[0]*29, scale[0]*6):

            ladders = 0
            hole = 0

            for j in range(scale[0], width-scale[0]*1, scale[0]):

                if self.skip:
                    self.skip -= 1
                if self.skip == 0: 

                    # holes
                    if randint(0, 30) == False and (hole == 0 or hole == 2):
                        
                        hole += 1
                        self.skip = 4
                        continue

                    if hole == 1 or hole == 3:

                        hole += 1
                        self.wall = wall((j, i), wImage)
                        self.walls.add(self.wall)
                        self.all_muh_sprites.add(self.wall)
                        self.skip = 5

                    # ladders
                    if randint(0, 30) == False and j < width-scale[0]*3 and ladders < 4:

                        ladders = ladders+1
                        self.ldr = ladder((j, i), lImage)
                        self.ladders.add(self.ldr)
                        self.all_muh_sprites.add(self.ldr)

                        for k in range(i, i+scale[0]*6, scale[0]):

                            self.ldr = ladder((j+scale[0], k), lImage)
                            self.ladders.add(self.ldr)
                            self.all_muh_sprites.add(self.ldr)

                        self.ldr = ladder((j+scale[0]*2, i), lImage)
                        self.ladders.add(self.ldr)
                        self.all_muh_sprites.add(self.ldr)
                        self.skip = 3

                    elif j > width-scale[0]*5 and ladders == 0:
                    
                        # emergency ladder    
                        ladders = ladders+1
                        self.ldr = ladder((j, i), lImage)
                        self.ladders.add(self.ldr)
                        self.all_muh_sprites.add(self.ldr)

                        for k in range(i, i+scale[0]*6, scale[0]):

                            self.ldr = ladder((j+scale[0], k), lImage)
                            self.ladders.add(self.ldr)
                            self.all_muh_sprites.add(self.ldr)

                        self.ldr = ladder((j+scale[0]*2, i), lImage)
                        self.ladders.add(self.ldr)
                        self.all_muh_sprites.add(self.ldr)
                        self.skip = 3

                    # walls
                    else:
                        
                        self.wall = wall((j, i), wImage)
                        self.walls.add(self.wall)
                        self.all_muh_sprites.add(self.wall)


        # player
        self.playah = player((scale[0]*3, height-2*scale[0]), pImage)
        self.all_muh_sprites.add(self.playah)

        # donkey
        self.dungi = donkey((scale[0]*2, scale[0]*5), dImage)
        self.donkey.add(self.dungi)
        self.all_muh_sprites.add(self.dungi)

        # princess
        self.prinsoo = princess((scale[0], scale[0]*2), prImage)
        self.princess.add(self.prinsoo)
        self.all_muh_sprites.add(self.prinsoo)

        # screen
        self.gameboard = board()
    
    def eventsk(self, speed, pScore):

        score = self.playah.returnScore()
            
        self.events = pygame.event.get()

        # exit game
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

        # spawn fireballs
        self.fb_spwn_ctr += 1
        if self.fb_spwn_ctr == 100:
            dpos = self.dungi.getPosition()
            self.fball = fireball((dpos[0], dpos[1]), fImage)
            self.fballs.add(self.fball)
            self.all_muh_sprites.add(self.fball)
            self.fb_spwn_ctr = 0

        # move sprites
        self.wgh = self.playah.move(self.walls, self.ladders, self.coins, self.donkey, self.princess, self.fballs, speed)
        self.dungi.move(self.walls, speed)
        for fb in self.fballs:
            fb.move(self.walls, speed)

        # kill fireballs
        for fb in self.fballs:
            self.fpos = fb.getPosition()
            if self.fpos[0] == scale[0] and self.fpos[1] == height-scale[0]*2:
                fb.kill()

        # game over
        if self.wgh == 0:
            self.gameboard.screen.fill(white)

            text = pygame.font.SysFont("None", 80)
            rtext = text.render("GAME OVER", 0, grey)
            self.gameboard.screen.blit(rtext, (440, 100))

            score = self.playah.returnScore()
            pScore += score
            finalScore = "Final Score: "+str(pScore)
            text = pygame.font.SysFont("None", 60)
            rtext = text.render(finalScore, 0, black)
            self.gameboard.screen.blit(rtext, (470, 180))

            rtext = text.render("Q to quit - R to restart", 0, black)
            self.gameboard.screen.blit(rtext, (400, 240))

            pygame.display.flip()
            
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            sys.exit()
                        if event.key == pygame.K_r:
                            self.killall()
                            return -1

        # win
        if self.wgh == 1:
            self.killall()
            return score

        return -2

    def update(self, pScore):
        
        # score
        score = self.playah.returnScore()
        pScore += score
        dScore = 'score: '+str(pScore)
        pygame.display.set_caption(dScore)

        # display part
        self.gameboard.screen.fill(white)
        self.all_muh_sprites.draw(self.gameboard.screen)
        pygame.display.flip()        

    def killall(self):

        for sprite in self.all_muh_sprites:
            sprite.kill()

    def intro(self):

        self.quit = 0
        self.leftAl = 460
        self.topAl = 150
        self.spacing = 40

        text = pygame.font.SysFont("None", 80)
        rtext = text.render("DKONG", 0, grey)
        self.gameboard.screen.blit(rtext, (self.leftAl, self.topAl+self.spacing*-2))

        text = pygame.font.SysFont("None", 40)
        rtext = text.render("AD to move", 0, black)
        self.gameboard.screen.blit(rtext, (self.leftAl+10, self.topAl))
        rtext = text.render("SPACE to jump", 0, black) 
        self.gameboard.screen.blit(rtext, (self.leftAl+10, self.topAl+self.spacing))
        rtext = text.render("WS on ladders", 0, black) 
        self.gameboard.screen.blit(rtext, (self.leftAl+10, self.topAl+self.spacing*2))
        rtext = text.render("Q to quit", 0, black) 
        self.gameboard.screen.blit(rtext, (self.leftAl+10, self.topAl+self.spacing*3))
        rtext = text.render("E to begin", 0, black) 
        self.gameboard.screen.blit(rtext, (self.leftAl+10, self.topAl+self.spacing*4))

        text = pygame.font.SysFont("None", 45)
        rtext = text.render("Get to the Princess - Avoid Fireballs and the Donkey - Collect Coins for Score", 0, black) 
        self.gameboard.screen.blit(rtext, (55, self.topAl+self.spacing*5+10))

        pygame.display.flip()

        while self.quit == 0:

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_e:
                        self.quit = 1

                    if event.key == pygame.K_q:
                        sys.exit()
