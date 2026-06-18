from tah import Tah


class GameLogger:
    def __init__(self):
        self.tahy: list[Tah] = []

    def uloz_tah(self, tah: Tah) -> None:
        self.tahy.append(tah)

    def vypis_log(self) -> None:
        print("Historie tahů:")

        for i, tah in enumerate(self.tahy, start=1):
            print(f"{i}. {tah.start} -> {tah.cil}")
