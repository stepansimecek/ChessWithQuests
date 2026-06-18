from models import Hrac
from tah import Tah
from herni_plocha import HerniPlocha
from revizor_tahu import RevizorTahu
from game_logger import GameLogger


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
