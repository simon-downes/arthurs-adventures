
import actions
import exceptions
import messages
from components.base import BaseComponent
from components.inventory import Inventory

class Consumable(BaseComponent):

    def get_action(self, consumer):
        return actions.ItemAction(consumer, self.parent)

    def use(self, action):
        raise NotImplementedError()

    def consume(self):
        # item that the component belongs to
        item = self.parent
        # inventory in which the item is stored
        inventory = item.parent
        if isinstance(inventory, Inventory):
            inventory.items.remove(item)

class HealingConsumable(Consumable):

    def __init__(self, amount):
        self.amount = amount

    def use(self, action):
        consumer = action.actor
        recovered = consumer.fighter.heal(self.amount)

        if not recovered:
            raise exceptions.Impossible("You are already at full health.")

        messages.add(f"You consume the {self.parent.name} and recover {recovered} health!")

        self.consume()
