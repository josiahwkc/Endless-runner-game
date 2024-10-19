from game_platform import Platform
from screen import *

import pygame


class Player:
    JUMP_SPEED = -12
    HORIZONTAL_ACCELERATION = 1
    COUNTER_ACCELERATION = 0.2
    MAX_HORIZONTAL_SPEED = 6
    GRAVITY = 0.5
    WIDTH = 30
    HEIGHT = 30
    INITIAL_POSITION = ((Screen.WIDTH/2)-(WIDTH/2), (Screen.HEIGHT * 5/6)-(HEIGHT)-5)

    def __init__(self) -> None:
        self.rect = pygame.Rect(*Player.INITIAL_POSITION, Player.WIDTH, Player.HEIGHT)
        self.rect.center = Player.INITIAL_POSITION
        self.y_velocity = 0
        self.x_velocity = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (0,255,0), self.rect)
        
    def restart(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.rect.center = Player.INITIAL_POSITION


class PlayerController:
    
    def __init__(self, player: Player, platforms) -> None:
        self.player = player
        self.platforms = platforms

    '''
    Handles directional key input from user
    '''
    def handle_keys(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_a] == True:
            if self.player.rect.right < 0:
                self.player.rect.left = Screen.WIDTH
            
            if self.player.x_velocity > -Player.MAX_HORIZONTAL_SPEED:
                self.player.x_velocity -= Player.HORIZONTAL_ACCELERATION
            
        elif key[pygame.K_d] == True:
            if self.player.rect.left > Screen.WIDTH:
                self.player.rect.right = 0
            
            if self.player.x_velocity < Player.MAX_HORIZONTAL_SPEED:
                self.player.x_velocity += Player.HORIZONTAL_ACCELERATION
          
    '''
    Checks if player is standing on a platform
    return True if player is standing on a platform
    '''
    def is_on_platform(self) -> bool:
        
        # Unable to use colliderect for unkown reasons
        for platform in self.platforms:
            if (self.player.rect.bottom == platform.rect.top and
                self.player.rect.right > platform.rect.left and
                self.player.rect.left < platform.rect.right and
                self.player.y_velocity >= 0):
                return True
        return False

    '''
    Moves player
    '''
    def move_player(self):
        #Keeps player jumping
        if self.is_on_platform():
            self.player.y_velocity = self.player.JUMP_SPEED
        
        self.player.rect.y += self.player.y_velocity
        self.player.y_velocity += Player.GRAVITY
        
        self.player.rect.x += self.player.x_velocity
        
        key = pygame.key.get_pressed()
        if key[pygame.K_a] == False and self.player.x_velocity > 0:
            self.player.x_velocity -= Player.COUNTER_ACCELERATION
        elif key[pygame.K_d] == False and self.player.x_velocity < 0:
            self.player.x_velocity += Player.COUNTER_ACCELERATION
        
        
    '''
    If player is on a platform, stops their vertical motion to make them stand on it
    '''
    def stand_on_platform(self):
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect) and self.player.y_velocity > 0:
                self.player.rect.bottom = platform.rect.top
                self.player.y_velocity = 0

    '''
    Facade for moving player
    '''
    def update_player_position(self):
        self.handle_keys()
        self.move_player()
        self.stand_on_platform()