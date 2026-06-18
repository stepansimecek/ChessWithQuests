from typing import Optional

from figurka import Figurka
from figurky import Pesak, Kral
from tah import Tah


class HerniPlocha:
    def __init__(self):
        self.deska: list[list[Optional[Figurka]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.nastav_start()

    def nastav_start(self) -> None:
        # Zjednodušené rozestavení: králové a pěšáci
        self.deska[0][4] = Kral("bila")
        self.deska[7][4] = Kral("cerna")

        for x in range(8):
            self.deska[1][x] = Pesak("bila")
            self.deska[6][x] = Pesak("cerna")

    def je_v_desce(self, pozice: tuple[int, int]) -> bool:
        x, y = pozice
        return 0 <= x < 8 and 0 <= y < 8

    def vrat_figuru(self, pozice: tuple[int, int]) -> Optional[Figurka]:
        x, y = pozice
        return self.deska[y][x]

    def posun_figuru(self, tah: Tah) -> bool:
        if not self.je_v_desce(tah.start) or not self.je_v_desce(tah.cil):
            return False

        figura = self.vrat_figuru(tah.start)

        if figura is None:
            return False

        sx, sy = tah.start
        cx, cy = tah.cil

        self.deska[cy][cx] = figura
        self.deska[sy][sx] = None
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
