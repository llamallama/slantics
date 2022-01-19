#!/usr/bin/env python
import pygame
import math
import numpy as np
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 100
MARGIN = 1

BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
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
    def __init__(self, shape, x, y, surface, size=BLOCK_SIZE, padding=2):
        # _og vars are used to track previous position. This is useful
        # to prevent one shape to be dropped onto another. If that happens
        # it will return to its original position.

        self.x = self._og_x = x * BLOCK_SIZE + MARGIN
        self.y = self._og_y = y * BLOCK_SIZE + MARGIN

        self.width = BLOCK_SIZE - padding
        self.height = BLOCK_SIZE - padding
        self.surface = surface
        self.shape = shape
        self.color_light = WHITE
        self.color_dark = BLUE
        self._dark = True
        self._coords = []
        self._offset_x = None
        self._offset_y = None
        self.enable_drag = False
        self.rotation = 0
        self.rect = self.drawSlantic()

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
                (self.x + self.width, self.y + self.height/2)
            ],
            [
                (self.x, self.y + self.height),
                (self.x + self.width/2, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
        ]

        self._coords = np.rot90(self._coords, self.rotation).tolist()

        poly_list = []

        fill_color = self.color_light if self._dark else self.color_dark
        poly_color = self.color_dark if self._dark else self.color_light

        for num in range(1, 10):
            for index, s in enumerate(self.shape):
                if num in s:
                    poly_list.append(self._coords[index][s.index(num)])
                    continue

        self.rect = pygame.draw.rect(
            self.surface, fill_color, (self.x, self.y, self.width, self.height)
        )

        if len(poly_list) > 2:
            pygame.draw.polygon(self.surface, poly_color, poly_list)

        return self.rect

    def flip(self):
        self._dark = not self._dark

    def rotate(self):
        self.rotation += 1
        if self.rotation == 4:
            self.rotation = 0

    # Snap to grid or snap back to original position if on top of another piece
    def _snap(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for s in slantics:
            if self != s:
                # Space is taken. Go back to original position
                if self.rect.colliderect(s.rect):
                    self.x = self._og_x
                    self.y = self._og_y
                    break
                # Space is free. Stay here.
                else:
                    mult_x = math.floor(mouse_x/BLOCK_SIZE)
                    mult_y = math.floor(mouse_y/BLOCK_SIZE)
                    self.x = mult_x * BLOCK_SIZE + MARGIN
                    self.y = mult_y * BLOCK_SIZE + MARGIN

        self._og_x = self.x
        self._og_y = self.y

    def drag(self):
        if self.enable_drag:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Set the mouse offset before we drag
            if not self._offset_x:
                self._offset_x = self.x - mouse_x
                self._offset_y = self.y - mouse_y

            self.x = mouse_x + self._offset_x
            self.y = mouse_y + self._offset_y
        else:
            # Only snap to grid once while offset still has a value
            if self._offset_x:
                self._snap()
            # Keep offset at none until it is time to drag
            self._offset_x = None
            self._offset_y = None

            self.enable_drag = False


def setup_tiles():
    bar_r = Slantic(SHAPES["bar"], 0, 0, screen)
    bar_l = Slantic(np.fliplr(SHAPES["bar"]).tolist(), 1, 0, screen)
    beam_r = Slantic(SHAPES["beam"], 2, 0, screen)
    beam_l = Slantic(np.fliplr(SHAPES["beam"]).tolist(), 3, 0, screen)
    bit = Slantic(SHAPES["bit"], 4, 0, screen)
    corner_r = Slantic(SHAPES["corner"], 5, 0, screen)
    corner_l = Slantic(np.fliplr(SHAPES["corner"]).tolist(), 6, 0, screen)
    crux = Slantic(SHAPES["crux"], 7, 0, screen)
    fang_r = Slantic(SHAPES["fang"], 0, 1, screen)
    fang_l = Slantic(np.fliplr(SHAPES["fang"]).tolist(), 1, 1, screen)
    hexx = Slantic(SHAPES["hexx"], 2, 1, screen)
    hill = Slantic(SHAPES["hill"], 3, 1, screen)
    peak = Slantic(SHAPES["peak"], 4, 1, screen)
    point = Slantic(SHAPES["point"], 5, 1, screen)
    slant = Slantic(SHAPES["slant"], 6, 1, screen)
    slope_r = Slantic(SHAPES["slope"], 7, 1, screen)
    slope_l = Slantic(np.fliplr(SHAPES["slope"]).tolist(), 0, 2, screen)
    spike_r = Slantic(SHAPES["spike"], 1, 2, screen)
    spike_l = Slantic(np.fliplr(SHAPES["spike"]).tolist(), 2, 2, screen)
    strip = Slantic(SHAPES["strip"], 3, 2, screen)
    bonus = Slantic(SHAPES["bonus"], 4, 2, screen)

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


def handle_keys(event):
    if event.type == pygame.KEYDOWN:
        for s in slantics:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_r:
                    s.rotate()
                if event.key == pygame.K_f:
                    s.flip()


def handle_mouse(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for s in slantics:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                s.enable_drag = True

    if event.type == pygame.MOUSEBUTTONUP:
        for s in slantics:
            s.enable_drag = False


def drawGrid():
    for y in range(len(BOARD)):
        for x in range(len(BOARD[y])):
            rect = pygame.Rect(
                x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(screen, BLACK, rect, 1)


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    fps = 60
    screen.fill(WHITE)

    global slantics
    slantics = setup_tiles()

    while True:
        pygame.display.update()
        screen.fill(WHITE)
        drawGrid()

        for s in slantics:
            s.drawSlantic()
            s.drag()

        for event in pygame.event.get():
            handle_mouse(event)
            handle_keys(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(fps)


main()
