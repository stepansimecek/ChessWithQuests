import time


class GameTimer:
    def __init__(self):
        self.nuluj_cas()

    def nuluj_cas(self):
        self.casy = {"bila": 0.0, "cerna": 0.0}
        self.aktivni_barva = None
        self.zacatek = None

    def spust(self, barva):
        self.zastav()
        self.aktivni_barva = barva
        self.zacatek = time.monotonic()

    def zastav(self):
        if self.aktivni_barva is not None:
            self.casy[self.aktivni_barva] += time.monotonic() - self.zacatek
        self.aktivni_barva = None
        self.zacatek = None

    def vrat_cas(self, barva):
        cas = self.casy[barva]
        if self.aktivni_barva == barva:
            cas += time.monotonic() - self.zacatek
        return cas
