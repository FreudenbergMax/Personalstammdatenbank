import unittest
import psycopg2

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestAdminNutzerEntsperren(unittest.TestCase):

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

        with self.assertRaises(ValueError) as context:
            self.nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        with self.assertRaises(ValueError) as context:
            self.nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

        with self.assertRaises(ValueError) as context:
            self.nutzer = self.login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'falsches_passwort')

    def test_entsperrung_erfolgreich(self):
        """
        Test prueft, ob eine Entsperrung erfolgreich durchgefuehrt wird
        """
        self.admin.nutzer_entsperren('M100001', 'neues_nutzerpw', 'neues_nutzerpw')

        # Pruefung, ob die Zahl der Anmeldeversuche wieder auf 0 zurueckgesetzt und das Passwort geaendert ist
        conn = psycopg2.connect(
            host="localhost",
            database="Personalstammdatenbank",
            user="postgres",
            password="@Postgres123",
            port=5432
        )

        nutzer_query = f"set search_path to {self.testschema}; " \
                       f"SELECT passwort, anmeldeversuche FROM nutzer WHERE personalnummer = 'M100001'"

        cur = conn.cursor()
        cur.execute(nutzer_query)
        ergebnis = cur.fetchall()

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        self.assertEqual(str(ergebnis), "[('neues_nutzerpw', 0)]")

    def test_passworteingaben_nicht_uebereinstimmend(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Administrator bei der Passwortneuvergabe bei der
        Zweiteingabe etwas anderes eingibt als bei der Ersteingabe
        """
        with self.assertRaises(ValueError) as context:
            self.admin.nutzer_entsperren('M100001', 'neues_nutzerpw', 'neues_nutzerpw_anders')

        self.assertEqual(str(context.exception), "Zweite Passworteingabe ist anders als erste Passworteingabe!")

    def test_nutzer_existiert_nicht(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn der Administrator eine Personalnummer eingibt, die
        keinem Nutzer zugeordnet ist.
        """
        with self.assertRaises(ValueError) as context:
            self.admin.nutzer_entsperren('M999999', 'neues_nutzerpw', 'neues_nutzerpw')

        self.assertEqual(str(context.exception), "Nutzer mit Personalnummer 'M999999' nicht vorhanden!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' mit allen Daten entfernt.
        """
        test_tear_down()
