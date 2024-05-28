from tile import Tile
import random


class Slantic(Tile):
    def __init__(self, pos=(0, 0), size=50):
        tile_types = [
            ("bar-dark-l", "bar-lite-l"),
            ("bar-dark-r", "bar-lite-r"),
            ("beam-dark-l", "beam-lite-l"),
            ("beam-dark-r", "beam-lite-r"),
            ("bit-dark", "bit-lite"),
            ("bonus-dark", "bonus-lite"),
            ("corner-dark-l", "corner-lite-l"),
            ("corner-dark-r", "corner-lite-r"),
            ("crux-dark", "crux-lite"),
            ("fang-dark-l", "fang-lite-l"),
            ("fang-dark-r", "fang-lite-r"),
            ("hex-dark", "hex-lite"),
            ("hill-dark", "hill-lite"),
            ("peak-dark", "peak-lite"),
            ("point-dark", "point-lite"),
            ("slope-dark-l", "slope-lite-l"),
            ("slope-dark-r", "slope-lite-r"),
            ("spike-dark-l", "spike-lite-l"),
            ("spike-dark-r", "spike-lite-r"),
            ("strip-dark", "strip-lite"),
            ("slant-dark", "slant-lite")
        ]

        tile_type = random.choice(tile_types)
        super().__init__(f'tiles/{tile_type[0]}.png',
                         f'tiles/{tile_type[1]}.png',
                         pos,
                         size)
