import pygame

class Screen:
    WIDTH = 540
    HEIGHT = 700
    
    def __init__(self) -> None:
        DISPLAY = pygame.display
        DISPLAY.set_caption("JUMP JUMP")
        self.surface = DISPLAY.set_mode((Screen.WIDTH, Screen.HEIGHT))