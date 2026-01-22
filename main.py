import pygame
from settings import *
from menu import main_menu, draw_text
from game import TetrisGame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)

# Define fonts for game loop
game_font = pygame.font.SysFont(None, FONT_SIZE_BUTTON)

# Keeps window open until you click X
running = True
while running:
    main_menu(screen)
    
    # Game loop placeholder
    game = TetrisGame()
    game_running = True
    while game_running:
        game.update()
        game.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False
            
            game.handle_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False

        if not game.running:
            game_running = False

        pygame.display.update()

pygame.quit()