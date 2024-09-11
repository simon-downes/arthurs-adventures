
from components.base import BaseComponent

import messages

class Inventory(BaseComponent):

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    @property
    def is_full(self):
        return len(self.items) >= self.capacity

    def summary(self):

        summary = {}

        for item in self.items:
            if item.name in summary:
                summary[item.name][1] += 1
            else:
                summary[item.name] = [item.tile.name, 1]

        return summary

    def drop(self, item):
        self.items.remove(item)
        # todo: handle different maps
        item.place(self.parent.x, self.parent.y)

        messages.add(f"You dropped the {item.name}.")
