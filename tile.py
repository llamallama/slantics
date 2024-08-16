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
    selected : bool
        If the tile is member of a group selection

    Methods
    -------
    drag(events):
        Drags the tile
    rotate():
        Rotates the tile
    flip():
        Flips the tile
    update(events):
        Override for the sprite update class. Runs all of the above functions.
    select(selected):
        Selects the tile for group dragging. Switches tiles to reflect
        its selection state.
    '''
    def __init__(
            self,
            front_tile=None,
            back_tile=None,
            select_front_tile=None,
            select_back_tile=None,
            pos=(0, 0),
            size=50
    ):
        '''
        Performs the initial tile setup.

        Parameters
        ----------
        front_tile : pygame.Surface, optional
            The path to the front tile
        back_tile : pygame.Surface, optional
            The path to the back tile
        select_front_tile : pygame.Surface, optional
            The path to the front tile when selected
        select_back_tile : pygame.Surface, optional
            The path to the back tile when selected
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
        back_tile = pygame.transform.smoothscale(back_tile, (size, size))

        self.tiles = [front_tile, back_tile, select_front_tile, select_back_tile]
        self.image = self.tiles[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False
        self.selected = False

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

        keys = pygame.key.get_pressed()

        for event in events:
            # Don't drag if the shift keys are pressed.
            # That means we are making a multiselection
            if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
                # Start dragging if selected
                if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
                    self.dragging = True
                # Move the tile in relation to the mouse
                if self.dragging and event.type == pygame.MOUSEMOTION:
                    self.rect.move_ip(event.rel)
            else:
                # Handle single shift click selection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.select(not self.selected)

            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

    def rotate(self):
        '''
        Rotates the tile 90 degrees and tracks the current rotation.
        '''
        # Keep the rotation value from growing too much
        self.rotation -= 90
        if self.rotation % 360 == 0:
            self.rotation = 0
        self.image = pygame.transform.rotate(self.image, -90)

    def flip(self):
        '''
        Flips the tile over. It does this by switching self.image between two surfaces.
        '''
        self.flipped = not self.flipped
        self.image = self.tiles[self.flipped + (self.selected * 2)]
        # Reapply previous rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)

    def select(self, selected):
        '''
        Selects the tile for group dragging. Switches tiles to reflect
        its selection state.

        Parameters
        ----------
        selected : bool
            Whether to select or not
        '''
        self.selected = selected
        self.image = self.tiles[self.flipped + (self.selected * 2)]
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
