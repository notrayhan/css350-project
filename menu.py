import pygame
import sys
from settings import *

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu(screen):
    # Fonts must be created after pygame.init(), which happens in main.py
    # So we create them inside this function
    title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
    button_font = pygame.font.SysFont(None, FONT_SIZE_BUTTON)

    while True:
        screen.fill(DARK_GREY)
        
        draw_text('Tetris', title_font, WHITE, screen, SCREEN_WIDTH // 2, 200)

        mx, my = pygame.mouse.get_pos()

        # Center buttons horizontally
        btn_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        button_play = pygame.Rect(btn_x, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_quit = pygame.Rect(btn_x, 450, BUTTON_WIDTH, BUTTON_HEIGHT)

        pygame.draw.rect(screen, GREEN, button_play)
        pygame.draw.rect(screen, RED, button_quit)

        draw_text('Play', button_font, WHITE, screen, SCREEN_WIDTH // 2, 375)
        draw_text('Quit', button_font, WHITE, screen, SCREEN_WIDTH // 2, 475)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_play.collidepoint((mx, my)):
                        return # Exit menu loop to start game
                    if button_quit.collidepoint((mx, my)):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()