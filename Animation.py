import pygame

animation_frames = {}

def load_animation(path,frame_duration,animation_frames):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_duration:
        animation_frame_id = animation_name + '_' + str(n)
        img_lc = path + '/' + animation_frame_id + '.png'
        animation_img = pygame.image.load(img_lc)
        animation_frames[animation_frame_id] = animation_img.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n+=1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

animation_db = {}

animation_db['Run'] = load_animation('Data/Character/Run',(7,7,7,7,7,7,7,7),animation_frames)
animation_db['Idle'] = load_animation('Data/Character/Idle',(7,7,7,7,7,7),animation_frames)
animation_db['Attack'] = load_animation('Data/Character/Attack',(1,2,2,3,3,3,3,3,3,2,1,1),animation_frames)
animation_db['Jump'] = load_animation('Data/Character/Jump',(7,7,7),animation_frames)
animation_db['Fall'] = load_animation('Data/Character/Fall',(7,7,7),animation_frames)
animation_db['Hurt'] = load_animation('Data/Character/Hurt',(10,7,7,7),animation_frames)
animation_db['Ladder'] = load_animation('Data/Character/Ladder',(7,7,7,7),animation_frames)
animation_db['Death'] = load_animation('Data/Character/Death',(10,7,7,7,7,7,7,7,7,7),animation_frames)


coin_db = []
coin_frames = {}
coin_db = load_animation('Data/Coin',(7,7,7,7,7),coin_frames)




