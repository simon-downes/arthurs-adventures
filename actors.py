
import tileset

from components.fighter import Fighter
from components.ai import Hostile

def spawn(actor, x, y):
    match actor:
        case "bandit":
            return Bandit(tileset.get_tile('bandit'), x, y, ai=Hostile, fighter=Fighter(hp=5, defense=1, power=200))
    return None

class Actor:
    """Base class for all actors in the game - things that can perform actions"""

    def __init__(self, tile, name, x, y, ai, fighter):

        self.tile = tile
        self.name = name
        self.x = x
        self.y = y
        self.ai = ai
        self.fighter = fighter

    @property
    def is_player(self):
        return self.name == 'Player'

    @property
    def is_alive(self):
        # player is alive if their hp is above 0
        if self.is_player:
            return self.fighter.hp > 0

        # all other actors are alive if they can perform actions
        return bool(self.ai)

    @property
    def is_fighter(self):
        return bool(self.fighter)

    def move(self, dx, dy):
        """Move the actor by dx, dy"""
        self.x += dx
        self.y += dy

    def teleport(self, x, y):
        """Teleport the actor to x, y"""
        self.x = x
        self.y = y

class Player(Actor):

    def __init__(self, x, y):
        super().__init__(tileset.get_tile('player'), 'Player', x, y, True, Fighter(hp=10, defense=2, power=5))
        self.fighter.actor = self


class Bandit(Actor):

    def __init__(self, tile, x, y, ai, fighter):
        super().__init__(tile, 'Bandit', x, y, ai(self), fighter)
        self.fighter.actor = self
