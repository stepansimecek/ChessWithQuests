from dataclasses import dataclass, field


@dataclass
class Uzivatel:
    jmeno: str
    email: str
    elo: int
    splnene_questy: list[str] = field(default_factory=list)


@dataclass
class Hrac:
    uzivatel: Uzivatel
    barva: str  # "bila" nebo "cerna"

    skore: int = 0

    def get_elo_rating(self) -> int:
        return self.uzivatel.elo
