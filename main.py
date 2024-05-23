#!/usr/bin/env python3
import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Slantics")
clock = pygame.time.Clock()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), dimensions=(50, 50),  color='black'):
        super().__init__()
        self.image = pygame.Surface(dimensions)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.dragging = False

    def click(self):
        print('here')

    def drag(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if self.dragging and event.type == pygame.MOUSEMOTION:
                self.rect.move_ip(event.rel)

    def update(self, events):
        self.drag(events)


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

    screen.fill('white')
    tile_group.update(events)
    tile_group.draw(screen)
    pygame.display.update()
    clock.tick(60)
