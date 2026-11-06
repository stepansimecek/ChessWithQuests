from pathlib import Path
from model.tah import Tah, pozice_na_text


class HraController:
    """Controller propojuje události z okna s modelem a následným vykreslením."""

    def __init__(self, hra, view, slozka_ulozeni):
        self.hra = hra
        self.view = view
        self.slozka_ulozeni = Path(slozka_ulozeni)
        self.vybrane = None
        self.mozne_cile = []
        self.casova_uloha = None

        # bind spojuje událost s metodou. <Button-1> je levé tlačítko myši.
        # Za názvem metody nejsou závorky: metoda se má spustit až po kliknutí.
        self.view.canvas.bind("<Button-1>", self.klik_na_desku)
        self.view.tlacitko_zrus.config(command=self.zrus_vyber)
        self.view.tlacitko_uloz.config(command=self.uloz)
        self.view.tlacitko_konec.config(command=self.zavri)
        self.view.okno.protocol("WM_DELETE_WINDOW", self.zavri)
        self.obnov_obrazovku()
        self.obnov_cas()

    def klik_na_desku(self, event):
        # Tkinter nám předá event.x a event.y: místo kliknutí v pixelech Canvasu.
        px = event.x - self.view.okraj
        py = event.y - self.view.okraj
        rozmer = 8 * self.view.velikost_pole
        if not (0 <= px < rozmer and 0 <= py < rozmer):
            return  # Kliknutí na popisek nebo okraj není tah.
        x = px // self.view.velikost_pole
        y = 7 - py // self.view.velikost_pole
        self.klik_na_pole((x, y))

    def klik_na_pole(self, pozice):
        if self.hra.stav in ["mat", "pat"]:
            self.view.zobraz_zpravu("Hra skončila. Můžeš uložit historii a zavřít okno.")
            return
        figura = self.hra.plocha.vrat_figuru(pozice)
        if pozice == self.vybrane:
            self.zrus_vyber()
            return

        # Kliknutí na vlastní figurku ji vybere (nebo změní předchozí výběr).
        if figura is not None and figura.barva == self.hra.aktivni_barva:
            self.vybrane = pozice
            self.mozne_cile = self.hra.revizor.mozne_tahy(pozice, self.hra.aktivni_barva)
            self.view.zobraz_zpravu("Vybráno " + pozice_na_text(pozice) + ". Tečky označují volná cílová pole, rámeček možnost braní.")
        elif self.vybrane is None:
            self.view.zobraz_zpravu("Nejprve vyber figurku hráče, který je na tahu.")
        else:
            # Pravidla nekopírujeme do controlleru. Rozhoduje existující model.
            tah = Tah(self.vybrane, pozice)
            if self.hra.proved_tah(tah):
                self.vybrane = None
                self.mozne_cile = []
            self.view.zobraz_zpravu(self.hra.zprava)
        self.obnov_obrazovku()

    def zrus_vyber(self):
        self.vybrane = None
        self.mozne_cile = []
        self.view.zobraz_zpravu("Výběr zrušen. Vyber svou figurku.")
        self.obnov_obrazovku()

    def obnov_obrazovku(self):
        self.view.vykresli_desku(self.hra.plocha.deska, self.vybrane, self.mozne_cile)
        barva = "bílý" if self.hra.aktivni_barva == "bila" else "černý"
        stav = "Na tahu: " + barva
        if self.hra.stav == "sach":
            stav += " – ŠACH"
        elif self.hra.stav == "mat":
            vitez = "černý" if self.hra.aktivni_barva == "bila" else "bílý"
            stav = "MAT – vyhrál " + vitez
        elif self.hra.stav == "pat":
            stav = "PAT – remíza"
        self.view.zobraz_stav(stav)
        self.view.zobraz_historii(self.hra.logger.zaznamy)

        radky = []
        for hrac in self.hra.hraci:
            jmeno_barvy = "Bílý" if hrac.barva == "bila" else "Černý"
            radky.append(f"{jmeno_barvy}: {hrac.skore} bodů")
            for quest in self.hra.quest_manager.questy[hrac.barva]:
                znacka = "hotovo" if quest.splneno else "čeká"
                radky.append(f"  {quest.nazev}: {znacka}")
        self.view.zobraz_questy("\n".join(radky))
        self.view.zobraz_cas(self.hra.casovac.vrat_cas("bila"), self.hra.casovac.vrat_cas("cerna"))

    def obnov_cas(self):
        self.view.zobraz_cas(self.hra.casovac.vrat_cas("bila"), self.hra.casovac.vrat_cas("cerna"))
        # after zavolá metodu za 500 ms. Na rozdíl od sleep nezablokuje okno.
        self.casova_uloha = self.view.okno.after(500, self.obnov_cas)

    def uloz(self):
        try:
            cesta = self.hra.uloz_hru(self.slozka_ulozeni)
        except OSError as chyba:
            self.view.zobraz_zpravu("Uložení se nepodařilo: " + str(chyba))
            return False
        self.view.zobraz_zpravu("Uloženo: " + str(cesta))
        return True

    def zavri(self):
        self.hra.casovac.zastav()
        if not self.uloz():
            # Při chybě necháme okno otevřené, aby se historie neztratila.
            if self.hra.stav not in ["mat", "pat"]:
                self.hra.casovac.spust(self.hra.aktivni_barva)
            return
        if self.casova_uloha is not None:
            self.view.okno.after_cancel(self.casova_uloha)
        self.view.okno.destroy()
