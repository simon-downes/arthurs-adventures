
import random
import yaml

import tileset

class Map:
    def __init__(self, name, player):

        self._player = player

        self.load(name)

    def load(self, name):

        # load the map
        with open(f"data/map-{name}.yaml", 'r') as f:
            map = yaml.safe_load(f)

        # set the map attributes
        self.width  = map.get('width')
        self.terrain = map.get('terrain')

        lines = []

        for n, line in enumerate(map.get('data').rstrip().split("\n")):

            # empty line so pad it with spaces
            if len(line) == 0:
                # TODO: log error
                line = " " * self.width

            # line too short so pad it with last character
            elif len(line) < self.width:
                line = line.ljust(self.width, line[-1])

            # line too long so truncate it
            elif len(line) > self.width:
                # TODO: log error
                line = line[:self.width]

            lines.append(line)

        # height of the map is always just the number of lines defined
        self.height = len(lines)

        for line in lines:
            print(line)

        print(self.width, self.height)

        # convert the map to a 2D array of tiles
        self.tiles = [[self._make_tile(char) for char in line] for line in lines]

        # position player - default to center of the map
        self._player.x = self.width // 2
        self._player.y = self.height // 2

    def move_player(self, player, dx, dy):

        if player.x + dx < 0 or player.x + dx >= self.width:
            dx = 0

        if player.y + dy < 0 or player.y + dy >= (self.height):
            dy = 0

        # if the tile is walkable then move the player
        if self.tiles[player.y + dy][player.x + dx].walkable:
            player.move(dx, dy)

    def _make_tile(self, char):
        """Decode a map character into a tile"""

        match char:
            # 75% tree, 25% grass
            case 'Y':
                char = random.choice('♣♣♣,')
            # 50% tree, 50% grass
            case 'y':
                char = random.choice('♣♣,,')
            # 25% tree, 75% grass
            case ';':
                char = random.choice('♣,,,,')

        # straight forward lookup for single purpose tiles
        lookup = {
            'D' : 'door_closed',
            ',' : 'grass',
            '~' : 'water',
            '╔' : 'wall_nw',
            '╦' : 'wall_n',
            '╗' : 'wall_ne',
            '║' : 'wall_v',
            '═' : 'wall_h',
            '╠' : 'wall_w',
            '╬' : 'wall_x',
            '╣' : 'wall_e',
            '╚' : 'wall_sw',
            '╩' : 'wall_s',
            '╝' : 'wall_se',
        }

        if char in lookup:
            return tileset.get_tile(lookup[char])

        match char:
            # path - make it random
            case '-':
                return tileset.get_tile(f"{self.terrain}_path")
                return tileset.get_tile('path_' + str(random.randint(1, 2)))

            # must be a tree so return a random one
            case '♣':
                return tileset.get_tile('tree_' + str(random.randint(1, 10)))
            # can be grass or tree

        # no match so return the null tile
        return tileset.get_tile('null')
