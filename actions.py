
import messages
import exceptions

from items import Container

class Action:
    def __init__(self, actor):
        self.actor = actor

    def perform(self, engine):
        raise NotImplementedError()

class WaitAction(Action):
    def perform(self, engine):
        pass

class EscapeAction(Action):
    def perform(self, engine):
        # TODO engine.pop_state()
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, actor, dx, dy):
        super().__init__(actor)

        self.dx = dx
        self.dy = dy

    def perform(self, engine):
        raise NotImplementedError()

class MovementAction(ActionWithDirection):
    def perform(self, engine):

        # check if we would move to a new map - only the player can do this
        if new_map := engine.would_change_map(self.actor, self.dx, self.dy):
            engine.move_map(*new_map)
            return

        x = self.actor.x + self.dx
        y = self.actor.y + self.dy

        # if not in bounds then don't move
        if not engine.map.in_bounds(x, y):
            raise exceptions.Impossible('That way is blocked.')

        # if the next tile isn't walkable then don't move
        if not engine.map.tiles[y][x].walkable:
            raise exceptions.Impossible('That way is blocked.')

        # is there someone in the way?
        a = engine.map.get_actor_at(x, y)
        if a and a.is_alive:
            raise exceptions.Impossible(f"There is someone in the way - {a.name}!")

        if not self.actor.is_player:
            # non-player actors can't open doors
            if engine.map.tiles[y][x].name.startswith('door'):
                raise exceptions.Impossible('That way is blocked.')

        self.actor.move(self.dx, self.dy)

        # if the player moved then display what they see
        if self.actor.is_player:
            here = engine.map.get_actor_at(self.actor.x, self.actor.y)
            here = ([here] if here else []) + engine.map.get_items_at(self.actor.x, self.actor.y)
            if here:
                msg = ",".join([thing.name for thing in here])
                messages.add(f"You see {msg}.")

class MeleeAction(ActionWithDirection):
    def perform(self, engine, target):

        if not target:
            raise exceptions.Impossible('Nothing to attack.')

        damage = max(0, self.actor.fighter.power - target.fighter.defense)

        msg = f"{self.actor.name} attacks {target.name}"
        if damage:
            msg += f" for {damage} hit points."
        else:
            msg += " but does no damage."

        messages.add(msg)

        # make sure we do the damage after the message is added
        # so that any death messages are displayed in the correct order
        target.fighter.hp -= damage

class BumpAction(ActionWithDirection):
    def perform(self, engine):

        target = engine.map.get_actor_at(self.actor.x + self.dx, self.actor.y + self.dy)

        if target and target.is_alive:
            return MeleeAction(self.actor, self.dx, self.dy).perform(engine, target)

        return MovementAction(self.actor, self.dx, self.dy).perform(engine)

class ItemAction(Action):
    def __init__(self, actor, item, target_xy=None):
        super().__init__(actor)

        self.item = item

        if not target_xy:
            target_xy = actor.x, actor.y

        self.target_xy = target_xy

    def perform(self, engine):
        self.item.consumable.use(self)

class PickupAction(Action):
    def perform(self, engine):

        items = engine.map.get_items_at(self.actor.x, self.actor.y)

        if not items:
            raise exceptions.Impossible('Nothing to pick up.')

        # TODO: handle multiple items at a location
        item = items[0]

        # TODO: handle containers
        # TODO: handle corpses

        inventory = self.actor.inventory

        if inventory.is_full:
            raise exceptions.Impossible('Your inventory is full.')

        engine.map.items.remove(item)
        inventory.items.append(item)
        item.parent = inventory

        messages.add(f"You picked up the {item.name}.")
