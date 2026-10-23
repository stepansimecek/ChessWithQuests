"""Spuštění grafické hry. Zde pouze sestavíme model, view a controller."""
import tkinter as tk
from pathlib import Path
from model.models import Uzivatel, Hrac
from model.game_manager import GameManager
from view.hra_view import HraView
from controller.hra_controller import HraController


def main():
    okno = tk.Tk()
    bily = Hrac(Uzivatel("Štěpán", "", 1200), "bila")
    cerny = Hrac(Uzivatel("Druhý hráč", "", 1200), "cerna")
    hra = GameManager(bily, cerny)  # Model: data a pravidla.
    view = HraView(okno)  # View: vzhled okna a kreslení.
    slozka = Path(__file__).resolve().parent / "ulozene_hry"
    controller = HraController(hra, view, slozka)  # Controller: reakce na události.
    okno.mainloop()  # Tkinter čeká na kliknutí a jiné události, dokud okno nezavřeme.


if __name__ == "__main__":
    main()
