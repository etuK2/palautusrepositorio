import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote
from kirjanpito import Kirjanpito

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()
        self.kirjanpito = Kirjanpito()
        self.kirjanpito_mock = Mock()
        self.varasto = Varasto(self.kirjanpito_mock)
        self.viitegeneraattori = Viitegeneraattori()

        self.tuote1 = Tuote(1, "Maito", 5)
        self.tuote2 = Tuote(2, "Leipä", 3)
        self.tuote3 = Tuote(1, "Maito", 5)

        self.varasto._saldot = {self.tuote1: 10, self.tuote2: 5}

        # Palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 5
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            if tuote_id == 3:
                return Tuote(3, "juusto", 3)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)
    
    def test_kaksi_eri_tuotetta_varastossa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 8)
    
    def test_kaksi_samaa_tuotetta_varastossa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 10)

    def test_tuote_varastossa_ja_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)


    def test_aloita_asiointi_nollaa_edellisen_ostoksen(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "67890")

        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "67890", ANY, 5)

    def test_kauppa_pyytää_uuden_viitenumeron_jokaiselle_maksulle(self):
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "67890")
        self.pankki_mock.tilisiirto.assert_called_with("matti", 43, "67890", ANY, 5)

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_tuotteen_voi_poistaa_ostoskorista(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(2)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_tapahtuman_lisaaminen_kirjanpitoon(self):
        tapahtuma = "Ostettiin maitoa"
        self.kirjanpito.lisaa_tapahtuma(tapahtuma)

        self.assertIn(tapahtuma, self.kirjanpito.tapahtumat)
        self.assertEqual(len(self.kirjanpito.tapahtumat), 1)

    def test_eq(self):
        self.assertEqual(self.tuote1, self.tuote3)
        self.assertNotEqual(self.tuote1, self.tuote2)

    def test_str(self):
        self.assertEqual(str(self.tuote1), "Maito")
        self.assertEqual(str(self.tuote2), "Leipä")

    def test_hae_tuote(self):
        result = self.varasto.hae_tuote(1)
        self.assertEqual(result, self.tuote1)

        result = self.varasto.hae_tuote(99)
        self.assertIsNone(result)

    def test_saldo(self):
        saldo = self.varasto.saldo(1)
        self.assertEqual(saldo, 10)

        with self.assertRaises(KeyError):
            self.varasto.saldo(99)

    def test_ota_varastosta(self):
        self.varasto.ota_varastosta(self.tuote1)
        self.assertEqual(self.varasto.saldo(1), 9)
        self.kirjanpito_mock.lisaa_tapahtuma.assert_called_with(
            "otettiin varastosta Maito"
        )

    def test_palauta_varastoon(self):
        self.varasto.palauta_varastoon(self.tuote1)
        self.assertEqual(self.varasto.saldo(1), 11)  
        self.kirjanpito_mock.lisaa_tapahtuma.assert_called_with(
            "palautettiin varastoon Maito"
        )

    def test_uusi_increments_seuraava(self):
        self.assertEqual(self.viitegeneraattori._seuraava, 1)
        
        self.viitegeneraattori.uusi()
        self.assertEqual(self.viitegeneraattori._seuraava, 2)
        
