import decimal
import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down
from src.main.Mandant import Mandant


class TestExistenzZahlenDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                            'Normalverbraucher', 'adminpw', 'adminpw')
        self.admin = login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        self.nutzer = login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        self.nutzer.passwort_aendern('neues passwort', 'neues passwort')

    def test_optionaler_zahlenwert_ist_leer(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' ein 'None' zurückgibt, wenn die
        übergegebene Variable ein optionaler leerer String ist.
        """
        zahlenwert = ''
        zahlenwert = self.nutzer._existenz_zahlen_daten_feststellen(zahlenwert, 50, 'Zahlenwert', False)

        self.assertEqual(zahlenwert, None)

    def test_pflicht_zahlenwert_ist_leer(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' ein ValueError-Exception wirft, wenn die
        übergegebene Variable ein leerer Pflicht-String ist.
        """
        zahlenwert = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            zahlenwert = self.nutzer._existenz_zahlen_daten_feststellen(zahlenwert, 50, 'Zahlenwert', True)

        self.assertEqual(str(context.exception), "'Zahlenwert' ist nicht vorhanden.")

    def test_str_konvertierung_scheitert(self):
        """
        Test prüft, ob eine TypeError-Exeption geworfen wird, weil der Methode '_existenz_zahlen_daten_feststellen'
        ein String übergeben wird, der nicht in eine Dezimal-Zahl konvertiert werden kann
        """
        zahlenwert = 'hallo welt'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(TypeError) as context:
            zahlenwert = self.nutzer._existenz_zahlen_daten_feststellen(zahlenwert, 50, 'Zahlenwert', True)

        self.assertEqual(str(context.exception), "Der übergebene Wert 'hallo welt' konnte nicht in eine Gleitkommazahl "
                                                 "konvertiert werden!")

    def test_none_konvertierung_scheitert(self):
        """
        Test prüft, ob eine TypeError-Exeption geworfen wird, weil der Methode '_existenz_zahlen_daten_feststellen'
        ein None übergeben wird, der nicht in eine Dezimal-Zahl konvertiert werden kann
        """
        none = None

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(TypeError) as context:
            none = self.nutzer._existenz_zahlen_daten_feststellen(none, 50, 'None', True)

        self.assertEqual(str(context.exception), "Der übergebene Wert 'None' konnte nicht in eine Gleitkommazahl "
                                                 "konvertiert werden!")

    def test_hoechstbetrag_ueberschritten(self):
        """
        Test prüft, ob eine ValueError-Exeption geworfen wird, weil der Methode '_existenz_zahlen_daten_feststellen'
        ein Wert uebergeben wird, der hoeher ist, als der definierte Hoechstbetrag
        """
        testzahl = 6543.21
        hoechstbetrag = 6000

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            none = self.nutzer._existenz_zahlen_daten_feststellen(testzahl, hoechstbetrag, 'Testzahl', True)

        self.assertEqual(str(context.exception), "'Testzahl' ist mit '6543.21' hoeher als der zulaessige Maximalbetrag "
                                                 "von '6000'!")

    def test_anzahl_kinder_ist_integer(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' die Variable 'Anzahl Kinder' bei einer
        Ganzzahl belaesst, wenn der übergebene Wert bereits ein integer ist
        """
        anzahl_kinder = 3

        anzahl_kinder = self.nutzer._existenz_zahlen_daten_feststellen(anzahl_kinder, 99, 'Anzahl Kinder', False)

        self.assertEqual(type(anzahl_kinder), int)

    def test_jahr_ist_integer(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' die Variable 'beitragsjahr_uv' bei einer
        Ganzzahl belaesst, wenn der übergebene Wert bereits ein integer ist. Dies sit wichtig, wenn für die Unfall-
        versicheurng der BEitragsjahr an die DAtenbank uebergeben werden soll
        """
        beitragsjahr_uv = 2023

        beitragsjahr_uv = self.nutzer._existenz_zahlen_daten_feststellen(beitragsjahr_uv, 9999,
                                                                         'Beitragsjahr Unfallversicherung', False)

        self.assertEqual(type(beitragsjahr_uv), int)

    def test_float_zu_dezimalzahl(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' einen Float-Wert (was bereits eine Dezimalzahl
        ist) in einen Wert vom Datentyp 'decimal.Decimal' (welche für SQL benötigt wird) zurückgibt.
        """
        dezimalzahl = 1.5

        dezimalzahl = self.nutzer._existenz_zahlen_daten_feststellen(dezimalzahl, 50, 'Dezimalzahl', False)

        self.assertEqual(type(dezimalzahl), decimal.Decimal)

    def test_ganzzahl_zu_dezimalzahl(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' eine Dezimalzahl zurückgibt, wenn die
        übergegebene Variable eine Ganzzahl ist.
        """
        zahlenwert = 35

        zahlenwert = self.nutzer._existenz_zahlen_daten_feststellen(zahlenwert, 50, 'Zahlenwert', False)

        self.assertEqual(type(zahlenwert), decimal.Decimal)

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
