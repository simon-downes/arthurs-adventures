
from map import Map
import messages

WORLD_WIDTH = 10
WORLD_HEIGHT = 10

MAP_WIDTH = 80
MAP_HEIGHT = 25

class World:

    def __init__(self, player):

        self._maps = [[None for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

        self._maps[5][5] = map = Map('home', player)

        self._x = 5
        self._y = 5

        self.map = self._maps[self._y][self._x]

    def move_player(self, player, dx, dy):

        map_dx,  map_dy = 0, 0

        px, py = player.x, player.y

        # move to map left
        if player.x + dx < 0:
            map_dx = -1
            px = MAP_WIDTH - 1

        # move to map right
        elif player.x + dx >= MAP_WIDTH:
            map_dx = 1
            px = 0

        # move to map up
        elif player.y + dy < 0:
            map_dy = -1
            py = MAP_HEIGHT - 1

        # move to map down
        elif player.y + dy >= (MAP_HEIGHT):
            map_dy = 1
            py = 0

        # move to a new map
        if map_dx or map_dy:

            if self._x + map_dx < 0 or self._x + map_dx >= WORLD_WIDTH:
                messages.add("You have reached the edge of the known world!")
                return

            if self._y + map_dy < 0 or self._y + map_dy >= WORLD_HEIGHT:
                messages.add("You have reached the edge of the known world!")
                return

            self._x += map_dx
            self._y += map_dy

            # generate a new map if it doesn't exist
            if not self._maps[self._y][self._x]:
                self._maps[self._y][self._x] = Map('new', player, MAP_WIDTH, MAP_HEIGHT)

            # set the new map
            self.map = self._maps[self._y][self._x]

            # set the player's position on the new map
            player.x = px
            player.y = py

        # same map
        else:

            # if the next tile is walkable then move the player
            if self.map.tiles[player.y + dy][player.x + dx].walkable:
                player.move(dx, dy)
