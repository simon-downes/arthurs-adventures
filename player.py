
class Player:

    def __init__(self):
        self.x = 0
        self.y = 0
        #self.health = 10

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
