from game import *

import pygame
import sys
import time

pygame.init()

   
'''
Initialises and runs the game
'''
game = Game()
game.create_game()


clock = pygame.time.Clock()

while True:
    game.surface.fill((255,255,255))
    
    for event in pygame.event.get():
        # Exits and closes the game if window closed, or Q key pressed
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q] == True:
            pygame.quit()
            sys.exit()
    
    # Press SPACE key to start the game
    if not game.started:
        font = pygame.font.Font('PressStart2P-Regular.ttf', 26)
        text_surface = font.render('Press SPACE to start', True, (0, 0, 0))
        textRect = text_surface.get_rect()
        textRect.center = (Screen.WIDTH/2, Screen.HEIGHT/2)
        game.surface.blit(text_surface, textRect)
        
        if pygame.key.get_pressed()[pygame.K_SPACE] == True:
            game.started = True
    
    if game.ended:
        game.file_reader.update_high_score(game.scoreboard.score)
        game.show_game_over(game.scoreboard.score, game.file_reader.high_score)
        
        # Player presses P to reset highscore
        if pygame.key.get_pressed()[pygame.K_p] == True:
            game.confirming_reset = True
            game.ended = False
        
        # Player presses SPACE key to restart game
        elif pygame.key.get_pressed()[pygame.K_SPACE] == True:
            game = Game()
            game.create_game()
            
    elif game.confirming_reset:
        game.get_confirmation()
        
         # Player confirms reset
        if pygame.key.get_pressed()[pygame.K_y] == True:
            game.file_reader.reset_high_score()
            game = Game()
            game.create_game()
        elif pygame.key.get_pressed()[pygame.K_n] == True:
            game.ended = True
                      
    elif game.started and not game.ended:
        # Game ends when player falls off screen
        if game.player.rect.y > Screen.HEIGHT:
            game.ended = True
            
        # Displays scoreboard
        game.scoreboard.draw(game.surface)
        
        for platform in game.platforms:
            if platform.rect.y > Screen.HEIGHT:
                game.platform_generator.randomise_position(platform)

        # draws platform onto screen
        for platform in game.platforms:
            platform.draw(game.surface)
        #draws player onto screen
        game.player.draw(game.surface) 

        game.apply_ascending_effect()
        
        game.scoreboard.calc_score(game.player)
        game.scoreboard.update()
        
        
        game.player_controller.update_player_position()
        
        
    clock.tick(60)
    pygame.display.flip() #updates display