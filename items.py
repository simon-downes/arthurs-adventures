
import yaml

from entity import Entity
from components.consumable import HealingConsumable
from components.inventory import Inventory

_items = {}

def spawn(item, x, y):

    global _items

    with open('data/items.yaml', 'r') as f:
        _items = yaml.safe_load(f)

    if item in _items:
        item = _items[item]

        # if 'capacity' in item:
        #     return Container(item['tile'], item['name'], x, y, item['capacity'])

        consumable = None
        if 'hp' in item.get('consumable', {}):
            consumable = HealingConsumable(item['consumable']['hp'])

        return Item(
            item['tile'],
            item['name'],
            x,
            y,
            consumable=consumable
        )

    raise ValueError(f"Unknown Item: '{item}'")

class Item(Entity):
    """Base class for all items in the game - things that can be picked up"""

    # thing to which the item belongs - usually an inventory
    parent = None

    def __init__(self, tile, name, x, y, consumable=None):

        super().__init__(tile, name, x, y)

        self.consumable = consumable
        if self.consumable:
            self.consumable.parent = self

    @property
    def is_consumable(self):
        return self.consumable is not None

class Container(Entity):
    """Base class for all things in the game that can contain other things"""

    _inventory = None

    def __init__(self, tile, name, x, y, capacity):

        super().__init__(tile, name, x, y)

        self._inventory = Inventory(capacity)

    @property
    def is_full(self):
        return self._inventory.is_full
