#!/usr/bin/env python
import pygame

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

        self.coords = [(0,0),              (self.width/2, 0),             (self.width, 0),
                       (0, self.height/2), (self.width/2, self.height/2), (self.width, self.height/2),
                       (0, self.height),   (self.width/2, self.height),   (self.width, self.height)]

        self.shapes = {
            "bar_r": [2, 5, 6, 3],
            "bar_l": [0, 5, 8, 3],
            "fang_r": [3, 7, 8],
            "fang_l": [5, 6, 7],
            "crux": [4, 6, 7, 8]
        }

        self.drawSlantic()


    def drawSlantic(self):
        if self.mode == "dark":
            fill_color = self.color_light
            poly_color = self.color_dark
        else:
            fill_color = self.color_dark
            poly_color = self.color_light

        poly_list = [self.coords[x] for x in self.shapes[self.shape]]
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

    slantics.append(Slantic("bar_r", 0, 0, SCREEN))
    slantics.append(Slantic("bar_l", 1, 0, SCREEN))
    slantics.append(Slantic("fang_r", 2, 0, SCREEN))
    slantics.append(Slantic("fang_l", 3, 0, SCREEN))
    slantics.append(Slantic("crux", 4, 0, SCREEN))

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


