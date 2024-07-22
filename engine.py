
from blessed import Terminal as BlessedTerminal

import tileset


import states

from actors import *
from actions import *
from map import *

from buffer import *

SCREEN_WIDTH = 110
SCREEN_HEIGHT = 34

WORLD_WIDTH = 9
WORLD_HEIGHT = 9

MAP_WIDTH = 80
MAP_HEIGHT = 25

class Engine:

    def __init__(self):

        self._term = BlessedTerminal()

        print(self._term.home + self._term.clear)

        # create a screen buffer big enough to hold the largest screen
        self.screen = self.new_screen_buffer()

        # initialise the state machine
        self._states = []

        # load our tiles
        tileset.load()

        # create a player and set starting position - back room of the house
        # TODO: come up with a better way of setting the starting position
        self.player = Player(40, 10)

        # create an empty world space
        # TODO: use a buffer
        self._maps = [[None for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

        # screen = ScreenBuffer(self._term, 110, 34)

        # frames = {
        #     'map' : (0, 0, 80, 27, "World Map"),
        #     'status' : (82, 0, 26, 27, "Status"),
        #     'messages' : (0, 27, 80, 7, "Messages"),
        #     'debug' : (82, 27, 26, 7, "Debug"),
        # }

        # for frame in frames:
        #     screen.frame(*frames[frame])


        # print(screen)

        # quit()

        # t = Terminal(110, 34)

        # t.render()

        # quit()

        # buf = Buffer(20, 10, '-')
        # buf2 = Buffer(3, 3, '#')

        # buf3 = buffer.from_string("Hello World")

        # buf._data[2][1] = 'X'
        # # buf._data[1][2] = None



        # buf.merge(5, 7, buf2)
        # buf.merge((buf.width - buf3.width) // 2, 1, buf3)

        # buf.print(10, 3, "Hello World", True)

        # print(buf)

        # quit()

        self._map_x = WORLD_WIDTH // 2
        self._map_y = WORLD_HEIGHT // 2

        # add the home map - center of the world
        self.map = self._maps[self._map_y][self._map_x] = Map('home', self.player, MAP_WIDTH, MAP_HEIGHT)

        # add a welcome message
        messages.add("Welcome to Arthur's Adventures!")

    def push_state(self, state):

        # pause current state if any
        if len(self._states):
            self._states[-1].pause(self)

        # enter the new state
        state.enter(self)

        # add the new state to the stack
        self._states.append(state)

    def pop_state(self):

        # remove the current state from the stack
        state = self._states.pop()

        # exit the current state
        state.exit(self)

        # resume the previous state
        self._states[-1].resume(self)

    def new_screen_buffer(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        return ScreenBuffer(self._term, width, height)

    def wait_for_keypress(self):
        with self._term.cbreak():
            key = self._term.inkey()

        return key.name or key

    def run(self):

        self.push_state(states.MainMenu())

        # never show the cursor
        with self._term.hidden_cursor():

            while True:

                # wait for input
                key = self.wait_for_keypress()

                # send input to the current state - this may change the state
                self._states[-1].handle_input(self, key)

                # update the current state - this may not be the same state as the input handler
                self._states[-1].update(self)

                # render the current state to the screen
                self._states[-1].render(self)

                # render the screen

                # wait for a keypress that generates an action
                # while not (action := self._input.wait_for_action(self.player)):
                #     pass

                # action.perform(self)

                # self.actor_actions()

                # self._screen.update(self.map, self.player)

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
