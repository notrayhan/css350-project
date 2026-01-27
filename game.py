import pygame
import random
from settings import *

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

class TetrisGame:
    def __init__(self):
        self.grid = [[BLACK for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.fall_time = 0
        self.fall_speed = 0.27  # Time in seconds before piece falls
        self.clock = pygame.time.Clock()
        self.running = True

    def get_new_piece(self):
        return Piece(5, 0, random.choice(SHAPES))

    def update(self):
        # Handle automatic falling
        self.fall_time += self.clock.get_rawtime()
        self.clock.tick()

        # Check if down key is held for soft drop
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            current_speed = 0.05
        else:
            current_speed = self.fall_speed

        if self.fall_time / 1000 > current_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not self.valid_space(self.current_piece) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.lock_piece(self.current_piece)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.current_piece.x -= 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.x += 1
            elif event.key == pygame.K_RIGHT:
                self.current_piece.x += 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.x -= 1
            elif event.key == pygame.K_UP:
                self.current_piece.rotation += 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.rotation -= 1

    def valid_space(self, piece):
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
        accepted_pos = [x for sub in accepted_pos for x in sub]

        formatted = self.convert_shape_format(piece)

        for pos in formatted:
            if pos[1] > -1:
                if pos not in accepted_pos:
                    return False
            else:
                # Check side boundaries for pieces above screen
                if pos[0] < 0 or pos[0] >= GRID_WIDTH:
                    return False
        return True

    def lock_piece(self, piece):
        formatted = self.convert_shape_format(piece)
        for pos in formatted:
            p = (pos[0], pos[1])
            if p[1] > -1:
                self.grid[p[1]][p[0]] = piece.color
        
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        
        # Check if lost (new piece collides immediately)
        if not self.valid_space(self.current_piece):
             self.running = False

    def convert_shape_format(self, piece):
        positions = []
        format = piece.shape[piece.rotation % len(piece.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((piece.x + j - 2, piece.y + i - 4))
        return positions

    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw Grid Blocks
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(surface, self.grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Draw Current Piece
        formatted = self.convert_shape_format(self.current_piece)
        for pos in formatted:
            x, y = pos
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, (TOP_LEFT_X + x*BLOCK_SIZE, TOP_LEFT_Y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Draw Border
        pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)