from dataclasses import dataclass


@dataclass
class Uzivatel:
    jmeno: str
    email: str
    elo: int


@dataclass
class Hrac:
    uzivatel: Uzivatel
    barva: str  # "bila" nebo "cerna"

    def get_elo_rating(self) -> int:
        return self.uzivatel.elo
