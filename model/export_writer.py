import json
from pathlib import Path


class ExportWriter:
    def uloz(self, cesta, text):
        Path(cesta).write_text(text, encoding="utf-8")


class ChessNotationWriter(ExportWriter):
    def export(self, zaznamy):
        # Jednoduchý souřadnicový zápis, nikoliv standardní PGN.
        radky = []
        for i, zaznam in enumerate(zaznamy, start=1):
            radky.append(f"{i}. {zaznam}")
        return "\n".join(radky)


class MetadataWriter(ExportWriter):
    def export(self, hra):
        data = {"stav": hra.stav, "na_tahu": hra.aktivni_barva, "pocet_tahu": len(hra.logger.tahy), "hraci": []}
        for hrac in hra.hraci:
            splnene = []
            for quest in hra.quest_manager.questy[hrac.barva]:
                if quest.splneno:
                    splnene.append(quest.nazev)
            data["hraci"].append({
                "jmeno": hrac.uzivatel.jmeno,
                "barva": hrac.barva,
                "skore": hrac.skore,
                "cas_sekundy": round(hra.casovac.vrat_cas(hrac.barva), 2),
                "questy": splnene,
            })
        return json.dumps(data, ensure_ascii=False, indent=2)
