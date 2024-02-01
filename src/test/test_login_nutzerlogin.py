import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestLoginNutzerlogin(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        self.login = Login(self.testschema)
        self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                                 'Normalverbraucher', 'adminpw', 'adminpw')
        self.admin = self.login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

    def test_erfolgreicher_nutzerlogin(self):
        """
        Test prueft, ob ein Login erfolgreich durchgefuehrt wird, sofern die richtigen Werte beim Nutzerlogin eingegeben
        werden
        """
        nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        self.assertIsNotNone(nutzer)

    def test_falsches_nutzerpasswort(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Nutzer existiert, aber das eingebene
        Nutzerpasswort falsch ist.
        """
        with self.assertRaises(ValueError) as context:
            nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        self.assertEqual(str(context.exception), "Eingegebene Passwoerter sind falsch!")

    def test_falsches_mandantenpasswort(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Nutzer existiert, aber das eingebene
        Mandantenpasswort falsch ist.
        """
        with self.assertRaises(ValueError) as context:
            nutzer = self.login.login_nutzer('Testfirma', 'falsches_passwort', 'M100001', 'nutzerpw')

        self.assertEqual(str(context.exception), "Eingegebene Passwoerter sind falsch!")

    def test_nutzer_nicht_vorhanden(self):
        """
        Test prueft ab, ob eine Fehlermeldung ausgegeben wird, wenn eine falsche Personalnummer eingegeben wird.
        """
        with self.assertRaises(ValueError) as context:
            admin = self.login.login_admin('Testfirma', 'mandantenpw', 'falsche_personalnummer', 'nutzerpw')

        self.assertEqual(str(context.exception), "Admin mit Personalnummer 'falsche_personalnummer' nicht vorhanden!")

    def test_nutzer_sperre(self):
        """
        Test prueft, ob ein Nutzer gesperrt ist, wenn er das Passwort dreimal hintereinander falsche eingibt
        """
        with self.assertRaises(ValueError) as context:
            nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        with self.assertRaises(ValueError) as context:
            nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        with self.assertRaises(ValueError) as context:
            nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        with self.assertRaises(Exception) as context:
            nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        erwartete_fehlermeldung = "FEHLER:  Nutzer ist gesperrt!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' mit allen Daten entfernt.
        """
        test_tear_down()
