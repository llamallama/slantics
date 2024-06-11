#!/usr/bin/env python3
import pygame
from slantic import Slantic
from board import Board
from sys import exit
# import pudb; pu.db

pygame.init()

# Figure out how many blocks can fit on the screen
# Round down the rows and cols and take 2 off for good measure
block_size = 50
rows = int(pygame.display.Info().current_w/block_size) - 10
cols = int(pygame.display.Info().current_h/block_size) - 2

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
        if (i == 0 or i == len(board.board) - 1
                or
                (i != 0 and (j == 0 or j == len(board.board[i]) - 1))):
            tile_group.add(
                Slantic(size=block_size)
            )
            board.board[i][j] = tile_group.sprites()[-1]

board.sync()


def is_out_of_bounds(sprite):
    if sprite.rect.centerx < 0 or sprite.rect.centerx > pygame.display.Info().current_w:
        return True
    if sprite.rect.centery < 0 or sprite.rect.centery > pygame.display.Info().current_h:
        return True
    return False


def clear_positions(event):
    # clears out the board cells for slantics being dragged somewhere else
    board_backup = [row.copy() for row in board.board]
    for sprite in tile_group.sprites():
        if sprite.rect.collidepoint(event.pos) or sprite.group:
            row = int(sprite.rect.y / block_size)
            col = int(sprite.rect.x / block_size)
            board.board[row][col] = 0
    return board_backup


def update_positions(board_backup):
    # Check is a space is occupied.
    # If so, revert from backup
    # Otherwise update board with new value
    for sprite in tile_group.sprites():
        if sprite.dragging:
            row = int(sprite.rect.centery / block_size)
            col = int(sprite.rect.centerx / block_size)

            if board.board[row][col] or is_out_of_bounds(sprite):
                board.board = [row.copy() for row in board_backup]
                break
            else:
                board.board[row][col] = sprite


def deselect_all():
    for sprite in tile_group.sprites():
        sprite.dragging = False
        sprite.group = False


if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row = int(event.pos[1] / block_size)
                col = int(event.pos[0] / block_size)

                # If not clicking on anything, stop all dragging and grouping
                if not board.board[row][col]:
                    deselect_all()

                # Backup the board and clear positions of sprites being dragged
                board_backup = clear_positions(event)

            if event.type == pygame.MOUSEBUTTONUP:
                update_positions(board_backup)
                board.debug()

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
