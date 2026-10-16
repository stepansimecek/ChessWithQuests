# ChessWithQuests

Školní projekt šachů s jednoduchými questy. Dva lidé hrají u jednoho počítače v terminálu.
Tato verze rozšiřuje původní fork o další figurky, pravidla pohybu a podpůrné části hry.

## Spuštění

Potřebuješ Python 3.10 nebo novější. Žádné další knihovny se neinstalují.
Otevři terminál v hlavní složce projektu a spusť:

```text
python main.py
```

Pro krátkou ukázku bez zadávání použij `python main.py --demo`.
Funguje také původní cesta `python model/main.py` nebo `python -m model.main`.

## Ovládání

| Co zadat | Co se stane |
| --- | --- |
| `e2 e4` | Přesune figurku z e2 na e4, pokud je tah platný. |
| `mozne e2` | Ukáže možné cíle pro figurku na e2. |
| `historie` | Vypíše provedené tahy. |
| `questy` | Ukáže úkoly a body obou hráčů. |
| `cas` | Ukáže, kolik sekund každý hráč zatím přemýšlel. |
| `uloz` | Uloží historii a přehled hry. |
| `konec` | Ukončí program a uloží historii. |

Bílé figurky jsou velká písmena, černé malá: K král, D dáma, V věž,
S střelec, J jezdec (kůň), P pěšák. Tečka znamená prázdné pole.
Bílý začíná dole a táhne směrem k vyšším číslům řad.

Vyzkoušej postupně `e2 e4`, `d7 d5`, `e4 d5`, potom `questy` a `historie`.
Bílý dostane 10 bodů za první tah a 30 za první sebranou figurku.
Každý hráč může každý quest splnit pouze jednou za partii.
Dalších 20 bodů získá za koně v soupeřově polovině desky.

## Co funguje a co zatím chybí

- Všech šest druhů figurek a jejich běžný pohyb, blokování cesty a braní.
- Pěšák může ze startovní řady o dvě pole, bere šikmo a na konci se mění v dámu.
- Střídání hráčů, ochrana vlastního krále, šach, mat a pat podle podporovaných tahů.
- Historie, jednoduché questy, měření spotřebovaného času a vyhledání uživatele.
- Export do `ulozene_hry/hra_1.txt` a `hra_1.json`; další export dostane další číslo.

Jde o zjednodušené šachy: **není rošáda ani braní mimochodem** a při proměně
nelze vybrat jinou figurku než dámu. Neřeší se trojí opakování pozice,
pravidlo 50 tahů ani remíza pro nedostatek materiálu. Čas se měří směrem nahoru,
není tu prohra na čas. Není grafika, počítačový soupeř ani síťová hra.
TXT používá souřadnice (např. `e2-e4`), **není to standardní PGN**; FEN se neexportuje.
JSON obsahuje přehled hráčů, bodů, času a questů. Export slouží k prohlédnutí,
zatím z něj nejde rozehranou hru načíst. Účty a questy se neukládají do databáze.

## Jak se v kódu vyznat

| Soubor ve složce model | Úloha |
| --- | --- |
| `main.py` | Čte příkazy a vypisuje výsledek. |
| `models.py` | Uchovává údaje o uživateli a hráči. |
| `figurka.py`, `figurky.py` | Popisují figurky a jejich symboly. |
| `herni_plocha.py` | Uchovává desku a přesouvá figurky. |
| `tah.py`, `vektor.py` | Uchovávají tah a pomáhají se souřadnicemi. |
| `revizor_tahu.py` | Rozhoduje, jestli je tah dovolený. |
| `game_manager.py` | Spojuje všechny části hry. |
| `game_logger.py` | Uchovává historii. |
| `game_timer.py` | Měří čas obou hráčů. |
| `quest.py`, `quest_manager.py` | Popisují a vyhodnocují úkoly. |
| `export_writer.py` | Vytváří textový zápis a JSON přehled. |
| `user_manager.py` | Uchovává a vyhledává uživatele podle jména. |

### Jeden tah krok za krokem

1. `main.py` převede text `e2 e4` na dvojice `(4, 1)` a `(4, 3)`.
2. Vznikne objekt `Tah` a předá se do `GameManager.proved_tah`.
3. Revizor zkontroluje pohyb, obsazení polí a bezpečí krále.
4. Plocha provede přesun. Logger uloží zápis a quest manager zkontroluje úkoly.
5. Vymění se aktivní hráč, zjistí se šach/mat/pat a spustí se čas druhému hráči.

`self` označuje konkrétní objekt. Například `self.deska` je deska právě této hry.
`None` znamená prázdnou hodnotu, tady často prázdné pole. `return False` oznámí,
že kontrola neprošla. Deska je seznam řádků: `deska[y][x]`; souřadnice se počítají od nuly.
`@dataclass` v původních třídách automaticky připraví ukládání hodnot při vytvoření objektu.
Nejsložitější část je kontrola šachu: revizor dočasně zkusí tah a potom desku obnoví.

Deska sama řeší jen přesun. Při hraní vždy volej `GameManager.proved_tah`,
aby se neobešla pravidla, střídání hráčů, historie a questy.
Složky `controller` a `view` zůstávají připravené pro případné další rozdělení projektu.

## Ověření

Z hlavní složky spusť:

```text
python -m unittest test_hra -v
```

Testy ověřují pohyb a blokování figurek, vlastní šach, obnovu desky po simulaci,
mat/pat, questy, export, čas a neplatné vstupy. Testovací kód není nutné znát pro ovládání hry.
