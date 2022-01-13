#!/usr/bin/env python
import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 100

BOARD=[
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]


SHAPES = {
    "bar": [
        [0, 0, 1],
        [4, 0, 2],
        [3, 0, 0],
    ],
    "beam": [
        [1, 2, 0],
        [5, 0, 3],
        [0, 0, 4],
    ]
}


class Slantic(object):
    def __init__(self, shape, x, y, screen, size=BLOCK_SIZE, padding=2):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.width = BLOCK_SIZE - padding
        self.height = BLOCK_SIZE - padding
        self.surface = pygame.Surface((self.width, self.height))
        self.screen = screen
        self.shape = shape
        self.color_light = WHITE
        self.color_dark = BLUE
        self.mode = "dark"

        print(self.shape)

        self.coords = [
            [(0,0),              (self.width/2, 0),             (self.width, 0)],
            [(0, self.height/2), (self.width/2, self.height/2), (self.width, self.height/2)],
            [(0, self.height),   (self.width/2, self.height),   (self.width, self.height)]
        ]

        self.drawSlantic()


    def drawSlantic(self):
        poly_list = []

        if self.mode == "dark":
            fill_color = self.color_light
            poly_color = self.color_dark
        else:
            fill_color = self.color_dark
            poly_color = self.color_light

        for num in range(1,6):
            for index, s in enumerate(self.shape):
                if num in s:
                    poly_list.append(self.coords[index][s.index(num)])
                    continue

        self.surface.fill(fill_color)
        pygame.draw.polygon(self.surface, poly_color, poly_list)
        self.screen.blit(self.surface, (self.x + 1, self.y + 1))


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 30
    SCREEN.fill(WHITE)

    slantics=[]

    slantics.append(Slantic(SHAPES["bar"], 0, 0, SCREEN))
    slantics.append(Slantic(np.fliplr(SHAPES["bar"]).tolist(), 1, 0, SCREEN))
    slantics.append(Slantic(SHAPES["beam"], 2, 0, SCREEN))
    slantics.append(Slantic(np.fliplr(SHAPES["beam"]).tolist(), 3, 0, SCREEN))

    while True:
        SCREEN.fill(WHITE)
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for s in slantics:
            s.drawSlantic()

        pygame.display.update()
        CLOCK.tick(FPS)


def drawGrid():
    for y in range(len(BOARD)):
        for x in range(len(BOARD[y])):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

main()


