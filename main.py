#!/usr/bin/env python
import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 100
PADDED_BLOCK_SIZE = 98

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

SLANTIC_TYPES = {
    "bar": [
        (0,PADDED_BLOCK_SIZE/2),
        (PADDED_BLOCK_SIZE, 0),
        (PADDED_BLOCK_SIZE, PADDED_BLOCK_SIZE/2),
        (0, PADDED_BLOCK_SIZE)]
}

slantics=[]

class Slantic(object):
    def __init__(self, x, y, color, screen):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.width = PADDED_BLOCK_SIZE
        self.height = PADDED_BLOCK_SIZE
        self.color = color
        self.surface = pygame.Surface((self.width, self.height))
        self.screen = screen

        self.drawSlantic()

    def drawSlantic(self):

        poly = SLANTIC_TYPES["bar"][::-1]
        pygame.draw.polygon(self.surface, self.color, poly)
        # self.surface.fill(self.color)
        self.screen.blit(self.surface, (self.x + 1, self.y + 1))


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    drawGrid()

    fps = 30

    for y in range(len(BOARD)):
        slantics.append([])
        for x in range(len(BOARD[y])):
            slantics[y].append(Slantic(x, y, RED, SCREEN))

    while True:
        SCREEN.fill(BLACK)
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for y in range(len(BOARD)):
            slantics.append([])
            for x in range(len(BOARD[y])):
                slantics[y][x].drawSlantic()

        pygame.display.update()
        CLOCK.tick(fps)


def drawGrid():
    for y in range(len(BOARD)):
        for x in range(len(BOARD[y])):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

main()


