import pygame

pygame.init()
# 400x400 window
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Tetris Group Project")

# Keeps window open until you click X
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((50, 50, 50)) # Dark Grey bg
    pygame.display.flip()

pygame.quit()