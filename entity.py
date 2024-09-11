import logging

import tileset

class Entity:
    """Base class for all things in the game that can appear on the map"""

    def __init__(self, tile, name, x, y):

        self.tile = tileset.get_tile(tile)
        self.name = name
        self.x = x
        self.y = y

        logging.debug(f"Spwaned {self.name} at {self.x}, {self.y}")
