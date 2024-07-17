
import messages
import tileset

class Screen:
    """"Central class for rendering the game screen"""

    def __init__(self, term):

        self._term = term

        # store current terminal width and height
        self.width = term.width
        self.height = term.height

        self._ticks = 0

    def _draw_frame(self, x, y, width, height, title):

        # draw a frame at x, y with width, height and title
        self.print(x, y, "╭" + ("─" * 2) + f" {title} " + ("─" * (width - len(title) - 4)) + "╮")
        for yy in range(1, height):
            self.print(x, y + yy, "│" + (" " * width) + "│")
        self.print(x, y + height - 1, "╰" + ("─" * width) + "╯")

    def clear(self):
        #  reset cursor and clear screen
        print(self._term.home + self._term.clear)

    def print(self, x, y, text):
        # print text at x, y
        print(self._term.move_xy(x, y) + text, end='', flush=True)

    def has_resized(self):
        # check if the terminal has been resized

        if self.width != self._term.width or self.height != self._term.height:
            self.width = self._term.width
            self.height = self._term.height
            return True

        return False

    def is_too_small(self):
        return self._term.width < 104 or self._term.height < 32

    def main(self):

        self.clear()

        frames = {
            'map' : (0, 0, 80, 27, "World Map"),
            'status' : (82, 0, 26, 27, "Status"),
            'messages' : (0, 27, 80, 7, "Messages"),
            'debug' : (82, 27, 26, 7, "Debug"),
        }

        for frame in frames:
            self._draw_frame(*frames[frame])

        # status text
        self.print(84, 2, f"{self._render_tile('health')} 123 / 456")
        self.print(84, 3, f"  {self._render_tile('health_full') * 6}{self._render_tile('health_empty') * 4}")

        self.print(84, 5, f"{self._render_tile('xp')} 9,999 / 9,999")
        self.print(84, 6, f"  {self._render_tile('xp_full') * 6}{self._render_tile('xp_empty') * 4}")

        self.print(84, 8, f"{self._render_tile('rank')} Outsider")

        self.print(84, 10, f"{self._render_tile('gold')} 1,234")
        self.print(84, 11, f"{self._render_tile('gem')} 1,123")

        self.print(84, 13, f"{self._render_tile('weapon')} Two-Handed Sword")
        self.print(84, 14, f"{self._render_tile('armour')} Studded Coat")

        # example inventory
        self.print(84, 16, f"! Health Potions.... 123")
        self.print(84, 17, f"! Mana Potions...... 123")
        self.print(84, 18, f"! Stamina Potions... 123")
        self.print(84, 19, f"! Antidote.......... 123")
        self.print(84, 20, f"! Elixirs........... 123")
        self.print(84, 21, f"! Scrolls........... 123")

    def update(self, map, player):

        if self.has_resized():
            self.main()

        x_offset =  1 #+ ((80 - map.width) // 2)
        y_offset =  1 #+ ((25 - map.height) // 2)

        lines = []

        # for row in the map, generate a string of characters that represent the tiles
        for row in map.tiles:
            lines.append("".join([self._render_tile(tile) for tile in row]))

        # for each line of characters, print it to the screen in the correct position
        for dy, line in enumerate(lines):
            self.print(x_offset, y_offset + dy, line)

        # draw player
        self.print(x_offset + player.x, y_offset + player.y, self._render_tile('player'))

        self._render_messages()

        self._ticks += 1

        # debug output
        self.print(84, 28, f"Player: {player.x}, {player.y}")
        self.print(84, 32, f"Ticks: {self._ticks}")

    def _render_messages(self):

        # get the last 5 messages
        for n, message in enumerate(messages.get(5)):
            # TODO: handle colour codes in messages e.g. {red}{/red} or {green}{/green}
            self.print(2, 28 + n, str(message).ljust(79, " "))

    def _render_tile(self, tile):

        # we didn't get given a tile instance so look it up in the tileset
        if not isinstance(tile, tileset.Tile):
            tile = tileset.get_tile(tile)

        # no foreground colour so just return the character
        if not tile.fg:
            return tile.char

        style = tile.fg

        if tile.bg:
            style += f"_on_{tile.bg}"

        # create a string formatter and use it to render the tile character with the correct colours
        return self._term.formatter(style)(tile.char)
