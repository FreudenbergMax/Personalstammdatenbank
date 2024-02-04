import unittest
import psycopg2

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNeuerAdministrator(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        self.login = Login(self.testschema)

    def test_administrator_erfolgreich_angelegt(self):
        """
        Test prueft ab, ob ein neuer Administrator angelegt wird, sofern alle Bedingungen erfuellt sind.
        """
        self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                                 'Normalverbraucher', 'adminpw', 'adminpw')

        # Pruefung, ob Nutzer in Datenbank angelegt ist
        conn = psycopg2.connect(
            host="localhost",
            database="Personalstammdatenbank",
            user="postgres",
            password="@Postgres123",
            port=5432
        )

        nutzer_query = f"set search_path to {self.testschema}; SELECT * FROM administratoren"

        cur = conn.cursor()
        cur.execute(nutzer_query)
        ergebnis = cur.fetchall()

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        self.assertEqual(str(ergebnis), "[(1, 1, 'M100000', 'Otto', 'Normalverbraucher', 'adminpw', 0)]")

    def test_leere_personalnummer_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die Personalnummer des Administrators ein leerer String
        ist.
        """
        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', '', 'Otto',
                                                     'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), "Die Personalnummer des Nutzers muss aus mindestens einem Zeichen "
                                                 "bestehen.")

    def test_zu_lange_personalnummer_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn versucht wird, einen Vornamen fuer einen Administrator
        zu waehlen, der laenger als 64 Zeichen lang ist. Es wird auch gleichzeitig getestet, ob Personalnummern, welche
        nur aus Zahlen bestehen, in ein String umgewandelt werden.
        """
        personalnummer_33_zeichen = 123456789012345678901234567890123

        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw',
                                                     personalnummer_33_zeichen, 'Otto', 'Normalverbraucher',
                                                     'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), f"Die Personalnummer darf hoechstens 32 Zeichen lang sein. "
                                                 f"'123456789012345678901234567890123' besitzt "
                                                 f"33 Zeichen!")

    def test_leerer_vorname_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn der Vorname des Administrators ein leerer String ist.
        """
        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', '',
                                                     'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), 'Der Vorname des Nutzers muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_vorname_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn versucht wird, einen Vornamen fuer einen Administrator
        zu waehlen, der laenger als 64 Zeichen lang ist.
        """
        vorname_65_zeichen = "a" * 65

        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000',
                                                     vorname_65_zeichen, 'Normalverbraucher', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), "Der Vorname darf hoechstens 64 Zeichen lang sein. "
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 65 Zeichen!")

    def test_leerer_nachname_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn der Nachname des Administrators ein leerer String ist.
        """
        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000',
                                                     'Otto', '', 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), 'Der Nachname des Nutzers muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_nachname_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn versucht wird, einen Nachnamen fuer einen Administrator
        zu waehlen, der laenger als 64 Zeichen lang ist.
        """
        nachname_65_zeichen = "a" * 65

        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000',
                                                     'Otto', nachname_65_zeichen, 'adminpw', 'adminpw')

        self.assertEqual(str(context.exception), "Der Nachname darf hoechstens 64 Zeichen lang sein. "
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 65 Zeichen!")

    def test_zu_langes_passwort_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn versucht wird, ein Passwort zu waehlen, das laenger als
        128 Zeichen lang ist.
        """
        pw_129_zeichen = "a" * 129

        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000',
                                                     'Otto', 'Normalverbraucher', pw_129_zeichen, pw_129_zeichen)

        self.assertEqual(str(context.exception), "Passwort darf hoechstens 128 Zeichen haben!")

    def test_wiederholtes_passwort_falsch_exception(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn bei der zweiten Passworteingabe ein anderer String
        eingegeben wird, als in der ersten Eingabe.
        """
        erste_pw_eingabe = 'nutzerpasswort'
        zweite_pw_eingabe = 'npw'

        with self.assertRaises(ValueError) as context:
            self.login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000',
                                                     'Otto', 'Normalverbraucher', erste_pw_eingabe, zweite_pw_eingabe)

        self.assertEqual(str(context.exception), "Passwoerter stimmen nicht ueberein!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' mit allen Daten entfernt.
        """
        test_tear_down()
