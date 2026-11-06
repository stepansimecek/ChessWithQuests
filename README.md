# ♟ ChessWithQuests

**Školní šachová hra v Pythonu pro dva hráče.**

Hrají dva hráči u jednoho počítače. Kromě šachů plní jednoduché úkoly (questy), za které získávají body.

## Spuštění

Potřebuješ **Python 3.10 nebo novější**. Ve složce projektu spusť:

```bash
python main.py
```

Otevře se okno se šachovnicí.

## Jak hrát

1. **Klikni na svou figurku.**
2. **Klikni na cílové pole.** Možné tahy se zvýrazní.
3. **Po platném tahu hraje druhý hráč.**

Vedle šachovnice uvidíš **hráče na tahu, čas, questy a historii**.
Tlačítkem **Uložit historii** uložíš přehled partie do složky `ulozene_hry`.

### Označení figurek

| K | D | V | S | J | P |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Král | Dáma | Věž | Střelec | Jezdec | Pěšák |

## Co hra umí

- **Pravidla:** pohyb a braní figurek, střídání hráčů a kontrola šachu, matu a patu.
- **Questy:** jednoduché úkoly a počítání bodů.
- **Přehled partie:** měření času a historie tahů.
- **Ukládání:** přehled hry ve formátu TXT a JSON.

### Co zatím chybí

Hra je zjednodušená:

- Chybí rošáda a braní mimochodem. Pěšák se mění jen v dámu.
- Neřeší se remíza opakováním pozice, pravidlem 50 tahů ani nedostatkem materiálu.
- Čas se pouze měří.
- Uloženou partii zatím nejde znovu načíst.
- Není tu počítačový soupeř ani hra po síti.

## Rozdělení projektu

| Část | Co dělá |
| :--- | :--- |
| `model` | Uchovává stav hry a kontroluje pravidla. |
| `view` | Kreslí šachovnici a další části okna pomocí Tkinter Canvas. |
| `controller` | Reaguje na kliknutí a propojuje pravidla se zobrazením. |
| `gui.py` | Spojí jednotlivé části a otevře okno. |

## Další možnosti

| Možnost | Příkaz |
| :--- | :--- |
| Textová verze | `python main.py --terminal` |
| Krátká ukázka | `python main.py --demo` |
