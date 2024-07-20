
import tileset

def spawn(actor, x, y):
    match actor:
        case "bandit":
            return Bandit(tileset.get_tile('bandit'), x, y)
    return None

class Actor:
    """Base class for all actors in the game - things that can move around the map"""

    def __init__(self, tile, name, x, y):

        self.tile = tile
        self.name = name
        self.x = x
        self.y = y

    def is_player(self):
        return self.name == 'Player'

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
        super().__init__(tileset.get_tile('player'), 'Player', x, y)


class Bandit(Actor):

    def __init__(self, tile, x, y):
        super().__init__(tile, 'Bandit', x, y)
