import unittest

import psycopg2

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestGetNutzer(unittest.TestCase):

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

    def test_nutzer_objekt_vorhanden(self):
        """
        Test prüft, ob ein tatsächlich angelegter Nutzer gefunden und übergeben wird
        """
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        vorname = self.admin.get_mandant().get_nutzerliste()[0].get_vorname()
        nachnamename = self.admin.get_mandant().get_nutzerliste()[0].get_nachname()
        personalnummer = self.admin.get_mandant().get_nutzerliste()[0].get_personalnummer()

        self.assertEqual(vorname, 'Erika')
        self.assertEqual(nachnamename, 'Musterfrau')
        self.assertEqual(personalnummer, 'M100001')

        # Pruefen, ob der Nutzer auch in der Datenbank vorhanden ist
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

        self.assertEqual(str(ergebnis), "[(1, 1, 'M100001', 'Erika', 'Musterfrau', 'nutzerpw', 0)]")

    def test_nutzer_objekt_nicht_vorhanden(self):
        """
        Test prüft, ob bei der Eingabe eines nicht vorhandenen Nutzers eine Fehlermeldung kommt.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')

        erwartete_fehlermeldung = "FEHLER:  Nutzer existiert nicht!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_kein_zugriff_auf_nutzer_anderer_mandanten(self):
        """
        Test prüft, ob Mandant A keinen Zugriff auf Nutzer des Mandanten B hat und umgekehrt.
        """
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        # zweiten Mandanten mit Administrator und Nutzer erstellen
        self.login.registriere_mandant_und_admin('Prueffirma', 'mpw', 'mpw', 'M1', 'Max', 'Mustermann', 'apw', 'apw')
        admin_m2 = self.login.login_admin('Prueffirma', 'mpw', 'M1', 'apw')
        admin_m2.nutzer_anlegen('M1', 'Max', 'Mustermann', 'npw', 'npw')

        # Ueber den ersten Mandanten 'Testfirma' wird versucht, den Nutzer des zweiten Mandanten 'Prueffirma' auszulesen
        with self.assertRaises(Exception) as context:
            self.nutzer_m2 = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M1', 'npw')
        erwartete_fehlermeldung = "FEHLER:  Nutzer existiert nicht!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Ueber den zweiten Mandanten 'Prueffirma' wird versucht, den Nutzer des ersten Mandanten 'Testfirma' auszulesen
        with self.assertRaises(Exception) as context:
            self.nutzer_m1 = self.login.login_nutzer('Prueffirma', 'mpw', 'M100001', 'nutzerpw')
        erwartete_fehlermeldung = "FEHLER:  Nutzer existiert nicht!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
