#!/usr/bin/env python3
import pygame
from slantic import Slantic
from board import Board
from sys import exit

pygame.init()

# Figure out how many blocks can fit on the screen
# Round down the rows and cols and take 2 off for good measure
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
block_size = 75
rows = int(screen_width/block_size) - 2
cols = int(screen_height/block_size) - 2

# Initial pygame setup
pygame.display.set_caption("Slantics")
screen = pygame.display.set_mode(
    ((block_size * rows),
     (block_size * cols))
)
clock = pygame.time.Clock()

# Set up the board
tile_group = pygame.sprite.Group()
board = Board(screen, block_size)
for i in range(0, len(board.board)):
    for j in range(0, len(board.board[i])):
        print(f"{i} : {j}")
        # if (i == 0 or i == len(board.board) - 1
        #         or
        #         (i != 0 and (j == 0 or j == len(board.board[i]) - 1))):
        tile_group.add(
            Slantic(size=block_size)
        )
        board.board[i][j] = tile_group.sprites()[-1]

# board_backup = []

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

        # Update and draw the board
        board.update()

        # Update and draw tiles
        tile_group.update(events)
        tile_group.draw(screen)

        # # Update the display
        pygame.display.update()

        # Lock at 60 FPS
        clock.tick(60)
