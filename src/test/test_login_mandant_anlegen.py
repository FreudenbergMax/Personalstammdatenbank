import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNeuerMandant(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

    def test_erster_mandant_angelegt(self):
        """
        Test prueft ab, ob ein neuer Mandant angelegt wird, sofern alle Bedingungen erfuellt sind.
        """
        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                            'Normalverbraucher', 'adminpw', 'adminpw')
        admin = login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        nutzer = login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        nutzer.passwort_aendern('neues passwort', 'neues passwort')

        ausgabe = nutzer.abfrage_ausfuehren("SELECT * FROM mandanten WHERE firma = 'Testfirma'")

        self.assertEqual(str(ausgabe), "[(1, 'Testfirma', 'mandantenpw')]")

    def test_weiterer_mandant_mit_gleichem_Namen_Exception(self):
        """
        Test prueft ab, ob bei der Neuanlage eines Mandanten die Exception der Stored Procedure 'mandant_anlegen'
        geworfen wird, wenn der Name des Mandanten bereits existiert.
        """
        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                            'Normalverbraucher', 'adminpw', 'adminpw')

        with self.assertRaises(Exception) as context:
            login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                                'Normalverbraucher', 'adminpw', 'adminpw')

        erwartete_fehlermeldung = "FEHLER:  Dieser Mandant ist bereits angelegt!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_leerer_name_exception(self):
        """
        Test prueft, ob die Raise-Funktion aufgerufen wird, wenn bei der Anlage eines neuen Mandanten
        kein Name bzw. ein leerer String vorhanden ist
        """
        login = Login(self.testschema)

        with self.assertRaises(ValueError) as context:
            login.registriere_mandant_und_admin('', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                                'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), 'Der Name des Mandanten muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_name_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn versucht wird, einen Mandantennamen zu
        waehlen, der laenger als 128 Zeichen lang ist.
        """
        name_129_zeichen = "a" * 129

        login = Login(self.testschema)

        with self.assertRaises(ValueError) as context:
            login.registriere_mandant_und_admin(name_129_zeichen, 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                                'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), "Der Name des Mandanten darf hoechstens 128 Zeichen lang sein."
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 129 Zeichen!")

    def test_falsches_schema_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergebene Schema-Bezeichnung nicht 'public'
        oder 'temp_test_schema' lautet
        """
        falsches_schema = 'hallo_welt_schema'

        with self.assertRaises(ValueError) as context:
            login = Login(falsches_schema)

        self.assertEqual(str(context.exception), "Diese Bezeichnung fuer ein Schema ist nicht erlaubt!")

    def test_zu_langes_passwort_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn versucht wird, ein Passwort zu
        waehlen, das laenger als 128 Zeichen lang ist.
        """
        pw_129_zeichen = "a" * 129

        login = Login(self.testschema)

        with self.assertRaises(ValueError) as context:
            login.registriere_mandant_und_admin('Testfirma', pw_129_zeichen, pw_129_zeichen, 'M100000', 'Otto',
                                                'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), "Passwort darf hoechstens 128 Zeichen haben!")

    def test_wiederholtes_passwort_falsch_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn bei der zweiten Passworteingabe ein anderer String
        enthalten ist, als in der ersten Eingabe.
        """
        erste_pw_eingabe = 'mandantenpasswort'
        zweite_pw_eingabe = 'mpw'

        login = Login(self.testschema)

        with self.assertRaises(ValueError) as context:
            login.registriere_mandant_und_admin('Testfirma', erste_pw_eingabe, zweite_pw_eingabe, 'M100000', 'Otto',
                                                'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), "Passwoerter stimmen nicht ueberein!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' mit allen Daten entfernt.
        """
        test_tear_down()
