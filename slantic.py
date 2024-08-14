import pygame
from tile import Tile
import random


class Slantic(Tile):
    '''
    The main slantics class. Inherits from Tile.
    It sets up four images drawn using the pygame.draw.polygon method.
    The definition of the polygons are defined by the "shapes" variable.
    Four shapes are drawn.
        * front_tile
        * back_tile
        * select_front_tile
        * select_back_tile

    It then makes a random choice on whether the tile should be flipped
    horizontally.

    These images are then passed to the main Tile class.

    Attributes
    ----------
    pos : tuple, optional
        The position to create the tile at. Default is (0,0)
    size : int, optional
        The size to scale the tile down or up to.

    Methods
    -------
    rotate():
        Rotates the tile
    flip():
        Flips the tile
    '''
    def __init__(self, pos=(0, 0), size=50):
        # Setting up colors
        fg_color = 'dark blue'
        bg_color = 'light blue'
        select_fg_color = 'dark green'
        select_bg_color = 'light green'

        # Setting up coords for drawing polygons
        top_left = (0, 0)
        top_middle = (size/2, 0)
        top_right = (size, 0)
        middle_left = (0, size/2)
        middle = (size/2, size/2)
        middle_right = (size, size/2)
        bottom_left = (0, size)
        bottom_middle = (size/2, size)
        bottom_right = (size, size)

        # Set up the shapes using the above coords
        # The tuples describes the order in which to drag the polygons
        shapes = {
            'bar_l': {
                "poly": (middle_left,
                         top_right,
                         middle_right,
                         bottom_left),
                "edges": ((True, True),
                          (False, True),
                          (True, True),
                          (False, True))
            },
            'bar_r': {
                "poly": (middle_right,
                         top_left,
                         middle_left,
                         bottom_right),
                "edges": ((True, True),
                          (True, False),
                          (True, True),
                          (True, False))
            },
            'beam_l': {
                "poly": (middle_left,
                         top_middle,
                         top_right,
                         middle_right,
                         bottom_left),
                "edges": ((True, False),
                          (False, True),
                          (True, True),
                          (False, True))
            },
            'beam_r': {
                "poly": (middle_right,
                         top_middle,
                         top_left,
                         middle_left,
                         bottom_right),
                "edges": ((False, True),
                          (True, False),
                          (True, True),
                          (True, False))
            },
            'bit': {
                "poly": (middle_left,
                         bottom_middle,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (True, False),
                          (False, True))
            },
            'bonus': {
                "poly": (top_left,
                         top_right,
                         bottom_right,
                         bottom_left),
                "edges": ((False, False),
                          (False, False),
                          (False, False),
                          (False, False))
            },
            'corner_l': {
                "poly": (top_middle,
                         middle_right,
                         bottom_right,
                         bottom_left),
                "edges": ((True, True),
                          (True, False),
                          (False, False),
                          (True, True))
            },
            'corner_r': {
                "poly": (top_middle,
                         middle_left,
                         bottom_left,
                         bottom_right),
                "edges": ((True, True),
                          (True, True),
                          (False, False),
                          (False, True))
            },
            'crux': {
                "poly": (middle,
                         bottom_right,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (False, False),
                          (True, True))
             },
            'fang_l': {
                "poly": (middle_right,
                         bottom_middle,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (True, False),
                          (True, True))
            },
            'fang_r': {
                "poly": (middle_left,
                         bottom_middle,
                         bottom_right),
                "edges": ((True, True),
                          (True, True),
                          (False, True),
                          (True, True))
            },
            'hex': {
                "poly": (top_middle,
                         top_right,
                         middle_right,
                         bottom_middle,
                         bottom_left,
                         middle_left),
                "edges": ((True, False),
                          (False, True),
                          (True, False),
                          (False, True))
            },
            'hill': {
                "poly": (top_middle,
                         middle_right,
                         bottom_right,
                         bottom_left,
                         middle_left),
                "edges": ((True, True),
                          (True, False),
                          (False, False),
                          (False, True))
            },
            'peak': {
                "poly": (top_middle,
                         bottom_right,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (False, False),
                          (True, True))
            },
            'point': {
                "poly": (top_left,
                         middle_right,
                         bottom_right,
                         bottom_middle),
                "edges": ((True, True),
                          (True, False),
                          (False, True),
                          (True, True))
            },
            'slant': {
                "poly": (top_left,
                         top_right,
                         bottom_left),
                "edges": ((False, False),
                          (True, True),
                          (True, True),
                          (False, False))
            },
            'slope_l': {
                "poly": (middle_left,
                         bottom_right,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (False, False),
                          (False, True))
            },
            'slope_r': {
                "poly": (middle_right,
                         bottom_left,
                         bottom_right),
                "edges": ((True, True),
                          (True, False),
                          (False, False),
                          (True, True))
            },
            'spike_l': {
                "poly": (top_right,
                         bottom_left,
                         middle_left),
                "edges": ((True, True),
                          (True, True),
                          (True, True),
                          (False, True))
            },
            'spike_r': {
                "poly": (top_left,
                         bottom_right,
                         middle_right),
                "edges": ((True, True),
                          (True, False),
                          (True, True),
                          (True, True))
            },
            'strip': {
                "poly": (top_middle,
                         top_right,
                         bottom_left,
                         middle_left),
                "edges": ((True, False),
                          (True, True),
                          (True, True),
                          (False, True))
            }
        }

        # Choose a shape at random
        self.shape_key = random.choice(list(shapes.keys()))

        # Draw the front tile
        front_tile = pygame.Surface((size, size))
        front_tile.fill(bg_color)
        pygame.draw.polygon(front_tile,
                            fg_color,
                            shapes[self.shape_key]["poly"])

        # Draw the back tile
        back_tile = pygame.Surface((size, size))
        back_tile.fill(fg_color)
        pygame.draw.polygon(back_tile,
                            bg_color,
                            shapes[self.shape_key]["poly"])

        # Draw the front select tile
        select_front_tile = pygame.Surface((size, size))
        select_front_tile.fill(select_bg_color)
        pygame.draw.polygon(select_front_tile,
                            select_fg_color,
                            shapes[self.shape_key]["poly"])

        # Draw the back select tile
        select_back_tile = pygame.Surface((size, size))
        select_back_tile.fill(select_fg_color)
        pygame.draw.polygon(select_back_tile,
                            select_bg_color,
                            shapes[self.shape_key]["poly"])

        # Set the edges variable for future reference
        self.edges = shapes[self.shape_key]["edges"]

        super().__init__(front_tile=front_tile,
                         back_tile=back_tile,
                         select_front_tile=select_front_tile,
                         select_back_tile=select_back_tile,
                         pos=pos,
                         size=size)

    def rotate(self):
        '''
        Override for the tile rotate method. Adds rotation of edges.
        '''
        self.edges = (self.edges[3],
                      self.edges[0],
                      self.edges[1],
                      self.edges[2])
        print(self.edges)
        print('---------')

        super().rotate()

    def flip(self):
        '''
        Override for the tile flip method. Adds flipping of edges.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        flipped_edges = ()

        # Switch all 0s to 1s and all 1s to 0s
        # Use a temp tuple because tuples are immutable
        for edge in self.edges:
            flipped_edge = ()
            for val in edge:
                flipped_edge += (not val,)
            flipped_edges += (flipped_edge,)

        self.edges = flipped_edges

        super().flip()

    def handle_events(self, events):
        for event in events:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
                and self.rect.collidepoint(pygame.mouse.get_pos())
            ):
                self.rotate()
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_f
                and self.rect.collidepoint(pygame.mouse.get_pos())
            ):
                self.flip()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button:
                keys = pygame.key.get_pressed()
                if (
                    (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
                    and self.rect.collidepoint(pygame.mouse.get_pos())
                ):
                    super().select(True)

    def update(self, events):
        '''
        Override for the sprite update class. Handles key events.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        self.handle_events(events)
        super().update(events)
