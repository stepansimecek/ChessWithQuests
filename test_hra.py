import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from model.main import nova_hra
from model.herni_plocha import HerniPlocha
from model.figurky import Kral, Dama, Vez, Strelec, Kun, Pesak
from model.revizor_tahu import RevizorTahu
from model.tah import Tah, text_na_pozici
from model.game_timer import GameTimer
from model.models import Hrac, Uzivatel
from model.quest_manager import QuestManager
from model.user_manager import UserManager


def tah(odkud, kam):
    return Tah(text_na_pozici(odkud), text_na_pozici(kam))


class TestPravidel(unittest.TestCase):
    def setUp(self):
        self.plocha = HerniPlocha()
        self.revizor = RevizorTahu(self.plocha)

    def prazdna_deska(self):
        self.plocha.deska = [[None for _ in range(8)] for _ in range(8)]
        self.plocha.deska[0][0] = Kral("bila")
        self.plocha.deska[7][7] = Kral("cerna")

    def poloz(self, pole, figura):
        x, y = text_na_pozici(pole)
        self.plocha.deska[y][x] = figura

    def test_start_a_obnova(self):
        self.assertEqual(sum(f is not None for r in self.plocha.deska for f in r), 32)
        self.assertEqual(len(self.revizor.mozne_tahy((1, 0), "bila")), 2)
        self.plocha.posun_figuru(tah("e2", "e4"))
        self.plocha.nastav_start()
        self.assertIsNone(self.plocha.vrat_figuru((4, 3)))
        self.assertEqual(len(self.plocha.sebrane_figurky), 0)

    def test_okraje_barva_a_vlastni_figura(self):
        for t in [Tah((-1, 0), (0, 0)), Tah((8, 0), (0, 0)), Tah((0, 1), (0, 8)),
                  tah("e7", "e5"), tah("e2", "e2"), tah("b1", "d2"), tah("a1", "a3")]:
            with self.subTest(t=t):
                self.assertFalse(self.revizor.over_tah(t, "bila"))
        self.assertIsNone(self.plocha.vrat_figuru((-1, 0)))

    def test_pesaci(self):
        self.assertTrue(self.revizor.over_tah(tah("e2", "e4"), "bila"))
        self.assertTrue(self.revizor.over_tah(tah("e7", "e5"), "cerna"))
        self.assertFalse(self.revizor.over_tah(tah("e2", "d3"), "bila"))
        self.assertFalse(self.revizor.over_tah(tah("e2", "e1"), "bila"))
        self.poloz("e3", Pesak("cerna"))
        self.assertFalse(self.revizor.over_tah(tah("e2", "e4"), "bila"))
        self.assertFalse(self.revizor.over_tah(tah("e2", "e3"), "bila"))
        self.poloz("d3", Pesak("cerna"))
        self.assertTrue(self.revizor.over_tah(tah("e2", "d3"), "bila"))

    def test_pohyb_ostatnich_figurek(self):
        for cls, dobre, spatne in [(Vez, "d6", "e5"), (Strelec, "f6", "d6"),
                                  (Dama, "f6", "e6"), (Kun, "e6", "e5"), (Kral, "e5", "f6")]:
            with self.subTest(figurka=cls.__name__):
                self.prazdna_deska()
                self.poloz("d4", cls("bila"))
                self.assertTrue(self.revizor.spravny_pohyb(tah("d4", dobre)))
                self.assertFalse(self.revizor.spravny_pohyb(tah("d4", spatne)))
        self.prazdna_deska()
        self.poloz("d4", Strelec("bila"))
        self.poloz("e5", Pesak("cerna"))
        self.assertFalse(self.revizor.spravny_pohyb(tah("d4", "f6")))
        self.assertTrue(self.revizor.over_tah(tah("d4", "e5"), "bila"))

    def test_odkryti_krale_a_obnova_simulace(self):
        self.prazdna_deska()
        self.poloz("a8", Vez("cerna"))
        self.poloz("a2", Vez("bila"))
        self.poloz("b2", Kun("cerna"))
        puvodni = [r[:] for r in self.plocha.deska]
        self.assertFalse(self.revizor.over_tah(tah("a2", "b2"), "bila"))
        self.assertEqual(self.plocha.deska, puvodni)
        self.assertEqual(self.plocha.sebrane_figurky, [])
        self.assertTrue(self.revizor.over_tah(tah("a2", "a8"), "bila"))
        self.assertEqual(self.plocha.deska, puvodni)

    def test_kralove_a_utok_pesaka(self):
        self.prazdna_deska()
        self.poloz("a1", None)
        self.poloz("e4", Kral("bila"))
        self.poloz("e6", Kral("cerna"))
        self.assertFalse(self.revizor.over_tah(tah("e4", "e5"), "bila"))
        self.poloz("e6", None)
        self.poloz("d5", Pesak("cerna"))
        self.assertTrue(self.revizor.check_sach("bila"))
        self.poloz("d5", None)
        self.poloz("e5", Pesak("cerna"))
        self.assertFalse(self.revizor.check_sach("bila"))

    def test_promena_a_zakaz_sebrani_krale(self):
        self.prazdna_deska()
        self.poloz("b7", Pesak("bila"))
        self.assertTrue(self.revizor.over_tah(tah("b7", "b8"), "bila"))
        self.plocha.posun_figuru(tah("b7", "b8"))
        self.assertEqual(self.plocha.vrat_figuru((1, 7)).nazev, "dama")
        self.assertFalse(self.revizor.over_tah(tah("b8", "h8"), "bila"))

    def test_mat_a_pat(self):
        self.prazdna_deska()
        self.poloz("a1", None)
        self.poloz("f6", Kral("bila"))
        self.poloz("g7", Dama("bila"))
        self.assertTrue(self.revizor.check_mat("cerna"))
        self.assertFalse(self.revizor.check_pat("cerna"))
        self.poloz("g7", None)
        self.poloz("g6", Dama("bila"))
        self.assertTrue(self.revizor.check_pat("cerna"))
        self.assertFalse(self.revizor.check_mat("cerna"))


class TestPropojeni(unittest.TestCase):
    def test_prubeh_questy_historie_export(self):
        hra = nova_hra()
        self.assertFalse(hra.proved_tah(tah("e7", "e5")))
        self.assertEqual(hra.aktivni_barva, "bila")
        self.assertEqual(hra.logger.tahy, [])
        for a, b in [("e2", "e4"), ("d7", "d5"), ("e4", "d5"), ("g8", "f6"), ("d5", "d6")]:
            self.assertTrue(hra.proved_tah(tah(a, b)))
        hra.casovac.zastav()
        self.assertEqual(hra.hraci[0].skore, 40)
        self.assertEqual(hra.hraci[1].skore, 10)
        self.assertEqual(len(hra.logger.tahy), 5)
        self.assertEqual(len(hra.plocha.sebrane_figurky), 1)
        with tempfile.TemporaryDirectory() as slozka:
            prvni = hra.uloz_hru(slozka)
            druhy = hra.uloz_hru(slozka)
            self.assertNotEqual(prvni, druhy)
            self.assertIn("e4-d5", prvni.read_text(encoding="utf-8"))
            data = json.loads(prvni.with_suffix(".json").read_text(encoding="utf-8"))
            self.assertEqual(data["pocet_tahu"], 5)
            self.assertEqual(data["hraci"][0]["skore"], 40)
            self.assertNotIn("email", data["hraci"][0])

    def test_mat_zastavi_hru(self):
        hra = nova_hra()
        for a, b in [("f2", "f3"), ("e7", "e5"), ("g2", "g4"), ("d8", "h4")]:
            self.assertTrue(hra.proved_tah(tah(a, b)))
        self.assertEqual(hra.stav, "mat")
        self.assertIsNone(hra.casovac.aktivni_barva)
        self.assertFalse(hra.proved_tah(tah("a2", "a3")))
        self.assertEqual(len(hra.logger.tahy), 4)

    def test_quest_kone_pro_obe_barvy(self):
        qm = QuestManager()
        for barva, odkud, kam in [("bila", "c3", "d5"), ("cerna", "c6", "d4")]:
            hrac = Hrac(Uzivatel(barva, "", 1000), barva)
            qm.zkontroluj(hrac, tah(odkud, kam), Kun(barva), None)
            self.assertEqual(hrac.skore, 30)
            qm.zkontroluj(hrac, tah(odkud, kam), Kun(barva), None)
            self.assertEqual(hrac.skore, 30)

    def test_casovac_bez_skutecneho_cekani(self):
        with patch("model.game_timer.time.monotonic") as hodiny:
            hodiny.return_value = 100
            cas = GameTimer()
            cas.spust("bila")
            hodiny.return_value = 105
            self.assertEqual(cas.vrat_cas("bila"), 5)
            cas.spust("cerna")
            hodiny.return_value = 108
            cas.zastav()
            hodiny.return_value = 200
            self.assertEqual(cas.vrat_cas("bila"), 5)
            self.assertEqual(cas.vrat_cas("cerna"), 3)
            cas.nuluj_cas()
            self.assertEqual(cas.vrat_cas("bila"), 0)

    def test_uzivatele_a_vstup(self):
        manager = UserManager()
        u = Uzivatel("Test", "", 1000)
        self.assertTrue(manager.pridej(u))
        self.assertFalse(manager.pridej(u))
        self.assertIs(manager.najdi("Test"), u)
        self.assertIsNone(manager.najdi("Nikdo"))
        self.assertEqual(text_na_pozici(" E2 "), (4, 1))
        for neplatne in ["", "a0", "i2", "a22", "22"]:
            with self.assertRaises(ValueError):
                text_na_pozici(neplatne)


if __name__ == "__main__":
    unittest.main()
