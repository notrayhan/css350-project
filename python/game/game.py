import pygame
import random
import os
from settings import *

class Piece:
    def __init__(self, x, y, shape, texture=None):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0
        self.texture = texture

class TetrisGame:
    def __init__(self):
        self.block_assets = []
        self.load_assets()
        self.grid = [[BLACK for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.fall_time = 0
        self.fall_speed = 0.27  # Time in seconds before piece falls
        self.clock = pygame.time.Clock()
        self.running = True

    def load_assets(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_path, 'assets')
        try:
            # Load images and scale them to BLOCK_SIZE
            for filename in ['pandablock.png', 'flowerblock.png']:
                img = pygame.image.load(os.path.join(assets_dir, filename))
                self.block_assets.append(pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE)))
        except (FileNotFoundError, pygame.error) as e:
            print(f"Warning: Could not load block assets: {e}")

    def get_new_piece(self):
        # 30% chance to use a texture if assets are available
        texture = None
        if self.block_assets and random.random() < 0.3:
            texture = random.choice(self.block_assets)
        return Piece(5, 0, random.choice(SHAPES), texture)

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
                # Store texture if it exists, otherwise store color
                if piece.texture:
                    self.grid[p[1]][p[0]] = piece.texture
                else:
                    self.grid[p[1]][p[0]] = piece.color
        
        self.clear_rows()
        
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        
        # Check if lost (new piece collides immediately)
        if not self.valid_space(self.current_piece):
             self.running = False

    def clear_rows(self):
        # Filter out full rows (rows that have no BLACK blocks)
        new_grid = [row for row in self.grid if BLACK in row]
        
        # Calculate how many rows were cleared
        cleared = GRID_HEIGHT - len(new_grid)
        
        # Add new empty rows at the top
        for _ in range(cleared):
            new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            
        self.grid = new_grid

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
                val = self.grid[i][j]
                rect = (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if isinstance(val, pygame.Surface):
                    surface.blit(val, (rect[0], rect[1]))
                else:
                    pygame.draw.rect(surface, val, rect, 0)

        # Draw Current Piece
        formatted = self.convert_shape_format(self.current_piece)
        for pos in formatted:
            x, y = pos
            if y > -1:
                rect = (TOP_LEFT_X + x*BLOCK_SIZE, TOP_LEFT_Y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if self.current_piece.texture:
                    surface.blit(self.current_piece.texture, (rect[0], rect[1]))
                else:
                    pygame.draw.rect(surface, self.current_piece.color, rect, 0)

        # Draw Border
        pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)