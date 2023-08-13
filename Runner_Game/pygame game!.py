import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_idx = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_idx]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('sounds/jump_2.mp3')
        self.jump_sound.set_volume(0.05)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_idx += 0.1
            if self.player_idx >= len(self.player_walk):
                self.player_idx = 0
            self.image = self.player_walk[int(self.player_idx)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'Fly':
            fly_walk_1 = pygame.image.load('graphics/enemies/fly1.png').convert_alpha()
            fly_walk_2 = pygame.image.load('graphics/enemies/fly2.png').convert_alpha()
            self.frames = [fly_walk_1, fly_walk_2]
            y_pos = randint(100,250)
        else:
            snail_walk_1 = pygame.image.load('graphics/enemies/snail1.png').convert_alpha()
            snail_walk_2 = pygame.image.load('graphics/enemies/snail2.png').convert_alpha()
            self.frames = [snail_walk_1, snail_walk_2]
            y_pos = 300
            
        self.animation_idx = 0
        self.image = self.frames[self.animation_idx]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
        
    def animation_state(self):
        self.animation_idx += 0.1
        if self.animation_idx >= len(self.frames):
            self.animation_idx = 0
        self.image = self.frames[int(self.animation_idx)]
    
    def update(self):
        self.animation_state()
        speed = randint(6,14)
        extra_speed = display_score() / 100
        if extra_speed <= 10 : self.rect.x -= speed + extra_speed
        else: self.rect.x -= speed + 10
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
        
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surf = test_font.render(f'Score: {current_time}', False, (253, 255, 228))
    score_rect = score_surf.get_rect(center = (400,50))      
    screen.blit(score_surf, score_rect)                        
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite , obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True
    
pygame.init()
screen = pygame.display.set_mode((800, 400))               
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)                           
game_active = False
start_time = 0
score = 0
music = pygame.mixer.Sound('sounds/onlymp3.to - DREAMYARD POKEMON BLACK WHITE-MO3D2PCM760-192k-1691928023.mp3')
music.set_volume(0.05)
music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#Importing Background
night_surf = pygame.image.load('graphics/starry_night.webp').convert()                   
ground_surf = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surf.get_rect(topleft = (-400,300))
ground_surf_2 = pygame.image.load('graphics/ground.png').convert()
ground_rect_2 = ground_surf_2.get_rect(topleft = (0,300))
ground_surf_3 = pygame.image.load('graphics/ground.png').convert()
ground_rect_3 = ground_surf_3.get_rect(topleft = (400,300))


#intro screen                                  
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_big = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_big.get_rect(center = (400,200))

game_name = test_font.render('Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,75))

game_message = test_font.render('Press Space To Start', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,350))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)


while True:
    #check if user clicked X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        #Game Start
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
            
                start_time = pygame.time.get_ticks()
                
        if game_active:       
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['Fly', 'Snail', 'Snail'])))
             
    ground_speed = 3           
    if game_active:
        #Display Background
        screen.blit(night_surf,(0,0) )  #surface, position
        screen.blit(ground_surf, ground_rect )
        screen.blit(ground_surf_2, ground_rect_2)
        screen.blit(ground_surf_3, ground_rect_3)
        score = display_score()
        
        #Moving Ground
        extra_ground_speed = display_score() / 100
        ground_rect.x -= ground_speed + extra_ground_speed
        ground_rect_2.x -= ground_speed + extra_ground_speed
        ground_rect_3.x -= ground_speed + extra_ground_speed
        if ground_rect.left < -600 : ground_rect.left = 800 
        if ground_rect_2.left < -600 : ground_rect_2.left = 800 
        if ground_rect_3.left < -600 : ground_rect_3.left = 800
        if extra_ground_speed >= 10 : extra_ground_speed = 10
        
        #Player 
        player.draw(screen)
        player.update()
        
        #Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        #Collision
        game_active = collision_sprite()
        
    else:
        
        screen.fill((94,129,162))
        screen.blit(player_stand_big, player_stand_rect)
        
        score_message = test_font.render(f'Your Score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,350))
        screen.blit(game_name, game_name_rect)
        
        if score == 0 : screen.blit(game_message, game_message_rect)
        else : screen.blit(score_message, score_message_rect)
        
    pygame.display.update()
    clock.tick(60)   