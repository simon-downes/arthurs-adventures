
import random

import messages

from actions import *

class BaseAI(Action):
    def perform(self):
        raise NotImplementedError()

class Player(BaseAI):
    def perform(self):
        pass

class Hostile(BaseAI):

    def perform(self, engine):

        # hostiles always target the player
        target = engine.player

        dx = target.x - self.actor.x
        dy = target.y - self.actor.y

        distance = max(abs(dx), abs(dy))  # Chebyshev (chessboard) distance.

        # next to the player so attack!
        if distance <= 1:
            return MeleeAction(self.actor, dx, dy).perform(engine, target)

        # patrol the map randomly
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        if dx or dy:
            return MovementAction(self.actor, dx, dy).perform(engine)

        return WaitAction(self.actor).perform(engine)
