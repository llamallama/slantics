import pygame

class Board():
    def __init__(self, screen, block_size):

        self.rows = int(screen.get_rect().width/block_size)
        self.cols = int(screen.get_rect().height/block_size)
        self.block_size = block_size

        # Initialize the blank board
        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        self.screen = screen


    def set(self, pos, val):
        row = int(pos[0]/self.block_size)
        col = int(pos[1]/self.block_size)
        self.board[col][row] = val

    def get(self, pos):
        return self.board[pos[0]][pos[1]]

    def draw_grid(self):
        for x in range(self.rows):
            for y in range(self.cols):
                rect = pygame.Rect(
                    x * self.block_size,
                    y * self.block_size,
                    self.block_size,
                    self.block_size
                )
                pygame.draw.rect(self.screen, 'black', rect, 1)

    def snap(self):
        for rows in self.board:
            for cell in rows:
                if cell:
                    mouse_pos = pygame.mouse.get_pos()
                    cell.rect.x = int(mouse_pos[0]/self.block_size) * self.block_size
                    cell.rect.y = int(mouse_pos[1]/self.block_size) * self.block_size

    def update(self, events):
        self.draw_grid()
        # self.snap()
