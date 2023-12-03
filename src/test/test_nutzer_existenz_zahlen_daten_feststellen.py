import decimal
import unittest
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down
from src.main.Mandant import Mandant


class TestExistenzZahlenDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M10001', 'Max', 'Mustermann', self.testschema)

    def test_optionaler_zahlenwert_ist_leer(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' ein 'None' zurückgibt, wenn die
        übergegebene Variable ein optionaler leerer String ist.
        """
        zahlenwert = ''
        zahlenwert = self.testfirma.get_nutzer('M10001'). \
            _existenz_zahlen_daten_feststellen(zahlenwert, 'Zahlenwert', False)

        self.assertEqual(zahlenwert, None)

    def test_pflicht_zahlenwert_ist_leer(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' ein ValueError-Exception wirft, wenn die
        übergegebene Variable ein leerer Pflicht-String ist.
        """
        zahlenwert = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            zahlenwert = self.testfirma.get_nutzer('M10001'). \
                _existenz_zahlen_daten_feststellen(zahlenwert, 'Zahlenwert', True)

        self.assertEqual(str(context.exception), "'Zahlenwert' ist nicht vorhanden.")

    def test_str_konvertierung_scheitert(self):
        """
        Test prüft, ob eine TypeError-Exeption geworfen wird, weil der Methode '_existenz_zahlen_daten_feststellen'
        ein String übergeben wird, der nicht in eine Dezimal-Zahl konvertiert werden kann
        """
        zahlenwert = 'hallo welt'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(TypeError) as context:
            zahlenwert = self.testfirma.get_nutzer('M10001'). \
                _existenz_zahlen_daten_feststellen(zahlenwert, 'Zahlenwert', True)

        self.assertEqual(str(context.exception), "Der übergebene Wert 'hallo welt' konnte nicht in eine Gleitkommazahl "
                                                 "konvertiert werden!")

    def test_ganzzahl_zu_dezimalzahl(self):
        """
        Test prüft, ob die Methode '_existenz_zahlen_daten_feststellen' eine Dezimalzahl zurückgibt, wenn die
        übergegebene Variable eine Ganzzahl ist.
        """
        zahlenwert = 35

        zahlenwert = self.testfirma.get_nutzer('M10001'). \
            _existenz_zahlen_daten_feststellen(zahlenwert, 'Zahlenwert', False)

        self.assertEqual(type(zahlenwert), decimal.Decimal)

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
