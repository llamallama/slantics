import pygame
from tile import Tile
import random


class Slantic(Tile):
    def __init__(self, pos=(0, 0), size=50):
        # Setting up colors
        fg_color = 'dark blue'
        bg_color = 'light blue'

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
                "poly": (middle_left, top_right, middle_right, bottom_left)
            },
            'beam': {
                "poly": (middle_left, top_middle, top_right, middle_right, bottom_left)
            },
            'bit': {
                "poly": (middle_left, bottom_middle, bottom_left)
            },
            'bonus': {
                "poly": (top_left, top_right, bottom_right, bottom_left)
            },
            'corner': {
                "poly": (top_middle, middle_right, bottom_right, bottom_left)
            },
            'crux': {
                "poly": (middle, bottom_right, bottom_left)
             },
            'fang': {
                "poly": (middle_right, bottom_middle, bottom_left)
            },
            'hex': {
                "poly": (top_middle, top_right, middle_right, bottom_middle, bottom_left, middle_left)
            },
            'hill': {
                "poly": (top_middle, middle_right, bottom_right, bottom_left, middle_left)
            },
            'peak': {
                "poly": (top_middle, bottom_right, bottom_left)
            },
            'point': {
                "poly": (top_left, middle_right, bottom_right, bottom_middle)
            },
            'slant': {
                "poly": (top_left, top_right, bottom_left)
            },
            'slope': {
                "poly": (middle_left, bottom_right, bottom_left)
            },
            'spike': {
                "poly": (top_right, bottom_left, middle_left)
            },
            'strip': {
                "poly": (top_middle, top_right, bottom_left, middle_left)
            }
        }

        # Choose a shape at random
        shape_key = random.choice(list(shapes.keys()))

        # Draw the front tile
        front_tile = pygame.Surface((size, size))
        front_tile.fill(bg_color)
        pygame.draw.polygon(front_tile, fg_color, shapes[shape_key]["poly"])

        # Draw the back tile
        back_tile = pygame.Surface((size, size))
        back_tile.fill(fg_color)
        pygame.draw.polygon(back_tile, bg_color, shapes[shape_key]["poly"])

        # Randomly choose to flip the slantic
        if random.choice([True, False]):
            front_tile = pygame.transform.flip(front_tile, True, False)
            back_tile = pygame.transform.flip(back_tile, True, False)

        super().__init__(front_tile=front_tile,
                         back_tile=back_tile,
                         pos=pos,
                         size=size)
