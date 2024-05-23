#!/usr/bin/env python3
import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Slantics")
clock = pygame.time.Clock()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), dimensions=(100, 100),  color='black'):
        super().__init__()
        # self.image = pygame.Surface(dimensions)
        self.image = pygame.image.load('tile.png').convert_alpha()
        # self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False

    def drag(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if self.dragging and event.type == pygame.MOUSEMOTION:
                self.rect.move_ip(event.rel)

    def rotate(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = pygame.transform.rotate(self.image, -90)

    def update(self, events):
        self.drag(events)
        self.rotate(events)


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
