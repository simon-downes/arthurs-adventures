from blessed import Terminal as BlessedTerminal

from screen import Screen
from input import InputHandler

from engine import Engine

def main():

    term = BlessedTerminal()

    engine = Engine(Screen(term), InputHandler(term))

    try:
        engine.run()

    except SystemExit:
        # move the cursor to the bottom of the game screen before we quit
        print(term.move_xy(0, 32))

    # if term.width < 104 or term.height < 32:
    #     print("Please resize the terminal to at least 104x32")
    #     return



if __name__ == "__main__":
    main()
