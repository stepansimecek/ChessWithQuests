from figurka import Figurka


class Pesak(Figurka):
    def __init__(self, barva: str):
        super().__init__("pesak", barva)


class Kral(Figurka):
    def __init__(self, barva: str):
        super().__init__("kral", barva)
