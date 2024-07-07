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
    rotate(events):
        Rotates the tile
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
            'bar': {
                "poly": (middle_left,
                         top_right,
                         middle_right,
                         bottom_left),
                "edges": ((True, True),
                          (False, True),
                          (True, True),
                          (False, True))
            },
            'beam': {
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
            'corner': {
                "poly": (top_middle,
                         middle_right,
                         bottom_right,
                         bottom_left),
                "edges": ((True, True),
                          (True, False),
                          (False, False),
                          (True, True))
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
            'fang': {
                "poly": (middle_right,
                         bottom_middle,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (True, False),
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
            'slope': {
                "poly": (middle_left,
                         bottom_right,
                         bottom_left),
                "edges": ((True, True),
                          (True, True),
                          (False, False),
                          (False, True))
            },
            'spike': {
                "poly": (top_right,
                         bottom_left,
                         middle_left),
                "edges": ((True, True),
                          (True, True),
                          (True, True),
                          (False, True))
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
        shape_key = random.choice(list(shapes.keys()))

        # Draw the front tile
        front_tile = pygame.Surface((size, size))
        front_tile.fill(bg_color)
        pygame.draw.polygon(front_tile,
                            fg_color,
                            shapes[shape_key]["poly"])

        # Draw the back tile
        back_tile = pygame.Surface((size, size))
        back_tile.fill(fg_color)
        pygame.draw.polygon(back_tile,
                            bg_color,
                            shapes[shape_key]["poly"])

        # Draw the front select tile
        select_front_tile = pygame.Surface((size, size))
        select_front_tile.fill(select_bg_color)
        pygame.draw.polygon(select_front_tile,
                            select_fg_color,
                            shapes[shape_key]["poly"])

        # Draw the back select tile
        select_back_tile = pygame.Surface((size, size))
        select_back_tile.fill(select_fg_color)
        pygame.draw.polygon(select_back_tile,
                            select_bg_color,
                            shapes[shape_key]["poly"])

        # Set the edges variable for future reference
        self.edges = shapes[shape_key]["edges"]

        # Randomly choose to flip the slantic
        if random.choice([True, False]):
            front_tile = pygame.transform.flip(front_tile, True, False)
            back_tile = pygame.transform.flip(back_tile, True, False)
            select_front_tile = pygame.transform.flip(select_front_tile,
                                                      True,
                                                      False)
            select_back_tile = pygame.transform.flip(select_back_tile,
                                                     True,
                                                     False)

            # Swap edge 1 and 3. Reverse them so the edge is properly flipped.
            self.edges = (
                self.edges[0][::-1],
                self.edges[3][::-1],
                self.edges[2][::-1],
                self.edges[1][::-1])

        super().__init__(front_tile=front_tile,
                         back_tile=back_tile,
                         select_front_tile=select_front_tile,
                         select_back_tile=select_back_tile,
                         pos=pos,
                         size=size)

    def rotate(self, events):
        '''
        Override for the tile rotate method. Adds rotation of edges.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        for event in events:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
                and self.rect.collidepoint(pygame.mouse.get_pos())
            ):
                self.edges = (self.edges[3],
                              self.edges[0],
                              self.edges[1],
                              self.edges[2])

        super().rotate(events)

    def flip(self, events):
        '''
        Override for the tile flip method. Adds flipping of edges.

        Parameters
        ----------
        events : list
            The pygame.events list passed in as a parameter
        '''
        for event in events:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_f
                and self.rect.collidepoint(pygame.mouse.get_pos())
            ):
                flipped_edges = ()

                # Switch all 0s to 1s and all 1s to 0s
                for edge in self.edges:
                    flipped_edge = ()
                    for val in edge:
                        flipped_edge += (not val,)
                    flipped_edges += (flipped_edge,)

                self.edges = flipped_edges

        super().flip(events)
