"""Testy propojení kliknutí s modelem. Nespouštějí viditelné okno."""
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from model.main import nova_hra
from controller.hra_controller import HraController


class TestController(unittest.TestCase):
    def setUp(self):
        self.slozka = tempfile.TemporaryDirectory()
        self.hra = nova_hra()
        self.view = Mock()
        self.view.okraj = 24
        self.view.velikost_pole = 60
        self.view.okno.after.return_value = "casova-uloha"
        self.controller = HraController(self.hra, self.view, self.slozka.name)

    def tearDown(self):
        self.hra.casovac.zastav()
        self.slozka.cleanup()

    def klik(self, x, y):
        event = SimpleNamespace(x=24 + x * 60 + 30, y=24 + (7 - y) * 60 + 30)
        self.controller.klik_na_desku(event)

    def test_vyber_a_tah_pres_pixely(self):
        self.klik(4, 1)
        self.assertEqual(self.controller.vybrane, (4, 1))
        self.assertEqual(self.controller.mozne_cile, [(4, 2), (4, 3)])
        self.klik(4, 3)
        self.assertIsNone(self.hra.plocha.vrat_figuru((4, 1)))
        self.assertEqual(self.hra.plocha.vrat_figuru((4, 3)).barva, "bila")
        self.assertEqual(self.hra.aktivni_barva, "cerna")
        self.assertIsNone(self.controller.vybrane)
        self.assertEqual(len(self.hra.logger.tahy), 1)
        self.assertEqual(self.hra.hraci[0].skore, 10)

    def test_neplatny_tah_nemeni_hrace(self):
        self.klik(4, 1)
        self.klik(4, 4)
        self.assertEqual(self.hra.aktivni_barva, "bila")
        self.assertEqual(self.controller.vybrane, (4, 1))
        self.assertEqual(self.hra.logger.tahy, [])

    def test_vyber_soupere_prazdna_a_zruseni(self):
        self.klik(4, 6)
        self.klik(4, 4)
        self.assertIsNone(self.controller.vybrane)
        self.klik(4, 1)
        self.klik(3, 1)
        self.assertEqual(self.controller.vybrane, (3, 1))
        self.klik(3, 1)
        self.assertIsNone(self.controller.vybrane)
        self.assertEqual(self.controller.mozne_cile, [])

    def test_okraje_canvasu_a_prevod_rohu(self):
        with patch.object(self.controller, "klik_na_pole") as pole:
            for x, y in [(23, 24), (24, 23), (504, 24), (24, 504), (-1, -1)]:
                self.controller.klik_na_desku(SimpleNamespace(x=x, y=y))
            pole.assert_not_called()
            self.controller.klik_na_desku(SimpleNamespace(x=24, y=24))
            pole.assert_called_with((0, 7))
            self.controller.klik_na_desku(SimpleNamespace(x=503, y=503))
            pole.assert_called_with((7, 0))

    def test_brani_a_quest(self):
        for x, y in [(4, 1), (4, 3), (3, 6), (3, 4), (4, 3), (3, 4)]:
            self.klik(x, y)
        self.assertEqual(len(self.hra.plocha.sebrane_figurky), 1)
        self.assertEqual(self.hra.hraci[0].skore, 40)
        self.assertIn("e4-d5", self.hra.logger.zaznamy[-1])
        self.view.zobraz_historii.assert_called_with(self.hra.logger.zaznamy)

    def test_konec_partie_neprijme_dalsi_tah(self):
        for x, y in [(5, 1), (5, 2), (4, 6), (4, 4), (6, 1), (6, 3), (3, 7), (7, 3)]:
            self.klik(x, y)
        self.assertEqual(self.hra.stav, "mat")
        self.view.zobraz_stav.assert_called_with("MAT – vyhrál černý")
        self.klik(0, 1)
        self.klik(0, 2)
        self.assertEqual(len(self.hra.logger.tahy), 4)

    def test_ulozeni_a_zavreni(self):
        from pathlib import Path
        self.klik(4, 1)
        self.klik(4, 3)
        self.assertTrue(self.controller.uloz())
        self.controller.zavri()
        self.assertEqual(len(list(Path(self.slozka.name).glob("*.txt"))), 2)
        self.assertIsNone(self.hra.casovac.aktivni_barva)
        self.view.okno.after_cancel.assert_called_once_with("casova-uloha")
        self.view.okno.destroy.assert_called_once()

    def test_chyba_ulozeni_nezavre_okno(self):
        with patch.object(self.hra, "uloz_hru", side_effect=OSError("Test chyby")):
            self.controller.zavri()
        self.view.okno.destroy.assert_not_called()
        self.assertEqual(self.hra.casovac.aktivni_barva, "bila")
        self.assertIn("Test chyby", self.view.zobraz_zpravu.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
