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
    instr_img = None
    instr_mask = None

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
        
        instr_temp = pygame.image.load(os.path.join(assets_dir, 'instructions.png'))
        i_w, i_h = instr_temp.get_size()
        # Scale to 500px width
        instr_w = 500
        instr_img = pygame.transform.smoothscale(instr_temp, (instr_w, int(i_h * (instr_w / i_w)))).convert_alpha()
        instr_mask = pygame.mask.from_surface(instr_img)
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


        if instr_img:
            button_instr = instr_img.get_rect(center=(SCREEN_WIDTH // 2, 600))
            screen.blit(instr_img, button_instr)
        else:
            instr_w = 500
            button_instr = pygame.Rect((SCREEN_WIDTH - instr_w) // 2, 600, instr_w, BUTTON_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 150), button_instr)
            draw_text('Help', button_font, WHITE, screen, SCREEN_WIDTH // 2, 600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_instr.collidepoint((mx, my)):
                        if instr_mask:
                            if instr_mask.get_at((mx - button_instr.x, my - button_instr.y)):
                                show_instructions(screen)
                        else:
                            show_instructions(screen)

        pygame.display.update()