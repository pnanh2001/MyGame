import random
from Define import *
from Animation import *
from options import *


class SLIME():
    def __init__(self,HP):
        self.name = 'slime'
        self.db,self.frames = {},{}
        self.loc = [200,227]
        self.action ='Idle'
        self.HP = HP
        self.rect = pygame.Rect(self.loc,[33,64])
        self.flip = False
        self.frame = 0
        self.img = None
        self.guard_time = 200
        self.rect1 = pygame.Rect(0,0,33,64)


    def mv_check(self):
        if self.rect.x<100:
            self.rect.x = 100
            self.action = 'Idle'
        if self.rect.x>360:
            self.rect.x = 360
            self.action = 'Idle'

    def get_animation(self):
        self.db['Idle'] = load_animation('Data/Monster/Slime/Idle',(10,10,10,10),self.frames)
        self.db['Move'] = load_animation('Data/Monster/Slime/Move',(7,7,7,7,7),self.frames)

    def spawn(self,scroll):
        self.rect.width = self.img.get_width()
        self.rect.height = self.img.get_height()
        self.rect1 = self.rect.copy()
        self.rect1.width = self.img.get_width()-7
        self.rect1.height = self.img.get_height()-4
        self.rect1.x = self.rect.x +2
        DISPLAY.blit(pygame.transform.flip(self.img,self.flip,False),(self.rect.x-scroll[0],self.rect.y-scroll[1]))

    def animation(self):
        if self.frame >= len(self.db[self.action]):
            self.frame = 0
        self.img = self.frames[self.db[self.action][self.frame]]
        self.frame+=1

    def guard(self):
        self.guard_time -= 1
        if self.action == 'Move':
            if self.flip == False:
                self.rect.x +=1
            else:
                self.rect.x -=1

        if self.guard_time == 0:
            if self.action != 'Move':
                self.action = 'Move'
                self.guard_time = random.randrange(10,150)
                self.flip = random.choice([True, False])

            elif self.action != 'Idle':
                self.action = 'Idle'
                self.guard_time = random.randrange(200,500)

    def hurt(self,rect,DMG):
        self.rect.x -=2
        self.HP -= DMG

    def die(self):
        pass