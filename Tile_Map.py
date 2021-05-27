import pygame

def load_map(path):
    f = open(path)
    data = f.read()
    f.close()
    data = data.split('\n')
    map = []
    for row in data:
        map.append(list(row.split(",")))
    return map

map = load_map('Data/Map_2.txt')

def get_map_coll():
    map_rect = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile != '0':
                map_rect.append(pygame.Rect(x*16,y*16,16,16))
            x+=1
        y+=1
    return map_rect

MAP_data = []
MAP_frames ={}
def load_map_frames(path,frame_duration):
    n=1
    for frame in frame_duration:
        map_path = path.split('/')[-1]
        map_name = map_path +'_'+ str(n)
        map_lc = path + '/' + map_name + '.png'
        MAP_img = pygame.image.load(map_lc)
        MAP_frames[map_name] = MAP_img.copy()
        for i in range(frame):
            MAP_data.append(map_name)
        n+=1
    return MAP_data

MAP_db = load_map_frames('Data/Map',(10,10,10,10))
heart_img = pygame.image.load('Data/Heart.png')
