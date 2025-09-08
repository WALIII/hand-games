import pygame
import math
import random
from HandTracker import HandTracker
import time
from background import SpriteAnimator, static, Enemy
import os

pygame.init()
pygame.mixer.init()


paused = False
show_controls = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
last_call_time = 0
cooldown = 0.5
angle = 270
YELLOW = (255, 255, 0)
targets = []
enemies = []
WIDTH, HEIGHT = 262, 512
SCALE = 3
WINDOW_WIDTH, WINDOW_HEIGHT = int(WIDTH*SCALE), int(HEIGHT*SCALE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)


VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 230, 230
camera_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

turntime = time.time()
HT = HandTracker()
MIN_TARGET_DISTANCE = 200

animations = SpriteAnimator()
music_path = os.path.join("Music","OGG","Slingerswagger.ogg")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)

fontpath = os.path.join(BASE_DIR, "16bitfont.ttf")
clock = pygame.time.Clock()
BLACK = (0,0,0)
score = 0

center_x, center_y = WIDTH//2, HEIGHT//2
radius = (WIDTH+HEIGHT)/20
cannonballs = []

Tilesize = 16
tiles = static.load_tiles("SandTilemap.png", Tilesize)
background_data = static.load_csv_map("SandTilemap_Background.csv")
foreground_data = static.load_csv_map("SandTilemap_Tile Layer 1.csv")

world_width = len(background_data[0])*Tilesize
world_height = len(background_data)*Tilesize


def get_camera_offset(cx, cy):
    offset_x = cx - VIRTUAL_WIDTH//2
    offset_y = cy - VIRTUAL_HEIGHT//2
    offset_x = max(0, min(offset_x, world_width - VIRTUAL_WIDTH))
    offset_y = max(0, min(offset_y, world_height - VIRTUAL_HEIGHT))
    return offset_x, offset_y

def is_far_enough(x,y):
    dx = x - center_x
    dy = y - center_y
    return math.hypot(dx,dy) > MIN_TARGET_DISTANCE

while len(targets) < 5:
    tx = random.randint(50, world_width - 90)
    ty = random.randint(50, world_height - 90)
    if is_far_enough(tx, ty):
        targets.append({"rect":pygame.Rect(tx,ty,16,64), "alive":True})
        enemies.append(Enemy(tx-24, ty+16))


running = True

while running:
    current_time = time.time()
    camera_surface.fill((0,0,0))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                show_controls = not show_controls
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not show_controls:
                radians = math.radians(angle)
                x = center_x + radius*math.cos(radians)
                y = center_y + radius*math.sin(radians)
                barrel_tip_x = x + (50/2)*math.cos(radians)
                barrel_tip_y = y + (50/2)*math.sin(radians)
                speed = 20
                velocity = [speed*math.cos(radians), speed*math.sin(radians)]
                cannonballs.append({'pos':[barrel_tip_x,barrel_tip_y],'velocity':velocity,'angle':angle,'speed':speed})

   
    if show_controls:
        scale_factor = min(WINDOW_WIDTH/VIRTUAL_WIDTH, WINDOW_HEIGHT/VIRTUAL_HEIGHT)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0,0,0))
        font_size = max(12, int(18*scale_factor))
        ui_font = pygame.font.Font(fontpath, font_size)
        controls_text = [
            "Controls:",
            "Move: Close index finger to wrist",
            "Shoot: Close middle finger to wrist",
            "Turn left: Thumb close to wrist",
            "Turn right: Pinky close to wrist",
            "Press TAB to close this screen"
        ]
        y=50
        for line in controls_text:
            surf = ui_font.render(line, True, (255,255,255))
            overlay.blit(surf, (50,y))
            y += font_size + 10
        screen.blit(overlay,(0,0))
        pygame.display.flip()
        clock.tick(30)
        continue  

    
    frame = HT.capture_frame()
    if frame.any():
        HT.update(frame)
        wristdist = HT.wristdist()
        pinky = HT.pinkywrist()
        thumb = HT.thumbwrist()
        index = HT.indexwrist()
        angle %=360

        if index != None and index<1:
            speed = 1
            center_x = max(0, min(center_x + math.cos(math.radians(angle))*speed, world_width))
            center_y = max(0, min(center_y + math.sin(math.radians(angle))*speed, world_height))
            animations.change_action("walk")
        if animations.current_action == "walk" and (index is None or index >= 1):
            animations.change_action("idle")

        if thumb and thumb<0.9 and current_time-turntime>1:
            angle-=90
            animations.rotate_direction(clockwise=True)
            turntime=current_time
        if pinky and pinky<0.95 and current_time-turntime>1:
            angle+=90
            animations.rotate_direction(clockwise=False)
            turntime=current_time
        if animations.current_action == "attack":
            print(animations.current_frame_index)
            if animations.current_frame_index is not 0:
                if animations.current_frame_index > 3:
                    animations.change_action("idle")
        
        if wristdist and current_time-last_call_time>=cooldown and 0.000001<wristdist<1.2:
            dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            barrel_tip_x = center_x + dx
            barrel_tip_y = center_y + dy
            speed = 20
            cannonballs.append({'pos':[barrel_tip_x,barrel_tip_y],'velocity':[dx*speed,dy*speed],'angle':angle,'speed':speed})
            last_call_time=current_time
            animations.change_action("attack")
        
                

    animations.update(current_time)



    bullet_surf = pygame.Surface((10,5),pygame.SRCALPHA)
    bullet_surf.fill(YELLOW)
    for ball in cannonballs:
        ball['pos'][0]+=ball['velocity'][0]
        ball['pos'][1]+=ball['velocity'][1]
    for ball in cannonballs[:]:
        bx,by = ball['pos']
        if bx<0 or by<0 or bx>world_width or by>world_height:
            cannonballs.remove(ball)
            continue
        ball_rect = pygame.Rect(bx,by,2.5,10)
        for target, enemy in zip(targets,enemies):
            if target["alive"] and ball_rect.colliderect(target["rect"]):
                target["alive"]=False
                enemy.animator.change_enemy_action("enemy_death")
                score+=1
                try: cannonballs.remove(ball)
                except ValueError: pass
                break

    for enemy,target in zip(enemies,targets):
        if target["alive"]:
            enemy.animator.change_enemy_action("enemy_idle")
        else:
            if enemy.alive:
                enemy.animator.change_enemy_action("enemy_death")
            if enemy.animator.enemy_frame_index==len(enemy.animator.enemy_animations["enemy_death"])-1:
                enemy.alive=False
        enemy.animator.update_enemy(current_time)

    cam_x, cam_y = get_camera_offset(center_x, center_y)

    static.draw_map(camera_surface, background_data, tiles, Tilesize, -cam_x, -cam_y)
    static.draw_map(camera_surface, foreground_data, tiles, Tilesize, -cam_x, -cam_y)

    for e in enemies:
        if e.alive:
            eframe = e.animator.get_enemy_frame()
            camera_surface.blit(eframe,(e.position[0]-cam_x,e.position[1]-cam_y))

    frame = animations.get_current_frame()
    frame_rect = frame.get_rect(center=(center_x-cam_x,center_y-cam_y))
    camera_surface.blit(frame, frame_rect)

    for ball in cannonballs:
        rotated = pygame.transform.rotate(bullet_surf,-ball['angle'])
        bpos = (ball['pos'][0]-cam_x, ball['pos'][1]-cam_y)
        brect = rotated.get_rect(center=bpos)
        camera_surface.blit(rotated,brect)

    scale_factor = min(WINDOW_WIDTH/VIRTUAL_WIDTH, WINDOW_HEIGHT/VIRTUAL_HEIGHT)
    scaled_surface = pygame.transform.scale(camera_surface,(int(VIRTUAL_WIDTH*scale_factor), int(VIRTUAL_HEIGHT*scale_factor)))
    x_offset = (WINDOW_WIDTH-scaled_surface.get_width())//2
    y_offset = (WINDOW_HEIGHT-scaled_surface.get_height())//2
    screen.fill((0,0,0))
    screen.blit(scaled_surface,(x_offset,y_offset))

    hud_font = pygame.font.Font(fontpath,max(12,int(18*scale_factor)))
    text_surface = hud_font.render(f"Score: {score}",True,BLACK)
    bg_rect = text_surface.get_rect(topleft=(x_offset+8,y_offset+8)).inflate(8,8)
    pygame.draw.rect(screen,(230,230,230),bg_rect)
    screen.blit(text_surface,(x_offset+12,y_offset+12))

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()
