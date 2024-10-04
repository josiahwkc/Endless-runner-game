
import pygame

from player import *
from game_platform import *
import scoreboard
from screen import *
from scoreboard import *
from file_reader import *

class Game:
    #Set player spawn position
    PLAYER_X_POS = (Screen.WIDTH/2)-(Player.WIDTH/2)
    PLAYER_Y_POS = (Screen.HEIGHT * 5/6)-(Player.HEIGHT)-5

    NUMBER_OF_PLATFORMS = 10 # Change this value to change the number of platforms present in the game

    SCOREBOARD_POSITION = (10,10)
    
    FONT_STYLE = 'PressStart2P-Regular.ttf'
    
    def __init__(self) -> None:
        self.surface = None
        self.file_reader = None
        self.scoreboard = None
        self.platform_generator = None
        self.platforms = None
        self.player = None
        self.player_controller = None
        self.running = False
        self.started = False
        self.ended = False
        
    def create_game(self):
        screen = Screen()
        self.surface = screen.surface

        self.file_reader = FileReader()
        
        self.scoreboard = Scoreboard(self.file_reader.high_score)
        self.scoreboard.high_score_Rect.topleft = Game.SCOREBOARD_POSITION
        self.scoreboard.scoreRect.top = self.scoreboard.high_score_Rect.bottom + 10
        self.scoreboard.scoreRect.left = 10

        self.platform_generator = PlatformGenerator(Game.NUMBER_OF_PLATFORMS)
        self.platforms = self.platform_generator.platforms

        self.player = Player(Game.PLAYER_X_POS, Game.PLAYER_Y_POS)
        self.player_controller = PlayerController(self.player, self.platforms)

    '''
    Moves platform down when player is above a certain height.
    This gives the illusion of the player ascending 
    '''
    def apply_ascending_effect(self):
        if self.player.rect.top < (Screen.HEIGHT * 3/4) - Player.HEIGHT and self.player.y_velocity <= 0:
            move_amount = -self.player.y_velocity
            for platform in self.platforms:
                platform.rect.y += move_amount    
            self.player.rect.y += move_amount # moves player down
            
    '''
    Creates 'GAME OVER' screen
    '''
    def show_game_over(self, score: int, high_score: int):
         # Create 'GAME OVER' text
        
        game_over_font = pygame.font.Font(Game.FONT_STYLE, 32)
        game_over_surface = game_over_font.render('GAME OVER!', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (Screen.WIDTH/2, Screen.HEIGHT * 4/9)
        self.surface.blit(game_over_surface , game_over_rect)
        
        # Create 'Score' text
        score_font = pygame.font.Font(Game.FONT_STYLE, 18)
        score_surface = score_font.render('Score: ' + str(score), True, (0, 0, 255))
        score_rect = score_surface.get_rect()
        score_rect.center = (Screen.WIDTH/2, game_over_rect.bottom + 20)
        self.surface.blit(score_surface , score_rect)
        
        # Create 'High-Score' text
        high_score_font = pygame.font.Font(Game.FONT_STYLE, 18)
        high_score_surface = high_score_font.render('High-Score: ' + str(high_score), True, (0, 0, 255))
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.center = (Screen.WIDTH/2, score_rect.bottom + 20)
        self.surface.blit(high_score_surface , high_score_rect)
        
        # Create 'Restart' text
        restart_font = pygame.font.Font(Game.FONT_STYLE, 18)
        restart_surface = restart_font.render('Press SPACE to restart', True, (0, 0, 0))
        restart_rect = restart_surface.get_rect()
        restart_rect.center = (Screen.WIDTH/2, high_score_rect.bottom + 20)
        self.surface.blit(restart_surface, restart_rect)