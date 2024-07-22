
import tileset

def buffer_from_string(data, fill=''):
    """Create a buffer from a string"""
    # remove any trailing whitespace and split into lines
    lines = data.rstrip().split("\n")

    # calculate the width and height of the buffer
    height = len(lines)
    width = max(len(line) for line in lines)

    # create and populate the buffer
    buffer = Buffer(width, height, fill)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            buffer.set(x, y, char)

    return buffer

class Buffer:
    """A 2D co-ordinate space of rows(lines) and columns"""

    def __init__(self, width, height, fill=None):

        self.width = width
        self.height = height

        # create a 2D list of width x height filled with fill
        self._data = [[fill for _ in range(width)] for _ in range(height)]

    def get(self, x, y):
        return self._data[y][x]

    def set(self, x, y, value):
        self._data[y][x] = value

    def row(self, y):
        # we use list() to make a copy of the row, elements are still references
        return list(self._data[y])

    def merge(self, x, y, buffer):
        """Merge another buffer into this buffer at x, y"""

        if not isinstance(buffer, Buffer):
            raise ValueError(f"Can't merge a {type(buffer)} into a Buffer")

        if x + buffer.width > self.width or y + buffer.height > self.height:
            raise ValueError("Buffer is too big to merge at this position")

        for dy, row in enumerate(buffer._data):
            for dx, value in enumerate(row):
                if value is not None:
                    self._data[y + dy][x + dx] = value

    def merge_string(self, x, y, data):
        """Merge a string into the buffer at x, y"""
        self.merge(x, y, buffer_from_string(data))

    def center(self, y, text):
        """Print text centered on the buffer at y"""

        x = (self.width - len(text)) // 2
        self.print(x, y, text)

    def print(self, x, y, text, truncate=False):
        """Print text to the buffer at x, y"""

        if x + len(text) > self.width:
            if truncate:
                text = text[:self.width - x]
            else:
                raise ValueError("Text is too long to print at this position")

        for dx, char in enumerate(text):
            self._data[y][x + dx] = char

    def __str__(self):
        """Print the buffer as rows of text"""
        s = ''
        for row in self._data:
            s += ''.join(str(x) for x in row) + "\n"
        return s

class ScreenBuffer(Buffer):

    def __init__(self, term, width, height):

        super().__init__(width, height, ' ')

        self._term = term

    def set(self, x, y, value):

        # if we are given a tile instance then render it to a formatted string
        if isinstance(value, tileset.Tile):
            value = self.render_tile(value)

        self._data[y][x] = value

    def frame(self, x, y, width, height, title = ''):

        if title:
            title = f" {title} "

        # draw a frame at x, y with width, height and title
        self.print(x, y, "╭" + ("─" * 2) + title + ("─" * (width - len(title) - 2)) + "╮", True)
        for yy in range(1, height):
            self.set(x, y + yy, "│")
            self.set(x + width + 1, y + yy, "│")
        self.print(x, y + height - 1, "╰" + ("─" * width) + "╯")

    def bar(self, x, y, width, value, max_value, fg, bg=''):

            # calculate the width of the bar
            bar_width = int((value / max_value) * width)

            formatter = self._formatter(fg, bg)

            # draw the bar
            for dx in range(width):
                if dx < bar_width:
                    self.set(x + dx, y, formatter('▪'))
                else:
                    self.set(x + dx, y, formatter('▫'))

    def render(self, clear=False):
        """Render the screen buffer to the terminal"""

        print(self._term.home)

        if clear:
            print(self._term.clear)

        print(self)

    def render_tile(self, tile):

        # we didn't get given a tile instance so look it up in the tileset
        if not isinstance(tile, tileset.Tile):
            tile = tileset.get_tile(tile)

        # no foreground colour so just return the character
        if not tile.fg:
            return tile.char

        # create a string formatter and use it to render the tile character with the correct colours
        return self._formatter(tile.fg, tile.bg)(tile.char)

    def _formatter(self, fg, bg=''):
        """Return a string formatter for the given colours"""

        style = fg

        if bg:
            style += f"_on_{bg}"

        return self._term.formatter(style)
