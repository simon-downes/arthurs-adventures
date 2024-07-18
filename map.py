
import random
import yaml

import tileset
import messages

class Map:
    def __init__(self, name, player, width = 80, height = 25):

        self._width = width
        self._height = height

        self._player = player

        map = {}

        # load the map
        try:
            with open(f"data/map-{name}.yaml", 'r') as f:
                map = yaml.safe_load(f)
        except Exception as e:
            pass

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

            # convert the string to a list so we can change it later
            lines.append(list(line))

        # if we have less lines than the height of the map then center it vertically
        if len(lines) < self._height:
            tpad = (self._height - len(lines)) // 2
            bpad = self._height - len(lines) - tpad
            lines = [list(" " * self._width) for _ in range(tpad)] + lines + [list(" " * self._width) for _ in range(bpad)]

        # generate random origin points on each edge of the map
        origins = {
            'top' : [random.choice(range(20, 60)), 0],
            'bottom' : [random.choice(range(20, 60)), 24],
            'left' : [0, random.choice(range(6, 19))],
            'right' : [79, random.choice(range(6, 19))],
        }

        # generate an inflection point somewhere in the middle of the map
        inflection = self._inflection(*[0,0], *[80,25])

        # join the top and bottom origins to the inflection point
        self._make_path(lines, *origins['top'], *inflection, False)
        self._make_path(lines, *inflection, *origins['bottom'], False)

        # join the left and right origins to the inflection point
        self._make_path(lines, *origins['left'], *inflection, True)
        self._make_path(lines, *inflection, *origins['right'], True)

        # for debuging - dumps the map to the console
        # for line in lines:
        #     for char in line:
        #         print(char , end='')
        #     print("")
        # quit()

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

    def _hpath(self, lines, x, y, x2):
        for px in range(min(x, x2), max(x, x2) + 1):
            if lines[y][px] == ' ':
                lines[y][px] = '-'

    def _vpath(self, lines, x, y, y2):
        for py in range(min(y, y2), max(y, y2) + 1):
            if lines[py][x] == ' ':
                lines[py][x] = '-'


    def _inflection(self, x, y, x2, y2):

        # calc horizontal and vertical distance between the 2 points
        dx = max(x, x2) - min(x, x2)
        dy = max(y, y2) - min(y, y2)

        px = x
        py = y

        if dx:
            offset = dx // 5
            px = min(x, x2) + random.choice(range(offset, dx - offset))

        if dy:
            offset = dy // 5
            py = min(y, y2) + random.choice(range(offset, dy - offset))

        return px, py

    def _make_path(self, lines, x, y, x2, y2, hpath=None):

        # calc horizontal and vertical distance between the 2 points
        dx = max(x, x2) - min(x, x2)
        dy = max(y, y2) - min(y, y2)

        # debuging
        # px, py = self._inflection(x, y, x2, y2)
        # lines[py][px] = '%'

        # if haven't been told to prefer a horizontal path then decide based on the distance
        if hpath == None:
            hpath = dx > dy

        # if the points are on the same axis then we can just draw a straight line
        if dx == 0:
            self._vpath(lines, x, y, y2)

        elif dy == 0:
            self._hpath(lines, x, y, x2)

        # horizontal path with a vertical split
        elif hpath:

            offset = dx // 4
            px = min(x, x2) + random.choice(range(offset, dx - offset))

            self._hpath(lines, x, y, px)
            self._vpath(lines, px, y, y2)
            self._hpath(lines, px, y2, x2)

            # for debuging
            # lines[y][px] = '*'
            # lines[y2][px] = '*'

        # vertical path with a horizontal split
        else:

            offset = dy // 5
            py = min(y, y2) + random.choice(range(offset, dy - offset))

            self._vpath(lines, x, y, py)
            self._hpath(lines, x, py, x2)
            self._vpath(lines, x2, py, y2)

            # for debuging
            # lines[py][x] = '+'
            # lines[py][x2] = '+'

        # for debuging
        # lines[y][x] = '<'
        # lines[y2][x2] = '>'

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
                return tileset.get_tile(f"forest_path")
                # return tileset.get_tile(f"{self.terrain}_path")
                return tileset.get_tile('path_' + str(random.randint(1, 2)))

            # must be a tree so return a random one
            case '♣':
                return tileset.get_tile('tree_' + str(random.randint(1, 10)))
            # can be grass or tree

        # no match so return the null tile
        return tileset.get_tile('null')
