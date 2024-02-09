from datetime import datetime
import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestVorherigenTagBerechnen(unittest.TestCase):

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

    def test_vorherigen_tag_berechnen(self):
        """
        Test prueft, ob der vorherige Tag eines uebergebenen Datums korrekt berechnet wird
        """
        eingabedatum = datetime.strptime("01.01.2024", '%d.%m.%Y').date()
        vorheriger_tag = self.nutzer._vorherigen_tag_berechnen(eingabedatum)

        self.assertEqual(str(vorheriger_tag), "2023-12-31")

    def test_falscher_Datentyp(self):
        """
        Test prueft, ob das uebergebene Datum den richtigen Datentyp hat. Es wird der datetime-Datentyp benoetigt.
        """
        eingabedatum = datetime.strptime("01.01.2024", '%d.%m.%Y').date()
        vorheriger_tag = self.nutzer._vorherigen_tag_berechnen(eingabedatum)

        self.assertEqual(str(vorheriger_tag), "2023-12-31")

        with self.assertRaises(TypeError) as context:
            vorheriger_tag = self.nutzer._vorherigen_tag_berechnen("01.01.2024")

        self.assertEqual(str(context.exception), "'01.01.2024' ist kein datetime-Objekt!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
