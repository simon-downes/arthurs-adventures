
from actions import *

class InputHandler:

    def __init__(self, term):
        self._term = term

    def wait_for_action(self, player):
        with self._term.cbreak():
            key = self._term.inkey()

        return self._key_to_action(key.name or key, player)

    def _key_to_action(self, key, player):

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

        if key in MOVE_KEYS and player.is_alive:
            return BumpAction(player, *MOVE_KEYS[key])

        if key in WAIT_KEYS:
            return WaitAction(player)

        if key in QUIT_KEYS:
            return EscapeAction(player)

        print(key)

        return None
