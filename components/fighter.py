
import messages
import tileset

class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.actor.ai:
            self.die()

    def die(self):

        if self.actor.is_player:
            death_message = "You died!"
            self.actor.tile = tileset.get_tile('player_corpse')
        else:
            death_message = f"{self.actor.name} is dead!"
            self.actor.tile = tileset.get_tile('corpse')

        self.actor.ai = None

        self.actor.name = f"remains of {self.actor.name}"

        messages.add(death_message)
