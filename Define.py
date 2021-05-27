from options import *
from Animation import *

def swap(sw):
    if sw == True:
        return False
    elif sw == False:
        return True

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0]>0:
            rect.right = tile.left
            collision_types['right'] =True
        elif movement[0]<0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1]>0:
            rect.bottom = tile.top
            collision_types['bottom']=True
        elif movement[1]<0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def hurt(rect1,rect2):
    rect1.y -= 2
    if rect1.x > rect2:
        return 3
    else:
        return -3

def life(HP):
    HP_text = font.render("X  "+ str(HP),False, (240,0,0))
    DISPLAY.blit(HP_text,(38,12))

def show_coin(coin,frame):
    DISPLAY.blit(coin_frames[coin_db[frame]],(300,10))
    coin_text = font.render("X  "+ str(coin),False, (240,0,0))
    DISPLAY.blit(coin_text,(320,12))

def upgrade():
    HP_text_1 = font.render("   Press P to LV Up !!!", False, (127,255,0))
    HP_text_2 = font.render("Cost: 20 GOLD", False, (127,255,0))
    DISPLAY.blit(HP_text_1, (120, 100))
    DISPLAY.blit(HP_text_2, (140, 110))

def show_dmg(DMG):
    HP_text = font.render("LV: "+ str(DMG),False, (240,0,0))
    DISPLAY.blit(HP_text,(170,12))

