from datetime import datetime
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

    def test_vorherigen_tag_berechnen(self):
        """
        Test prüft, ob der vorherige Tag eines übergebenen Datums korrekt berechnet wird
        """
        eingabedatum = datetime.strptime("01.01.2024", '%d.%m.%Y').date()
        vorheriger_tag = self.testfirma.get_nutzer('M10001')._vorherigen_tag_berechnen(eingabedatum)

        self.assertEqual(str(vorheriger_tag), "2023-12-31")

    def test_falscher_Datentyp(self):
        """
        Test prüft, ob das uebergebene Datum den richtigen Datentyp hat. Es wird der datetime-Datentyp benoetigt.
        """
        eingabedatum = datetime.strptime("01.01.2024", '%d.%m.%Y').date()
        vorheriger_tag = self.testfirma.get_nutzer('M10001')._vorherigen_tag_berechnen(eingabedatum)

        self.assertEqual(str(vorheriger_tag), "2023-12-31")

        with self.assertRaises(TypeError) as context:
            vorheriger_tag = self.testfirma.get_nutzer('M10001')._vorherigen_tag_berechnen("01.01.2024")

        self.assertEqual(str(context.exception), "'01.01.2024' ist kein datetime-Objekt!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)