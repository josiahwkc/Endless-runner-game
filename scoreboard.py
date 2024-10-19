
import pygame
import sys
import os

from player import Player
from file_reader import *

pygame.init()
pygame.font.init()

class Scoreboard:
    POINTS = 3
    FONT_STYLE = 'PressStart2P-Regular.ttf'
    FONT_SIZE = 10
    
    def __init__(self, file_reader) -> None:
        self.file_reader = file_reader
        self.high_score = self.file_reader.high_score 
        self.score = 0
        self.max_score = 0
        
        self.high_score_font = pygame.font.Font(Scoreboard.FONT_STYLE, Scoreboard.FONT_SIZE)
        self.high_score_surface = self.high_score_font.render('High-Score: ' + str(self.high_score), True, (0, 0, 255))
        self.high_score_Rect = self.high_score_surface.get_rect()
        
        self.score_font = pygame.font.Font(Scoreboard.FONT_STYLE, Scoreboard.FONT_SIZE)
        self.score_surface = self.score_font.render('Score: ' + str(self.score), True, (0, 0, 255))
        self.scoreRect = self.score_surface.get_rect()
        
        
        
    def draw(self, surface):
        surface.blit(self.high_score_surface, self.high_score_Rect)
        surface.blit(self.score_surface, self.scoreRect)
        
    
    def calc_score(self, player: Player):
        if player.y_velocity < 0:
            self.max_score += Scoreboard.POINTS
        elif player.y_velocity > 0:
            self.max_score -= Scoreboard.POINTS
        
        if self.score < self.max_score:
            self.score = self.max_score
     
        
    def update(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.high_score_surface = self.high_score_font.render('High-Score: ' + str(self.high_score), True, (0, 0, 255))
        self.score_surface = self.score_font.render('Score: ' + str(self.score), True, (0, 0, 255))
        
    
    def restart(self):
        self.score = 0
        self.max_score = 0
        
    
    def reset_high_score(self):
        self.restart()
        self.high_score = 0
        self.file_reader.reset_high_score()