import pygame

class Board():
    '''
    A class that handles all slantics board operations

    Attributes
    ----------
    rows : int
        The number of rows in the board
    cols : int
        The number of columns in the board
    block_size : int
        The size of the board cells in pixels
    board : list
        The board's data represents as a two dimension array
    screen : pygame.Surface
        The pygame surface to draw the board on

    Methods
    -------
    draw_grid():
        Draws the grid onto the screen
    snap():
        Snaps tiles into place after dragging
    '''
    def __init__(self, screen, block_size):
        '''
        Performs the initial board setup

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw the board on
        block_size : int
            The size of the board cells in pixels
        '''

        self.rows = int(screen.get_rect().width/block_size)
        self.cols = int(screen.get_rect().height/block_size)
        self.block_size = block_size

        # Initialize the blank board
        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        self.screen = screen


    def draw_grid(self):
        '''
        Draws the grid onto the screen

        Parameters
        ---------
        None

        Returns
        -------
        None
        '''
        for x in range(self.rows):
            for y in range(self.cols):
                rect = pygame.Rect(
                    x * self.block_size,
                    y * self.block_size,
                    self.block_size,
                    self.block_size
                )
                pygame.draw.rect(self.screen, 'gray80', rect, 1)

    def sync(self):
        '''
        Updates tile positions as they are represented in the board array.

        Parameters
        ---------
        None

        Returns
        -------
        None
        '''

        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                if self.board[row][col]:
                    cell_y = row * self.block_size
                    cell_x = col * self.block_size
                    self.board[row][col].rect.x = cell_x
                    self.board[row][col].rect.y = cell_y


    def update(self):
        '''
        Continually updates the board

        Parameters
        ---------
        None

        Returns
        -------
        None
        '''
        self.draw_grid()
        self.sync()
