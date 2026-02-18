import pygame
import sys
import os
from settings import *

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def show_instructions(screen):
    font = pygame.font.SysFont(None, FONT_SIZE_BUTTON)
    title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
    running = True
    
    while running:
        screen.fill(DARK_GREY)
        draw_text('Instructions', title_font, WHITE, screen, SCREEN_WIDTH // 2, 100)
        
        lines = [
            "Left / Right Arrow : Move",
            "Up Arrow : Rotate",
            "Down Arrow : Soft Drop",
            "",
            "Click anywhere to return"
        ]
        
        for i, line in enumerate(lines):
            draw_text(line, font, WHITE, screen, SCREEN_WIDTH // 2, 300 + i * 50)
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

def main_menu(screen):
    # Fonts must be created after pygame.init(), which happens in main.py
    title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
    button_font = pygame.font.SysFont(None, FONT_SIZE_BUTTON)

    # Use absolute path to ensure assets are found regardless of where the script is run
    base_path = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_path, 'assets')

    # Load assets
    bg_image = None
    start_img = None
    instr_img = None

    try:
        # Load mainscreen.png - Scale to COVER the screen (preserves aspect ratio)
        temp_bg = pygame.image.load(os.path.join(assets_dir, 'mainscreen.png'))
        bg_w, bg_h = temp_bg.get_size()
        scale_w = SCREEN_WIDTH / bg_w
        scale_h = SCREEN_HEIGHT / bg_h
        scale = max(scale_w, scale_h) # Use max to cover the screen, min to fit inside
        
        new_w, new_h = int(bg_w * scale), int(bg_h * scale)
        temp_bg_scaled = pygame.transform.smoothscale(temp_bg, (new_w, new_h))
        
        # Create a surface for the background and center the image on it
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.blit(temp_bg_scaled, ((SCREEN_WIDTH - new_w) // 2, (SCREEN_HEIGHT - new_h) // 2))
        bg_image = bg_image.convert()
        
        # Load buttons - Scale to width, preserve aspect ratio
        start_temp = pygame.image.load(os.path.join(assets_dir, 'start.png'))
        s_w, s_h = start_temp.get_size()
        start_img = pygame.transform.smoothscale(start_temp, (BUTTON_WIDTH, int(s_h * (BUTTON_WIDTH / s_w)))).convert_alpha()
        
        instr_temp = pygame.image.load(os.path.join(assets_dir, 'instructions.png'))
        i_w, i_h = instr_temp.get_size()
        instr_img = pygame.transform.smoothscale(instr_temp, (BUTTON_WIDTH, int(i_h * (BUTTON_WIDTH / i_w)))).convert_alpha()
        print("Assets loaded successfully!")
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: Could not load assets. Error: {e}")
        pass # Fallback to defaults if files are missing

    while True:
        mx, my = pygame.mouse.get_pos()

        # Always fill screen first to handle transparency in bg_image or missing background
        screen.fill(DARK_GREY)

        # Draw Background
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            draw_text('Tetris', title_font, WHITE, screen, SCREEN_WIDTH // 2, 200)

        # --- Draw Buttons ---
        
        # Start Button (y=350)
        if start_img:
            button_start = start_img.get_rect(center=(SCREEN_WIDTH // 2, 350))
            screen.blit(start_img, button_start)
        else:
            button_start = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, GREEN, button_start)
            draw_text('Play', button_font, WHITE, screen, SCREEN_WIDTH // 2, 375)

        # Instructions Button (y=450)
        if instr_img:
            button_instr = instr_img.get_rect(center=(SCREEN_WIDTH // 2, 740))
            screen.blit(instr_img, button_instr)
        else:
            button_instr = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 150), button_instr)
            draw_text('Help', button_font, WHITE, screen, SCREEN_WIDTH // 2, 475)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_start.collidepoint((mx, my)):
                        return # Exit menu loop to start game
                    if button_instr.collidepoint((mx, my)):
                        show_instructions(screen)

        pygame.display.update()