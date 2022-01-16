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
    ],
    "bit": [
        [0, 0, 0],
        [1, 0, 0],
        [3, 2, 0],
    ],
    "corner": [
        [0, 1, 0],
        [5, 0, 0],
        [4, 3, 2],
    ],
    "crux": [
        [0, 0, 0],
        [0, 1, 0],
        [2, 3, 4],
    ]
}


class Slantic(object):
    def __init__(self, shape, x, y, surface, size=BLOCK_SIZE, margin=1, padding=2):
        self.x = x * BLOCK_SIZE + margin
        self.y = y * BLOCK_SIZE + margin
        self.width = BLOCK_SIZE - padding
        self.height = BLOCK_SIZE - padding
        self.surface = surface
        self.shape = shape
        self.color_light = WHITE
        self.color_dark = BLUE
        self.dark = True

        self.coords = [
            [
                (self.x, self.y),
                (self.x + self.width/2, self.y),
                (self.x + self.width, self.y)
            ],
            [
                (self.x, self.y + self.height/2),
                (self.x + self.width/2, self.y + self.height/2),
                (self.x + self.width, self.y + self.height/2)]
            ,
            [
                (self.x, self.y + self.height),
                (self.x + self.width/2, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
        ]

        self.rect = self.drawSlantic()


    def drawSlantic(self):
        poly_list = []

        fill_color = self.color_light if self.dark else self.color_dark
        poly_color = self.color_dark if self.dark else self.color_light

        for num in range(1,6):
            for index, s in enumerate(self.shape):
                if num in s:
                    poly_list.append(self.coords[index][s.index(num)])
                    continue

        rect = pygame.draw.rect(self.surface, fill_color, (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(self.surface, poly_color, poly_list)
        return rect

    def flip(self):
        self.dark = not self.dark

    def rotate(self):
        self.coords = np.rot90(self.coords).tolist()



def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 30
    SCREEN.fill(WHITE)

    bar_r = Slantic(SHAPES["bar"], 0, 0, SCREEN)
    bar_l = Slantic(np.fliplr(SHAPES["bar"]).tolist(), 1, 0, SCREEN)
    beam_r = Slantic(SHAPES["beam"], 2, 0, SCREEN)
    beam_l = Slantic(np.fliplr(SHAPES["beam"]).tolist(), 3, 0, SCREEN)
    bit = Slantic(SHAPES["bit"], 4, 0, SCREEN)
    corner_r = Slantic(SHAPES["corner"], 5, 0, SCREEN)
    corner_l = Slantic(np.fliplr(SHAPES["corner"]).tolist(), 6, 0, SCREEN)
    crux = Slantic(SHAPES["crux"], 7, 0, SCREEN)

    slantics = [bar_r, bar_l, beam_r, beam_l, bit, corner_r, corner_l, crux]


    while True:
        pygame.display.update()
        SCREEN.fill(WHITE)
        drawGrid()

        for s in slantics:
            s.drawSlantic()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for s in slantics:
                    if s.rect.collidepoint(pygame.mouse.get_pos()):
                        s.flip()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    for s in slantics:
                        if s.rect.collidepoint(pygame.mouse.get_pos()):
                            s.rotate()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        CLOCK.tick(FPS)


def drawGrid():
    for y in range(len(BOARD)):
        for x in range(len(BOARD[y])):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

main()


