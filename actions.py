
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
        if engine.map.get_actor_at(x, y):
            messages.add("There is someone in the way!")
            return

        self.actor.move(self.dx, self.dy)


class MeleeAction(ActionWithDirection):
    def perform(self, engine):

        target = engine.map.get_actor_at(self.actor.x + self.dx, self.actor.y + self.dy)

        if not target:
            return

        messages.add(f"You kick the {target.name}, much to its annoyance!")

class BumpAction(ActionWithDirection):
    def perform(self, engine):

        if engine.map.get_actor_at(self.actor.x + self.dx, self.actor.y + self.dy):
            return MeleeAction(self.actor, self.dx, self.dy).perform(engine)

        return MovementAction(self.actor, self.dx, self.dy).perform(engine)
