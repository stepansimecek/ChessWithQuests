class Quest:
    def __init__(self, nazev, popis, odmena):
        self.nazev = nazev
        self.popis = popis
        self.odmena = odmena
        self.splneno = False

    def spln(self):
        # Opakované splnění už další body nepřidá.
        if self.splneno:
            return 0
        self.splneno = True
        return self.odmena
