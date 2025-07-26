import pygame
import csv
import os
class static:
    def load_tiles(tileset_path, tile_size):
        tileset_image = pygame.image.load(tileset_path).convert_alpha()
        tiles = []
        tileset_width = tileset_image.get_width()
        tileset_height = tileset_image.get_height()

        for y in range(0, tileset_height, tile_size):
            for x in range(0, tileset_width, tile_size):
                rect = pygame.Rect(x, y, tile_size, tile_size)
                tile = tileset_image.subsurface(rect)
                tiles.append(tile)
        return tiles
    def load_tiles2(tileset_path, tile_size2):
        tileset_image = pygame.image.load(tileset_path).convert_alpha()
        tiles = []
        tileset_width = tileset_image.get_width()
        tileset_height = tileset_image.get_height()

        for y in range(0, tileset_height, tile_size2):
            for x in range(0, tileset_width, tile_size2):
                rect = pygame.Rect(x, y, tile_size2, tile_size2)
                tile = tileset_image.subsurface(rect)
                tiles.append(tile)
        return tiles

    def load_csv_map(csv_path):
        with open(csv_path, newline='') as f:
            reader = csv.reader(f)
            return [[int(tile) for tile in row] for row in reader]

    def draw_map(screen, tilemap, tiles, tile_size):
        for y, row in enumerate(tilemap):
            for x, tile_index in enumerate(row):
                if 0 <= tile_index < len(tiles):
                    screen.blit(tiles[tile_index], (x * tile_size , y * tile_size ))

class SpriteAnimator:
    def __init__(self):
        base_path = "Wild West Pixel Cowboy - Pixel Art Asset Pack"

        # Main character animations
        self.animations = {
            # Walk
            "walk_up": self.load_frames(os.path.join(base_path, "walk", "walkup.png"), 4),
            "walk_down": self.load_frames(os.path.join(base_path, "walk", "walkdown.png"), 4),
            "walk_left": self.load_frames(os.path.join(base_path, "walk", "walkleft.png"), 4),
            "walk_right": self.load_frames(os.path.join(base_path, "walk", "walkright.png"), 4),

            # Attack
            "attack_up": self.load_frames(os.path.join(base_path, "attack & reload", "attackup.png"), 5),
            "attack_down": self.load_frames(os.path.join(base_path, "attack & reload", "attackdown.png"), 5),
            "attack_left": self.load_frames(os.path.join(base_path, "attack & reload", "attackleft.png"), 5),
            "attack_right": self.load_frames(os.path.join(base_path, "attack & reload", "attackright.png"), 5),

            # Idle
            "idle_up": self.load_frames(os.path.join(base_path, "idle", "idleup.png"), 4),
            "idle_down": self.load_frames(os.path.join(base_path, "idle", "idledown.png"), 4),
            "idle_left": self.load_frames(os.path.join(base_path, "idle", "idleleft.png"), 4),
            "idle_right": self.load_frames(os.path.join(base_path, "idle", "idleright.png"), 4),

            # Reload
            "reload_up": self.load_frames(os.path.join(base_path, "attack & reload", "reloadup.png"), 5),
            "reload_down": self.load_frames(os.path.join(base_path, "attack & reload", "reloaddown.png"), 5),
            "reload_left": self.load_frames(os.path.join(base_path, "attack & reload", "reloadleft.png"), 3),
            "reload_right": self.load_frames(os.path.join(base_path, "attack & reload", "reloadright.png"), 3),

            # Death
            "death": self.load_frames(os.path.join(base_path, "death", "death.png"), 6),

            # Slash
            "slash_up": self.load_frames(os.path.join(base_path, "slash", "slashup.png"), 3),
            "slash_down": self.load_frames(os.path.join(base_path, "slash", "slashdown.png"), 3),
            "slash_right": self.load_frames(os.path.join(base_path, "slash", "slashright.png"), 3),
            "slash_left": self.load_frames(os.path.join(base_path, "slash", "slashleft.png"), 3),
        }

        # 🔹 NEW: Enemy animations (64x64 tiles)
        enemy_path = os.path.join(base_path, "enemy")
        self.enemy_animations = {
            "enemy_idle": self.load_frames(os.path.join(base_path,"enemyidle", "enemyidle.png"), 2, tile_size=64),
            "enemy_attack": self.load_frames(os.path.join(base_path,"enemyattack", "enemyattack.png"), 5, tile_size=64),
            "enemy_death": self.load_frames(os.path.join(base_path,"enemydeath", "enemydeath.png"), 7, tile_size=64),
        }

        # Grouping for easy reference
        self.animation_sets = {
            "walk": ["walk_up", "walk_left", "walk_down", "walk_right"],
            "idle": ["idle_up", "idle_left", "idle_down", "idle_right"],
            "attack": ["attack_up", "attack_left", "attack_down", "attack_right"],
            "reload": ["reload_up", "reload_left", "reload_down", "reload_right"],
            "slash": ["slash_up", "slash_left", "slash_down", "slash_right"],
        }

        # Enemy only needs single-direction actions for now
        self.enemy_action = "enemy_idle"
        self.enemy_frame_index = 0
        self.enemy_last_update = 0
        self.enemy_anim_speed = 0.2

        self.current_action = "idle"
        self.current_direction_index = 0
        self.current_animation = self.animation_sets[self.current_action][self.current_direction_index]
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.last_update_time = 0

    def load_frames(self, image_path, frame_count, tile_size=None):
        sprite_sheet = pygame.image.load(image_path).convert_alpha()
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        # Override frame size if tile_size specified (e.g., for enemy 64x64)
        if tile_size:
            frame_height = tile_size
            frame_width = tile_size

        frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def update(self, current_time):
        if current_time - self.last_update_time > self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animations[self.current_animation])
            self.last_update_time = current_time

    def update_enemy(self, current_time):
        if current_time - self.enemy_last_update > self.enemy_anim_speed:
            self.enemy_frame_index = (self.enemy_frame_index + 1) % len(self.enemy_animations[self.enemy_action])
            self.enemy_last_update = current_time

    def set_animation(self, animation_name):
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame_index = 0

    def set_animation_from_state(self):
        if self.current_action in self.animation_sets:
            self.set_animation(self.animation_sets[self.current_action][self.current_direction_index])

    def rotate_direction(self, clockwise=True):
        self.current_direction_index = (self.current_direction_index + (1 if clockwise else -1)) % 4
        self.set_animation_from_state()

    def change_action(self, new_action):
        if new_action in self.animation_sets:
            self.current_action = new_action
            self.set_animation_from_state()

    def get_current_frame(self):
        return self.animations[self.current_animation][self.current_frame_index]

    def get_enemy_frame(self):
        return self.enemy_animations[self.enemy_action][self.enemy_frame_index]

    def change_enemy_action(self, new_action):
        if new_action in self.enemy_animations and new_action != self.enemy_action:
            self.enemy_action = new_action
            self.enemy_frame_index = 0
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.animator = SpriteAnimator()  # Each enemy has its own animation state
        self.animator.current_action = "enemy_idle"
        self.alive = True
        self.animator.current_direction_index = 2  # Default to down

    def update(self, current_time):
        self.animator.update(current_time)

    def draw(self, screen):
        frame = self.animator.get_current_frame()
        screen.blit(frame, (self.x, self.y))
    def change_enemy_action(self, new_action):
        if new_action in self.enemy_animations and new_action != self.enemy_action:
            self.enemy_action = new_action
            self.enemy_frame_index = 0

    def create_enemy_with_hitbox(position, animator, enemies, targets):
        # Enemy hitbox
        target_rect = pygame.Rect(position[0], position[1], 32, 48)  # adjust size to match sprite
        target_data = {
            "rect": target_rect,
            "health": 1,
            "alive": True
        }

        # Enemy sprite and data
        enemy_data = {
            "animator": animator,
            "position": position,
            "current_animation": "idle_down",  # default animation
            "alive": True,
            "frame": animator.get_current_frame()
        }

        targets.append(target_data)
        enemies.append(enemy_data)
