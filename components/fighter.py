
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
        if self._hp == 0 and self.parent.ai:
            self.die()

    def heal(self, hp):
        if self.hp == self.max_hp:
            return 0

        # new hp can't be greater than max_hp
        new_hp = min(self.hp + hp, self.max_hp)

        recovered = new_hp - self.hp

        self.hp = new_hp

        return recovered

    def take_damage(self, damage):
        self.hp -= damage

    def die(self):

        if self.parent.is_player:
            death_message = "You died!"
            self.parent.tile = tileset.get_tile('player_corpse')
        else:
            death_message = f"{self.parent.name} is dead!"
            self.parent.tile = tileset.get_tile('corpse')

        self.parent.ai = None

        self.parent.name = f"remains of {self.parent.name}"

        messages.add(death_message)
