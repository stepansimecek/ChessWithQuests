from herni_plocha import HerniPlocha
from tah import Tah


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
