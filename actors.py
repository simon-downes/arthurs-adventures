
import yaml

from entity import Entity
from components.fighter import Fighter
from components.ai import (Hostile, Player as PlayerAI)
from components.inventory import Inventory

_npcs = {}

def spawn(actor, x, y):

    global _npcs

    # load npc config if it hasn't been loaded yet
    if not _npcs:
        with open('data/npcs.yaml', 'r') as f:
            _npcs = yaml.safe_load(f)


    if actor in _npcs:
        npc = _npcs[actor]

        return Actor(
            npc['tile'],
            npc['name'],
            x,
            y,
            ai=npc['ai'],
            fighter=Fighter(**npc['fighter']) if 'fighter' in npc else None,
            inventory=Inventory(capacity=npc.get('inventory', 0)),
        )

    raise ValueError(f"Unknown NPC: '{actor}'")

class Actor(Entity):
    """Base class for all actors in the game - things that can perform actions"""

    def __init__(self, tile, name, x, y, ai, fighter, inventory):

        super().__init__(tile, name, x, y)

        match ai:
            case 'hostile':
                self.ai = Hostile(self)
            case 'player':
                self.ai = PlayerAI(self)
            case _:
                print(ai)
                self.ai = True

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self


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
        super().__init__(
            'player',
            'Player',
            x,
            y,
            ai='Player',
            fighter=Fighter(hp=10, defense=2, power=5),
            inventory=Inventory(capacity=20),
        )
