# Tento blok dovoluje i původní spuštění: python model/main.py.
if __package__ in (None, ""):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.models import Uzivatel, Hrac
from model.game_manager import GameManager
from model.tah import Tah, text_na_pozici, pozice_na_text


def nova_hra():
    bily = Hrac(Uzivatel("Štěpán", "", 1200), "bila")
    cerny = Hrac(Uzivatel("Druhý hráč", "", 1200), "cerna")
    return GameManager(bily, cerny)


def vypis_questy(hra):
    for hrac in hra.hraci:
        print(f"{hrac.uzivatel.jmeno} ({hrac.barva}): {hrac.skore} bodů")
        for quest in hra.quest_manager.questy[hrac.barva]:
            stav = "hotovo" if quest.splneno else "čeká"
            print(f"  {quest.nazev}: {quest.popis} [{stav}, {quest.odmena} bodů]")


def demo():
    hra = nova_hra()
    for odkud, kam in [("e2", "e4"), ("d7", "d5"), ("e4", "d5")]:
        hra.proved_tah(Tah(text_na_pozici(odkud), text_na_pozici(kam)))
        print(hra.zprava)
    hra.casovac.zastav()
    hra.plocha.vypis()
    hra.logger.vypis_log()
    vypis_questy(hra)


def main():
    hra = nova_hra()
    print("ChessWithQuests – dva hráči u jednoho počítače")
    print("Tah: e2 e4 | mozne e2 | historie | questy | cas | uloz | konec")
    print("Zjednodušená verze: bez rošády a braní mimochodem, proměna vždy na dámu.")
    hra.plocha.vypis()
    try:
        while True:
            if hra.stav == "mat":
                print("Mat. Vyhrává", "černý." if hra.aktivni_barva == "bila" else "bílý.")
                break
            if hra.stav == "pat":
                print("Pat – remíza.")
                break
            if hra.stav == "sach":
                print("Pozor, šach!")
            prikaz = input(f"{hra.aktivni_barva} > ").strip().lower()
            casti = prikaz.split()
            if prikaz == "konec":
                break
            if prikaz == "historie":
                hra.logger.vypis_log()
            elif prikaz == "questy":
                vypis_questy(hra)
            elif prikaz == "cas":
                for barva in ["bila", "cerna"]:
                    print(barva, round(hra.casovac.vrat_cas(barva), 1), "sekund")
            elif prikaz == "uloz":
                try:
                    print("Uloženo:", hra.uloz_hru())
                except OSError as chyba:
                    print("Uložení se nepodařilo:", chyba)
            else:
                try:
                    if len(casti) == 2 and casti[0] == "mozne":
                        pozice = text_na_pozici(casti[1])
                        cile = hra.revizor.mozne_tahy(pozice, hra.aktivni_barva)
                        print("Možné cíle:", " ".join(pozice_na_text(cil) for cil in cile) or "žádné")
                    elif len(casti) == 2:
                        tah = Tah(text_na_pozici(casti[0]), text_na_pozici(casti[1]))
                        if hra.proved_tah(tah):
                            hra.plocha.vypis()
                        print(hra.zprava)
                    else:
                        print("Zadej tah jako e2 e4 nebo některý z příkazů nahoře.")
                except ValueError as chyba:
                    print(chyba)
    except (EOFError, KeyboardInterrupt):
        print("\nHra přerušena.")
    finally:
        hra.casovac.zastav()
    try:
        print("Historie uložena:", hra.uloz_hru())
    except OSError as chyba:
        print("Uložení se nepodařilo:", chyba)


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        demo()
    else:
        main()
