import tkinter as tk


class HraView:
    """Vzhled okna. Pravidla stále řeší model, kliknutí controller."""

    def __init__(self, okno):
        self.okno = okno
        self.pozadi, self.karta = "#101b26", "#1b2b39"
        self.text, self.tlumena = "#edf2ef", "#a3b5bd"
        self.velikost_pole, self.okraj = 58, 26
        okno.title("ChessWithQuests • nová podoba")
        okno.configure(bg=self.pozadi)
        okno.resizable(False, False)
        okno.option_add("*Font", ("Segoe UI", -13))

        hlavicka = tk.Frame(okno, bg=self.pozadi)
        hlavicka.pack(fill="x", padx=22, pady=(16, 12))
        tk.Label(hlavicka, text="CHESS / QUESTS", font=("Segoe UI", -26, "bold"),
                 bg=self.pozadi, fg=self.text).pack(side="left")
        tk.Label(hlavicka, text="DVA HRÁČI · JEDNA DESKA", font=("Segoe UI", -12),
                 bg=self.pozadi, fg="#70cfb0").pack(side="right")

        obsah = tk.Frame(okno, bg=self.pozadi)
        obsah.pack(padx=22)
        leva = tk.Frame(obsah, bg=self.pozadi)
        leva.grid(row=0, column=0, sticky="n")
        rozmer = 8 * self.velikost_pole + 2 * self.okraj
        self.canvas = tk.Canvas(leva, width=rozmer, height=rozmer,
                                bg=self.karta, highlightthickness=0, cursor="hand2")
        self.canvas.pack()
        tk.Label(leva, text="VYBER FIGURKU  →  KLIKNI NA CÍLOVÉ POLE",
                 bg=self.pozadi, fg=self.tlumena, font=("Segoe UI", -12)).pack(pady=10)
        panel = tk.Frame(obsah, bg=self.pozadi)
        panel.grid(row=0, column=1, padx=(18, 0), sticky="n")
        stav_karta = self.nova_karta(panel, "PRŮBĚH PARTIE")
        self.stav = tk.Label(stav_karta, bg=self.karta, fg="#70cfb0",
                             font=("Segoe UI", -20, "bold"), anchor="w")
        self.stav.pack(fill="x", pady=(6, 8))
        hodiny = tk.Frame(stav_karta, bg=self.karta)
        hodiny.pack(fill="x")
        self.cas_bily = self.hodiny(hodiny, "BÍLÝ", "#ecede5", "#162736")
        self.cas_cerny = self.hodiny(hodiny, "ČERNÝ", "#101b26", "#edf2ef")
        quest_karta = self.nova_karta(panel, "QUESTY A BODY")
        self.questy = tk.Label(quest_karta, bg=self.karta, fg=self.text,
                               justify="left", anchor="w", font=("Segoe UI", -12),
                               wraplength=278)
        self.questy.pack(fill="x", pady=(6, 0))
        historie_karta = self.nova_karta(panel, "POSLEDNÍ TAHY")
        self.historie = tk.Listbox(historie_karta, width=33, height=4,
                                  bg=self.karta, fg=self.text, bd=0,
                                  highlightthickness=0, selectbackground="#356857",
                                  font=("Consolas", -13), activestyle="none")
        self.historie.pack(fill="x", pady=(6, 0))
        self.tlacitko_zrus = self.tlacitko(panel, "Zrušit výběr", False)
        self.tlacitko_uloz = self.tlacitko(panel, "Uložit historii", True)
        self.tlacitko_konec = self.tlacitko(panel, "Uložit a zavřít", False)
        self.zprava = tk.Label(okno, text="Vyber bílou figurku.",
                               bg=self.karta, fg=self.text, anchor="w", justify="left",
                               wraplength=790, padx=14, pady=10)
        self.zprava.pack(fill="x", padx=22, pady=(10, 6))
        tk.Label(okno, text="Zjednodušená pravidla · bez rošády a braní mimochodem · proměna na dámu",
                 bg=self.pozadi, fg=self.tlumena, font=("Segoe UI", -11)).pack(pady=(0, 12))

    def nova_karta(self, rodic, nadpis):
        # Karta sdružuje informace, které patří k sobě.
        karta = tk.Frame(rodic, bg=self.karta, padx=12, pady=10)
        karta.pack(fill="x", pady=(0, 9))
        tk.Label(karta, text=nadpis, bg=self.karta, fg=self.tlumena,
                 font=("Segoe UI", -11, "bold"), anchor="w").pack(fill="x")
        return karta

    def hodiny(self, rodic, nadpis, pozadi, barva):
        ramecek = tk.Frame(rodic, bg=pozadi, padx=10, pady=5)
        ramecek.pack(side="left", expand=True, fill="x", padx=2)
        tk.Label(ramecek, text=nadpis, bg=pozadi, fg=barva,
                 font=("Segoe UI", -11, "bold")).pack(anchor="w")
        cas = tk.Label(ramecek, text="00:00", bg=pozadi, fg=barva,
                       font=("Consolas", -23, "bold"))
        cas.pack(anchor="w")
        return cas

    def tlacitko(self, rodic, text, hlavni):
        barva = "#70cfb0" if hlavni else self.karta
        tlacitko = tk.Button(rodic, text=text, bg=barva,
                            fg="#101b26" if hlavni else self.text,
                            activebackground="#96e2c9", activeforeground="#101b26",
                            relief="flat", bd=0, pady=6, cursor="hand2")
        tlacitko.pack(fill="x", pady=(0, 5))
        return tlacitko

    def vykresli_desku(self, deska, vybrane, mozne_cile):
        self.canvas.delete("all")
        for y in range(8):
            for x in range(8):
                vlevo = self.okraj + x * self.velikost_pole
                nahore = self.okraj + (7 - y) * self.velikost_pole
                velikost = self.velikost_pole
                barva = "#e5e6d8" if (x + y) % 2 else "#668b7c"
                if (x, y) == vybrane:
                    barva = "#e6c66d"
                self.canvas.create_rectangle(vlevo, nahore, vlevo + velikost,
                                             nahore + velikost, fill=barva,
                                             outline=barva, tags="pole")
                figura = deska[y][x]
                if figura is not None:
                    self.nakresli_figurku(figura, vlevo + velikost / 2,
                                         nahore + velikost / 2)
                if (x, y) in mozne_cile:
                    # Tečka označuje volné pole, rámeček možnost braní.
                    if figura is None:
                        cx, cy = vlevo + velikost / 2, nahore + velikost / 2
                        self.canvas.create_oval(cx - 7, cy - 7, cx + 7, cy + 7,
                                                fill="#315f50", outline="", tags="cil")
                    else:
                        self.canvas.create_rectangle(vlevo + 3, nahore + 3,
                                                     vlevo + velikost - 3, nahore + velikost - 3,
                                                     outline="#b4514c", width=3, tags="cil")
        for cislo in range(8):
            stred = self.okraj + (cislo + 0.5) * self.velikost_pole
            self.canvas.create_text(stred, 13, text="abcdefgh"[cislo], fill=self.tlumena)
            self.canvas.create_text(stred, self.okraj + 8 * self.velikost_pole + 13,
                                    text="abcdefgh"[cislo], fill=self.tlumena)
            self.canvas.create_text(13, stred, text=str(8 - cislo), fill=self.tlumena)

    def nakresli_figurku(self, figura, x, y):
        # Plné šachové znaky obarvíme podle hráče a přidáme obrys.
        znaky = {"K": "♚", "D": "♛", "V": "♜", "S": "♝", "J": "♞", "P": "♟"}
        znak = znaky[figura.symbol().upper()]
        barva = "#fffaf0" if figura.barva == "bila" else "#182530"
        obrys = "#263d3a" if figura.barva == "bila" else "#cad4c7"
        font = ("Segoe UI Symbol", -48)  # Záporná velikost je v pixelech, nezvětší se s DPI.
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.canvas.create_text(x + dx, y + dy, text=znak, fill=obrys,
                                    font=font, tags="obrys")
        self.canvas.create_text(x, y, text=znak, fill=barva, font=font, tags="figurka")

    def zobraz_stav(self, text):
        self.stav.config(text=text, fg="#edc574" if "ŠACH" in text or "MAT" in text else "#70cfb0")

    def zobraz_zpravu(self, text):
        self.zprava.config(text=text)

    def zobraz_questy(self, text):
        self.questy.config(text=text.replace(": hotovo", "  ✓").replace(": čeká", "  ○"))

    def zobraz_historii(self, zaznamy):
        self.historie.delete(0, tk.END)
        for cislo, zaznam in enumerate(zaznamy, start=1):
            self.historie.insert(tk.END, f"{cislo:>2}.  {zaznam}")
        self.historie.yview_moveto(1)

    def zobraz_cas(self, bily, cerny):
        for popisek, sekundy in [(self.cas_bily, bily), (self.cas_cerny, cerny)]:
            minuty, sekundy = divmod(int(sekundy), 60)
            popisek.config(text=f"{minuty:02}:{sekundy:02}")