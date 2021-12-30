O = True
L = False
H = 5
W = 3
GLYPHS = [
    (O, O, O,  # 0
     O, L, O,
     O, L, O,
     O, L, O,
     O, O, O),

    (L, O, L,  # 1
     L, O, L,
     L, O, L,
     L, O, L,
     L, O, L),

    (O, O, O,  # 2
     L, L, O,
     O, O, O,
     O, L, L,
     O, O, O),

    (O, O, O,  # 3
     L, L, O,
     L, O, O,
     L, L, O,
     O, O, O),

    (O, L, O,  # 4
     O, L, O,
     O, O, O,
     L, L, O,
     L, L, O),

    (O, O, O,  # 5
     O, L, L,
     O, O, O,
     L, L, O,
     O, O, O),

    (O, O, O,  # 6
     O, L, L,
     O, O, O,
     O, L, O,
     O, O, O),

    (O, O, O,  # 7
     L, L, O,
     L, L, O,
     L, L, O,
     L, L, O),

    (O, O, O,  # 8
     O, L, O,
     O, O, O,
     O, L, O,
     O, O, O),

    (O, O, O,  # 9
     O, L, O,
     O, O, O,
     L, L, O,
     O, O, O),
]

class RenderNum:
    brightness = 1
    digits = []
    dx = 0
    dy = 0

    def __init__(self, display):
        self.display = display
        self.buflen = (3 * W + 2) * H
        self.front = list([L for x in range(self.buflen)])
        self.back = list([L for x in range(self.buflen)])

    def chg_brightness(self, value):
        self.set_brightness(self.brightness + value)

    def set_brightness(self, value):
        self.brightness = value
        self.back = self.front.copy()
        self.redraw(force=True)

    def diffflush(self, force=False):
        for i in range(self.buflen):
            y, x = divmod(i, self.display.width)
            x += self.dx
            y += self.dy
            f = self.front[i]
            b = self.back[i]

            if b and (not f or force):  # forces brightness change
                self.display.pixel(x, y, self.brightness)

            if not b and f:
                self.display.pixel(x, y, 0)

            self.front[i] = L

        self.front, self.back = self.back, self.front

    def factor(self, number, want_zeros = False):
        self.digits.clear()

        temp = number

        for i in range(3):
            digit = temp % 10
            temp = int(temp / 10)

            if not want_zeros and digit == 0 and temp == 0:
                continue

            self.digits.append(digit)

        return self.digits

    def offset(self, dx, dy):
        self.dx = int(dx)
        self.dy = int(dy)
        self.redraw()

    def print(self):
        chunks = list(zip(*[iter(map(int, self.back))]*self.display.width))

        for line in chunks:
            print(line)
        print("----")

    def redraw(self, force=False):
        self.back = self.front.copy()
        self.diffflush(force)

    def render(self, num, want_zeros=False, force=False):
        shift = self.display.width

        for digit in self.factor(num, want_zeros):
            glyph = GLYPHS[digit]

            for i, bit in enumerate(glyph):
                y, x = divmod(i, W)
                x += shift - W
                self.back[x + (y * self.display.width)] = bit

            shift -= W + 1

        self.diffflush(force)
