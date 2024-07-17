
import random
import yaml

import tileset
import messages

class Map:
    def __init__(self, name, player, width = 80, height = 25):

        self._width = width
        self._height = height

        self._player = player

        self.load(name)

    def load(self, name):

        # load the map
        with open(f"data/map-{name}.yaml", 'r') as f:
            map = yaml.safe_load(f)

        lines = []

        # if we have some map data, strip the trailing newline, replace spaces with dots and split into lines
        # we replace spaces with dots so that they resolve to null tiles
        # in map data, spaces should only be using inside buildings
        map_data = map.get('data', '').rstrip().replace(' ', '.').split("\n")

        # process each line of map data
        for n, line in enumerate(map_data):

            # calc it once
            line_len = len(line)

            # empty line so pad it with spaces - will become default terrain
            if line_len == 0:
                line = ' ' * self._width

            # line too short so center it with spaces
            elif line_len < self._width:
                lpad = (self._width - line_len) // 2
                rpad = self._width - line_len - lpad
                line = ' ' * lpad + line + ' ' * rpad

            # line too long so truncate it
            elif line_len > self._width:
                # TODO: log error
                line = line[:self._width]

            lines.append(line)

        # if we have less lines than the height of the map then center it vertically
        if len(lines) < self._height:
            tpad = (self._height - len(lines)) // 2
            bpad = self._height - len(lines) - tpad
            lines = ([" " * self._width] * tpad) + lines + ([" " * self._width] * bpad)

        # convert the map to a 2D array of tiles
        self.tiles = [[self._make_tile(char) for char in line] for line in lines]

    def move_player(self, player, dx, dy):

        if player.x + dx < 0 or player.x + dx >= self._width:
            dx = 0

        if player.y + dy < 0 or player.y + dy >= (self._height):
            dy = 0

        # if the tile is walkable then move the player
        if self.tiles[player.y + dy][player.x + dx].walkable:
            player.move(dx, dy)

    def _make_tile(self, char):
        """Decode a map character into a tile"""

        # spaces are default terrain
        if char == ' ':
            char = random.choice('♣,,,,')

        match char:
            # 75% tree, 25% grass
            case 'Y':
                char = random.choice('♣♣♣,')
            # 50% tree, 50% grass
            case 'y':
                char = random.choice('♣♣,,')
            # 10% tree, 90% grass
            case ';':
                char = random.choice('♣,,,,,,,,,')

        # straight forward lookup for single purpose tiles
        lookup = {
            'D' : 'door_open',
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
