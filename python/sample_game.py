import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 300
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Test")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Rectangle setup
rect_x, rect_y = 50, 50
rect_speed_x, rect_speed_y = 2, 2
rect_width, rect_height = 50, 50

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move rectangle
    rect_x += rect_speed_x
    rect_y += rect_speed_y

    # Bounce off edges
    if rect_x <= 0 or rect_x + rect_width >= WIDTH:
        rect_speed_x *= -1
    if rect_y <= 0 or rect_y + rect_height >= HEIGHT:
        rect_speed_y *= -1

    # Draw
    window.fill(BLACK)
    pygame.draw.rect(window, RED, (rect_x, rect_y, rect_width, rect_height))
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()