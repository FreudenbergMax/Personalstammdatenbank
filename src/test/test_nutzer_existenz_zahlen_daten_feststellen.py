import decimal
import unittest

from src.main.test_SetUp import test_set_up
from src.main.Mandant import Mandant


class TestExistenzZahlenDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        """
        self.conn, self.cursor = test_set_up()
        self.testfirma = Mandant('Testfirma', self.conn)
        self.testfirma.nutzer_anlegen('M10001', 'Max', 'Mustermann', self.conn)

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
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()