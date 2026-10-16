class UserManager:
    def __init__(self):
        self.uzivatele = []

    def pridej(self, uzivatel):
        if self.najdi(uzivatel.jmeno) is not None:
            return False
        self.uzivatele.append(uzivatel)
        return True

    def najdi(self, jmeno):
        for uzivatel in self.uzivatele:
            if uzivatel.jmeno == jmeno:
                return uzivatel
        return None
