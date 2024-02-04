import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestLoginAdminlogin(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        self.login = Login(self.testschema)
        self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                                 'Normalverbraucher', 'adminpw', 'adminpw')

    def test_erfolgreicher_adminlogin(self):
        """
        Test prueft, ob ein Login erfolgreich durchgefuehrt wird, sofern die richtigen Werte beim Adminlogin eingegeben
        werden
        """
        admin = self.login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        self.assertIsNotNone(admin)

    def test_falsches_adminpasswort(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Administrator existiert, aber das eingebene
        Adminpasswort falsch ist.
        """
        with self.assertRaises(ValueError) as context:
            admin = self.login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'falsches_passwort')

        self.assertEqual(str(context.exception), "Eingegebene Passwoerter sind falsch!")

    def test_falsches_mandantenpasswort(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Administrator existiert, aber das eingebene
        Mandantenpasswort falsch ist.
        """
        with self.assertRaises(ValueError) as context:
            admin = self.login.login_admin('Testfirma', 'falsches_passwort', 'M100000', 'adminpw')

        self.assertEqual(str(context.exception), "Eingegebene Passwoerter sind falsch!")

    def test_admin_nicht_vorhanden(self):
        """
        Test prueft ab, ob eine Fehlermeldung ausgegeben wird, wenn eine falsche Personalnummer eingegeben wird.
        """
        with self.assertRaises(ValueError) as context:
            admin = self.login.login_admin('Testfirma', 'mandantenpw', 'falsche_personalnummer', 'adminpw')

        self.assertEqual(str(context.exception), "Admin mit Personalnummer 'falsche_personalnummer' nicht vorhanden!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' mit allen Daten entfernt.
        """
        test_tear_down()