
import messages

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
            return

        # if the next tile isn't walkable then don't move
        if not engine.map.tiles[y][x].walkable:
            return

        # is there someone in the way?
        a = engine.map.get_actor_at(x, y)
        if a and a.is_alive:
            messages.add(f"{self.actor.name}: There is someone in the way - {a.name}!")
            return

        if not self.actor.is_player:
            # non-player actors can't open doors
            if engine.map.tiles[y][x].name.startswith('door'):
                return

        self.actor.move(self.dx, self.dy)


class MeleeAction(ActionWithDirection):
    def perform(self, engine, target):

        if not target:
            return

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
