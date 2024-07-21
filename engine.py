
import tileset

from actors import *
from actions import *
from map import *

WORLD_WIDTH = 9
WORLD_HEIGHT = 9

MAP_WIDTH = 80
MAP_HEIGHT = 25

class Engine:

    def __init__(self, screen, input):

        self._screen = screen
        self._input = input

        # load our tiles
        tileset.load()

        # create a player and set starting position - back room of the house
        # TODO: come up with a better way of setting the starting position
        self.player = Player(40, 10)

        # create an empty world space
        self._maps = [[None for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

        self._map_x = WORLD_WIDTH // 2
        self._map_y = WORLD_HEIGHT // 2

        # add the home map - center of the world
        self.map = self._maps[self._map_y][self._map_x] = Map('home', self.player, MAP_WIDTH, MAP_HEIGHT)

        # add a welcome message
        messages.add("Welcome to Arthur's Adventures!")


    def run(self):

        # show the main screen
        self._screen.main()

        self._screen.update(self.map, self.player)

        # never show the cursor
        with self._screen.hidden_cursor():

            while True:

                # wait for a keypress that generates an action
                while not (action := self._input.wait_for_action(self.player)):
                    pass

                action.perform(self)

                self.actor_actions()

                self._screen.update(self.map, self.player)

    def would_change_map(self, actor, dx, dy):
        """Check if moving the actor by dx, dy would change the map"""

        # only the player can change maps
        if not actor.is_player:
            return None

        map_dx,  map_dy = 0, 0
        px, py = actor.x, actor.y

        # move to map left and player to the right edge of the map
        if actor.x + dx < 0:
            map_dx = -1
            px = MAP_WIDTH - 1

        # move to map right and player to the left edge of the map
        elif actor.x + dx >= MAP_WIDTH:
            map_dx = 1
            px = 0

        # move to map up and player to the bottom edge of the map
        elif actor.y + dy < 0:
            map_dy = -1
            py = MAP_HEIGHT - 1

        # move to map down and player to the top edge of the map
        elif actor.y + dy >= (MAP_HEIGHT):
            map_dy = 1
            py = 0

        # we should be moving to a new map
        if map_dx or map_dy:

            # can't move to a new map if we are at the edge of the world
            if self._map_x + map_dx < 0 or self._map_x + map_dx >= WORLD_WIDTH:
                messages.add("You have reached the edge of the known world!")
                map_dx = 0
                px = actor.x

            # can't move to a new map if we are at the edge of the world
            if self._map_y + map_dy < 0 or self._map_y + map_dy >= WORLD_HEIGHT:
                messages.add("You have reached the edge of the known world!")
                map_dy = 0
                py = actor.y

            # return the new map and player co-ordinates
            return [map_dx, map_dy, px, py]

        # we are staying on the same map
        return None

    def move_map(self, dx, dy, px, py):
        """Move to a new map and set the player's position"""

        # update the current map co-ordinates
        self._map_x += dx
        self._map_y += dy

        # generate a new map if it doesn't exist
        if not self._maps[self._map_y][self._map_x]:
            self._maps[self._map_y][self._map_x] = Map('new', self.player, MAP_WIDTH, MAP_HEIGHT)

        # set the new map
        self.map = self._maps[self._map_y][self._map_x]

        # set the player's position on the new map
        self.player.teleport(px, py)

    def actor_actions(self):
        for actor in self.map.actors:
            if actor.ai and not actor.is_player:
                actor.ai.perform(self)
