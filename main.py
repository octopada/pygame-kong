# main loop

import sys
import pygame

from globalvars import *
from game import *

pygame.init() 

speed = 2
pScore = 0

ngame = game()
ngame.intro()

while 1:
    re = ngame.eventsk(speed, pScore)
    ngame.update(pScore)    
    pygame.time.delay(10)
    if re == -1:
        pygame.quit()
        pygame.init()
        speed = 2
        pScore = 0
        ngame = game()
        ngame.intro()
    if re >= 0:
        pygame.quit()
        pygame.init()
        speed += 1
        pScore = pScore+re
        ngame = game()
