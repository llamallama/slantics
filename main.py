#!/usr/bin/env python3
import pygame
from tile import Tile
from board import Board
from sys import exit

pygame.init()

# Figure out how many blocks can fit on the screen
# Round down the rows and cols and take 2 off for good measure
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
block_size = 50
rows = int(screen_width/block_size) - 5
cols = int(screen_height/block_size) - 5

# Initial pygame setup
pygame.display.set_caption("Slantics")
screen = pygame.display.set_mode(
    ((block_size * rows),
     (block_size * cols))
)
clock = pygame.time.Clock()

# Add some tile sprites
tile_group = pygame.sprite.Group()
tile_group.add(
    Tile(),
    Tile(),
    Tile()
)

# Set up the board
board = Board(screen, block_size)
board.board[0][0] = tile_group.sprites()[0]
board.board[1][1] = tile_group.sprites()[1]
board.board[2][2] = tile_group.sprites()[2]
board_backup = []

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Backup the board
                board_backup = [row.copy() for row in board.board]

                # Calculate and update the new board position
                for sprite in tile_group.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        mouse = pygame.mouse.get_pos()
                        row = int(mouse[1] / block_size)
                        col = int(mouse[0] / block_size)
                        board.board[row][col] = 0

            if event.type == pygame.MOUSEBUTTONUP:
                # Check is a space is occupied.
                # If so, revert from backup
                # Otherwise update board with new value
                for sprite in tile_group.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        mouse = pygame.mouse.get_pos()
                        row = int(mouse[1] / block_size)
                        col = int(mouse[0] / block_size)
                        if board.board[row][col]:
                            board.board = [row.copy() for row in board_backup]
                        else:
                            board.board[row][col] = sprite

        # Draw the background color
        screen.fill('white')

        # Update and draw tiles
        tile_group.update(events)
        tile_group.draw(screen)

        # # Update and draw the board
        board.update()

        # # Update the display
        pygame.display.update()

        # Lock at 60 FPS
        clock.tick(60)
        print(clock.get_fps())
