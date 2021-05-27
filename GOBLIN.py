import random
from Define import *
from Animation import *
from options import *

class BOMB():
    def __init__(self):
        self.frame = 0
        self.action = 'Bomb1'
        self.flip = False
        self.frames = {}
        self.db={}
        self.rect = pygame.Rect(10,10,10,10)

        self.db['Bomb1'] = load_animation('Data/Monster/Goblin/Bomb1',(7,7,7,7),self.frames)
        self.db['Bomb2'] = load_animation('Data/Monster/Goblin/Bomb2',(7,7,7,7),self.frames)
        self.db['Bomb3'] = load_animation('Data/Monster/Goblin/Bomb3',(4,4,4,4,4,4,4,4,4,4,4),self.frames)

        self.img = self.frames[self.db[self.action][self.frame]]

    def animation(self):
        if self.frame >= len(self.db[self.action]):
            self.frame = 0
        self.img = self.frames[self.db[self.action][self.frame]]
        self.frame+=1

    def draw(self,scroll):
        DISPLAY.blit(pygame.transform.flip(self.img,self.flip,False),(self.rect.x-scroll[0],self.rect.y-scroll[1]))

    def get_rect(self,rect_1,flip):
        self.rect.width = 0
        self.rect.height = 0

        if flip:
            self.rect.x = rect_1.x-2
            self.rect.y = rect_1.y -2

        if not flip:
            self.rect.x = rect_1.x+2+33
            self.rect.y = rect_1.y -2

class GOBLIN():
    def __init__(self,HP):
        self.db,self.frames = {},{}
        self.loc = [230,116]
        self.action ='Idle'
        self.HP = HP
        self.rect = pygame.Rect(self.loc,(33,64))
        self.flip = False
        self.frame = 0
        self.y_momentum = 0
        self.img = None
        self.speed = 1.5
        self.revive_cd = 100
        self.guard_time = 200
        self.attack_cd = 300


    def mv_check(self):
        if self.rect.x<100:
            self.rect.x = 100
            self.action = 'Idle'
        if self.rect.x>360:
            self.rect.x = 360
            self.action = 'Idle'

    def get_animation(self):
        self.db['Idle'] = load_animation('Data/Monster/Goblin/Idle',(7,7,7,7),self.frames)
        self.db['Attack'] = load_animation('Data/Monster/Goblin/Attack',(7,7,7,7,7,7,7,7,7,7,7,7),self.frames)
        self.db['Death'] = load_animation('Data/Monster/Goblin/Death',(10,10,10,10),self.frames)
        self.db['Move'] = load_animation('Data/Monster/Goblin/Move',(7,7,7,7,7,7,7,7),self.frames)
    def spawn(self,scroll):
        self.rect.width = self.img.get_width()
        self.rect.height = self.img.get_height()
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
            if self.action == 'Idle':
                self.action = 'Move'
                self.guard_time = random.randrange(10,150)
                self.flip = random.choice([True, False])

            elif self.action == 'Move':
                self.action = 'Idle'
                self.guard_time = random.randrange(200,500)

    def attack(self,rect):
        if self.flip and self.attack_cd<0:
            if rect.x in range (self.rect.x-100,self.rect.x):
                self.action = 'Attack'
                self.attack_cd = 400
                return True

        if not self.flip and self.attack_cd<0:
            if rect.x in range (self.rect.x+33,self.rect.x+150):
                self.action = 'Attack'
                self.attack_cd = 400
                return True

        elif self.attack_cd == 325:
            self.action = 'Idle'
            self.attack_cd -= 1
        else:
            self.attack_cd -= 1

    def take_dmg(self):
        i = 10
        for i in range(10):
            self.rect.x -=1
            self.HP-=1

    def kill(self):
        self.delete()