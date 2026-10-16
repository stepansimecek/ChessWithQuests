from model.figurka import Figurka


class Pesak(Figurka):
    def __init__(self, barva: str):
        super().__init__("pesak", barva)


class Kral(Figurka):
    def __init__(self, barva: str):
        super().__init__("kral", barva)


class Dama(Figurka):
    def __init__(self, barva):
        super().__init__("dama", barva)


class Vez(Figurka):
    def __init__(self, barva):
        super().__init__("vez", barva)


class Strelec(Figurka):
    def __init__(self, barva):
        super().__init__("strelec", barva)


class Kun(Figurka):
    def __init__(self, barva):
        super().__init__("kun", barva)
