# your_game.py
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up window
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test Game Window")

# Fill background
screen.fill((100, 150, 200))

# Font for text
font = pygame.font.Font(None, 36)
text = font.render("Hello from your game!", True, (255, 255, 255))
text_rect = text.get_rect(center=(200, 150))
screen.blit(text, text_rect)

# Update the display
pygame.display.flip()

# Print to console as well
print("Game started successfully!")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()