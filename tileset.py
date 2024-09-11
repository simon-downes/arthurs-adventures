# tiles represent all the graphically elements of the game

import yaml

_tileset = {}

def get_tile(name):

    global _tileset

    # if the name is already a Tile object, return it
    if isinstance(name, Tile):
        return name

    # if the tileset hasn't been loaded yet, load it
    if not _tileset:

        with open('data/tileset.yaml', 'r') as f:
            tiles = yaml.safe_load(f)

        # for every tile in the tileset, create a Tile object and store it in the _tileset dictionary
        _tileset = {name: Tile(name, *tile) for name, tile in tiles.items()}

    # lookup the tile in the tileset, default to the empty tile if not found
    return _tileset.get(name, _tileset.get('empty'))

class Tile():
    def __init__(self, name, char, fg="", bg="", walkable=True):
        self.name = name
        self.char = char
        self.fg = fg
        self.bg = bg
        self.walkable = walkable

    def __str__(self):
        return self.char
