import pygame

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.mixer.set_num_channels(64)

WINDOW_SIZE = (1200,800)

SCREEN = pygame.display.set_mode(WINDOW_SIZE,0,32)
pygame.display.set_caption('DAA ADVENTURE!!!')
clock = pygame.time.Clock()

DISPLAY = pygame.Surface((384,216))

PLAYER_location = [1030,80]
BACKGROUND_IMAGE = pygame.image.load('Data/TL/Background.png')
MIDDGOUND_IMAGE = pygame.image.load('Data/TL/Middleground.png')

pygame.mixer.music.load('Data/Sound/y2mate (mp3cut.net).mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

swing_sound = pygame.mixer.Sound('Data/Sound/SwordSwing.wav')
swing_sound.set_volume(0.1)

lose_sound = pygame.mixer.Sound('Data/Sound/Die.mp3')
swing_sound.set_volume(0.5)

font = pygame.font.Font('Data/bit02.otf',10)
font_1 = pygame.font.SysFont('Data/font1.ttf',50)
font_2 = pygame.font.Font('Data/bit02.otf',15)

Die_menu = pygame.image.load("Data/Die_menu.png")
Tutor_menu = pygame.image.load("Data/Tutor_menu.png")