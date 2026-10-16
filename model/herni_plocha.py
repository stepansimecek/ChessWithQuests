from typing import Optional

from model.figurka import Figurka
from model.figurky import Pesak, Kral, Dama, Vez, Strelec, Kun
from model.tah import Tah


class HerniPlocha:
    def __init__(self):
        self.deska: list[list[Optional[Figurka]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.nastav_start()

    def nastav_start(self) -> None:
        self.deska = [[None for _ in range(8)] for _ in range(8)]
        self.sebrane_figurky = []
        poradi = [Vez, Kun, Strelec, Dama, Kral, Strelec, Kun, Vez]
        for x in range(8):
            self.deska[0][x] = poradi[x]("bila")
            self.deska[7][x] = poradi[x]("cerna")

        for x in range(8):
            self.deska[1][x] = Pesak("bila")
            self.deska[6][x] = Pesak("cerna")

    def je_v_desce(self, pozice: tuple[int, int]) -> bool:
        x, y = pozice
        return 0 <= x < 8 and 0 <= y < 8

    def vrat_figuru(self, pozice: tuple[int, int]) -> Optional[Figurka]:
        if not self.je_v_desce(pozice):
            return None
        x, y = pozice
        return self.deska[y][x]

    def posun_figuru(self, tah: Tah) -> bool:
        if not self.je_v_desce(tah.start) or not self.je_v_desce(tah.cil):
            return False

        figura = self.vrat_figuru(tah.start)

        cil = self.vrat_figuru(tah.cil)
        if figura is None or tah.start == tah.cil:
            return False
        if cil is not None and (cil.barva == figura.barva or cil.nazev == "kral"):
            return False

        sx, sy = tah.start
        cx, cy = tah.cil

        self.deska[cy][cx] = figura
        self.deska[sy][sx] = None
        if cil is not None:
            self.sebrane_figurky.append(cil)
        # Na konci desky se pěšák v této verzi vždy promění v dámu.
        if figura.nazev == "pesak" and cy in (0, 7):
            self.deska[cy][cx] = Dama(figura.barva)
        return True

    def vypis(self) -> None:
        for y in range(7, -1, -1):
            radek = []

            for x in range(8):
                figura = self.deska[y][x]

                if figura:
                    radek.append(figura.symbol())
                else:
                    radek.append(".")

            print(y + 1, " ".join(radek))

        print("  a b c d e f g h")
