from dataclasses import dataclass


@dataclass
class Tah:
    start: tuple[int, int]
    cil: tuple[int, int]

    def __str__(self):
        return pozice_na_text(self.start) + "-" + pozice_na_text(self.cil)


def pozice_na_text(pozice):
    x, y = pozice
    return "abcdefgh"[x] + str(y + 1)


def text_na_pozici(text):
    text = text.strip().lower()
    if len(text) != 2 or text[0] not in "abcdefgh" or text[1] not in "12345678":
        raise ValueError("Pole musí být například e2 nebo a7.")
    return ("abcdefgh".index(text[0]), int(text[1]) - 1)
