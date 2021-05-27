import sys
from pygame.locals import *
from Tile_Map import *
from options import *
from Skeleton import *
from Slime import *


def game():
    pygame.mixer.music.play(-1)
    moving_right = False
    moving_left = False
    attack = False
    hurt = False

    player_y_momentum = 0
    air_timer = 0
    map_frame = 0

    player_action = 'idle'
    player_frame = 0
    player_flip = False
    player_HP = 10
    player_hurt_cd = 0
    DMG = 1

    true_scroll = [0, 0]
    PLAYER_rect = pygame.Rect(PLAYER_location[0], PLAYER_location[1], 16, 31)

    map_rect = get_map_coll()

    monster_lst = []
    monster_1 = SKELETON(250)
    slime_1 = SLIME(50)
    monster_lst.append(slime_1)
    monster_lst.append(monster_1)
    monster_1.get_animation()
    slime_1.get_animation()
    slime_spawn_cd = 100
    slime_count = 1

    skeleton_count = 1
    skeleton_spawn_cd = 100

    ladder = False

    coin = 0
    coin_frame = 0

    health_cd = 0

    coin_total = 0
    monster_kill_total = 0
    while True:
        if player_HP <1:
            die_menu(coin_total,monster_kill_total)
        player_hurt_cd -= 1
        slime_spawn_cd -=1
        skeleton_spawn_cd -=1
        health_cd -=1
        if slime_spawn_cd<0 and slime_count < 5:
            slime = SLIME(100)
            slime.get_animation()
            monster_lst.append(slime)
            slime_count += 1
            slime_spawn_cd = 200

        if skeleton_spawn_cd<0 and skeleton_count < 2:
            ske = SKELETON(500)
            ske.get_animation()
            monster_lst.append(ske)
            skeleton_count+=1
            skeleton_spawn_cd = 500
        PLAYER_rect1 = PLAYER_rect.copy()
        true_scroll[0] += (PLAYER_rect.x-true_scroll[0]-160)/10
        true_scroll[1] += (PLAYER_rect.y-true_scroll[1]-370)/10

        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        MAP_id = MAP_db[map_frame]
        MAP_IMAGE = MAP_frames[MAP_id]
        map_frame+=1
        if map_frame >= len(MAP_db):
            map_frame = 0

        DISPLAY.blit(BACKGROUND_IMAGE,(0,0))
        DISPLAY.blit(MIDDGOUND_IMAGE,(-10-scroll[0]/20,10))
        DISPLAY.blit(MAP_IMAGE,(5-scroll[0],0-240-scroll[1]))
        print(PLAYER_rect.y)
        for monster in monster_lst:
            if monster.name == 'skeleton':
                if PLAYER_rect.y <= 115:
                    if PLAYER_rect.x - monster.rect.x < 100 :
                        monster.attack()
                    else:
                        monster.chase(PLAYER_rect)
                elif not hurt:
                    monster.guard()

            elif not hurt:
                monster.guard()

            if monster.HP < 1:
                monster_lst.remove(monster)
                if monster.name == "skeleton":
                    skeleton_count -=1
                    coin += 5
                    coin_total +=5
                    skeleton_spawn_cd = 1000
                    monster_kill_total +=1
                else:
                    slime_count -=1
                    coin += 1
                    coin_total +=1
                    slime_spawn_cd = 500
                    monster_kill_total +=1
            monster.mv_check()
            monster.animation()
            monster.spawn(scroll)

        #Player movement
        player_movement = [0,0]
        if moving_right:
            player_movement[0] += 3
        if moving_left:
            player_movement[0] -= 2.7

        player_movement[1] +=player_y_momentum
        player_y_momentum +=0.3
        if player_y_momentum > 5:
            player_y_momentum = 5

        PLAYER_rect, collisions = move(PLAYER_rect, player_movement, map_rect)

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        if collisions['top']:
            player_y_momentum = 0
        else:
            air_timer += 1

        if attack:
            player_action,player_frame = change_action(player_action,player_frame,'Attack')
            PLAYER_rect1.y = PLAYER_rect.y-10
            if player_flip:
                PLAYER_rect1.x -=30
            if not player_flip:
                PLAYER_rect1.x -=5

        elif hurt:
            moving_left = False
            moving_right = False
            if player_hurt_cd < 0:
                player_action, player_frame = change_action(player_action, player_frame, 'Hurt')
                player_HP -= 1
                player_hurt_cd = 40
                hurt = False

        elif ladder:
            player_action,player_frame = change_action(player_action,player_frame,'Ladder')
            if PLAYER_rect.y < 161:
                PLAYER_rect.y = 161
            else: PLAYER_rect.y -= 1
            player_y_momentum = 0

        elif int(player_y_momentum) < 0:
            player_action,player_frame = change_action(player_action,player_frame,'Jump')
        elif int(player_y_momentum) > 1:
            player_action,player_frame = change_action(player_action,player_frame,'Fall')


        elif player_movement[0]>0:
            player_action,player_frame = change_action(player_action,player_frame,'Run')
            player_flip = False

        elif player_movement[0]==0:
            player_action,player_frame = change_action(player_action,player_frame,'Idle')

        elif player_movement[0]<0:
            player_action,player_frame = change_action(player_action,player_frame,'Run')
            player_flip = True

        for monster in monster_lst:
            PLAYER_rect_clone = PLAYER_rect.copy()
            if PLAYER_rect.y - 225 in range(monster.rect.y, monster.rect.y + monster.rect.height):
                PLAYER_rect_clone.y = monster.rect.y + (monster.rect.height- PLAYER_rect.height )
            elif PLAYER_rect.y - 222 in range(monster.rect.y, monster.rect.y + monster.rect.height):
                PLAYER_rect_clone.y = monster.rect.y

            if monster.rect1.colliderect(PLAYER_rect_clone) and not attack:
                moving_right = False
                moving_left = False
                hurt = True
                if PLAYER_rect.x > monster.rect.x:
                    PLAYER_rect.x += 10
                else:
                    PLAYER_rect.x -= 10
                PLAYER_rect.y -= 4

            elif attack:
                PLAYER_rect_clone.x = PLAYER_rect1.x
                if monster.rect1.colliderect(PLAYER_rect_clone):
                    monster.hurt(PLAYER_rect_clone,DMG)


        player_frame += 1
        if player_frame >= len(animation_db[player_action]):
            player_frame = 0
            attack = False

        player_img_id = animation_db[player_action][player_frame]
        PLAYER_IMAGE = animation_frames[player_img_id]

        PLAYER_rect1.width = PLAYER_IMAGE.get_width()
        PLAYER_rect1.height = PLAYER_IMAGE.get_height()

        if PLAYER_rect.y>510:
            PLAYER_rect.y-=200
            PLAYER_rect.x-=20

        if PLAYER_rect.x in range (1068, 1076) :
            if player_HP < 10 and health_cd < 0:
                player_HP +=1
                health_cd = 100
            upgrade()


        DISPLAY.blit(pygame.transform.flip(PLAYER_IMAGE,player_flip,False),(PLAYER_rect1.x-scroll[0],PLAYER_rect1.y-scroll[1]-240))
        DISPLAY.blit(heart_img,(10,10))
        life(player_HP)
        show_coin(coin,coin_frame)
        show_dmg(DMG)

        coin_frame +=1
        if coin_frame==len(coin_db):
            coin_frame = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key ==K_1:
                    pygame.mixer.music.fadeout(1)
                if event.key ==K_2:
                    pygame.mixer.music.play(-1)
                if event.key == K_d or event.key == K_RIGHT and attack == False:
                    moving_right = True
                    attack = False
                if event.key == K_a or event.key==K_LEFT and attack == False:
                    moving_left = True
                    attack = False
                if event.key == K_w or event.key==K_UP and attack == False:
                    if PLAYER_rect.x == 960 :
                        ladder = True
                    elif air_timer < 6:
                        player_y_momentum = -5
                        ladder = False
                    else:
                        ladder = False

                elif event.key == K_j:
                    if attack == False:
                        swing_sound.play()
                    attack = True
                    moving_right = False
                    moving_left = False

                if event.key == K_p and PLAYER_rect.x in range (1068, 1076) and coin>=20:
                    coin -= 20
                    DMG +=1
                if event.key == K_7:
                    coin_total = 67
                    monster_kill_total = 30
                    die_menu(coin_total, monster_kill_total)

            if event.type == KEYUP:
                if event.key == K_d or event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_a or event.key==K_LEFT:
                    moving_left = False
                if event.key == K_w or event.key==K_UP and attack == False:
                    ladder = False

        surf = pygame.transform.scale(DISPLAY,WINDOW_SIZE)
        SCREEN.blit(surf,(0,0))
        pygame.display.update()
        clock.tick(60)

def main_menu():
    while True:
        SCREEN.fill((0,0,0))
        menu_txt = font_1.render('Press 1 to start game',0,(255,255,255))
        SCREEN.blit(menu_txt, (30, 30))
        menu_txt = font_1.render('Press 2 to Tutorial', 0, (255, 255, 255))
        SCREEN.blit(menu_txt, (30, 100))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    game()
                if event.key == K_2:
                    tutorial()
        pygame.display.update()
        clock.tick(60)

def tutorial():
    while True:
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(Tutor_menu, (0, 0))
        menu_txt = font_2.render('Press 1 to main menu', 0, (255, 255, 255))
        DISPLAY.blit(menu_txt, (127, 180))
        surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
        SCREEN.blit(surf, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    main_menu()
        pygame.display.update()
        clock.tick(60)

def die_menu(coin,kill):
    pygame.mixer.music.fadeout(1)
    lose_sound.play()
    while True:
        DISPLAY.blit(Die_menu, (0,0))
        txt1 = font_2.render('Coin total = '+ str(coin), 0, (0,255,0))
        DISPLAY.blit(txt1, (127, 120))
        txt2 = font_2.render('Monster killed = '+ str(kill), 0, (0,255,0))
        DISPLAY.blit(txt2, (127, 135))
        txt3 = font_2.render('Press 1 to main menu', 0, (255, 255, 255))
        DISPLAY.blit(txt3, (127, 160))
        surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
        SCREEN.blit(surf, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    main_menu()
        pygame.display.update()
        clock.tick(60)

main_menu()
