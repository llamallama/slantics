#!/usr/bin/env python3
import pygame
from tile import Tile
from board import Board
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Slantics")
clock = pygame.time.Clock()

board = Board(20, 15)

# def draw_grid():
#     block_size = 50
#     for x in range(20):
#         for y in range(15):
#             rect = pygame.Rect(
#                 x * block_size, y * block_size, block_size, block_size
#             )
#             pygame.draw.rect(screen, 'black', rect, 1)


tile_group = pygame.sprite.Group()
tile_group.add(
    Tile(),
    Tile((0, 100)),
    Tile((0, 200)),
)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            for tile in tile_group.sprites():
                print(tile.rect.collidepoint(pygame.mouse.get_pos()))

    screen.fill('white')
    # draw_grid()
    tile_group.update(events)
    tile_group.draw(screen)
    pygame.display.update()
    clock.tick(60)
