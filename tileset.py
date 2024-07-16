# tiles represent all the graphically elements of the game

import yaml

_tileset = {}

def load():

    global _tileset

    with open('data/tileset.yaml', 'r') as f:
        tiles = yaml.safe_load(f)

    # for every tile in the tileset, create a Tile object and store it in the _tileset dictionary
    _tileset = {name: Tile(name, *tile) for name, tile in tiles.items()}

def get_tile(name):

    global _tileset

    return _tileset.get(name, _tileset.get('empty'))

class Tile():
    def __init__(self, name, char, fg="", bg="", walkable=True):
        self.name = name
        self.char = char
        self.fg = fg
        self.bg = bg
        self.walkable = walkable
