from screen import *

import pygame
import random
import math


class Platform:
    WIDTH = 80
    HEIGHT = 5

    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, Platform.WIDTH, Platform.HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.rect)
        
        
class PlatformGenerator:

    def __init__(self, number_of_platforms: int) -> None:
        self.platforms = []
        self.top_platform = self.generate(number_of_platforms)

    '''
    Creates a number of platforms above the screen then places the first platform randomly
    @param number The number of platforms to be created
    '''
    def create_platforms(self, number_of_platforms: int):
        for i in range(number_of_platforms):
            game_platform = Platform(0, -100)
            self.platforms.append(game_platform)
        
        # Places the initial platform
        initial_x_position = Screen.WIDTH / 2
        initial_y_position = Screen.HEIGHT * (5/6)
        self.platforms[0].rect.center = (initial_x_position, initial_y_position)
        self.top_platform = self.platforms[0]
    
    
    '''
    Randomly places a platform on screen
    @param platform The platform to be placed
    ''' 
    def randomise_position(self, platform: Platform):
        
        #Sets position based on previous platform
        MAX_X_DISTANCE = 300
        MIN_Y_DISTANCE = 120


        # gets left most x position, defaults to 0 if position is out of bounds
        min_x = max(Platform.WIDTH/2, self.top_platform.rect.x - MAX_X_DISTANCE)
        # gets right most x position, defaults to WIDTH if position is out of bounds
        max_x = min(MAX_X_DISTANCE + self.top_platform.rect.x, Screen.WIDTH - (Platform.WIDTH/2))
        x_position = random.uniform(min_x,max_x)
        
        relative_x = abs(x_position - self.top_platform.rect.x)
            
        # Calculates minimum y position of new platform
        min_y = self.top_platform.rect.y + self.calculate_relative_y(relative_x)
        
        # If the horizontal gap is less than half the maximum horizontal distance reachable,
        # then the largest vertical gap is MIN_Y_DISTANCE
        if relative_x < MAX_X_DISTANCE/2:
            min_y = self.top_platform.rect.y - MIN_Y_DISTANCE
        
        y_position = random.uniform(min_y, self.top_platform.rect.y - 125)

        # sets platform's position
        platform.rect.center = (x_position, y_position)
        self.top_platform = platform

    '''
    Calculates the highest possible position of y relative to x
    Position is calculated using equation of projectile motion
    @param x The position relative to y being calculated
    '''
    def calculate_relative_y(self, x):
        ANGLE_RAD =  1.144168834
        INITIAL_VELOCITY_SQUARED = 146
        GRAVITY = 0.5
        TAN_THETA = math.tan(ANGLE_RAD)
        COS_THETA_SQUARED = math.cos(ANGLE_RAD) ** 2
        
        # Equation of projectile motion
        y = x * TAN_THETA - ((GRAVITY * x ** 2) / (2 * INITIAL_VELOCITY_SQUARED * COS_THETA_SQUARED))
        return -y
    
    '''
    Generates platforms
    Platforms are created outside the screen, then placed randomly
    '''
    def generate(self, number_of_platforms: int) -> Platform:
        self.create_platforms(number_of_platforms)

        for i in range(1, len(self.platforms)):
            platform = self.platforms[i]
            self.randomise_position(platform)
            
        return self.platforms[number_of_platforms - 1]
