from model.tah import Tah
from model.vektor import Vektor


class RevizorTahu:
    def __init__(self, plocha):
        self.plocha = plocha

    def volna_cesta(self, start, cil):
        # Kontrolujeme pole mezi začátkem a cílem, ne samotný cíl.
        smer = Vektor(cil[0] - start[0], cil[1] - start[1])
        krok_x, krok_y = smer.krok()
        x, y = start[0] + krok_x, start[1] + krok_y
        while (x, y) != cil:
            if self.plocha.vrat_figuru((x, y)) is not None:
                return False
            x += krok_x
            y += krok_y
        return True

    def spravny_pohyb(self, tah, utok=False):
        if not self.plocha.je_v_desce(tah.start) or not self.plocha.je_v_desce(tah.cil):
            return False
        figura = self.plocha.vrat_figuru(tah.start)
        if figura is None or tah.start == tah.cil:
            return False
        cil = self.plocha.vrat_figuru(tah.cil)
        dx = tah.cil[0] - tah.start[0]
        dy = tah.cil[1] - tah.start[1]

        if figura.nazev == "pesak":
            smer = 1 if figura.barva == "bila" else -1
            if utok:
                return abs(dx) == 1 and dy == smer
            if abs(dx) == 1 and dy == smer:
                return cil is not None and cil.barva != figura.barva
            if dx != 0 or cil is not None:
                return False
            if dy == smer:
                return True
            startovni_rada = 1 if figura.barva == "bila" else 6
            if tah.start[1] == startovni_rada and dy == 2 * smer:
                return self.volna_cesta(tah.start, tah.cil)
            return False

        if figura.nazev == "kun":
            return (abs(dx), abs(dy)) in [(1, 2), (2, 1)]
        if figura.nazev == "kral":
            return max(abs(dx), abs(dy)) == 1
        rovne = dx == 0 or dy == 0
        sikmo = abs(dx) == abs(dy)
        if figura.nazev == "vez" and not rovne:
            return False
        if figura.nazev == "strelec" and not sikmo:
            return False
        if figura.nazev == "dama" and not (rovne or sikmo):
            return False
        if figura.nazev not in ["vez", "strelec", "dama"]:
            return False
        return self.volna_cesta(tah.start, tah.cil)

    def check_sach(self, barva):
        kral = None
        for y in range(8):
            for x in range(8):
                figura = self.plocha.vrat_figuru((x, y))
                if figura is not None and figura.nazev == "kral" and figura.barva == barva:
                    kral = (x, y)
        if kral is None:
            return False
        for y in range(8):
            for x in range(8):
                figura = self.plocha.vrat_figuru((x, y))
                if figura is not None and figura.barva != barva:
                    if self.spravny_pohyb(Tah((x, y), kral), utok=True):
                        return True
        return False

    def over_tah(self, tah, aktivni_barva):
        if not self.spravny_pohyb(tah):
            return False
        figura = self.plocha.vrat_figuru(tah.start)
        cil = self.plocha.vrat_figuru(tah.cil)
        if figura.barva != aktivni_barva:
            return False
        if cil is not None and (cil.barva == aktivni_barva or cil.nazev == "kral"):
            return False

        # Tah si zkusíme a obě pole pak obnovíme. Historii tím neměníme.
        sx, sy = tah.start
        cx, cy = tah.cil
        self.plocha.deska[sy][sx] = None
        self.plocha.deska[cy][cx] = figura
        try:
            bezpecny = not self.check_sach(aktivni_barva)
        finally:
            self.plocha.deska[sy][sx] = figura
            self.plocha.deska[cy][cx] = cil
        return bezpecny

    def mozne_tahy(self, pozice, barva):
        vysledek = []
        for y in range(8):
            for x in range(8):
                if self.over_tah(Tah(pozice, (x, y)), barva):
                    vysledek.append((x, y))
        return vysledek

    def ma_tah(self, barva):
        for y in range(8):
            for x in range(8):
                figura = self.plocha.vrat_figuru((x, y))
                if figura is not None and figura.barva == barva:
                    if self.mozne_tahy((x, y), barva):
                        return True
        return False

    def check_mat(self, barva):
        return self.check_sach(barva) and not self.ma_tah(barva)

    def check_pat(self, barva):
        return not self.check_sach(barva) and not self.ma_tah(barva)
