import pygame

class Tile(pygame.sprite.Sprite):
    '''
    Tile class. Extends pygame.Sprite. Handles things like moving, rotating, and flipping square tiles.

    Attributes
    ----------
    tiles : list
        A list of the front and back face of the tile
    image : pygame.Surface
        The current image surface applied to the tile
    rect: int
        The size of the board cells in pixels
    board : list
        The board's data represents as a two dimension array
    dragging : bool
        Tracks if the tile is being dragged

    Methods
    -------
    drag(events):
        Drags the tile
    rotate(events):
        Rotates the tile
    flip(events):
        Flips the tile
    update(events):
        Override for the sprite update class. Runs all of the above functions.

    '''
    def __init__(self, pos=(0, 0)):
        '''
        Performs the initial tile setup.

        Parameters
        ----------
        pos : tuple, optional
            The position to create the tile at. Default is (0,0)

        Attributes
        ----------
        tiles : list
            A list that contains the front and back images of the tile
        dragging : bool
            Tracks if the tile is being dragged
        rotation : int
            The current rotation angle of the tile
        flipped : bool
            Whether or not the tile is currently flipped

        '''
        super().__init__()
        tile1 = pygame.image.load('tile1.png').convert_alpha()
        tile2 = pygame.image.load('tile2.png').convert_alpha()
        self.tiles = [tile1, tile2]
        self.image = self.tiles[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False

        # To track rotation value to reapply on flip
        self.rotation = 0
        self.flipped = False

    def drag(self, events):
        '''
        Mouse dragging for the tile

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if self.dragging and event.type == pygame.MOUSEMOTION:
                self.rect.move_ip(event.rel)

    def rotate(self, events):
        '''
        Rotates the tile 90 degrees and tracks the current rotation.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.rect.collidepoint(pygame.mouse.get_pos()):
                # Keep the rotation value from growing too much
                self.rotation -= 90
                if self.rotation % 360 == 0: self.rotation = 0
                self.image = pygame.transform.rotate(self.image, -90)

    def flip(self, events):
        '''
        Flips the tile over. It does this by switching self.image between two surfaces.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.flipped = not self.flipped
                self.image = self.tiles[self.flipped]
                # Reapply previous rotation
                self.image = pygame.transform.rotate(self.image, self.rotation)

    def update(self, events):
        '''
        Override for the sprite update class. Runs all of the above functions.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        self.drag(events)
        self.rotate(events)
        self.flip(events)

