import pygame
import os
from sys import exit
from random import randint, choice


''' Classes '''
class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        super().__init__()
        
        player_walk_1 = load_path_image('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = load_path_image('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = load_path_image('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jump_sound = load_path_sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)
    
    def player_input(self) :
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 :
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self) :
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300 :
            self.rect.bottom = 300
    
    def animation_state(self) :
        if self.rect.bottom < 300 :
            self.image = self.player_jump
        else :
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk) :
                self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]
    
    def update(self) :
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite) :
    def __init__(self, type) :
        super().__init__()
        
        if type == 'fly' :
            fly_frame_1 = load_path_image('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = load_path_image('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else :
            snail_frame_1 = load_path_image('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = load_path_image('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.animation_index = 0            
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self) :
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames) :
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self) :
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self) :
        if self.rect.x <= -100 :
            self.kill()


''' Funtions '''
def display_score() :
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = test_font.render("Score: " + str(current_time), False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    
    return current_time

def collision_sprite() :
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False) :
        obstacle_group.empty()
        return False
    else :
        return True


''' Pygame Settings '''
# Pygame Windows Setting
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")

# Path of File
current_path = os.path.dirname(__file__)
def load_path_image(file_name) :
    try :
        return_path = os.path.join(os.path.abspath('.'), file_name)
        return pygame.image.load(return_path)
    except :
        return_path = os.path.join(current_path, file_name)
        return pygame.image.load(return_path)

def load_path_font(file_name, font_size) :
    try :
        return_path = os.path.join(os.path.abspath('.'), file_name)
        return pygame.font.Font(return_path, font_size)
    except :
        return_path = os.path.join(current_path, file_name)
        return pygame.font.Font(return_path, font_size)

def load_path_sound(file_name) :
    try :
        return_path = os.path.join(os.path.abspath('.'), file_name)
        return pygame.mixer.Sound(return_path)
    except :
        return_path = os.path.join(current_path, file_name)
        return pygame.mixer.Sound(return_path)

# System Settings
clock = pygame.time.Clock()
test_font = load_path_font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bgm = load_path_sound('audio/music.wav')
bgm.play(loops = -1)


''' Groups '''
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


''' Images '''
# Backgrounds
sky_surface = load_path_image('graphics/Sky.png').convert()
ground_surface = load_path_image('graphics/ground.png').convert()

# Intro Screen
player_stand = load_path_image('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))


''' Timer '''
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


''' Main '''
while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        
        if game_active :
            if event.type == obstacle_timer :
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
       
        else :
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                game_active = True
                start_time = pygame.time.get_ticks()
    
    if game_active :
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # Collision
        game_active = collision_sprite()

    else :
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        
        score_message = test_font.render("Your score: " + str(score), False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        
        if score == 0 :
            screen.blit(game_message, game_message_rect)
        else :
            screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)
