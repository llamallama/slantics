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
    add_to_group(events):
        Groups the tile
    update(events):
        Override for the sprite update class. Runs all of the above functions.

    '''
    def __init__(self, front_tile=None, back_tile=None, pos=(0, 0), size=50):
        '''
        Performs the initial tile setup.

        Parameters
        ----------
        front_tile : pygame.Surface, optional
            The path to the front tile
        back_tile : pygame.Surface, optional
            The path to the back tile
        pos : tuple, optional
            The position to create the tile at. Default is (0,0)
        size : int, optional
            The size to scale the tile down or up to.

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
        # Set the tiles images
        if not front_tile:
            front_tile = pygame.Surface((size, size))
            front_tile.fill('blue')
        if not back_tile:
            back_tile = pygame.Surface((size, size))
            back_tile.fill('black')
        # Scale the tiles to size
        front_tile = pygame.transform.smoothscale(front_tile, (size, size))
        back_tile  = pygame.transform.smoothscale(back_tile, (size, size))

        self.tiles = [front_tile, back_tile]
        self.image = self.tiles[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False
        self.group = False

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
            if event.type == pygame.MOUSEBUTTONDOWN and self.group:
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


    def add_to_group(self, events):
        '''
        Groups the tile. It does this by switching the value of self.group.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.group = not self.group

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
        self.add_to_group(events)

