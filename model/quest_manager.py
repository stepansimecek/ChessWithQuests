from model.quest import Quest


class QuestManager:
    def __init__(self):
        self.questy = {}
        for barva in ["bila", "cerna"]:
            self.questy[barva] = [
                Quest("První tah", "Proveď jeden platný tah.", 10),
                Quest("První úlovek", "Seber soupeřovu figurku.", 30),
                Quest("Výprava koně", "Dostaň koně do soupeřovy poloviny.", 20),
            ]

    def zkontroluj(self, hrac, tah, figura, sebrana):
        rada = tah.cil[1]
        cizi_polovina = rada >= 4 if hrac.barva == "bila" else rada <= 3
        podminky = [True, sebrana is not None, figura.nazev == "kun" and cizi_polovina]
        nove = []
        for quest, splneno in zip(self.questy[hrac.barva], podminky):
            if splneno and not quest.splneno:
                hrac.skore += quest.spln()
                if quest.nazev not in hrac.uzivatel.splnene_questy:
                    hrac.uzivatel.splnene_questy.append(quest.nazev)
                nove.append(quest.nazev)
        return nove
