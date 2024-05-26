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
    set(pos, val):
        Adds a value to the board and the specified position
    get(pos):
        Gets a value from the board at the specified position
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

    def set(self, pos, val):
        '''
        Adds a value to the board and the specified position

        Parameters
        ----------
        pos : tuple
            The position to add the value to
        val : pygame.Sprite
            The value to store in the board
        '''
        row = int(pos[0]/self.block_size)
        col = int(pos[1]/self.block_size)
        self.board[col][row] = val

    def get(self, pos):
        '''
        Gets a value from the board at the specified position

        Parameters
        ----------
        pos : tuple
            The position to get the value from

        Returns
        -------
        val:
            The value from the specified position
        '''
        return self.board[pos[0]][pos[1]]

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
                pygame.draw.rect(self.screen, 'black', rect, 1)

    def snap(self):
        '''
        Snaps tiles into place after dragging

        Parameters
        ---------
        None

        Returns
        -------
        None
        '''
        for rows in self.board:
            for cell in rows:
                if cell:
                    mouse_pos = pygame.mouse.get_pos()
                    cell.rect.x = int(mouse_pos[0]/self.block_size) * self.block_size
                    cell.rect.y = int(mouse_pos[1]/self.block_size) * self.block_size

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
        # self.snap()
