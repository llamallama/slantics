#!/usr/bin/env python
import pygame
import math
import numpy as np
import sys
import random
import itertools

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
RES_WIDTH = pygame.display.Info().current_w
RES_HEIGHT = pygame.display.Info().current_h
GRID_WIDTH = 30 if RES_WIDTH > RES_HEIGHT else 15
GRID_HEIGHT = 15 if RES_WIDTH > RES_HEIGHT else 23
BLOCK_SIZE = math.floor((pygame.display.Info().current_w - 100) / GRID_WIDTH)
WINDOW_WIDTH = BLOCK_SIZE * GRID_WIDTH
WINDOW_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
MARGIN = 1

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

# The initial slantics global
slantics = []

# Create the initial board. It is a two dimensional array of zeros
board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


class Slantic(object):
    def __init__(self, shape, x, y, surface, size=BLOCK_SIZE, padding=2):
        # og vars are used to track previous position. This is useful
        # to prevent one shape to be dropped onto another. If that happens
        # it will return to its original position.

        self.x = self.og_x = x * BLOCK_SIZE + MARGIN
        self.y = self.og_y = y * BLOCK_SIZE + MARGIN

        self.width = BLOCK_SIZE - padding
        self.height = BLOCK_SIZE - padding
        self.surface = surface
        self.shape = shape
        self.color_light = LIGHT_BLUE
        self.color_dark = BLUE
        self.group = False
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

    # Handle dropping after a drag
    def drop(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for s in slantics:
            if self != s:
                # Space is taken. Go back to original position
                if s.rect.collidepoint(pygame.mouse.get_pos()):
                    s.x = s.og_x = self.og_x
                    s.y = s.og_y = self.og_y
                    break
                else:
                    # Space is free. Stay here.
                    mult_x = math.floor(mouse_x/BLOCK_SIZE)
                    mult_y = math.floor(mouse_y/BLOCK_SIZE)
                    self.x = mult_x * BLOCK_SIZE + MARGIN
                    self.y = mult_y * BLOCK_SIZE + MARGIN

        self.og_x = self.x
        self.og_y = self.y

        # Done dragging. Reset offsets
        self._offset_x = None
        self._offset_y = None

    def drag(self):
        if self.enable_drag:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Set the mouse offset before we drag
            if not self._offset_x:
                self._offset_x = self.x - mouse_x
                self._offset_y = self.y - mouse_y

            self.x = mouse_x + self._offset_x
            self.y = mouse_y + self._offset_y


# Random selects and draws the inital set of slantics arranged around the
# edges of the board
def setup_slantics(screen):
    slantics = []

    # List to allow for mirror versions of
    allow_flip = ["bar", "beam", "corner", "fang", "slope", "spike"]

    for y, x in itertools.product(range(GRID_HEIGHT), range(GRID_WIDTH)):
        # Only deal the slantics around the edges of the board
        if (y == 0 or y == GRID_HEIGHT - 1) or (x == 0 or x == GRID_WIDTH - 1):
            name = random.choice(list(SHAPES))
            shape = SHAPES[name]

            if name in allow_flip and random.choice((True, False)):
                shape = np.fliplr(shape).tolist()

            slantics.append(Slantic(shape, x, y, screen))

    return slantics


# Sync the position of the Slantics with their position in the board list
def sync_board():

    # reset the board
    global board
    board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # then update it with the current clantic positions
    for s in slantics:
        board_y = int((s.y - 1)/BLOCK_SIZE)
        board_x = int((s.x - 1)/BLOCK_SIZE)
        board[board_y][board_x] = s


def handle_keys(event, screen):
    if event.type == pygame.KEYDOWN:
        for s in slantics:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_r:
                    s.rotate()
                if event.key == pygame.K_f:
                    s.flip()
                if event.key == pygame.K_f:
                    s.group = not s.group
        refresh(screen)


def handle_mouse(event, screen):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for s in slantics:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                s.enable_drag = True

    if event.type == pygame.MOUSEBUTTONUP:
        for s in slantics:
            if(s.enable_drag):
                s.enable_drag = False
                s.drop()

        sync_board()
        refresh(screen)


def draw_grid(screen):
    for y in range(len(board)):
        for x in range(len(board[y])):
            rect = pygame.Rect(
                x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(screen, BLACK, rect, 1)


# A wrapper function that redraws the background, grid, and all slantics
def refresh(screen):
    screen.fill(WHITE)
    draw_grid(screen)
    for s in slantics:
        s.drawSlantic()
    pygame.display.update()


def main():
    print(WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Slantics")
    clock = pygame.time.Clock()
    fps = 60

    # Hack to work around weird pygame bug where screen is black at
    # certain window sizes
    initial_draw = False

    screen.fill(WHITE)

    global slantics
    slantics = setup_slantics(screen)
    refresh(screen)
    sync_board()

    while True:
        # Hack to work around weird pygame bug where screen is black at
        # certain window sizes
        if not initial_draw:
            refresh(screen)
            initial_draw = not initial_draw

        for s in slantics:
            if s.enable_drag:
                s.drag()
                refresh(screen)

        for event in pygame.event.get():
            handle_mouse(event, screen)
            handle_keys(event, screen)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(fps)


main()
