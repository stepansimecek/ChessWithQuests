from pathlib import Path
from model.herni_plocha import HerniPlocha
from model.revizor_tahu import RevizorTahu
from model.game_logger import GameLogger
from model.game_timer import GameTimer
from model.quest_manager import QuestManager
from model.user_manager import UserManager
from model.export_writer import ChessNotationWriter, MetadataWriter


class GameManager:
    def __init__(self, hrac1, hrac2):
        if {hrac1.barva, hrac2.barva} != {"bila", "cerna"}:
            raise ValueError("Hra potřebuje jednoho bílého a jednoho černého hráče.")
        self.hraci = [hrac1, hrac2]
        self.aktivni_barva = "bila"
        self.plocha = HerniPlocha()
        self.revizor = RevizorTahu(self.plocha)
        self.logger = GameLogger()
        self.casovac = GameTimer()
        self.quest_manager = QuestManager()
        self.user_manager = UserManager()
        for hrac in self.hraci:
            self.user_manager.pridej(hrac.uzivatel)
            hrac.skore = 0
        self.stav = "hra"
        self.zprava = ""
        self.casovac.spust("bila")

    def aktivni_hrac(self):
        for hrac in self.hraci:
            if hrac.barva == self.aktivni_barva:
                return hrac

    def proved_tah(self, tah):
        if self.stav in ["mat", "pat"]:
            self.zprava = "Hra už skončila."
            return False
        if not self.revizor.over_tah(tah, self.aktivni_barva):
            self.zprava = "Neplatný tah. Zkontroluj figurku, cestu a šach."
            return False
        figura = self.plocha.vrat_figuru(tah.start)
        sebrana = self.plocha.vrat_figuru(tah.cil)
        hrac = self.aktivni_hrac()
        self.casovac.zastav()
        self.plocha.posun_figuru(tah)
        promena = figura.nazev == "pesak" and tah.cil[1] in (0, 7)
        self.logger.uloz_tah(tah, figura, sebrana, promena)
        nove = self.quest_manager.zkontroluj(hrac, tah, figura, sebrana)
        self.prepni_hrace()
        if self.revizor.check_mat(self.aktivni_barva):
            self.stav = "mat"
        elif self.revizor.check_pat(self.aktivni_barva):
            self.stav = "pat"
        elif self.revizor.check_sach(self.aktivni_barva):
            self.stav = "sach"
        else:
            self.stav = "hra"
        self.zprava = "Tah proveden."
        if nove:
            self.zprava += " Splněné questy: " + ", ".join(nove)
        if self.stav not in ["mat", "pat"]:
            self.casovac.spust(self.aktivni_barva)
        return True

    def prepni_hrace(self):
        if self.aktivni_barva == "bila":
            self.aktivni_barva = "cerna"
        else:
            self.aktivni_barva = "bila"

    def uloz_hru(self, slozka="ulozene_hry"):
        slozka = Path(slozka)
        slozka.mkdir(parents=True, exist_ok=True)
        # Každý export dostane vlastní číslo, starší zápas nepřepíšeme.
        cislo = 1
        while (slozka / f"hra_{cislo}.txt").exists() or (slozka / f"hra_{cislo}.json").exists():
            cislo += 1
        zapis = ChessNotationWriter()
        metadata = MetadataWriter()
        cesta = slozka / f"hra_{cislo}.txt"
        zapis.uloz(cesta, zapis.export(self.logger.zaznamy))
        metadata.uloz(slozka / f"hra_{cislo}.json", metadata.export(self))
        return cesta
