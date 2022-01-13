#!/usr/bin/env python
import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
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

slantics=[]

class Slantic(object):
    def __init__(self, shape, x, y, screen, size=BLOCK_SIZE, padding=2):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.width = BLOCK_SIZE - padding
        self.height = BLOCK_SIZE - padding
        self.surface = pygame.Surface((self.width, self.height))
        self.screen = screen
        self.shape = shape
        self.color_light = (77, 94, 100)
        self.color_dark = (0, 9, 60)

        self.coords = [(0,0),              (self.width/2, 0),           (self.width, 0),
                       (0, self.height/2),                              (self.width, self.height/2),
                       (0, self.height),   (self.width/2, self.height), (self.width, self.height)]

        self.shapes = {
            "bar": [3, 2, 4, 5]
        }

        self.drawSlantic()


    def drawSlantic(self):
        poly_list = [self.coords[x] for x in self.shapes[self.shape]]
        self.surface.fill(self.color_light)
        pygame.draw.polygon(self.surface, self.color_dark, poly_list)
        self.screen.blit(self.surface, (self.x + 1, self.y + 1))


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    # drawGrid()

    fps = 30

    # for y in range(len(BOARD)):
    #     slantics.append([])
    #     for x in range(len(BOARD[y])):
    #         slantics[y].append(Slantic("bar", x, y, SCREEN))

    while True:
    #     SCREEN.fill(BLACK)
    #     drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    #     for y in range(len(BOARD)):
    #         slantics.append([])
    #         for x in range(len(BOARD[y])):
    #             slantics[y][x].drawSlantic()

        pygame.display.update()
        CLOCK.tick(fps)


def drawGrid():
    for y in range(len(BOARD)):
        for x in range(len(BOARD[y])):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

main()


