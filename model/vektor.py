class Vektor:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def krok(self):
        # Například posun (0, 4) má jeden krok (0, 1).
        x = 0 if self.dx == 0 else self.dx // abs(self.dx)
        y = 0 if self.dy == 0 else self.dy // abs(self.dy)
        return x, y
