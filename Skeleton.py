import random
from Define import *
from Animation import *
from options import *


class SKELETON():
    def __init__(self,HP):
        self.name = 'skeleton'
        self.db,self.frames = {},{}
        self.loc = [230,-150]
        self.action ='Idle'
        self.HP = HP
        self.rect = pygame.Rect(self.loc,(33,64))
        self.flip = False
        self.frame = 0
        self.y_momentum = 0
        self.img = None
        self.guard_time = 200
        self.attack_cd = 200
        self.rect1 = pygame.Rect(0,0,33,64)

    def mv_check(self):
        if self.rect.x<200:
            self.rect.x = 200
            self.action = 'Idle'
        if self.rect.x>400:
            self.rect.x = 400
            self.action = 'Idle'

    def get_animation(self):

        self.db['Idle'] = load_animation('Data/Monster/Skeleton/Idle',(7,7,7,7),self.frames)
        self.db['Attack'] = load_animation('Data/Monster/Skeleton/Attack',(3,3,3,3,3,3,10,10),self.frames)
        self.db['Death'] = load_animation('Data/Monster/Skeleton/Death',(10,10,10,10),self.frames)
        self.db['Move'] = load_animation('Data/Monster/Skeleton/Move',(10,10,10,10),self.frames)

    def spawn(self,scroll):
        self.rect.width = self.img.get_width()
        self.rect.height = self.img.get_height()
        self.rect1 = self.rect.copy()
        self.rect1.width = self.img.get_width()-10
        self.rect1.height = self.img.get_height()-5
        self.rect1.x = self.rect.x -5
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

    def attack(self):
        if self.attack_cd < 0:
            self.attack_cd = 200
            self.action, self.frame = change_action(self.action,self.frame,"Attack")

        elif self.frame >= len(self.db['Attack']):
            self.action, self.frame = change_action(self.action,self.frame,"Idle")
        else:self.attack_cd -= 1

    def chase(self,rect):
        self.action, self.frame = change_action(self.action, self.frame, "Move")

        self.flip = False
        if rect.x-60 > self.rect.x:
            self.rect.x += 1
        else:
            self.action = 'Idle'

    def hurt(self, rect ,DMG):
        if self.rect.x > rect.x:
            self.rect.x +=1
        else: self.rect.x -=1
        self.HP -= DMG

    def die(self):
        self.action, self.frame = change_action(self.action, self.frame, "Death")
