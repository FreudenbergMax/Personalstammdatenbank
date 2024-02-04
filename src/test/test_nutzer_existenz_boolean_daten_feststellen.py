import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestExistenzBooleanDatenFeststellen(unittest.TestCase):

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
        Test prueft, ob die Methode '_existenz_boolean_daten_feststellen' ein 'None' zurueckgibt, wenn die
        uebergegebene Variable ein optionaler leerer String ist.
        """
        boolean = ''
        boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, None)

    def test_pflicht_zahlenwert_ist_leer(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable leer ist.
        """
        boolean = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', True)

        self.assertEqual(str(context.exception), "'boolean' ist nicht vorhanden.")

    def test_nein_zu_false(self):
        """
        Test prueft, ein 'nein'-String zu einem boolean mit Wert 'False' umgewandelt wird.
        """
        boolean = 'nein'

        boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, False)

    def test_NEIN_zu_false(self):
        """
        Test prueft, ob die Methode '_existenz_boolean_daten_feststellen' 'False' zurueckgibt, wenn die
        uebergegebene Variable ein String 'NEIN' mit Grossbuchstaben ist.
        """
        boolean = 'NEIN'

        boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, False)

    def test_ja_zu_true(self):
        """
        Test prueft, ob die Methode '_existenz_boolean_daten_feststellen' 'True' zurueckgibt, wenn die
        uebergegebene Variable ein String 'ja' ist.
        """
        boolean = 'ja'

        boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, True)

    def test_JA_zu_true(self):
        """
        Test prueft, ob die Methode '_existenz_boolean_daten_feststellen' 'True' zurueckgibt, wenn die
        uebergegebene Variable ein String 'JA' mit Grossbuchstaben ist.
        """
        boolean = 'JA'

        boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', False)

        self.assertEqual(boolean, True)

    def test_inkompatibler_wert(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, weil der Methode '_existenz_boolean_daten_feststellen'
        ein String uebergeben wird, der nicht in einen Wahrheitswert konvertiert werden kann
        """
        boolean = 'hallo welt'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(TypeError) as context:
            boolean = self.nutzer._existenz_boolean_daten_feststellen(boolean, 'boolean', True)

        self.assertEqual(str(context.exception), "Der uebergebene Wert 'hallo welt' konnte nicht verarbeitet werden. "
                                                 "Bitte geben Sie ausschliesslich 'ja' oder 'nein' ein.")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
