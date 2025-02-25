
import logging

import messages
import exceptions
from actions import *

class GameState:

    _screen = None

    def __init__(self):
        pass

    def enter(self, engine):
        """Called when the state is entered for the first time"""

        logging.info(f"Entering state: {self.__class__.__name__}")

        # create a new screen buffer for the state
        self._screen = engine.new_screen_buffer()

    def exit(self, engine):
        """Called when the state is exited"""
        logging.info(f"Exiting state: {self.__class__.__name__}")

        pass

    def pause(self, engine):
        """Called when the state is paused by another state being pushed on top of it"""

        logging.info(f"Pausing state: {self.__class__.__name__}")

        pass

    def resume(self, engine):
        """Called when the state is resumed after the state that paused it is popped"""

        logging.info(f"Resuming state: {self.__class__.__name__}")


        # render our screen buffer to the screen to replace the previous state
        self.render(engine)

    def handle_input(self, engine, key):
        pass

    def render(self, engine, clear=False):
        # merge our screen buffer into the main screen buffer
        engine.screen.merge(0, 0, self._screen)

        # flush the screen buffer to the terminal so we can we see the menu
        engine.screen.render(clear)

    def update(self, engine):
        pass

class MainMenu(GameState):

    def enter(self, engine):

        super().enter(engine)

        screen = self._screen

        screen.center(4, '-' * 25)
        screen.center(5, "Arthur's Adventures")
        screen.center(6, '-' * 25)

        screen.frame(35, 10, 40, 7)
        screen.center(10, ' Main Menu ')

        screen.print(40, 12, "[p] Play Game")
        screen.print(40, 14, "[q] Quit")

        # render our screen buffer to the screen
        self.render(engine, True)

    def handle_input(self, engine, key):

        match key:
            case 'q' | 'KEY_ESCAPE':
                raise SystemExit()

            case 'p':
                engine.push_state(Playing())

class MessageViewer(GameState):

    _to_show = 32

    def enter(self, engine):

        # default to the last "_to_show" messages
        self._cursor = messages.count() - self._to_show

        super().enter(engine)

        # we only need our buffer to be big enough to display the messages
        self._screen = engine.new_screen_buffer(82, self._to_show + 2)

        screen = self._screen

        # map is replaced with messages
        screen.frame(0, 0, 82, self._to_show + 2, "Message Log", clear=True)

        # render our screen buffer to the screen
        self.render(engine, True)

    def handle_input(self, engine, key):

        QUIT_KEYS = ['q', 'KEY_ESCAPE', 'KEY_F9']

        CURSOR_KEYS = {
            'KEY_UP': -1,
            'KEY_DOWN': 1,
            'KEY_PGUP': -10,
            'KEY_PGDOWN': 10,
        }

        if key in CURSOR_KEYS:

            # adjust cursor
            self._cursor += CURSOR_KEYS[key]

            # make sure cursor is within bounds
            self._cursor = min(messages.count() - self._to_show, max(0, self._cursor))

        elif key == 'KEY_HOME':
            self._cursor = 0

        elif key == 'KEY_END':
            self._cursor = messages.count() - self._to_show

        elif key in QUIT_KEYS:
            engine.pop_state()

    def render(self, engine, clear=False):

        screen = self._screen

        for n, message in enumerate(messages.get(32, self._cursor)):
            # TODO: handle colour codes in messages e.g. {red}{/red} or {green}{/green}
            txt = message['text']
            if message['count'] > 1:
                txt = f"{txt} (x{message['count']})"
            screen.print(2, 1 + n, str(txt).ljust(79, " "))

        super().render(engine)

class Playing(GameState):

    _action = None

    def enter(self, engine):

        self._ticks = 0

        super().enter(engine)

        screen = self._screen

        frames = {
            'map' : (0, 0, 82, 27, "World Map"),
            'status' : (82, 0, 28, 27, "Status"),
            'messages' : (0, 27, 82, 7, "Messages"),
            'debug' : (82, 27, 28, 7, "Debug"),
        }

        for frame in frames:
            screen.frame(*frames[frame])

        # status icons
        screen.set(84, 2, screen.render_tile('health'))
        screen.set(84, 5, screen.render_tile('xp'))
        screen.set(84, 8, screen.render_tile('rank'))
        screen.set(84, 10, screen.render_tile('gold'))
        screen.set(84, 11, screen.render_tile('gem'))
        screen.set(84, 13, screen.render_tile('weapon'))
        screen.set(84, 14, screen.render_tile('armour'))

        # # example inventory
        screen.print(84, 16, f"! Health Potions.... 123")
        screen.print(84, 17, f"! Mana Potions...... 123")
        screen.print(84, 18, f"! Stamina Potions... 123")
        screen.print(84, 19, f"! Antidote.......... 123")
        screen.print(84, 20, f"! Elixirs........... 123")
        screen.print(84, 21, f"! Scrolls........... 123")

        # render our screen buffer to the screen
        self.render(engine, True)

    def handle_input(self, engine, key):

        # TODO: home - teleport to home map
        # TODO: end - teleport to camelot map

        MOVE_KEYS = {
            'KEY_UP': (0, -1),
            'KEY_DOWN': (0, 1),
            'KEY_LEFT': (-1, 0),
            'KEY_RIGHT': (1, 0),
            '1': (-1, 1),
            '2': (0, 1),
            '3': (1, 1),
            '4': (-1, 0),
            '6': (1, 0),
            '7': (-1, -1),
            '8': (0, -1),
            '9': (1, -1),
        }

        WAIT_KEYS = ['KEY_ENTER']

        QUIT_KEYS = ['q', 'KEY_ESCAPE']

        player = engine.player

        # clear any previous action
        self._action = None

        if key in MOVE_KEYS and player.is_alive:
            self._action = BumpAction(player, *MOVE_KEYS[key])

        elif key == 'g':
            self._action = PickupAction(player)

        elif key == 'h':
            for item in player.inventory.items:
                if item.name == 'Food':
                    self._action = item.consumable.get_action(player)

            if not self._action:
                messages.add('No food to eat.')

        elif key in WAIT_KEYS:
            self._action =  WaitAction(player)

        elif key == 'KEY_F9':
            engine.push_state(MessageViewer())

        elif key == 'i':
            engine.push_state(InventoryViewer())

        elif key in QUIT_KEYS:
            engine.pop_state()

    def update(self, engine):

        # if there's no player action then there's nothing to do
        # bad guys shouldn't move if the player hasn't taken an action
        if not self._action:
            return

        try:

            # perform the player action
            self._action.perform(engine)

        # can't perform the action so skip enemy turns
        except exceptions.Impossible as e:
            messages.add(e.args[0])
            return

        # run any actor actions
        engine.npc_actions()

    def render(self, engine, clear=False):

        screen = self._screen
        player = engine.player

        # map is rendered inside a frame
        x_offset =  1
        y_offset =  1

        # render map tiles to the state screen buffer
        for dy, row in enumerate(engine.map.tiles):
            for dx, tile in enumerate(row):
                screen.set(x_offset + dx, y_offset + dy, screen.render_tile(tile))

        # draw map items
        for item in engine.map.items:
            screen.set(x_offset + item.x, y_offset + item.y, screen.render_tile(item.tile))

        # draw map actors
        for actor in engine.map.actors:
            screen.set(x_offset + actor.x, y_offset + actor.y, screen.render_tile(actor.tile))

        self._ticks += 1

        # # debug output
        screen.print(84, 28, f"Player: {player.x}, {player.y}")
        screen.print(84, 32, f"Ticks: {self._ticks}")

        # self. _draw_frame(20, 7, 40, 10, "Inventory")

        # render last 5 messages
        for n, message in enumerate(messages.last(5)):
            # TODO: handle colour codes in messages e.g. {red}{/red} or {green}{/green}
            txt = message['text']
            if message['count'] > 1:
                txt = f"{txt} (x{message['count']})"
            screen.print(2, 28 + n, str(txt).ljust(79, " "))


        screen.print(86, 2, f"{player.fighter.hp} / {player.fighter.max_hp}".ljust(20))
        screen.bar(86, 3, 10, player.fighter.hp, player.fighter.max_hp, 'red')

        screen.print(86, 5, f"9,999 / 9,999")
        screen.bar(86, 6, 10, 6, 10, 'blue')

        screen.print(86, 8, f"Outsider")
        screen.print(86, 10, f"1,234")
        screen.print(86, 11, f"1,234")
        screen.print(86, 13, f"Two-Handed Sword")
        screen.print(86, 14, f"Studded Coat")

        # take the inventory summary and produce a list of tuples (tile, text)
        inventory = [
            [v[0], f"{k.ljust(18, '.')}{str(v[1]).rjust(4)}"] for k, v in player.inventory.summary().items()
        ]

        # for each tuple, render the tile and text to the screen buffer
        for n, v in enumerate(inventory[:10]):
            screen.set(84, 16 + n, screen.render_tile(v[0]))
            screen.print(86, 16 + n, v[1])

        # if there are less than 10 items in the inventory, pad the list
        for n in range(len(inventory), 10):
            screen.print(84, 16 + n, " " * 24)

        super().render(engine, clear)

class InventoryViewer(GameState):

    def enter(self, engine):

        # default to the last "_to_show" messages
        # self._cursor = messages.count() - self._to_show

        super().enter(engine)

        # we only need our buffer to be big enough to display the messages
        self._screen = engine.new_screen_buffer(32, 14)

        screen = self._screen

        # map is replaced with messages
        screen.frame(1, 1, 30, 12, "Inventory", clear=True)

        # render our screen buffer to the screen
        self.render(engine, True)

    def handle_input(self, engine, key):

        QUIT_KEYS = ['KEY_ESCAPE', 'i']

        if key in QUIT_KEYS:
            engine.pop_state()

    def render(self, engine, clear=False):

        screen = self._screen

        x = (engine.screen.width - screen.width) // 2
        y = (engine.screen.height - screen.height) // 2

        # merge our screen buffer into the main screen buffer
        engine.screen.merge(x, y, screen)

        # flush the screen buffer to the terminal so we can we see the menu
        engine.screen.render(clear)
