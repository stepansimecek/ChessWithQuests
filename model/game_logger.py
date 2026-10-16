class GameLogger:
    def __init__(self):
        self.tahy = []
        self.zaznamy = []

    def uloz_tah(self, tah, figura=None, sebrana=None, promena=False):
        self.tahy.append(tah)
        zapis = str(tah)
        if figura is not None:
            zapis = figura.barva + " " + figura.nazev + " " + zapis
        if sebrana is not None:
            zapis += " (sebrána: " + sebrana.nazev + ")"
        if promena:
            zapis += " (proměna v dámu)"
        self.zaznamy.append(zapis)

    def vypis_log(self):
        print("Historie tahů:")
        for i, zapis in enumerate(self.zaznamy, start=1):
            print(f"{i}. {zapis}")
