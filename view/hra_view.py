import tkinter as tk


class HraView:
    """View má na starosti vzhled okna. Nerozhoduje o platnosti tahů."""

    def __init__(self, okno):
        self.okno = okno
        self.okno.title("ChessWithQuests – šachy s questy")
        self.okno.resizable(False, False)
        self.velikost_pole = 60
        self.okraj = 24

        tk.Label(okno, text="ChessWithQuests", font=("Arial", 20, "bold")).pack(pady=(12, 4))
        tk.Label(okno, text="Klikni na svou figurku a potom na cílové pole.").pack()
        obsah = tk.Frame(okno)
        obsah.pack(padx=12, pady=10)

        # Canvas je kreslicí plocha. Budeme na ni kreslit pole a figurky.
        rozmer = 8 * self.velikost_pole + 2 * self.okraj
        self.canvas = tk.Canvas(obsah, width=rozmer, height=rozmer,
                                bg="#f5f1e8", highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        panel = tk.Frame(obsah, width=300)
        panel.grid(row=0, column=1, padx=(16, 0), sticky="n")
        self.stav = tk.Label(panel, font=("Arial", 13, "bold"), anchor="w")
        self.stav.pack(fill="x")
        self.cas = tk.Label(panel, anchor="w")
        self.cas.pack(fill="x", pady=(5, 12))
        tk.Label(panel, text="Questy", font=("Arial", 12, "bold"), anchor="w").pack(fill="x")
        self.questy = tk.Label(panel, justify="left", anchor="w", wraplength=300)
        self.questy.pack(fill="x", pady=(4, 12))
        tk.Label(panel, text="Historie tahů", font=("Arial", 12, "bold"), anchor="w").pack(fill="x")
        self.historie = tk.Listbox(panel, width=43, height=8)
        self.historie.pack(pady=(4, 12))
        self.tlacitko_zrus = tk.Button(panel, text="Zrušit výběr")
        self.tlacitko_zrus.pack(fill="x", pady=2)
        self.tlacitko_uloz = tk.Button(panel, text="Uložit historii")
        self.tlacitko_uloz.pack(fill="x", pady=2)
        self.tlacitko_konec = tk.Button(panel, text="Uložit a zavřít")
        self.tlacitko_konec.pack(fill="x", pady=2)

        self.zprava = tk.Label(okno, text="Vyber bílou figurku.", wraplength=800)
        self.zprava.pack(padx=12, pady=(0, 8))
        tk.Label(okno, text="K král · D dáma · V věž · S střelec · J jezdec · P pěšák").pack()
        tk.Label(okno, text="Bez rošády a braní mimochodem. Proměna pěšáka vždy na dámu.",
                 fg="#555555").pack(pady=(3, 12))

    def vykresli_desku(self, deska, vybrane, mozne_cile):
        # Nejjednodušší překreslení: starý obrázek smažeme a nakreslíme nový.
        self.canvas.delete("all")
        for y in range(8):
            for x in range(8):
                # Model počítá řady odspodu, Canvas má nulu nahoře.
                vlevo = self.okraj + x * self.velikost_pole
                nahore = self.okraj + (7 - y) * self.velikost_pole
                vpravo = vlevo + self.velikost_pole
                dole = nahore + self.velikost_pole
                barva = "#eadcc4" if (x + y) % 2 else "#8caa90"
                if (x, y) == vybrane:
                    barva = "#f4cf61"
                self.canvas.create_rectangle(vlevo, nahore, vpravo, dole,
                                             fill=barva, outline=barva, tags="pole")
                figura = deska[y][x]
                if figura is not None:
                    # Kruh s písmenem je čitelný i bez obrázků a speciálních fontů.
                    vypln = "#ffffff" if figura.barva == "bila" else "#27352e"
                    pismo = "#27352e" if figura.barva == "bila" else "#ffffff"
                    self.canvas.create_oval(vlevo + 9, nahore + 9, vpravo - 9, dole - 9,
                                            fill=vypln, outline="#27352e", tags="figurka")
                    self.canvas.create_text((vlevo + vpravo) / 2, (nahore + dole) / 2,
                                            text=figura.symbol().upper(), fill=pismo,
                                            font=("Arial", 22, "bold"), tags="symbol")
                if (x, y) in mozne_cile:
                    self.canvas.create_rectangle(vlevo + 3, nahore + 3, vpravo - 3, dole - 3,
                                                 outline="#1966ba", width=3, tags="cil")
        for cislo in range(8):
            stred = self.okraj + cislo * self.velikost_pole + self.velikost_pole / 2
            self.canvas.create_text(stred, 12, text="abcdefgh"[cislo])
            self.canvas.create_text(stred, 8 * self.velikost_pole + self.okraj + 12,
                                    text="abcdefgh"[cislo])
            self.canvas.create_text(12, stred, text=str(8 - cislo))

    def zobraz_stav(self, text):
        self.stav.config(text=text)

    def zobraz_zpravu(self, text):
        self.zprava.config(text=text)

    def zobraz_questy(self, text):
        self.questy.config(text=text)

    def zobraz_historii(self, zaznamy):
        self.historie.delete(0, tk.END)
        for cislo, zaznam in enumerate(zaznamy, start=1):
            self.historie.insert(tk.END, f"{cislo}. {zaznam}")
        self.historie.yview_moveto(1)

    def zobraz_cas(self, bily, cerny):
        self.cas.config(text=f"Čas: bílý {int(bily)} s | černý {int(cerny)} s")
