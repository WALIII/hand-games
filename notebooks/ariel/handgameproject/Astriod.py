import pygame
import math
import random
from HandTracker import HandTracker 
import time
from background import SpriteAnimator, static, Enemy
import os
def draw_text(text,x,y):
    base_surface.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    base_surface.blit(text_surface, (x, y))
    pygame.display.flip()
calibrated = False
bulletangle = 10
bulletangle2 = 5
last_call_time = 0
cooldown = 0.5
Tilesize2 = 64
targetnum = 1
angle = 270
SCALE = 3
YELLOW = (255, 255, 0)
targets = []
enemies = []
WIDTH, HEIGHT = 262, 512
WINDOW_WIDTH, WINDOW_HEIGHT = int(WIDTH * SCALE), int(HEIGHT * SCALE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

# Base surface (where we draw everything before scaling)
base_surface = pygame.Surface((WIDTH, HEIGHT))
thumbvalues = []
pointervalues = []
middlevalues = []
ringvalues = []
pinkyvalues = []
turntime = time.time()
HT = HandTracker()
MIN_TARGET_DISTANCE = 200
Left = False
Right = False

def is_far_enough(x, y):
    dx = x - center_x
    dy = y - center_y
    distance = math.sqrt(dx**2 + dy**2)
    return distance > MIN_TARGET_DISTANCE

current_time = 0
pygame.init()
pygame.mixer.init()
animations = SpriteAnimator()
music_path = os.path.join("Music", "OGG", "Slingerswagger.ogg")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

BLACK = [100, 100, 100]
score = 0

rect_length = 50
rect_width = 20
rect_surf = pygame.Surface((rect_length, rect_width), pygame.SRCALPHA)
rect_surf.fill((0, 255, 0, 255))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
angle = 270
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = (WIDTH + HEIGHT) / 20
cannonballs = []

running = True
Tilesize = 16
tiles = static.load_tiles("SandTilemap.png", Tilesize)
background_data = static.load_csv_map("SandTilemap_Background.csv")
foreground_data = static.load_csv_map("SandTilemap_Tile Layer 1.csv")
base_surface = pygame.Surface((WIDTH, HEIGHT))
while calibrated == True:
    if current_time == 0:
        current_time = time.time() - 5
    if current_time - time.time() < 0:
        draw_text(str(time.time() - current_time),50,150) 
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                calibrated = True
        if not HT.capture_frame():
            continue  # Skip frame if camera failed

        HT.update()  # Update hand tracking with new frame
        wristdist = HT.thumbwrist()
        pinkywrist = HT.pinkywrist()
        thumbwrist = HT.thumbwrist()
        indexwrist = HT.indexwrist()
        if thumbwrist is not None:
            thumbvalues.append(thumbwrist)
        if pinkywrist is not None:
            pinkyvalues.append(pinkywrist)
        if indexwrist is not None:
            pointervalues.append(indexwrist)
        if wristdist is not None:
            middlevalues.append(wristdist)



            

while len(targets) < 5:
    tx = random.randint(50, WIDTH - 90)
    ty = random.randint(50, HEIGHT - 90)
    if is_far_enough(tx, ty):
        target_data = {
            "rect": pygame.Rect(tx, ty, 16, 64),
            "alive": True
        }
        targets.append(target_data)

        enemy = Enemy(tx - 24, ty + 16)
        enemies.append(enemy)

while running:
    current_time = time.time()
    base_surface.fill((0, 0, 0))
    score_text = font.render(f"Score: {score}", True, BLACK)
    base_surface.blit(score_text, (WIDTH - 180, 20))
    current_time = time.time()
    animations.update(current_time)

    static.draw_map(base_surface, background_data, tiles, Tilesize)
    static.draw_map(base_surface, foreground_data, tiles, Tilesize)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y + radius * math.sin(radians)
            barrel_tip_x = x + (rect_length / 2) * math.cos(radians)
            barrel_tip_y = y + (rect_length / 2) * math.sin(radians)
            speed = 20
            velocity = [speed * math.cos(radians), speed * math.sin(radians)]

            cannonballs.append({
                'pos': [barrel_tip_x, barrel_tip_y],
                'velocity': velocity,
                'angle': angle
            })

    frame = HT.capture_frame()
    if frame is None:
        continue
    HT.update(frame)
    wristdist = HT.wristdist()
    pinkywrist = HT.pinkywrist()
    thumbwrist = HT.thumbwrist()
    indexwrist = HT.indexwrist()
    #indexmodified = HT.min_max_scale(indexwrist,pointervalues)
    angle %= 360  

    if indexwrist is not None and indexwrist < 1:
        speed = 1
        radians = math.radians(angle)
        mx = math.cos(radians) * speed
        my = math.sin(radians) * speed
        center_x = center_x + mx
        center_y = center_y + my
        animations.change_action("walking")
        print("walking"+str(indexwrist))

    current_time = time.time()
    if thumbwrist is not None and thumbwrist < 0.9:
        if current_time - turntime > 1:
            angle = angle - 90
            animations.rotate_direction(clockwise=True)
            turntime = current_time
            print("thumb"+str(thumbwrist))

    if pinkywrist is not None and pinkywrist < 0.95:
        if current_time - turntime > 1:
            angle = angle + 90
            animations.rotate_direction(clockwise=False)
            turntime = current_time
            print("pinky"+str(pinkywrist))

    if wristdist is not None and current_time - last_call_time >= cooldown:
        if 0.000001 < wristdist < 1.2:
            radians = math.radians(angle)
            dx = math.cos(radians)
            dy = math.sin(radians)
            barrel_tip_x = center_x + dx
            barrel_tip_y = center_y + dy 
            speed = 20
            velocity = [speed * dx, speed * dy]
            cannonballs.append({
                'pos': [barrel_tip_x, barrel_tip_y],
                'velocity': velocity,
                'angle': angle
            })

            last_call_time = current_time
            animations.change_action("attack")

        if current_time - last_call_time >= cooldown:
            animations.change_action("idle")

    bullet_surf = pygame.Surface((10, 5), pygame.SRCALPHA)
    bullet_surf.fill((255, 255, 0))

    if angle == 270 or angle == 90:
        bulletangle = 5
        bulletangle2 = 10
    elif angle in (180, 0, 360):
        bulletangle = 10
        bulletangle2 = 5

    for ball in cannonballs:
        ball['pos'][0] += ball['velocity'][0]
        ball['pos'][1] += ball['velocity'][1]

    for ball in cannonballs[:]:
        ball_rect = pygame.Rect(ball['pos'][0], ball['pos'][1], 2.5, 10)
        if ball['pos'][0] > WIDTH or ball['pos'][0] < 0 or ball['pos'][1] > HEIGHT or ball['pos'][1] < 0:
            cannonballs.remove(ball)
            continue

        for target, enemy in zip(targets, enemies):
            if target["alive"] and ball_rect.colliderect(target["rect"]):
                target["alive"] = False
                enemy.animator.change_enemy_action("enemy_death")
                score += 1
                try:
                    cannonballs.remove(ball)
                except ValueError:
                    pass
                break

    for enemy, target in zip(enemies, targets):
        if target["alive"]:
            enemy.animator.change_enemy_action("enemy_idle")
        else:
            if enemy.alive:
                enemy.animator.change_enemy_action("enemy_death")
            if enemy.animator.enemy_frame_index == len(enemy.animator.enemy_animations["enemy_death"]) - 1:
                enemy.alive = False

        enemy.animator.update_enemy(current_time)

        if enemy.alive:
            frame = enemy.animator.get_enemy_frame()
            base_surface.blit(frame, enemy.position)

    handwall = HT.handwall()
    if handwall is not None:
        if handwall[0] > 0:
            pygame.draw.rect(base_surface, RED, pygame.Rect(0, HEIGHT * 0.9, WIDTH, HEIGHT * 0.1))
        if handwall[1] > 0:
            pygame.draw.rect(base_surface, RED, pygame.Rect(0, 0, WIDTH, HEIGHT * 0.1))
        if handwall[2] > 0:
            pygame.draw.rect(base_surface, RED, pygame.Rect(0, 0, WIDTH * 0.1, HEIGHT))
        if handwall[3] > 0:
            pygame.draw.rect(base_surface, RED, pygame.Rect(WIDTH * 0.9, 0, WIDTH, HEIGHT))

    frame = animations.get_current_frame()
    frame_rect = frame.get_rect(center=(center_x, center_y))
    base_surface.blit(frame, frame_rect)


    for ball in cannonballs:
        rotated_bullet = pygame.transform.rotate(bullet_surf, -ball['angle'])
        bullet_rect = rotated_bullet.get_rect(center=(ball['pos'][0], ball['pos'][1]))
        base_surface.blit(rotated_bullet, bullet_rect)
    window_width, window_height = screen.get_size()
    scale_factor = min(window_width / WIDTH, window_height / HEIGHT)
    scaled_width = int(WIDTH * scale_factor)
    scaled_height = int(HEIGHT * scale_factor)

    x_offset = (window_width - scaled_width) // 2
    y_offset = (window_height - scaled_height) // 2

    scaled_surface = pygame.transform.scale(base_surface, (scaled_width, scaled_height))
    screen.fill((0, 0, 0))  
    screen.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()
