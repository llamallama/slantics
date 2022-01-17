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
        [3, 0, 0]
    ],
    "beam": [
        [1, 2, 0],
        [5, 0, 3],
        [0, 0, 4]
    ],
    "bit": [
        [0, 0, 0],
        [1, 0, 0],
        [3, 2, 0]
    ],
    "corner": [
        [0, 1, 0],
        [5, 0, 0],
        [4, 3, 2]
    ],
    "crux": [
        [0, 0, 0],
        [0, 1, 0],
        [2, 3, 4]
    ],
    "fang": [
        [0, 0, 0],
        [1, 0, 0],
        [0, 3, 2]
    ],
    "hexx": [
        [0, 1, 2],
        [6, 0, 3],
        [5, 4, 0]
    ],
    "hill": [
        [0, 1, 0],
        [6, 0, 2],
        [5, 4, 3]
    ],
    "peak": [
        [0, 1, 0],
        [0, 0, 0],
        [4, 3, 2]
    ],
    "point": [
        [1, 0, 0],
        [0, 0, 2],
        [0, 4, 3]
    ],
    "slant": [
        [0, 0, 1],
        [0, 0, 2],
        [5, 4, 3]
    ],
    "slope": [
        [0, 0, 0],
        [0, 0, 2],
        [1, 4, 3]
    ],
    "spike": [
        [1, 0, 0],
        [0, 0, 2],
        [0, 0, 3]
    ],
    "strip": [
        [0, 1, 2],
        [4, 0, 0],
        [3, 0, 0]
    ],
    "bonus": [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
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
        self._dark = True
        self._coords = []
        self.rect = self.drawSlantic()
        self.drag = False

    def drawSlantic(self):
        self._coords = [
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

        poly_list = []

        fill_color = self.color_light if self._dark else self.color_dark
        poly_color = self.color_dark if self._dark else self.color_light

        for num in range(1,10):
            for index, s in enumerate(self.shape):
                if num in s:
                    poly_list.append(self._coords[index][s.index(num)])
                    continue

        self.rect = pygame.draw.rect(self.surface, fill_color, (self.x, self.y, self.width, self.height))

        if len(poly_list) > 2:
            pygame.draw.polygon(self.surface, poly_color, poly_list)

        return self.rect

    def flip(self):
        self._dark = not self._dark

    def rotate(self):
        self._coords = np.rot90(self._coords).tolist()

def setup_tiles():
    bar_r = Slantic(SHAPES["bar"], 0, 0, SCREEN)
    bar_l = Slantic(np.fliplr(SHAPES["bar"]).tolist(), 1, 0, SCREEN)
    beam_r = Slantic(SHAPES["beam"], 2, 0, SCREEN)
    beam_l = Slantic(np.fliplr(SHAPES["beam"]).tolist(), 3, 0, SCREEN)
    bit = Slantic(SHAPES["bit"], 4, 0, SCREEN)
    corner_r = Slantic(SHAPES["corner"], 5, 0, SCREEN)
    corner_l = Slantic(np.fliplr(SHAPES["corner"]).tolist(), 6, 0, SCREEN)
    crux = Slantic(SHAPES["crux"], 7, 0, SCREEN)
    fang_r = Slantic(SHAPES["fang"], 0, 1, SCREEN)
    fang_l = Slantic(np.fliplr(SHAPES["fang"]).tolist(), 1, 1, SCREEN)
    hexx = Slantic(SHAPES["hexx"], 2, 1, SCREEN)
    hill = Slantic(SHAPES["hill"], 3, 1, SCREEN)
    peak = Slantic(SHAPES["peak"], 4, 1, SCREEN)
    point = Slantic(SHAPES["point"], 5, 1, SCREEN)
    slant = Slantic(SHAPES["slant"], 6, 1, SCREEN)
    slope_r = Slantic(SHAPES["slope"], 7, 1, SCREEN)
    slope_l = Slantic(np.fliplr(SHAPES["slope"]).tolist(), 0, 2, SCREEN)
    spike_r = Slantic(SHAPES["spike"], 1, 2, SCREEN)
    spike_l = Slantic(np.fliplr(SHAPES["spike"]).tolist(), 2, 2, SCREEN)
    strip = Slantic(SHAPES["strip"], 3, 2, SCREEN)
    bonus = Slantic(SHAPES["bonus"], 4, 2, SCREEN)

    return [
        bar_r,
        bar_l,
        beam_r,
        beam_l,
        bit,
        corner_r,
        corner_l,
        crux,
        fang_r,
        fang_l,
        hexx,
        hill,
        peak,
        point,
        slant,
        slope_r,
        slope_l,
        spike_r,
        spike_l,
        strip,
        bonus
    ]

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 30
    SCREEN.fill(WHITE)

    slantics = setup_tiles()

    while True:
        pygame.display.update()
        SCREEN.fill(WHITE)
        drawGrid()

        for s in slantics:
            s.drawSlantic()

            if s.drag:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                s.x = mouse_x + offset_x
                s.y = mouse_y + offset_y

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for s in slantics:
                    if s.rect.collidepoint(pygame.mouse.get_pos()):
                        s.drag = True
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        offset_x = s.x - mouse_x
                        offset_y = s.y - mouse_y

            if event.type == pygame.MOUSEBUTTONUP:
                for s in slantics:
                    s.drag = False

            if event.type == pygame.KEYDOWN:
                for s in slantics:
                    if s.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.key == pygame.K_r:
                            s.rotate()
                        if event.key == pygame.K_f:
                            s.flip()

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


