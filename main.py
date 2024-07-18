from blessed import Terminal as BlessedTerminal

import tileset
import messages

from player import Player
from screen import Screen
from map import Map
from world import World


def main():

    term = BlessedTerminal()

    if term.width < 104 or term.height < 32:
        print("Please resize the terminal to at least 104x32")
        return

    # load our tiles
    tileset.load()

    # initialise the screen
    screen = Screen(term)

    # create a player
    player = Player()

    # set the player's starting position - back room of the house
    # TODO: come up with a better way of doing this
    player.x = 40
    player.y = 10

    world = World(player)

    messages.add("Welcome to Arthur's Adventures!")

    # show the main screen
    screen.main()

    screen.update(world.map, player)

    # never show the cursor
    with term.hidden_cursor():

        while True:

            with term.cbreak():
                key = term.inkey(timeout=0.5)

            key = key.name or key

            dx, dy = 0, 0

            match key:
                case 'KEY_UP':
                    dy = -1
                case 'KEY_DOWN':
                    dy = 1
                case 'KEY_LEFT':
                    dx = -1
                case 'KEY_RIGHT':
                    dx = 1
                case 'q' | 'KEY_ESCAPE':
                    break

            world.move_player(player, dx, dy)

            screen.update(world.map, player)

        # move the cursor to the bottom of the game screen before we quit
        print(term.move_xy(0, 32))

if __name__ == "__main__":
    main()
