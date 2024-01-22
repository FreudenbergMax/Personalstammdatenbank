import unittest

import psycopg2

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerEntfernen(unittest.TestCase):

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

        self.nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        self.nutzer.passwort_aendern('neues passwort', 'neues passwort')

    def test_nutzer_erfolgreich_entfernen(self):
        """
        Test prüft, ob nach Ausführung der Methode 'nutzer_entfernen' der Nutzer erfolgreich entfernt wurde.
        """
        # Zwischenprüfung, ob Nutzer in Nutzerliste angelegt ist
        vorname = self.admin.get_mandant().get_nutzerliste()[0].get_vorname()
        nachnamename = self.admin.get_mandant().get_nutzerliste()[0].get_nachname()
        personalnummer = self.admin.get_mandant().get_nutzerliste()[0].get_personalnummer()

        self.assertEqual(vorname, 'Erika')
        self.assertEqual(nachnamename, 'Musterfrau')
        self.assertEqual(personalnummer, 'M100001')

        # Prüfung, ob Nutzer nun entfernt wird
        self.admin.nutzer_entfernen('M100001')

        # Nachdem der Nutzer entfernt wurde, darf in der Nutzer-Liste kein Nutzerobjekt mehr vorhanden sein, da zuvor
        # nur ein einziger Nutzer erstellt wurde
        with self.assertRaises(IndexError) as context:
            self.admin.get_mandant().get_nutzerliste()[0].get_personalnummer()
        self.assertEqual(str(context.exception), "list index out of range")

        # Pruefen, ob der Nutzer auch aus der Datenbank entfernt wurde
        conn = psycopg2.connect(
            host="localhost",
            database="Personalstammdatenbank",
            user="postgres",
            password="@Postgres123",
            port=5432
        )

        nutzer_query = f"set search_path to {self.testschema}; SELECT * FROM nutzer"

        cur = conn.cursor()
        cur.execute(nutzer_query)
        ergebnis = cur.fetchall()

        # Commit der Änderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

        self.assertEqual(str(ergebnis), "[]")

    def test_nicht_existierenden_nutzer_entfernen(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Administrator versucht, einen Nutzer zu entfernen,
        der nicht existiert.
        """
        with self.assertRaises(ValueError) as context:
            self.admin.nutzer_entfernen('M999999')
        self.assertEqual(str(context.exception), "Nutzer M999999 existiert nicht!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
