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
rows = int(screen_width/block_size) - 2
cols = int(screen_height/block_size) - 2

screen = pygame.display.set_mode(
    ((block_size * rows),
     (block_size * cols))
)

board = Board(screen, block_size)

pygame.display.set_caption("Slantics")
clock = pygame.time.Clock()

tile_group = pygame.sprite.Group()
tile_group.add(
    Tile()
)

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in tile_group.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        board.set(pygame.mouse.get_pos(), 0)
            if event.type == pygame.MOUSEBUTTONUP:
                for sprite in tile_group.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        board.set(pygame.mouse.get_pos(), sprite)
                        board.snap()
                for row in board.board:
                    print(row)


        screen.fill('white')
        tile_group.update(events)
        tile_group.draw(screen)
        board.update()
        pygame.display.update()
        clock.tick(60)
