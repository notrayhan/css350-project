import pygame
from settings import *
from menu import main_menu, draw_text

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
    game_running = True
    while game_running:
        screen.fill(BLACK)
        draw_text('Game Started', game_font, WHITE, screen, SCREEN_WIDTH // 2, 400)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False

        pygame.display.update()

pygame.quit()