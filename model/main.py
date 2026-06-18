
from dataclasses import dataclass
from typing import Optional


@dataclass
class Uzivatel:
    jmeno: str
    email: str
    elo: int


@dataclass
class Hrac:
    uzivatel: Uzivatel
    barva: str  # "bila" nebo "cerna"

    def get_elo_rating(self) -> int:
        return self.uzivatel.elo


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
        return znak if self.barva == "bila" else znak.lower()


class Pesak(Figurka):
    def __init__(self, barva: str):
        super().__init__("pesak", barva)


class Kral(Figurka):
    def __init__(self, barva: str):
        super().__init__("kral", barva)


@dataclass
class Tah:
    start: tuple[int, int]
    cil: tuple[int, int]


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
                radek.append(figura.symbol() if figura else ".")
            print(y + 1, " ".join(radek))
        print("  a b c d e f g h")


class RevizorTahu:
    def __init__(self, plocha: HerniPlocha):
        self.plocha = plocha

    def over_tah(self, tah: Tah, aktivni_barva: str) -> bool:
        figura = self.plocha.vrat_figuru(tah.start)

        if figura is None:
            return False

        if figura.barva != aktivni_barva:
            return False

        # Základní jednoduchá validace:
        # figura se nesmí posunout mimo desku
        # a nesmí stát na místě
        if not self.plocha.je_v_desce(tah.cil):
            return False

        if tah.start == tah.cil:
            return False

        return True


class GameLogger:
    def __init__(self):
        self.tahy: list[Tah] = []

    def uloz_tah(self, tah: Tah) -> None:
        self.tahy.append(tah)

    def vypis_log(self) -> None:
        print("Historie tahů:")
        for i, tah in enumerate(self.tahy, start=1):
            print(f"{i}. {tah.start} -> {tah.cil}")


class GameManager:
    def __init__(self, hrac1: Hrac, hrac2: Hrac):
        self.hraci = [hrac1, hrac2]
        self.aktivni_barva = "bila"
        self.plocha = HerniPlocha()
        self.revizor = RevizorTahu(self.plocha)
        self.logger = GameLogger()

    def proved_tah(self, tah: Tah) -> bool:
        if self.revizor.over_tah(tah, self.aktivni_barva):
            self.plocha.posun_figuru(tah)
            self.logger.uloz_tah(tah)
            self.prepni_hrace()
            return True

        print("Neplatný tah.")
        return False

    def prepni_hrace(self) -> None:
        if self.aktivni_barva == "bila":
            self.aktivni_barva = "cerna"
        else:
            self.aktivni_barva = "bila"


def main():
    uzivatel1 = Uzivatel("Štěpán", "stepan@email.cz", 1200)
    uzivatel2 = Uzivatel("Bot", "bot@email.cz", 1000)

    hrac1 = Hrac(uzivatel1, "bila")
    hrac2 = Hrac(uzivatel2, "cerna")

    hra = GameManager(hrac1, hrac2)

    print("Start hry:")
    hra.plocha.vypis()

    print("\nProvedu ukázkové tahy:")
    hra.proved_tah(Tah((4, 1), (4, 2)))  # bílý pěšák
    hra.proved_tah(Tah((4, 6), (4, 5)))  # černý pěšák

    print("\nDeska po tazích:")
    hra.plocha.vypis()

    print()
    hra.logger.vypis_log()


if __name__ == "__main__":
    main()
