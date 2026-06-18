class Figurka:
    def __init__(self, nazev: str, barva: str):
        self.nazev = nazev
        self.barva = barva

    def symbol(self) -> str:
        znaky = {
            "kral": "K",
            "dama": "D",
            "vez": "V",
            "strelec": "S",
            "kun": "J",
            "pesak": "P",
        }

        znak = znaky[self.nazev]

        if self.barva == "bila":
            return znak
        else:
            return znak.lower()
