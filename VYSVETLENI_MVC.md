# Jak funguje okno a klikání

Tato úprava přidává jednoduché grafické rozhraní k existující hře.
Základ jsou dvě nové třídy a jeden soubor pro jejich spuštění.
Nejdřív si zkus hru spustit pomocí `python main.py` a kliknout na e2 a potom e4.

## Tři části MVC

| Část | Soubor / třída | Co dělá |
| --- | --- | --- |
| Model | `model/game_manager.py` – `GameManager` a další stávající třídy | Pamatuje si figurky, kontroluje tahy, střídá hráče, počítá questy. |
| View | `view/hra_view.py` – `HraView` | Vytvoří tlačítka, texty a Canvas. Kreslí to, co dostane. |
| Controller | `controller/hra_controller.py` – `HraController` | Přijme kliknutí, zjistí pole, vybere figurku nebo požádá model o tah. Pak aktualizuje view. |

Controller nečte obrázek obrazovky. Tkinter sám pozná kliknutí a zavolá metodu,
kterou jsme mu předem předali. Naše metoda dostane údaje o události v objektu `event`.

## 1. Spuštění (`gui.py`)

- `tk.Tk()` vytvoří hlavní okno.
- `GameManager(...)` vytvoří model hry pro dva hráče.
- `HraView(okno)` vytvoří obsah okna.
- `HraController(hra, view, slozka)` propojí model a view.
- `okno.mainloop()` nechá okno čekat na události. Program se zde nezasekl – čeká na uživatele.

Hlavní `main.py` podle argumentu spustí grafiku, terminál (`--terminal`) nebo ukázku (`--demo`).

## 2. View a Canvas (`view/hra_view.py`)

Canvas je kreslicí plocha v okně. `create_rectangle` kreslí pole,
`create_oval` kruh figurky a `create_text` písmeno. Obrázky tedy nemusíme stahovat.

Dva cykly `for` procházejí 8 řad a 8 sloupců. Jedno pole má 60 pixelů.
Kolem desky je okraj 24 pixelů pro popisky.

```python
vlevo = self.okraj + x * self.velikost_pole
nahore = self.okraj + (7 - y) * self.velikost_pole
```

Canvas má levý horní roh na `(0, 0)` a souřadnice y rostou dolů.
Herní model má bílou první řadu dole, takže použijeme `7 - y`.
Bez tohoto otočení by byla deska vzhůru nohama.

Při překreslení nejdřív `canvas.delete("all")` smaže kresbu. Nemaže figurky z modelu.
Potom nakreslíme všechna pole znovu. Pro 64 polí je to jednoduchý a dostačující postup.
View nemusí vědět, jestli kůň smí na e4. Pouze zobrazí předaný seznam možných cílů.

## 3. Propojení události a metody

V controlleru je řádek:

```python
self.view.canvas.bind("<Button-1>", self.klik_na_desku)
```

`<Button-1>` znamená kliknutí levým tlačítkem myši. `bind` říká:
„Když se tohle stane, zavolej tuto metodu.“ Za `klik_na_desku` nejsou závorky,
protože ji nechceme zavolat hned při spuštění.

U tlačítka používáme podobně `command=self.uloz`. Canvas přes `bind` předá `event`,
zato metoda připojená přes `command` se volá bez tohoto argumentu.

## 4. Z pixelu na políčko

Metoda `klik_na_desku` dostane `event.x` a `event.y` relativně ke Canvasu.
Odečteme okraj a zkontrolujeme, že jsme uvnitř desky. Pak použijeme celočíselné dělení `//`.

```python
x = px // self.view.velikost_pole
y = 7 - py // self.view.velikost_pole
```

Příklad: střed e2 je v Canvasu `(294, 414)`.
Po odečtení okraje dostaneme `(270, 390)`.
`270 // 60` je 4. `7 - 390 // 60` je 1.
Výsledek `(4, 1)` je e2 v modelu. Nula znamená první sloupec/řadu.
Kliknutí do okraje se ignoruje, aby nevznikla souřadnice mimo desku.

## 5. První a druhé kliknutí

`self.vybrane` si pamatuje vybrané pole. Na začátku je `None`, tedy nic vybraného.

1. Kliknutí na vlastní figurku ji vybere a od modelu získá možné tahy.
2. Kliknutí na jinou vlastní figurku změní výběr.
3. Kliknutí znovu na tutéž figurku výběr zruší.
4. Kliknutí na prázdné pole nebo soupeřovu figurku při existujícím výběru vytvoří `Tah`.
5. `hra.proved_tah(tah)` prověří a provede tah. Vrátí `True`, nebo `False`.
6. Platný tah zruší výběr. Po neplatném tahu zůstává figurka vybraná a hráč může zkusit jiný cíl.
7. `obnov_obrazovku()` znovu zobrazí desku, hráče na tahu, historii a questy.

Pravidla patří do modelu. Controller nikdy sám nepřesouvá figurky v seznamu `deska`.
Proto se vždy provede i kontrola šachu, zápis historie a střídání hráčů.

## 6. Čas a zavírání

`after(500, self.obnov_cas)` naplánuje další aktualizaci času za půl sekundy.
Je to lepší než nekonečný cyklus nebo `sleep`, které by mohly blokovat klikání.
Po zavření okna se naplánovaná aktualizace zruší pomocí `after_cancel`.

Uložení používá původní model: TXT s historií a JSON s přehledem.
Křížek okna je připojen přes `protocol("WM_DELETE_WINDOW", self.zavri)`.
Pokud ukládání selže, controller zobrazí chybu a okno nechá otevřené.
Úspěšné zavření zastaví čas, uloží historii a zavolá `destroy()`.

## Co se změnilo

- Nové `view/hra_view.py`, `controller/hra_controller.py` a `gui.py`.
- Pomocné `spustit.pyw` pro dvojklik na Windows s nastaveným přiřazením Pythonu.
- `main.py` běžně spouští okno, textový režim je pod `--terminal`.
- Aktualizovaný návod a `model/README.txt`.
- Nový `test_controller.py`: osm testů. Společně s původními je 21 testů.
- Stávající herní pravidla a ostatní modelové soubory se nemění.

## Co si před nahráním vyzkoušet

- Otevři `python main.py`. Jsou vidět obě barvy a celá deska?
- Klikni na e2: zvýrazní se e2 a nabídnou se e3 a e4?
- Klikni na e4: přesune se pěšák a je na tahu černý?
- Zkus neplatný tah, výběr soupeřovy figurky a zrušení výběru.
- Zahraj `e2–e4`, `d7–d5`, `e4–d5`: zmizí černý pěšák a bílý má 40 bodů?
- Ulož historii a zkontroluj TXT a JSON ve složce `ulozene_hry`.
- Projdi komentáře v nových souborech a zkus vlastními slovy popsat jeden tah.

Omezení šachových pravidel z minulé verze zůstávají (bez rošády a braní mimochodem,
proměna vždy na dámu). Okno nemá přetahování figurek, tlačítko zpět ani online hru.
