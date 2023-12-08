import unittest
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down
from src.main.Mandant import Mandant


class TestExistenzBooleanDatenFeststellen(unittest.TestCase):

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
        Test prüft, ob die Methode '_existenz_boolean_daten_feststellen' ein 'None' zurückgibt, wenn die
        übergegebene Variable ein optionaler leerer String ist.
        """
        boolean = ''
        boolean = self.testfirma.get_nutzer('M10001'). \
            _existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, None)

    def test_pflicht_zahlenwert_ist_leer(self):
        """
        Test prüft, ob die Methode '_existenz_boolean_daten_feststellen' ein ValueError-Exception wirft, wenn die
        übergegebene Variable ein leerer Pflicht-String ist.
        """
        boolean = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            boolean = self.testfirma.get_nutzer('M10001'). \
                _existenz_boolean_daten_feststellen(boolean, 'boolean', True)

        self.assertEqual(str(context.exception), "'boolean' ist nicht vorhanden.")

    def test_nein_zu_false(self):
        """
        Test prüft, ob die Methode '_existenz_boolean_daten_feststellen' 'False' zurückgibt, wenn die
        übergegebene Variable ein String 'nein' ist.
        """
        boolean = 'nein'

        boolean = self.testfirma.get_nutzer('M10001'). \
            _existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, False)

    def test_NEIN_zu_false(self):
        """
        Test prüft, ob die Methode '_existenz_boolean_daten_feststellen' 'False' zurückgibt, wenn die
        übergegebene Variable ein String 'NEIN' mit Grossbuchstaben ist.
        """
        boolean = 'NEIN'

        boolean = self.testfirma.get_nutzer('M10001'). \
            _existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, False)

    def test_ja_zu_true(self):
        """
        Test prüft, ob die Methode '_existenz_boolean_daten_feststellen' 'True' zurückgibt, wenn die
        übergegebene Variable ein String 'ja' ist.
        """
        boolean = 'ja'

        boolean = self.testfirma.get_nutzer('M10001'). \
            _existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, True)

    def test_JA_zu_true(self):
        """
        Test prüft, ob die Methode '_existenz_boolean_daten_feststellen' 'True' zurückgibt, wenn die
        übergegebene Variable ein String 'JA' mit Grossbuchstaben ist.
        """
        boolean = 'JA'

        boolean = self.testfirma.get_nutzer('M10001'). \
            _existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, True)

    def test_inkompatibler_wert(self):
        """
        Test prüft, ob eine TypeError-Exeption geworfen wird, weil der Methode '_existenz_boolean_daten_feststellen'
        ein String übergeben wird, der nicht in einen Wahrheitswert konvertiert werden kann
        """
        boolean = 'hallo welt'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(TypeError) as context:
            boolean = self.testfirma.get_nutzer('M10001'). \
                _existenz_boolean_daten_feststellen(boolean, 'boolean', True)

        self.assertEqual(str(context.exception), "Der übergebene Wert 'hallo welt' konnte nicht verarbeitet werden. "
                                                 "Bitte geben Sie ausschließlich 'ja' oder 'nein' ein.")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)